import os
from app.components.web_loader import fetch_all_pages, split_into_chunks
from app.components.vector_store import save_vector_store

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def process_and_store_data():
    try:
        logger.info("Making the vectorstore....")
        documents = fetch_all_pages()
        if not documents:
            raise RuntimeError("No documents fetched—pipeline aborting")

        text_chunks = split_into_chunks(documents)
        db = save_vector_store(text_chunks)
        if db is None:
            raise RuntimeError("Failed to save vector store")
        logger.info("Vectorstore created successfully....")
        return db

    except Exception as e:
        logger.error(f"Full error details: {repr(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        if hasattr(e, 'args'):
            logger.error(f"Error args: {e.args}")
        error_message = CustomException("Failed to create new vectorstore", e)
        logger.error(str(error_message))
        return None

if __name__=="__main__":
    process_and_store_data()