"""Unit tests for TailorTalkAgent with LLM function calling and conversational styling reasoning."""

from unittest.mock import MagicMock, patch
import pytest
from app.agent.agent import TailorTalkAgent
from app.agent.tools import VisualSareeSimilaritySearchTool


@pytest.fixture
def mock_search_tool():
    tool = MagicMock(spec=VisualSareeSimilaritySearchTool)
    tool.run.return_value = {
        "status": "success",
        "results": [
            {
                "rank": 1,
                "image_id": "banarasi_01",
                "image_path": "banarasi_crimson.jpg",
                "score": 0.91,
                "score_percentage": "91.0%",
                "similarity_breakdown": {
                    "embedding_similarity": 0.93,
                    "color_similarity": 0.90,
                    "texture_similarity": 0.88,
                    "composition_similarity": 0.85,
                },
                "attributes": {
                    "primary_color": "Crimson Red",
                    "fabric": "Silk",
                    "weave": "Banarasi Brocade",
                    "border": "Gold Zari",
                },
                "visual_explanation": "Strong crimson color alignment and gold floral brocade match.",
            },
            {
                "rank": 2,
                "image_id": "kanjeevaram_02",
                "image_path": "kanjeevaram_ruby.jpg",
                "score": 0.84,
                "score_percentage": "84.0%",
                "similarity_breakdown": {
                    "embedding_similarity": 0.85,
                    "color_similarity": 0.84,
                    "texture_similarity": 0.82,
                    "composition_similarity": 0.80,
                },
                "attributes": {
                    "primary_color": "Ruby Red",
                    "fabric": "Mulberry Silk",
                    "weave": "Korvai Weave",
                    "border": "Temple Zari",
                },
                "visual_explanation": "Complementary red hue with temple zari border.",
            },
        ],
    }
    return tool


def test_agent_tool_schema_declaration():
    """Verify tool definition format conforms to OpenAI/Gemini function calling standard."""
    agent = TailorTalkAgent()
    tools = agent.get_tool_definitions()
    assert len(tools) == 1
    assert tools[0]["name"] == "search_similar_sarees"
    assert "parameters" in tools[0]
    assert "top_k" in tools[0]["parameters"]["properties"]


def test_agent_conversational_greeting():
    """Verify agent answers greetings without triggering search tool."""
    mock_tool = MagicMock(spec=VisualSareeSimilaritySearchTool)
    agent = TailorTalkAgent(search_tool=mock_tool)
    reply, results = agent.process_message(user_message="Hello, can you help me?")
    assert "TailorTalk" in reply or "assist" in reply
    assert results is None
    mock_tool.run.assert_not_called()


def test_agent_textile_knowledge():
    """Verify agent provides textile expertise on Banarasi sarees."""
    mock_tool = MagicMock(spec=VisualSareeSimilaritySearchTool)
    agent = TailorTalkAgent(search_tool=mock_tool)
    reply, results = agent.process_message(user_message="Tell me about Banarasi sarees")
    assert "Banarasi" in reply
    assert "zari" in reply.lower() or "brocade" in reply.lower()
    assert results is None
    mock_tool.run.assert_not_called()


def test_agent_visual_search_execution(mock_search_tool):
    """Verify search tool is called when image is supplied."""
    agent = TailorTalkAgent(search_tool=mock_search_tool)
    reply, results = agent.process_message(
        user_message="Find sarees similar to this image",
        image_input="sample_query.jpg",
        top_k=5,
    )
    mock_search_tool.run.assert_called_once_with(image_reference="sample_query.jpg", top_k=5, candidate_k=None)
    assert results is not None
    assert len(results) == 2
    assert "Top Match" in reply or "analyzed" in reply.lower()


def test_agent_comparison_flow(mock_search_tool):
    """Verify comparative reasoning on previously retrieved items."""
    agent = TailorTalkAgent(search_tool=mock_search_tool)
    # 1. Search
    agent.process_message(user_message="Search matching sarees", image_input="sample_query.jpg")
    # 2. Compare
    reply, results = agent.process_message(user_message="Which one is most similar? Compare top 2.")
    assert "Comparison" in reply or "Rank 1" in reply
    assert "Rank 2" in reply
    assert results is not None
