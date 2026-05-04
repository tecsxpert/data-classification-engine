# services/chroma_service.py
# ChromaDB service for storing domain knowledge
# Gives AI background knowledge about data classification

import os
import logging
import chromadb
from chromadb.utils import embedding_functions

logger = logging.getLogger(__name__)

# Global variables
chroma_client = None
collection = None
embedding_function = None


def initialize_chromadb():
    """
    Initialize ChromaDB and sentence-transformers.
    Called once at startup.
    Pre-loads sentence-transformers model.
    """
    global chroma_client, collection, embedding_function

    try:
        logger.info("Initializing ChromaDB...")

        # Initialize sentence-transformers embedding function
        # This pre-loads the model at startup
        logger.info("Pre-loading sentence-transformers model...")
        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        logger.info("sentence-transformers model loaded!")

        # Initialize ChromaDB client
        # Stores data in chroma_data/ folder
        chroma_client = chromadb.PersistentClient(
            path="./chroma_data"
        )

        # Get or create collection
        collection = chroma_client.get_or_create_collection(
            name="domain_knowledge",
            embedding_function=embedding_function
        )

        logger.info(f"ChromaDB initialized! Collection: domain_knowledge")
        logger.info(f"Documents in collection: {collection.count()}")

        return True

    except Exception as e:
        logger.error(f"ChromaDB initialization failed: {str(e)}")
        return False


def search_knowledge(query, n_results=3):
    """
    Search ChromaDB for relevant knowledge.
    Returns relevant documents for given query.
    """
    global collection

    try:
        if collection is None:
            logger.warning("ChromaDB not initialized")
            return []

        if collection.count() == 0:
            logger.warning("No documents in ChromaDB")
            return []

        results = collection.query(
            query_texts=[query],
            n_results=min(n_results, collection.count())
        )

        documents = results.get('documents', [[]])[0]
        logger.info(f"Found {len(documents)} relevant documents")
        return documents

    except Exception as e:
        logger.error(f"ChromaDB search error: {str(e)}")
        return []


def get_collection_count():
    """Returns number of documents in ChromaDB"""
    try:
        if collection:
            return collection.count()
        return 0
    except Exception:
        return 0


def is_chromadb_ready():
    """Check if ChromaDB is initialized"""
    return collection is not None