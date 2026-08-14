"""Unit tests for Agent tool definitions, execution, and structured result formatting."""

import json
from unittest.mock import MagicMock
import pytest

from app.agent.tools import VisualSareeSimilaritySearchTool
from app.schemas import SearchResultItem, SimilarityBreakdown, SareeMetadata, SearchResponse


@pytest.fixture
def mock_search_response():
    """Create a mock structured search response."""
    metadata = SareeMetadata(
        image_id="banarasi_crimson",
        filename="banarasi_crimson_red_gold_zari_brocade.jpg",
        relative_path="banarasi_crimson_red_gold_zari_brocade.jpg",
        primary_color="Crimson Red",
        fabric_type="Pure Katan Silk",
        weave_style="Banarasi Brocade",
        border_type="Zari Border",
        pallu_style="Heavy Floral Zari",
        description="Rich crimson red silk saree with intricate gold zari brocade work.",
    )
    breakdown = SimilarityBreakdown(
        embedding_similarity=0.92,
        color_similarity=0.88,
        texture_similarity=0.85,
        composition_similarity=0.80,
    )
    result = SearchResultItem(
        rank=1,
        image_id="banarasi_crimson",
        relative_path="banarasi_crimson_red_gold_zari_brocade.jpg",
        score=0.895,
        score_percentage="89.5%",
        breakdown=breakdown,
        metadata=metadata,
        visual_explanation="Strong crimson hue harmony and fine gold brocade alignment.",
    )
    return SearchResponse(
        query_id="q123",
        query_source="query.jpg",
        results=[result],
        total_candidates_retrieved=20,
        execution_time_ms=25.4,
    )


def test_tool_execution_with_mock_engine(mock_search_response):
    """Test executing VisualSareeSimilaritySearchTool and verifying structured JSON output."""
    mock_engine = MagicMock()
    mock_engine.search.return_value = mock_search_response
    
    tool = VisualSareeSimilaritySearchTool(search_engine=mock_engine)
    data = tool.run(image_reference="test_query.jpg", top_k=5)
    
    assert data["status"] == "success"
    assert "results" in data
    assert len(data["results"]) == 1
    assert data["results"][0]["rank"] == 1
    assert data["results"][0]["score"] == 0.895
    assert data["results"][0]["attributes"]["primary_color"] == "Crimson Red"
    assert data["results"][0]["attributes"]["fabric"] == "Pure Katan Silk"
    assert "embedding_similarity" in data["results"][0]["similarity_breakdown"]


def test_tool_empty_query_error():
    """Test executing tool with empty reference returns structured error."""
    tool = VisualSareeSimilaritySearchTool(search_engine=MagicMock())
    res = tool.run(image_reference="", top_k=5)
    assert res["status"] == "error"
    assert "error_message" in res
