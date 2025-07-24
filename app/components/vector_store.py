from langchain_pinecone import PineconeVectorStore
import os
import time
from pinecone import Pinecone, ServerlessSpec

from app.components.embeddings import get_embedding_model
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.config.config import PINECONE_INDEX_NAME, PINECONE_API_KEY

logger = get_logger(__name__)

# Function to load existing vector store
def load_vector_store():
    try:
        embedding_model = get_embedding_model()
        
        # Initialize Pinecone client
        pc = Pinecone(api_key=PINECONE_API_KEY)
        
        # Check if index exists
        if PINECONE_INDEX_NAME in [index.name for index in pc.list_indexes()]:
            logger.info("Loading existing vectorstore...")
            
            # Get the index
            index = pc.Index(PINECONE_INDEX_NAME)
            
            # Create PineconeVectorStore from existing index
            return PineconeVectorStore(
                index=index,
                embedding=embedding_model,
                text_key="text"
            )
        else:
            logger.warning("No vector store found..")
            return None

    except Exception as e:
        error_message = CustomException("Failed to load vectorstore", e)
        logger.error(str(error_message))
        return None

# Create new Vector Store Funtion
def save_vector_store(text_chunks):
    try:
        if not text_chunks:
            raise CustomException("No chunks were found..")
        
        logger.info("Generating your new vectorstore")

        embedding_model = get_embedding_model()
        
        # Initialize Pinecone client
        pc = Pinecone(api_key=PINECONE_API_KEY)
        
        # Create index if it doesn't exist
        if PINECONE_INDEX_NAME not in [index.name for index in pc.list_indexes()]:
            logger.info("Creating new Pinecone index...")
            
            # Get embedding dimension from the first chunk
            sample_embedding = embedding_model.embed_query("sample text")
            dimension = len(sample_embedding)
            
            pc.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            
            # Wait for index to be ready
            while not pc.describe_index(PINECONE_INDEX_NAME).status['ready']:
                time.sleep(1)
                
        # Get the index
        index = pc.Index(PINECONE_INDEX_NAME)
        
        logger.info("Saving vectorstore")
        
        # Clean up documents before saving
        cleaned_chunks = []
        for chunk in text_chunks:
            if hasattr(chunk, 'metadata') and chunk.metadata is not None:
                # Remove null values from metadata
                chunk.metadata = {k: v for k, v in chunk.metadata.items() if v is not None}
                # Set default language if needed
                if 'language' not in chunk.metadata:
                    chunk.metadata['language'] = 'en'  # default to English
            cleaned_chunks.append(chunk)
        
        logger.info(f"Starting to save {len(cleaned_chunks)} chunks to Pinecone")
        batch_size = 100
        for i in range(0, len(cleaned_chunks), batch_size):
            batch = cleaned_chunks[i:i+batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}/{(len(cleaned_chunks)//batch_size)+1}")
            PineconeVectorStore.from_documents(
                documents=batch,
                embedding=embedding_model,
                index_name=PINECONE_INDEX_NAME
            )
        
        # Create vectorstore from documents
        db = PineconeVectorStore.from_documents(
            documents=cleaned_chunks,
            embedding=embedding_model,
            index_name=PINECONE_INDEX_NAME
        )

        logger.info("Vectorstore saved successfully...")

        return db
    
    except Exception as e:
        logger.error(f"Failed to create vector store. Details: {str(e)}")
        logger.error(f"Pinecone index status: {pc.describe_index(PINECONE_INDEX_NAME) if PINECONE_INDEX_NAME in pc.list_indexes() else 'Index does not exist'}")
        logger.error(f"Text chunks count: {len(text_chunks) if text_chunks else 0}")
        error_message = CustomException("Failed to create new vectorstore", e)
        logger.error(str(error_message))
        return None
