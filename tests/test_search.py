"""Unit tests for the end-to-end multi-stage search engine pipeline."""

from unittest.mock import MagicMock
import numpy as np
import pytest
from PIL import Image

from app.retrieval.search import SareeSearchEngine
from app.schemas import SareeMetadata, SearchResponse


@pytest.fixture
def mock_search_pipeline():
    """Build a search engine with mocked vector store and encoder for unit tests."""
    mock_encoder = MagicMock()
    mock_encoder.encode_image.return_value = np.ones(512, dtype=np.float32) / np.sqrt(512)
    
    mock_meta = SareeMetadata(
        image_id="saree_sample",
        filename="sample.jpg",
        relative_path="sample.jpg",
        file_size_bytes=1024,
        dimensions=(800, 600),
        fabric_type="Silk",
        primary_color="Green",
        weave_style="Kanjeevaram",
    )
    
    mock_store = MagicMock()
    mock_store.count.return_value = 1
    mock_store.search.return_value = [
        ("saree_sample", 0.88, mock_meta.model_dump())
    ]
    
    engine = SareeSearchEngine(encoder=mock_encoder, vector_store=mock_store)
    return engine


def test_search_pipeline_execution(mock_search_pipeline):
    """Test running search returns valid SearchResponse."""
    img = Image.new("RGB", (200, 200), color=(0, 150, 50))
    response = mock_search_pipeline.search(query=img, top_k=1)
    
    assert isinstance(response, SearchResponse)
    assert len(response.results) >= 1
    assert response.results[0].image_id == "saree_sample"
    assert response.results[0].metadata.fabric_type == "Silk"
    assert response.execution_time_ms >= 0


def test_candidate_k_propagation_to_vector_store():
    """Verify candidate_k controls the Stage-1 vector store candidate retrieval pool."""
    mock_encoder = MagicMock()
    mock_encoder.encode_image.return_value = np.ones(512, dtype=np.float32) / np.sqrt(512)
    
    mock_store = MagicMock()
    mock_store.count.return_value = 50
    # Simulate returning 25 candidates
    mock_store.search.return_value = [
        (f"saree_{i}", 0.9 - (i * 0.01), {
            "image_id": f"saree_{i}",
            "filename": f"saree_{i}.jpg",
            "relative_path": f"saree_{i}.jpg",
            "file_size_bytes": 1000,
            "dimensions": [300, 300],
            "primary_color": "Red",
            "fabric_type": "Silk",
            "weave_style": "Zari",
            "border_type": "Gold",
            "pallu_style": "Brocade",
        })
        for i in range(25)
    ]
    
    engine = SareeSearchEngine(encoder=mock_encoder, vector_store=mock_store)
    img = Image.new("RGB", (100, 100), color=(200, 50, 50))
    
    # Request candidate_k=25, top_k=5
    resp = engine.search(query=img, top_k=5, candidate_k=25)
    
    # Verify vector store received candidate_k=25
    mock_store.search.assert_called_once()
    call_args, call_kwargs = mock_store.search.call_args
    assert call_kwargs.get("top_k") == 25 or (len(call_args) > 1 and call_args[1] == 25)
    
    # Verify final returned items are capped at top_k=5
    assert len(resp.results) == 5
    assert resp.total_candidates_retrieved == 25
    assert resp.total_results_returned == 5


def test_candidate_k_auto_promotion_when_less_than_top_k():
    """Verify candidate_k is automatically raised to top_k if candidate_k < top_k."""
    mock_encoder = MagicMock()
    mock_encoder.encode_image.return_value = np.ones(512, dtype=np.float32) / np.sqrt(512)
    
    mock_store = MagicMock()
    mock_store.count.return_value = 10
    mock_store.search.return_value = []
    
    engine = SareeSearchEngine(encoder=mock_encoder, vector_store=mock_store)
    img = Image.new("RGB", (100, 100), color=(200, 50, 50))
    
    # top_k=8, candidate_k=3 -> candidate_k should be promoted to 8
    engine.search(query=img, top_k=8, candidate_k=3)
    call_args, call_kwargs = mock_store.search.call_args
    assert call_kwargs.get("top_k") == 8 or (len(call_args) > 1 and call_args[1] == 8)

