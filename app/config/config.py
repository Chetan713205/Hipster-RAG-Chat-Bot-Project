import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

HF_TOKEN = os.environ.get("HF_TOKEN") 
HUGGINGFACE_REPO_ID = os.environ.get("HUGGINGFACE_REPO_ID") 
DB_PATH = "vectorstore/db_faiss"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50 

# Web scraping configuration
USE_SITEMAP = True

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")