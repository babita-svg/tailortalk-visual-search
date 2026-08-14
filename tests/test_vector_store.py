"""Unit tests for FAISS vector store indexing, persistence, duplicate prevention, and integrity."""

import os
import shutil
import tempfile
from pathlib import Path
import numpy as np
import pytest

from app.exceptions import VectorStoreIndexError
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
    store = FAISSVectorStore(index_file=idx_path, metadata_file=meta_path, dimension=512)
    assert store.count() == 0
    assert store.dimension == 512


def test_add_and_search(temp_index_files, mock_sarees_and_vectors):
    """Test indexing vectors and performing cosine similarity search."""
    idx_path, meta_path = temp_index_files
    vectors, ids, metadata = mock_sarees_and_vectors
    store = FAISSVectorStore(index_file=idx_path, metadata_file=meta_path, dimension=512)

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
    store1 = FAISSVectorStore(index_file=idx_path, metadata_file=meta_path, dimension=512)
    store1.add(vectors, ids, metadata)
    store1.save()

    # Load in store2
    store2 = FAISSVectorStore(index_file=idx_path, metadata_file=meta_path, dimension=512)
    store2.load()
    assert store2.count() == len(metadata)

    results = store2.search(vectors[3], top_k=1)
    assert results[0][0] == "saree_003"


def test_clear_method(temp_index_files, mock_sarees_and_vectors):
    """Test resetting store in memory and on disk."""
    idx_path, meta_path = temp_index_files
    vectors, ids, metadata = mock_sarees_and_vectors
    store = FAISSVectorStore(index_file=idx_path, metadata_file=meta_path, dimension=512)
    store.add(vectors, ids, metadata)
    store.save()
    assert store.count() == 10
    assert idx_path.exists()
    assert meta_path.exists()

    store.clear()
    assert store.count() == 0
    assert not idx_path.exists()
    assert not meta_path.exists()


def test_duplicate_id_prevention(temp_index_files, mock_sarees_and_vectors):
    """Test that duplicate image IDs raise VectorStoreIndexError."""
    idx_path, meta_path = temp_index_files
    vectors, ids, metadata = mock_sarees_and_vectors
    store = FAISSVectorStore(index_file=idx_path, metadata_file=meta_path, dimension=512)

    # 1. Batch internal duplicate
    dup_ids = ids.copy()
    dup_ids[1] = dup_ids[0]
    with pytest.raises(VectorStoreIndexError, match="Duplicate image IDs detected in addition batch"):
        store.add(vectors, dup_ids, metadata)

    # 2. Existing store conflict
    store.add(vectors[:5], ids[:5], metadata[:5])
    assert store.count() == 5

    # Re-adding existing ID
    with pytest.raises(VectorStoreIndexError, match="already exists in the vector store"):
        store.add(vectors[0:1], [ids[0]], [metadata[0]])


def test_index_model_compatibility_validation(temp_index_files, mock_sarees_and_vectors):
    """Test that loading an index built with mismatched model name or pretrained weights raises VectorStoreIndexError."""
    import json
    idx_path, meta_path = temp_index_files
    vectors, ids, metadata = mock_sarees_and_vectors
    store = FAISSVectorStore(index_file=idx_path, metadata_file=meta_path, dimension=512)
    store.add(vectors, ids, metadata)
    store.save()

    # Modify metadata file to simulate incompatible model
    with open(meta_path, "r", encoding="utf-8") as f:
        meta_json = json.load(f)
    meta_json["model_name"] = "IncompatibleModel-v999"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_json, f)

    store_incompat = FAISSVectorStore(index_file=idx_path, metadata_file=meta_path, dimension=512)
    with pytest.raises(VectorStoreIndexError, match="Model architecture mismatch"):
        store_incompat.load()
