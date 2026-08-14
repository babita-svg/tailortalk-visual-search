"""Agent tool implementations for visual saree similarity search.

Provides a callable, typed tool interface compliant with LangChain / standard function calling.
"""

from dataclasses import asdict
import json
import logging
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, Field

from app.config import config
from app.exceptions import TailorTalkError
from app.retrieval.search import SareeSearchEngine, get_search_engine
from app.schemas import AgentToolInput, AgentToolResponse

logger = logging.getLogger(__name__)


class VisualSareeSimilaritySearchTool:
    """Tool that executes fine-grained visual similarity search on the saree catalog."""

    name: str = "search_similar_sarees"
    description: str = (
        "Search the saree catalog for visually and aesthetically similar sarees based on an input image "
        "(file path, uploaded byte data, or URL). Returns ranked results with similarity scores, breakdown, "
        "and textile attributes."
    )
    args_schema = AgentToolInput

    def __init__(self, search_engine: Optional[SareeSearchEngine] = None) -> None:
        self.search_engine = search_engine or get_search_engine()

    def __call__(
        self,
        image_reference: Union[str, bytes],
        top_k: int = config.retrieval.default_top_k,
    ) -> Dict[str, Any]:
        """Execute the visual search tool."""
        return self.run(image_reference=image_reference, top_k=top_k)

    def run(
        self,
        image_reference: Union[str, bytes],
        top_k: int = config.retrieval.default_top_k,
    ) -> Dict[str, Any]:
        """Execute search and return a clean, structured JSON-compatible response."""
        try:
            if not image_reference:
                return {
                    "status": "error",
                    "error_message": "No query image was provided. Please upload an image or provide a valid image URL.",
                    "results": [],
                }

            top_k = max(1, min(top_k, config.retrieval.max_top_k))
            response = self.search_engine.search(query=image_reference, top_k=top_k)

            formatted_results = []
            for item in response.results:
                formatted_results.append({
                    "rank": item.rank,
                    "image_id": item.image_id,
                    "image_path": item.relative_path,
                    "score": item.score,
                    "score_percentage": item.score_percentage,
                    "similarity_breakdown": {
                        "embedding_similarity": item.breakdown.embedding_similarity,
                        "color_similarity": item.breakdown.color_similarity,
                        "texture_similarity": item.breakdown.texture_similarity,
                        "composition_similarity": item.breakdown.composition_similarity,
                    },
                    "attributes": {
                        "primary_color": item.metadata.primary_color if item.metadata else None,
                        "fabric": item.metadata.fabric_type if item.metadata else None,
                        "weave": item.metadata.weave_style if item.metadata else None,
                        "border": item.metadata.border_type if item.metadata else None,
                        "pallu": item.metadata.pallu_style if item.metadata else None,
                    },
                    "visual_explanation": item.visual_explanation,
                })

            return {
                "status": "success",
                "query": {
                    "query_id": response.query_id,
                    "query_source": response.query_source,
                    "total_candidates": response.total_candidates_retrieved,
                    "execution_time_ms": response.execution_time_ms,
                },
                "results": formatted_results,
            }

        except TailorTalkError as e:
            logger.error(f"TailorTalk search tool error: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "results": [],
            }
        except Exception as e:
            logger.error(f"Unexpected search tool failure: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error_message": f"Visual search failed unexpectedly: {str(e)}",
                "results": [],
            }
