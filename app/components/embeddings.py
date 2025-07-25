from langchain_huggingface import HuggingFaceEmbeddings
#from langchain.embeddings import HuggingFaceEmbeddings

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)
    
from sentence_transformers import SentenceTransformer

def get_embedding_model():
    try:
        logger.info("Initializing our Huggingface embedding model")
        
        # Load the model directly first
        st_model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            device="cpu"
        )
        
        # Then create the LangChain wrapper
        model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': False}
        )
        
        logger.info("Huggingface embedding model loaded successfully....")
        return model
    except Exception as e:
        logger.error(f"Full error details: {repr(e)}")
        raise CustomException("Error occurred while loading embedding model", e)