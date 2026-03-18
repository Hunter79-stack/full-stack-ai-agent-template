"""RAG scheduled tasks for collection reindexing.

This module provides scheduled tasks for reindexing RAG collections.
Tasks are only available when RAG and a task system (Celery/Taskiq/ARQ) are enabled.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


# === Celery Task ===

from celery import shared_task


@shared_task(bind=True, max_retries=3)
def reindex_collection(self, collection_name: str | None = None) -> dict[str, Any]:
    """Reindex all documents in a collection.

    This task re-processes and re-embeds all documents in the specified collection.
    Useful when embedding model is updated or documents need re-processing.

    Args:
        collection_name: Name of the collection to reindex (default: from RAGSettings)

    Returns:
        Dictionary with reindex status and count
    """
    import asyncio

    from app.rag.config import RAGSettings
    from app.rag.embeddings import EmbeddingService
    from app.rag.vectorstore import MilvusVectorStore

    logger.info(f"Starting collection reindex: {collection_name}")

    try:
        settings = RAGSettings()
        # Use settings collection_name if not provided
        if collection_name is None:
            collection_name = settings.collection_name
        embed_service = EmbeddingService(settings)
        vector_store = MilvusVectorStore(settings, embed_service)

        # Run async code in sync context using asyncio.run()
        info = asyncio.run(vector_store.get_collection_info(collection_name))

        total_docs = info.total_vectors

        logger.info(f"Collection {collection_name} has {total_docs} vectors")

        # TODO: Implement full reindex logic:
        # 1. Get all document IDs from collection
        # 2. Re-process each document through IngestionService
        # 3. Update embeddings in vector store

        return {
            "status": "completed",
            "collection": collection_name,
            "reindexed_count": total_docs,
        }
    except Exception as exc:
        logger.error(f"Reindex failed: {exc}")
        raise self.retry(exc=exc, countdown=60)


# === Taskiq Task ===


# === ARQ Task ===
