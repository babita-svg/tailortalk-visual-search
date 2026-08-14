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
