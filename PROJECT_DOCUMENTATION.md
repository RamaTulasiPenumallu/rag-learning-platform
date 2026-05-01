# RAG Learning Platform Documentation

## 1. Project Overview
RAG Learning Platform is a Flask-based web application that combines retrieval-augmented generation with an interactive learning dashboard.

The platform allows users to:
- Ask questions against a local knowledge base.
- Retrieve top relevant chunks using vector search.
- Generate answers using Groq LLM when API key is available.
- Fall back to grounded demo responses when API key is missing.
- Manage documents, chat history, and favorites from the UI.

## 2. Core Capabilities
- Retrieval with sentence-transformers embeddings.
- ChromaDB vector collection for semantic search.
- LLM answer generation using Groq chat completions.
- Local JSON persistence for chat history and favorites.
- Dashboard with tabs for Ask, Favorites, History, Documents, and Settings.

## 3. Technology Stack
- Backend: Flask
- LLM Provider: Groq
- Embeddings: sentence-transformers all-MiniLM-L6-v2
- Vector Database: ChromaDB
- Frontend: HTML, CSS, vanilla JavaScript, Jinja templates
- Persistence: JSON files for user activity

## 4. Application Architecture
The app follows a simple layered architecture:

1. Routing layer
- Handles page rendering and API endpoints.
- Located in [app/routes.py](app/routes.py).

2. RAG and data layer
- Embedding, retrieval, generation, and local persistence helpers.
- Located in [app/rag.py](app/rag.py).

3. Configuration layer
- Reads environment variables for API keys and collection names.
- Located in [config.py](config.py).

4. App bootstrap
- Registers blueprint and creates Flask app.
- Located in [app/__init__.py](app/__init__.py) and [run.py](run.py).

## 5. Project Structure
- [README.md](README.md): Existing readme file.
- [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md): This technical documentation file.
- [requirements.txt](requirements.txt): Python dependencies.
- [config.py](config.py): Environment-driven configuration.
- [run.py](run.py): Entry point to start Flask server.
- [chat_history.json](chat_history.json): Stored chat entries.
- [app/__init__.py](app/__init__.py): Flask app factory.
- [app/rag.py](app/rag.py): RAG logic, retrieval, generation, analytics, persistence utilities.
- [app/routes.py](app/routes.py): UI pages and REST APIs.
- [app/templates/index.html](app/templates/index.html): Main dashboard page.
- [app/templates/study.html](app/templates/study.html): Study mode page.
- [app/templates/documents.html](app/templates/documents.html): Document management page.

## 6. Setup and Installation
1. Create and activate virtual environment.
2. Install dependencies from requirements.txt.
3. Create a .env file in project root.
4. Add required variables:
- GROQ_API_KEY
- SECRET_KEY
- CHROMA_COLLECTION_NAME
5. Start the application using run.py.

Default local URL is http://127.0.0.1:5000

## 7. Configuration
Environment variables:
- GROQ_API_KEY: Enables live LLM answer generation.
- SECRET_KEY: Flask secret key for app security.
- CHROMA_COLLECTION_NAME: Name of Chroma collection.

If GROQ_API_KEY is missing, app works in demo mode with grounded fallback responses.

## 8. Retrieval and Generation Flow
1. On startup, default learning documents are indexed if collection is empty.
2. User submits question from dashboard.
3. Question is embedded with all-MiniLM-L6-v2.
4. Top 3 documents are retrieved from ChromaDB.
5. If Groq key exists, prompt with retrieved context is sent to LLM.
6. If Groq key does not exist or fails, fallback grounded summary is returned.
7. User question and assistant answer are stored in chat history.

## 9. API Endpoints
Pages:
- GET /
- GET /study
- GET /documents

Documents:
- GET /api/documents
- POST /api/documents
- DELETE /api/documents/<doc_id>

Chat history:
- GET /api/chat-history
- DELETE /api/chat-history

Favorites:
- GET /api/favorites
- POST /api/favorites
- DELETE /api/favorites/<fav_id>

Analytics:
- GET /api/analytics

## 10. Frontend Modules
Main dashboard in [app/templates/index.html](app/templates/index.html):
- Summary metric cards.
- Ask question form and sample prompts.
- Response panel with sources and relevance scores.
- Favorites tab with add, remove, and reuse actions.
- Chat history tab with clear operation.
- Documents tab with add and delete operations.
- Settings tab showing model and system status.

Study page in [app/templates/study.html](app/templates/study.html):
- Read-only listing of all documents for revision.

Documents page in [app/templates/documents.html](app/templates/documents.html):
- Dedicated add and delete workflow for knowledge base entries.

## 11. Data Persistence
- Chat history is stored in [chat_history.json](chat_history.json).
- Favorites are stored in favorites.json at runtime.
- Vectors and metadata are stored in Chroma collection in current runtime context.

## 12. Analytics Model
Analytics values include:
- Total documents
- Total user questions
- Total assistant answers
- Total favorites
- API readiness
- Model name
- Answer mode distribution
- Total chat entries

## 13. Current Known Issues
1. Duplicate HTML block detected in dashboard template after closing html tag, starting at [app/templates/index.html](app/templates/index.html#L1162).
2. favorites.json is expected by code and is created on demand, but it may not exist in repository until first favorite is saved.

## 14. Recommended Next Improvements
- Clean duplicate HTML section from dashboard template.
- Add request validation and structured error responses in API handlers.
- Add unit tests for retrieval, fallback mode, and API endpoints.
- Add persistent Chroma storage directory configuration for long-term retention.
- Add basic authentication if multi-user usage is planned.

## 15. Quick Start for Evaluators
1. Install dependencies.
2. Set GROQ_API_KEY for full mode, or skip for demo mode.
3. Run server and open root URL.
4. Ask sample questions from prompt chips.
5. Add custom documents and ask follow-up questions.
6. Verify history, favorites, and analytics updates in dashboard.
