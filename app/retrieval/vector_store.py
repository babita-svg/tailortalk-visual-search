"""Vector store abstraction and FAISS implementation.

Provides persistent vector indexing and fast inner-product (cosine) nearest-neighbor
retrieval for saree image embeddings.
"""

from abc import ABC, abstractmethod
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import faiss
import numpy as np

from app.config import config
from app.exceptions import VectorStoreIndexError
from app.schemas import SareeMetadata

logger = logging.getLogger(__name__)


class BaseVectorStore(ABC):
    """Abstract interface for vector database implementations."""

    @abstractmethod
    def add(self, vectors: np.ndarray, image_ids: List[str], metadata: List[Dict[str, Any]]) -> None:
        """Index a batch of vectors with associated IDs and metadata."""
        pass

    @abstractmethod
    def search(self, query_vector: np.ndarray, top_k: int) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Perform vector similarity search returning (image_id, similarity_score, metadata)."""
        pass

    @abstractmethod
    def save(self, index_path: Optional[Path] = None, metadata_path: Optional[Path] = None) -> None:
        """Persist index and metadata to disk."""
        pass

    @abstractmethod
    def load(self, index_path: Optional[Path] = None, metadata_path: Optional[Path] = None) -> bool:
        """Load index and metadata from disk."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Return total number of indexed vectors."""
        pass

    @abstractmethod
    def exists(self) -> bool:
        """Check if a populated index is available on disk."""
        pass


class FAISSVectorStore(BaseVectorStore):
    """FAISS-based vector index utilizing IndexFlatIP for exact cosine similarity."""

    def __init__(
        self,
        dimension: int = config.model.embedding_dim,
        index_file: Optional[Path] = None,
        metadata_file: Optional[Path] = None,
        index_path: Optional[Path] = None,
        metadata_path: Optional[Path] = None,
    ) -> None:
        self.dimension = dimension
        self.index_file = index_file or index_path or config.storage.faiss_index_file
        self.metadata_file = metadata_file or metadata_path or config.storage.metadata_file
        self._index: Optional[faiss.IndexFlatIP] = None
        self._id_to_index: Dict[str, int] = {}
        self._index_to_id: Dict[int, str] = {}
        self._metadata_store: Dict[str, Dict[str, Any]] = {}
        self._initialize_empty_index()

    def _initialize_empty_index(self) -> None:
        """Create a new in-memory FAISS IndexFlatIP."""
        self._index = faiss.IndexFlatIP(self.dimension)
        self._id_to_index.clear()
        self._index_to_id.clear()
        self._metadata_store.clear()

    def exists(self) -> bool:
        """Check if serialized index and metadata files exist."""
        return self.index_file.exists() and self.metadata_file.exists()

    def count(self) -> int:
        """Return number of indexed items."""
        return self._index.ntotal if self._index is not None else 0

    def add(self, vectors: np.ndarray, image_ids: List[str], metadata: List[Dict[str, Any]]) -> None:
        """Add vectors and associated metadata to FAISS index."""
        if len(vectors) == 0:
            return

        if len(image_ids) != len(vectors) or len(metadata) != len(vectors):
            raise VectorStoreIndexError(
                f"Mismatch in input lengths: {len(vectors)} vectors, {len(image_ids)} IDs, {len(metadata)} metadata items."
            )

        vectors = np.ascontiguousarray(vectors.astype(np.float32))
        
        # Verify normalization
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1.0, norms)
        vectors = vectors / norms

        start_idx = self.count()
        self._index.add(vectors)

        for i, (img_id, meta) in enumerate(zip(image_ids, metadata)):
            idx = start_idx + i
            self._id_to_index[img_id] = idx
            self._index_to_id[idx] = img_id
            self._metadata_store[img_id] = meta

        logger.info(f"Added {len(vectors)} items to FAISS index. Total count: {self.count()}")

    def search(self, query_vector: np.ndarray, top_k: int = config.retrieval.candidate_top_k) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Search nearest items for a query vector.

        Returns:
            List of (image_id, cosine_score, metadata_dict)
        """
        if self._index is None or self.count() == 0:
            # Try lazy loading
            if self.exists():
                self.load()
            else:
                raise VectorStoreIndexError("Vector index is empty. Run dataset ingestion to build the index.")

        if query_vector.ndim == 1:
            query_vector = np.expand_dims(query_vector, axis=0)

        query_vector = np.ascontiguousarray(query_vector.astype(np.float32))
        norm = np.linalg.norm(query_vector, axis=1, keepdims=True)
        norm = np.where(norm == 0, 1.0, norm)
        query_vector = query_vector / norm

        actual_k = min(top_k, self.count())
        if actual_k == 0:
            return []

        distances, indices = self._index.search(query_vector, actual_k)
        
        results: List[Tuple[str, float, Dict[str, Any]]] = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1 or idx not in self._index_to_id:
                continue
            image_id = self._index_to_id[idx]
            meta = self._metadata_store.get(image_id, {})
            # Clamp cosine similarity to [-1.0, 1.0]
            score = float(np.clip(dist, -1.0, 1.0))
            results.append((image_id, score, meta))

        return results

    def get_metadata(self, image_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve stored metadata for an image ID."""
        return self._metadata_store.get(image_id)

    def save(self, index_path: Optional[Path] = None, metadata_path: Optional[Path] = None) -> None:
        """Serialize FAISS index and metadata store to disk."""
        target_index = index_path or self.index_file
        target_meta = metadata_path or self.metadata_file

        target_index.parent.mkdir(parents=True, exist_ok=True)
        target_meta.parent.mkdir(parents=True, exist_ok=True)

        try:
            faiss.write_index(self._index, str(target_index))
            
            payload = {
                "dimension": self.dimension,
                "total_items": self.count(),
                "id_to_index": self._id_to_index,
                "index_to_id": {str(k): v for k, v in self._index_to_id.items()},
                "metadata": self._metadata_store,
            }
            with open(target_meta, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)

            logger.info(f"Successfully saved FAISS index to '{target_index}' ({self.count()} vectors).")
        except Exception as e:
            raise VectorStoreIndexError(f"Failed to save FAISS index: {str(e)}") from e

    def load(self, index_path: Optional[Path] = None, metadata_path: Optional[Path] = None) -> bool:
        """Load FAISS index and metadata from disk."""
        target_index = index_path or self.index_file
        target_meta = metadata_path or self.metadata_file

        if not target_index.exists() or not target_meta.exists():
            logger.warning(f"Index files not found at '{target_index}' or '{target_meta}'.")
            return False

        try:
            self._index = faiss.read_index(str(target_index))
            with open(target_meta, "r", encoding="utf-8") as f:
                payload = json.load(f)

            self.dimension = payload.get("dimension", self._index.d)
            self._id_to_index = payload.get("id_to_index", {})
            self._index_to_id = {int(k): v for k, v in payload.get("index_to_id", {}).items()}
            self._metadata_store = payload.get("metadata", {})

            logger.info(f"Loaded FAISS index with {self.count()} items from '{target_index}'.")
            return True
        except Exception as e:
            logger.error(f"Failed to load FAISS index: {str(e)}")
            raise VectorStoreIndexError(f"Could not load index: {str(e)}") from e
