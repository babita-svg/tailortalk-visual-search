"""Data models and schemas for TailorTalk.

Defines Pydantic models for dataset metadata, visual feature vectors,
search queries, reranking breakdowns, and tool interfaces.
"""

from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class SareeMetadata(BaseModel):
    """Metadata attributes stored for each catalog saree."""

    image_id: str = Field(..., description="Unique identifier for the saree image")
    filename: str = Field(..., description="Original image filename")
    relative_path: str = Field(..., description="Path relative to dataset root")
    file_size_bytes: int = Field(0, description="Image file size in bytes")
    dimensions: Tuple[int, int] = Field((0, 0), description="(width, height) in pixels")
    color_palette: List[str] = Field(default_factory=list, description="Extracted hex color codes")
    primary_color: Optional[str] = Field(None, description="Dominant color name or tone")
    fabric_type: Optional[str] = Field(None, description="Estimated or labeled fabric style")
    weave_style: Optional[str] = Field(None, description="Weave or print pattern")
    border_type: Optional[str] = Field(None, description="Border design classification")
    pallu_style: Optional[str] = Field(None, description="Pallu ornamentation description")
    description: Optional[str] = Field(None, description="Brief curated or visual description")
    visual_features: Optional[Dict[str, Any]] = Field(None, description="Precomputed fine-grained visual descriptors for zero-latency reranking")


class VisualFeatures(BaseModel):
    """Fine-grained visual feature descriptors used for multi-stage reranking."""

    # 3D Color Histogram (Hue-Saturation-Value) flattened and normalized
    color_histogram: List[float] = Field(default_factory=list)
    # Texture gradient energy across spatial frequency bands
    texture_energy: List[float] = Field(default_factory=list)
    # 3x3 Spatial Grid Color distribution for composition/layout alignment
    spatial_grid_colors: List[List[float]] = Field(default_factory=list)


class SimilarityBreakdown(BaseModel):
    """Explainable similarity sub-scores contributing to the final match score."""

    embedding_similarity: float = Field(..., description="Cosine similarity of normalized vision embeddings")
    color_similarity: float = Field(..., description="Histogram intersection / Lab color harmony similarity")
    texture_similarity: float = Field(..., description="Weave pattern and gradient texture similarity")
    composition_similarity: float = Field(..., description="Spatial layout, border & pallu structure similarity")
    final_score: float = Field(..., description="Weighted composite similarity score (0.0 to 1.0)")


class SearchResultItem(BaseModel):
    """Individual ranked result from visual similarity search."""

    rank: int = Field(..., description="Result position (1-indexed)")
    image_id: str = Field(..., description="Unique saree image ID")
    relative_path: str = Field(..., description="Relative path to saree image")
    score: float = Field(..., description="Final composite similarity score between 0.0 and 1.0")
    score_percentage: str = Field(..., description="Formatted similarity percentage")
    breakdown: SimilarityBreakdown = Field(..., description="Detailed score breakdown")
    metadata: Optional[SareeMetadata] = Field(None, description="Detailed catalog metadata")
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
    tool_results: Optional[List[SearchResultItem]] = Field(None, description="Structured search results if tool was called")
