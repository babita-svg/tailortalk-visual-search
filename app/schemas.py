"""Data models and schemas for TailorTalk visual search and agent."""

from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class SareeMetadata(BaseModel):
    """Metadata attributes for a catalog saree."""

    image_id: str = Field(..., description="Unique alphanumeric identifier (stem of filename)")
    filename: str = Field(..., description="Filename including extension")
    relative_path: str = Field(..., description="Relative path within images directory")
    file_size_bytes: int = Field(..., description="File size in bytes")
    dimensions: Tuple[int, int] = Field(..., description="(width, height) pixel resolution")
    color_palette: List[str] = Field(default_factory=list, description="Top dominant hex colors")
    primary_color: str = Field(default="Unknown", description="Dominant catalog color")
    fabric_type: str = Field(default="Unknown", description="Textile fabric categorization")
    weave_style: str = Field(default="Unknown", description="Craftsmanship weave style")
    border_type: str = Field(default="Unknown", description="Border motif categorization")
    pallu_style: str = Field(default="Unknown", description="Pallu / drape motif design")
    description: str = Field(default="", description="Truthful descriptive summary of saree")


class SimilarityBreakdown(BaseModel):
    """Granular breakdown of multi-signal similarity scores."""

    embedding_similarity: float = Field(..., description="OpenCLIP vision embedding cosine similarity [0.0, 1.0]")
    color_similarity: float = Field(..., description="HSV color distribution & dominant colors similarity [0.0, 1.0]")
    texture_similarity: float = Field(..., description="Sobel gradient texture and weave density similarity [0.0, 1.0]")
    composition_similarity: float = Field(..., description="3x3 spatial layout and composition similarity [0.0, 1.0]")
    final_score: float = Field(..., description="Weighted composite similarity score [0.0, 1.0]")


class SearchResultItem(BaseModel):
    """Individual ranked visual match returned by the search engine."""

    rank: int = Field(..., description="1-indexed final rank after multi-stage reranking")
    image_id: str = Field(..., description="Unique image identifier")
    relative_path: str = Field(..., description="Path to image relative to dataset root")
    score: float = Field(..., description="Composite similarity score [0.0, 1.0]")
    score_percentage: str = Field(..., description="Score formatted as percentage string")
    breakdown: SimilarityBreakdown = Field(..., description="Fine-grained metric breakdown")
    metadata: Optional[SareeMetadata] = Field(None, description="Catalog metadata if available")
    visual_explanation: str = Field(..., description="Deterministic explanation of visual relevance")


class SearchResponse(BaseModel):
    """Top-level visual similarity search response."""

    query_id: str = Field(..., description="Unique query session identifier")
    query_source: str = Field(..., description="Upload path or URL reference")
    total_candidates_retrieved: int = Field(..., description="Number of Stage-1 vector candidates")
    total_results_returned: int = Field(..., description="Number of Stage-3 reranked results")
    results: List[SearchResultItem] = Field(default_factory=list, description="Top-K matched sarees")
    execution_time_ms: float = Field(..., description="Total search pipeline latency in milliseconds")


class AgentToolInput(BaseModel):
    """Input payload for the callable Visual Saree Search tool."""

    image_path_or_url: str = Field(..., description="Local file path, data URI, or valid HTTP(S) image URL")
    top_k: int = Field(default=6, ge=1, le=20, description="Number of top similar sarees to retrieve")
    candidate_k: Optional[int] = Field(default=None, description="Stage-1 vector candidate pool size")
    color_focus: Optional[str] = Field(None, description="Optional color filter or emphasis")


class AgentToolResponse(BaseModel):
    """Structured response from the visual search tool consumed by the Agent."""

    status: str = Field("success", description="'success' or 'error'")
    query: Dict[str, Any] = Field(default_factory=dict)
    results: List[Dict[str, Any]] = Field(default_factory=list)
    error_message: Optional[str] = None


class ChatMessage(BaseModel):
    """Conversation history message."""

    role: str = Field(..., description="'user' or 'assistant' or 'system'")
    content: str = Field(..., description="Message text")
    image_reference: Optional[str] = Field(None, description="Associated query image path if any")
    tool_results: Optional[List[Dict[str, Any]]] = Field(None, description="Structured search results if tool was called")
