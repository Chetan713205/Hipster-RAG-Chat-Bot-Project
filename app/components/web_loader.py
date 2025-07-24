import os
import sys
import logging
import warnings
from typing import List

from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_community.document_loaders.sitemap import SitemapLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.config.config import CHUNK_SIZE, CHUNK_OVERLAP, USE_SITEMAP

warnings.filterwarnings("ignore", message="USER_AGENT environment variable not set, consider setting it to identify your requests.")

logger = get_logger(__name__)

WEBSITES = [
    {
        "root_url": "https://www.changiairport.com/in/en.html",
        "sitemap_url": "https://www.changiairport.com/sitemap.xml",
    },
    {
        "root_url": "https://www.jewelchangiairport.com/",
        "sitemap_url": None,
    },
]

MAX_DEPTH = 3
REQUESTS_TIMEOUT = 10
REQUESTS_PER_SECOND = 2
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

def fetch_all_pages() -> List:
    all_docs = []
    for site in WEBSITES:
        root = site["root_url"]
        sitemap = site["sitemap_url"]
        try:
            if USE_SITEMAP and sitemap:
                logger.info(f"Loading via sitemap: {sitemap}")
                loader = SitemapLoader(
                    web_path=sitemap,
                    restrict_to_same_domain=True,
                    continue_on_failure=True,
                    blocksize=10,
                    meta_function=None,
                )
            else:
                logger.info(f"Crawling recursively: {root}")
                loader = RecursiveUrlLoader(
                    url=root,
                    max_depth=MAX_DEPTH,
                    prevent_outside=True,
                    timeout=REQUESTS_TIMEOUT,
                    headers=DEFAULT_HEADERS,
                )
            docs = loader.load()
            logger.info(f"Fetched {len(docs)} pages from {root}")
            all_docs.extend(docs)
        except Exception as e:
            logger.error(f"Failed to load {root}: {e}")
    return all_docs

def split_into_chunks(all_docs: List) -> List:
    if not all_docs:
        raise CustomException("No documents to split", None)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    text_chunks = splitter.split_documents(all_docs)
    return text_chunks