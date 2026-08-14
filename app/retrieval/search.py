"""End-to-end multi-stage saree visual search engine.

Coordinates query loading, vision embedding generation, FAISS candidate retrieval,
and fine-grained multi-modal reranking.
"""

import logging
from pathlib import Path
import time
from typing import Optional, Union
import uuid
from PIL import Image

from app.config import config
from app.embeddings.image_encoder import BaseImageEncoder, get_image_encoder
from app.exceptions import VectorStoreIndexError
from app.image_utils.loader import ImageLoader
from app.retrieval.reranker import FineGrainedSareeReranker
from app.retrieval.vector_store import BaseVectorStore, FAISSVectorStore
from app.schemas import SearchResponse, SearchResultItem

logger = logging.getLogger(__name__)


class SareeSearchEngine:
    """Unified engine for fine-grained visual saree similarity search."""

    def __init__(
        self,
        vector_store: Optional[BaseVectorStore] = None,
        encoder: Optional[BaseImageEncoder] = None,
        reranker: Optional[FineGrainedSareeReranker] = None,
    ) -> None:
        self.vector_store = vector_store or FAISSVectorStore()
        self.encoder = encoder or get_image_encoder()
        self.reranker = reranker or FineGrainedSareeReranker()

        # Attempt to load index if exists
        if self.vector_store.exists() and self.vector_store.count() == 0:
            self.vector_store.load()

    def search(
        self,
        query: Union[str, Path, bytes, Image.Image],
        top_k: int = config.retrieval.default_top_k,
        candidate_k: int = config.retrieval.candidate_top_k,
    ) -> SearchResponse:
        """Execute multi-stage visual similarity search.

        Args:
            query: File path, HTTP URL, byte buffer, or PIL Image.
            top_k: Number of final reranked items to return.
            candidate_k: Candidate pool size retrieved from vector index in Stage 1.

        Returns:
            SearchResponse containing ranked results and latency metrics.
        """
        if top_k <= 0:
            raise ValueError(f"top_k must be a positive integer, received {top_k}")
        if candidate_k <= 0:
            raise ValueError(f"candidate_k must be a positive integer, received {candidate_k}")
        if candidate_k < top_k:
            candidate_k = top_k

        start_time = time.time()
        query_id = str(uuid.uuid4())[:8]

        # Stage 0: Load and normalize query image
        query_img = ImageLoader.load(query)
        query_source_name = str(query) if isinstance(query, (str, Path)) else f"Image-Query-{query_id}"

        # Verify index readiness
        if self.vector_store.count() == 0:
            if not self.vector_store.load():
                raise VectorStoreIndexError(
                    "Saree catalog index is empty. Please run the dataset ingestion pipeline first."
                )

        # Stage 1: Generate normalized vision embedding
        query_vector = self.encoder.encode_image(query_img)

        # Stage 2: Fast Vector Search (Retrieve broad candidate pool using candidate_k)
        candidates = self.vector_store.search(query_vector, top_k=candidate_k)

        # Stage 3: Fine-grained multi-modal reranking (Color + Texture + Composition)
        ranked_results = self.reranker.rerank_candidates(
            query_image=query_img,
            candidates=candidates,
            top_k=top_k,
        )

        elapsed_ms = (time.time() - start_time) * 1000.0

        return SearchResponse(
            query_id=query_id,
            query_source=query_source_name,
            total_candidates_retrieved=len(candidates),
            total_results_returned=len(ranked_results),
            results=ranked_results,
            execution_time_ms=round(elapsed_ms, 2),
        )


# Global singleton engine instance
_GLOBAL_ENGINE: Optional[SareeSearchEngine] = None


def get_search_engine() -> SareeSearchEngine:
    """Retrieve singleton instance of SareeSearchEngine."""
    global _GLOBAL_ENGINE
    if _GLOBAL_ENGINE is None:
        _GLOBAL_ENGINE = SareeSearchEngine()
    return _GLOBAL_ENGINE
