# RAG Learning Platform - Complete Edition

A comprehensive AI-powered learning platform combining **Retrieval-Augmented Generation (RAG)** with an attractive, feature-rich dashboard for knowledge management and interactive learning.

## 🚀 Features

### Core Features
- **RAG-Powered Q&A**: Ask questions and get grounded answers based on your knowledge base
- **Document Management**: Upload, organize, and manage learning documents
- **Chat History**: Track all your questions and answers for future reference
- **Favorites System**: Save important Q&A pairs for quick access
- **Analytics Dashboard**: View statistics on your learning journey

### Advanced Features
- **Study Mode**: Deep dive into your learning materials with dedicated study interface
- **Knowledge Base Management**: Create, organize, and delete documents
- **Vector Embeddings**: Semantic search using sentence-transformers
- **Intelligent Retrieval**: Top-3 relevant documents retrieved for each query
- **Multiple Answer Modes**: 
  - **Live Mode**: Uses Groq API for AI-powered answers
  - **Demo Mode**: Works offline with grounded summaries

### Dashboard Highlights
- **Beautiful Modern UI**: Dark theme with gradient accents and smooth animations
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Tab-Based Navigation**: Organized interface with 5 main sections
- **Real-Time Statistics**: Live updates of platform metrics
- **API Integration**: RESTful API endpoints for all operations

## 📊 Dashboard Overview

The main dashboard includes:

1. **Analytics Cards**
   - Total Documents Indexed
   - Questions Asked
   - Answers Generated
   - Saved Favorites

2. **Ask Question Tab**
   - Full-featured question input with character support
   - Quick prompt suggestions for common questions
   - Instant response display with source cards
   - Relevance scores for each retrieved document

3. **Favorites Tab**
   - Save memorable Q&A pairs
   - Quick access to previous answers
   - One-click reuse of favorite questions
   - Bulk clear functionality

4. **Chat History Tab**
   - Complete conversation log
   - Timestamped entries
   - Mode information for each response
   - Clear history option

5. **Documents Tab**
   - View all indexed documents
   - Add new documents with custom IDs
   - Delete documents from knowledge base
   - See document sources and categories

6. **Settings Tab**
   - System configuration details
   - Model information
   - API status
   - Platform statistics

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### Installation Steps

1. **Create Virtual Environment**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Mac/Linux
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Environment**
```bash
# Create a .env file in the root directory
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_secret_key
CHROMA_COLLECTION_NAME=learning_docs
```

4. **Run the Application**
```bash
python run.py
```

The application will be available at: **http://127.0.0.1:5000**

## 📁 Project Structure

```
rag_learning_platform/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── rag.py               # RAG logic & embeddings
│   ├── routes.py            # Flask routes & API endpoints
│   └── templates/
│       ├── index.html       # Main dashboard
│       ├── study.html       # Study mode page
│       └── documents.html   # Document management page
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
├── chat_history.json        # Chat history storage
├── favorites.json           # Favorites storage
└── README.md                # This file
```

## 📚 API Endpoints

### Documents API
- `GET /api/documents` - List all documents
- `POST /api/documents` - Add new document
- `DELETE /api/documents/<doc_id>` - Delete document

### Chat History API
- `GET /api/chat-history` - Get all chat entries
- `DELETE /api/chat-history` - Clear chat history

### Favorites API
- `GET /api/favorites` - Get all favorites
- `POST /api/favorites` - Add favorite Q&A
- `DELETE /api/favorites/<fav_id>` - Remove favorite

### Analytics API
- `GET /api/analytics` - Get platform statistics

### Pages
- `GET /` - Main dashboard
- `GET /study` - Study mode
- `GET /documents` - Document management

## 🎯 How to Use

### Asking Questions
1. Go to the "Ask Question" tab
2. Type your question in the text area
3. Click "Generate Answer" or use a quick prompt
4. View the answer and source documents
5. Click the heart icon to save to favorites

### Managing Documents
1. Go to the "Documents" tab
2. Enter document ID, content, and source
3. Click "Add Document"
4. View all documents or delete as needed

### Studying
1. Click "Study Mode" (from dashboard dropdown)
2. Review all learning materials
3. Use dashboard to ask questions about materials
4. Track your progress in chat history

### Tracking Progress
1. Check the Analytics section for statistics
2. Review Chat History for past questions
3. Access Favorites for important learnings
4. View documents by category/source

## 🔧 Configuration

### Environment Variables
```
GROQ_API_KEY        - Your Groq API key for LLM access
SECRET_KEY          - Flask session secret key
CHROMA_COLLECTION_NAME - ChromaDB collection name (default: learning_docs)
```

### Customization

**Change Models**: Edit `MODEL_NAME` in `app/rag.py`
```python
MODEL_NAME = "llama3-8b-8192"  # Current model
```

**Adjust Retrieval**: Modify the `n_results` parameter in `retrieve_documents()`
```python
n_results=3  # Top 3 documents retrieved
```

**Add Default Documents**: Edit `DEFAULT_DOCUMENTS` in `app/rag.py`

## 📊 Data Storage

- **Chat History**: Stored in `chat_history.json`
- **Favorites**: Stored in `favorites.json`
- **Vector Database**: ChromaDB (in-memory or persistent)
- **Models**: Downloaded from HuggingFace on first run

## 🎨 UI Features

### Styling
- **Color Scheme**: Modern dark theme with blue/purple accents
- **Animations**: Smooth transitions and hover effects
- **Typography**: Inter font for UI, Space Grotesk for headings
- **Icons**: Font Awesome 6.4.0 for visual elements
- **Responsive**: Mobile-first design approach

### User Experience
- One-click actions with confirmation dialogs
- Real-time form validation
- Loading states for async operations
- Helpful error messages
- Empty states with actionable prompts

## 🚀 Performance Optimizations

- **Vector Caching**: Embeddings cached in ChromaDB
- **Lazy Loading**: Data loaded only when tabs accessed
- **Minimal Dependencies**: Lightweight, focused libraries
- **API Response Format**: JSON for efficient data transfer
- **Client-Side Rendering**: Reduces server load

## 🔐 Security Considerations

- API keys stored in `.env` files (not in code)
- CORS enabled only for localhost in development
- Input validation on all forms
- XSS protection in template rendering
- No sensitive data in browser storage

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Try a different port
# Edit run.py: app.run(port=5001)
```

### Embedding model slow to load
- First run downloads the model (~400MB)
- Subsequent runs use cached model
- Consider using lighter model if needed

### ChromaDB issues
- Delete the ChromaDB directory to reset
- Documents will be re-indexed on next run

### API Key errors
- Verify GROQ_API_KEY in .env file
- Keep your API key private
- Regenerate if compromised

## 📈 Future Enhancements

- [ ] User authentication & accounts
- [ ] Multi-user collaboration
- [ ] Document upload from files
- [ ] Advanced search filters
- [ ] Custom model selection
- [ ] Export chat history to PDF
- [ ] Integration with external APIs
- [ ] Advanced analytics & visualizations

## 💡 Tips & Best Practices

1. **Organize Documents**: Use meaningful IDs and sources
2. **Regular Backups**: Export chat history periodically
3. **Manage Favorites**: Regularly clean up saved items
4. **Study Systematically**: Review materials in study mode first
5. **Leverage Quick Prompts**: Customize based on your needs
6. **Monitor Analytics**: Track your learning progress

## 🤝 Contributing

To contribute improvements:
1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

This project is provided as-is for educational purposes.

## 🎓 Learning Resources

- **RAG Concept**: See default documents in `app/rag.py`
- **Flask Guide**: Check `app/routes.py` for endpoint patterns
- **Embeddings**: Review `retrieve_documents()` in `app/rag.py`
- **UI Code**: Study `index.html` for dashboard implementation

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review error messages carefully
3. Check terminal output for stack traces
4. Verify all dependencies are installed

---

**Happy Learning! 🚀**

Built with ❤️ using Flask, ChromaDB, and Groq API
