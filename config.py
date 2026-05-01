import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "learning_docs")
