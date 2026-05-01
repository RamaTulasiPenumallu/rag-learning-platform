from flask import Blueprint, render_template, request, jsonify
from app.rag import (
    collection_stats, generate_answer, initialize_documents,
    save_chat_entry, get_chat_history, clear_chat_history,
    add_favorite, remove_favorite, get_favorites,
    add_document, delete_document, get_all_documents,
    get_analytics
)

main = Blueprint("main", __name__)

initialize_documents()

SAMPLE_QUESTIONS = [
    "What is retrieval-augmented generation?",
    "How does deep learning fit into AI?",
    "What should I measure when evaluating a RAG system?",
    "How does data science support learning platforms?",
]

@main.route("/", methods=["GET", "POST"])
def home():
    answer = None
    question = ""
    stats = collection_stats()
    analytics = get_analytics()
    favorites = get_favorites()

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            answer = generate_answer(question)
            # Save to chat history
            save_chat_entry("user", question)
            save_chat_entry("assistant", answer.get("answer", ""), answer.get("mode"))

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        stats=stats,
        analytics=analytics,
        favorites=favorites,
        sample_questions=SAMPLE_QUESTIONS,
    )


@main.route("/api/chat-history", methods=["GET"])
def get_history():
    """Get chat history."""
    history = get_chat_history()
    return jsonify(history)


@main.route("/api/chat-history", methods=["DELETE"])
def delete_history():
    """Clear chat history."""
    result = clear_chat_history()
    return jsonify(result)


@main.route("/api/favorites", methods=["GET"])
def get_fav():
    """Get all favorites."""
    favorites = get_favorites()
    return jsonify(favorites)


@main.route("/api/favorites", methods=["POST"])
def add_fav():
    """Add to favorites."""
    data = request.get_json()
    question = data.get("question")
    answer = data.get("answer")
    if question and answer:
        result = add_favorite(question, answer)
        return jsonify(result)
    return jsonify({"status": "error", "message": "Missing data"})


@main.route("/api/favorites/<int:fav_id>", methods=["DELETE"])
def remove_fav(fav_id):
    """Remove from favorites."""
    result = remove_favorite(fav_id)
    return jsonify(result)


@main.route("/api/documents", methods=["GET"])
def list_documents():
    """Get all documents."""
    docs = get_all_documents()
    return jsonify(docs)


@main.route("/api/documents", methods=["POST"])
def add_doc():
    """Add a new document."""
    data = request.get_json()
    doc_id = data.get("id")
    document_text = data.get("document")
    source = data.get("source", "uploaded")
    
    if doc_id and document_text:
        result = add_document(doc_id, document_text, source)
        return jsonify(result)
    return jsonify({"status": "error", "message": "Missing data"})


@main.route("/api/documents/<doc_id>", methods=["DELETE"])
def remove_doc(doc_id):
    """Delete a document."""
    result = delete_document(doc_id)
    return jsonify(result)


@main.route("/api/analytics", methods=["GET"])
def get_stats():
    """Get analytics."""
    analytics = get_analytics()
    return jsonify(analytics)


@main.route("/study", methods=["GET"])
def study_mode():
    """Study mode page."""
    stats = collection_stats()
    documents = get_all_documents()
    return render_template("study.html", stats=stats, documents=documents)


@main.route("/documents", methods=["GET"])
def documents_page():
    """Documents management page."""
    stats = collection_stats()
    documents = get_all_documents()
    return render_template("documents.html", stats=stats, documents=documents)

