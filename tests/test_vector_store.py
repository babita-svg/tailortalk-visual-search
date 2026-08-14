"""Unit tests for FAISS vector store indexing, persistence, and similarity search."""

import os
import shutil
import tempfile
from pathlib import Path
import numpy as np
import pytest

from app.retrieval.vector_store import FAISSVectorStore


@pytest.fixture
def temp_index_files():
    """Create temporary paths for vector index and metadata files."""
    tmp_dir = tempfile.mkdtemp()
    idx_path = Path(tmp_dir) / "test_saree.index"
    meta_path = Path(tmp_dir) / "test_saree.json"
    yield idx_path, meta_path
    shutil.rmtree(tmp_dir, ignore_errors=True)


@pytest.fixture
def mock_sarees_and_vectors():
    """Generate normalized synthetic vectors and metadata dictionaries."""
    dim = 512
    n_samples = 10
    rng = np.random.RandomState(42)
    
    raw_vectors = rng.randn(n_samples, dim).astype(np.float32)
    norms = np.linalg.norm(raw_vectors, axis=1, keepdims=True)
    unit_vectors = raw_vectors / norms
    
    image_ids = [f"saree_{i:03d}" for i in range(n_samples)]
    metadata_list = [
        {
            "id": f"saree_{i:03d}",
            "filename": f"saree_{i:03d}.jpg",
            "name": f"Test Saree {i}",
            "fabric": "Silk",
            "primary_color": "Red" if i % 2 == 0 else "Blue",
            "weave": "Zari",
        }
        for i in range(n_samples)
    ]
    return unit_vectors, image_ids, metadata_list


def test_vector_store_initialization(temp_index_files):
    """Test initializing a new empty vector store."""
    idx_path, meta_path = temp_index_files
    store = FAISSVectorStore(index_path=idx_path, metadata_path=meta_path, dimension=512)
    assert store.count() == 0
    assert store.dimension == 512


def test_add_and_search(temp_index_files, mock_sarees_and_vectors):
    """Test indexing vectors and performing cosine similarity search."""
    idx_path, meta_path = temp_index_files
    vectors, ids, metadata = mock_sarees_and_vectors
    store = FAISSVectorStore(index_path=idx_path, metadata_path=meta_path, dimension=512)
    
    store.add(vectors, ids, metadata)
    assert store.count() == len(metadata)
    
    # Query with exact first vector: top match must be id saree_000 with score ~1.0
    query_vec = vectors[0]
    results = store.search(query_vec, top_k=3)
    
    assert len(results) == 3
    top_id, top_score, top_meta = results[0]
    assert top_id == "saree_000"
    assert pytest.approx(top_score, abs=1e-4) == 1.0
    assert top_meta["name"] == "Test Saree 0"


def test_save_and_load_persistence(temp_index_files, mock_sarees_and_vectors):
    """Test saving index to disk and reloading into a new instance."""
    idx_path, meta_path = temp_index_files
    vectors, ids, metadata = mock_sarees_and_vectors
    store1 = FAISSVectorStore(index_path=idx_path, metadata_path=meta_path, dimension=512)
    store1.add(vectors, ids, metadata)
    store1.save()
    
    # Load in store2
    store2 = FAISSVectorStore(index_path=idx_path, metadata_path=meta_path, dimension=512)
    store2.load()
    assert store2.count() == len(metadata)
    
    results = store2.search(vectors[3], top_k=1)
    assert results[0][0] == "saree_003"
