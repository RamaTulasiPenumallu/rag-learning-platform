from groq import Groq
from sentence_transformers import SentenceTransformer
import chromadb
from config import Config
import json
from datetime import datetime
from pathlib import Path

MODEL_NAME = "llama-3.3-70b-versatile"
DEFAULT_DOCUMENTS = [
    {
        "id": "ml-basics",
        "document": "Machine Learning is a subset of AI that helps systems learn patterns from data.",
        "source": "foundations.md",
    },
    {
        "id": "deep-learning",
        "document": "Deep Learning uses neural networks with many layers to model complex patterns.",
        "source": "foundations.md",
    },
    {
        "id": "data-science",
        "document": "Data Science combines data analysis, statistics, and visualization to extract insights.",
        "source": "workflow.md",
    },
    {
        "id": "rag",
        "document": "RAG stands for Retrieval-Augmented Generation and combines search with generation.",
        "source": "workflow.md",
    },
    {
        "id": "evaluation",
        "document": "Evaluation should measure accuracy, groundedness, and usefulness of the retrieved answer.",
        "source": "quality.md",
    },
]

# Storage paths
CHAT_HISTORY_FILE = "chat_history.json"
FAVORITES_FILE = "favorites.json"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(Config.CHROMA_COLLECTION_NAME)


def _get_client():
    if not Config.GROQ_API_KEY:
        return None
    return Groq(api_key=Config.GROQ_API_KEY)

def initialize_documents():
    if collection.count() > 0:
        return collection.count()

    documents = [item["document"] for item in DEFAULT_DOCUMENTS]
    embeddings = [embedding_model.encode(doc).tolist() for doc in documents]
    ids = [item["id"] for item in DEFAULT_DOCUMENTS]
    metadatas = [{"source": item["source"]} for item in DEFAULT_DOCUMENTS]

    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas,
    )

    return len(documents)


def collection_stats():
    initialize_documents()
    return {
        "document_count": collection.count(),
        "index_name": Config.CHROMA_COLLECTION_NAME,
        "model_name": MODEL_NAME,
        "api_ready": bool(Config.GROQ_API_KEY),
    }

def retrieve_documents(query):
    initialize_documents()
    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include=["documents", "metadatas", "distances"],
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    retrieved = []
    for index, document in enumerate(documents):
        retrieved.append(
            {
                "document": document,
                "source": (metadatas[index] or {}).get("source", "knowledge-base"),
                "score": round(1 - distances[index], 3) if index < len(distances) and distances[index] is not None else None,
            }
        )

    return retrieved


def _fallback_answer(query, retrieved_docs):
    if not retrieved_docs:
        return {
            "answer": (
                "The local knowledge base is empty right now. Add documents or configure the Groq API key "
                "to enable full answers."
            ),
            "mode": "local-demo",
        }

    highlights = "\n".join(f"- {item['document']}" for item in retrieved_docs)
    return {
        "answer": (
            "Groq is not configured, so this dashboard is running in local demo mode.\n\n"
            f"Based on the most relevant indexed notes for '{query}', here is the grounded summary:\n{highlights}\n\n"
            "Set GROQ_API_KEY in your environment to unlock live generative answers."
        ),
        "mode": "local-demo",
    }

def generate_answer(query):
    retrieved_docs = retrieve_documents(query)
    context = "\n".join(item["document"] for item in retrieved_docs)
    client = _get_client()

    if client is None:
        fallback = _fallback_answer(query, retrieved_docs)
        fallback.update({"sources": retrieved_docs, "query": query, "model": None})
        return fallback

    prompt = f"""
You are an academic AI tutor.

Context:
{context}

Question:
{query}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.choices[0].message.content
        mode = "groq"
    except Exception as exc:
        answer = (
            "The live model request failed, so the app is falling back to a grounded summary. "
            f"Error details: {exc}"
        )
        mode = "error"

    return {
        "answer": answer,
        "sources": retrieved_docs,
        "query": query,
        "model": MODEL_NAME,
        "mode": mode,
    }


# ============== NEW: Document Management ==============
def add_document(doc_id, document_text, source):
    """Add a new document to the knowledge base."""
    try:
        embedding = embedding_model.encode(document_text).tolist()
        collection.add(
            documents=[document_text],
            embeddings=[embedding],
            ids=[doc_id],
            metadatas=[{"source": source}],
        )
        save_chat_entry("system", f"Document '{doc_id}' added from {source}")
        return {"status": "success", "message": f"Document '{doc_id}' added successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def delete_document(doc_id):
    """Delete a document from the knowledge base."""
    try:
        collection.delete(ids=[doc_id])
        save_chat_entry("system", f"Document '{doc_id}' deleted")
        return {"status": "success", "message": f"Document '{doc_id}' deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_all_documents():
    """Retrieve all documents in the collection."""
    try:
        results = collection.get(include=["documents", "metadatas"])
        documents = []
        for i, doc_id in enumerate(results.get("ids", [])):
            documents.append({
                "id": doc_id,
                "document": results["documents"][i],
                "source": (results["metadatas"][i] or {}).get("source", "unknown"),
            })
        return documents
    except Exception as e:
        return []


# ============== NEW: Chat History ==============
def load_chat_history():
    """Load chat history from file."""
    try:
        if Path(CHAT_HISTORY_FILE).exists():
            with open(CHAT_HISTORY_FILE, "r") as f:
                return json.load(f)
        return []
    except Exception:
        return []


def save_chat_entry(role, content, answer_mode=None):
    """Save a chat entry to history."""
    try:
        history = load_chat_history()
        entry = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
        }
        if answer_mode:
            entry["mode"] = answer_mode
        history.append(entry)
        with open(CHAT_HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
        return True
    except Exception:
        return False


def get_chat_history():
    """Get formatted chat history."""
    history = load_chat_history()
    return history[-50:]  # Return last 50 entries


def clear_chat_history():
    """Clear all chat history."""
    try:
        with open(CHAT_HISTORY_FILE, "w") as f:
            json.dump([], f)
        return {"status": "success", "message": "Chat history cleared"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============== NEW: Favorites System ==============
def load_favorites():
    """Load favorites from file."""
    try:
        if Path(FAVORITES_FILE).exists():
            with open(FAVORITES_FILE, "r") as f:
                return json.load(f)
        return []
    except Exception:
        return []


def add_favorite(question, answer):
    """Add a Q&A to favorites."""
    try:
        favorites = load_favorites()
        favorite = {
            "id": len(favorites) + 1,
            "question": question,
            "answer": answer,
            "saved_at": datetime.now().isoformat(),
        }
        favorites.append(favorite)
        with open(FAVORITES_FILE, "w") as f:
            json.dump(favorites, f, indent=2)
        return {"status": "success", "message": "Added to favorites"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def remove_favorite(favorite_id):
    """Remove a favorite by ID."""
    try:
        favorites = load_favorites()
        favorites = [f for f in favorites if f["id"] != favorite_id]
        with open(FAVORITES_FILE, "w") as f:
            json.dump(favorites, f, indent=2)
        return {"status": "success", "message": "Removed from favorites"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_favorites():
    """Get all favorites."""
    return load_favorites()


# ============== NEW: Analytics ==============
def get_analytics():
    """Get platform analytics."""
    stats = collection_stats()
    history = load_chat_history()
    favorites = load_favorites()
    
    # Count questions and answers
    questions = [h for h in history if h.get("role") == "user"]
    answers = [h for h in history if h.get("role") == "assistant"]
    
    # Modes breakdown
    modes = {}
    for h in answers:
        mode = h.get("mode", "unknown")
        modes[mode] = modes.get(mode, 0) + 1
    
    return {
        "total_documents": stats["document_count"],
        "total_questions": len(questions),
        "total_answers": len(answers),
        "total_favorites": len(favorites),
        "api_ready": stats["api_ready"],
        "model_name": stats["model_name"],
        "modes": modes,
        "chat_entries": len(history),
    }

