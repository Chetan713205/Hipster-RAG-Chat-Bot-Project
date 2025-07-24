from langchain_huggingface import HuggingFaceEmbeddings
#from langchain.embeddings import HuggingFaceEmbeddings

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def get_embedding_model():
    try:
        logger.info("Intializing our Huggingface embedding model")

        model_kwargs = {'device': 'cpu'}  # Force CPU usage
        encode_kwargs = {'normalize_embeddings': False}
        
        model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )

        logger.info("Huggingface embedding model loaded successfully....")
        return model
    
    except Exception as e:
        logger.error(f"Full error details: {repr(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        if hasattr(e, 'args'):
            logger.error(f"Error args: {e.args}")
        raise CustomException("Error occurred while loading embedding model", e)