"""RAG tool for agent knowledge base search."""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from app.rag.retrieval import BaseRetrievalService


@lru_cache(maxsize=1)
def _get_retrieval_service_cached() -> "BaseRetrievalService":
    """Get cached retrieval service singleton.

    This function uses lru_cache to create a cached singleton of the
    RetrievalService. The cache is initialized on first call and reused
    for subsequent calls.

    Returns:
        Configured BaseRetrievalService instance.
    """
    # Import here to avoid circular imports at module load time
    from app.rag.config import RAGSettings
    from app.rag.embeddings import EmbeddingService
    from app.rag.retrieval import RetrievalService
    from app.rag.vectorstore import MilvusVectorStore

    settings = RAGSettings()
    embedding_service = EmbeddingService(settings)
    vector_store = MilvusVectorStore(settings, embedding_service)
    return RetrievalService(vector_store, settings)


def get_retrieval_service() -> "BaseRetrievalService":
    """Get the cached RetrievalService instance.

    This function provides access to a cached RetrievalService singleton.
    It uses lru_cache for proper caching behavior.

    Returns:
        Configured BaseRetrievalService instance.
    """
    return _get_retrieval_service_cached()


async def search_knowledge_base(
    query: str,
    collection: str = "documents",
    collections: list[str] | None = None,
    top_k: int = 5,
) -> str:
    """Search the knowledge base and return formatted results.

    Args:
        query: The search query string.
        collection: Name of a single collection to search (default: "documents").
        collections: List of collection names for cross-collection search (overrides collection).
        top_k: Number of top results to retrieve (default: 5).

    Returns:
        Formatted string with search results including citations.
    """
    service = get_retrieval_service()

    if collections and len(collections) > 1:
        results = await service.retrieve_multi(
            query=query,
            collection_names=collections,
            limit=top_k,
        )
    else:
        target = collections[0] if collections else collection
        results = await service.retrieve(
            query=query,
            collection_name=target,
            limit=top_k,
        )

    if not results:
        return "No relevant documents found in the knowledge base."

    # Format results with citations for source attribution
    formatted_results = []
    for i, result in enumerate(results, start=1):
        source = result.metadata.get("filename", "unknown")
        page = result.metadata.get("page_num", "")
        chunk = result.metadata.get("chunk_num", "")
        col = result.metadata.get("collection", "")
        page_info = f", page {page}" if page else ""
        chunk_info = f", chunk {chunk}" if chunk else ""
        col_info = f" [{col}]" if col else ""

        formatted_results.append(
            f"[{i}] Source: {source}{page_info}{chunk_info}{col_info} (score: {result.score:.3f})\n"
            f"{result.content}"
        )

    return "Search results (cite sources using [1], [2], etc. in your response):\n\n" + "\n\n".join(
        formatted_results
    )


def _run_async_search(query: str, collection: str, top_k: int) -> str:
    """Run async search in a dedicated event loop within a thread.

    This creates a fresh event loop for each call, avoiding event loop
    conflicts with the main thread or other async contexts.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(search_knowledge_base(query, collection, top_k))
    finally:
        loop.close()


def search_knowledge_base_sync(
    query: str,
    collection: str = "documents",
    top_k: int = 5,
) -> str:
    """Synchronous wrapper for search_knowledge_base.

    Use this function in CrewAI agents where async tools need to run
    in a synchronous context.

    Args:
        query: The search query string.
        collection: Name of the collection to search (default: "default").
        top_k: Number of top results to retrieve (default: 5).

    Returns:
        Formatted string with search results.
    """
    logger.debug(
        "search_knowledge_base_sync called: query=%s, collection=%s, top_k=%s",
        query,
        collection,
        top_k,
    )
    try:
        # Use ThreadPoolExecutor with a dedicated event loop
        # This avoids "Event loop is closed" errors when asyncio.run()
        # is called multiple times or from within an async context
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_run_async_search, query, collection, top_k)
            result = future.result()
        logger.debug("search_knowledge_base_sync completed successfully")
        return result
    except Exception as e:
        logger.error(
            "search_knowledge_base_sync failed: %s",
            str(e),
            exc_info=True,
        )
        raise


__all__ = ["search_knowledge_base", "search_knowledge_base_sync"]
