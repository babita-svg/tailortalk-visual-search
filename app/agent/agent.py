"""Conversational Agent for TailorTalk.

Coordinates intent recognition, visual similarity search tool invocation,
and natural language response generation.
"""

import json
import logging
import os
import re
from typing import Any, Dict, List, Optional, Tuple, Union
from PIL import Image

from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import VisualSareeSimilaritySearchTool
from app.config import config
from app.schemas import ChatMessage, SearchResultItem

logger = logging.getLogger(__name__)


class TailorTalkAgent:
    """Intelligent saree stylist and visual retrieval agent."""

    def __init__(
        self,
        search_tool: Optional[VisualSareeSimilaritySearchTool] = None,
        api_key: Optional[str] = None,
    ) -> None:
        self.search_tool = search_tool or VisualSareeSimilaritySearchTool()
        self.api_key = api_key or config.agent.gemini_api_key
        self.history: List[ChatMessage] = []
        self.last_query_image: Optional[Union[str, bytes, Image.Image]] = None
        self.last_search_results: Optional[List[Dict[str, Any]]] = None

    def reset_conversation(self) -> None:
        """Clear conversation history and session state."""
        self.history.clear()
        self.last_query_image = None
        self.last_search_results = None

    def detect_intent(self, user_message: str, has_image: bool) -> str:
        """Classify user query intent into VISUAL_SEARCH, COMPARISON, or CONVERSATIONAL."""
        msg = user_message.lower().strip()

        # Check visual search intent triggers
        search_keywords = [
            "similar", "find", "search", "match", "closest", "look like",
            "recommend", "suggest", "like this", "show me", "catalogue",
            "retrieve", "where can i find", "resemble", "near", "comparable"
        ]
        
        comparison_keywords = [
            "which one", "compare", "difference", "explain", "top match",
            "why did", "best match", "highest score", "most similar"
        ]

        if any(kw in msg for kw in comparison_keywords) and self.last_search_results:
            return "COMPARISON"

        if has_image or any(kw in msg for kw in search_keywords):
            # If user asks to search or has an image attached
            return "VISUAL_SEARCH"

        return "CONVERSATIONAL"

    def process_message(
        self,
        user_message: str,
        image_input: Optional[Union[str, bytes, Image.Image]] = None,
        top_k: int = config.retrieval.default_top_k,
    ) -> Tuple[str, Optional[List[Dict[str, Any]]]]:
        """Process user input, manage tool execution, and formulate assistant response.

        Returns:
            Tuple of (assistant_text_reply, structured_search_results_or_None)
        """
        # Store user query image if provided
        if image_input is not None:
            self.last_query_image = image_input

        has_image = bool(image_input or self.last_query_image)
        intent = self.detect_intent(user_message, has_image=has_image)
        logger.info(f"Detected intent: {intent} for message: '{user_message}' (has_image={has_image})")

        # 1. VISUAL SEARCH INTENT
        if intent == "VISUAL_SEARCH":
            query_img = image_input or self.last_query_image
            if not query_img:
                reply = (
                    "I would love to help you find visually matching sarees! Please upload an image "
                    "or provide an image URL so our multi-stage computer vision model can analyze its "
                    "colors, weaves, borders, and textures."
                )
                self.history.append(ChatMessage(role="assistant", content=reply))
                return reply, None

            # Execute tool call
            tool_output = self.search_tool.run(image_reference=query_img, top_k=top_k)
            
            if tool_output.get("status") == "error":
                error_msg = tool_output.get("error_message", "Unknown error during search.")
                reply = f"⚠️ I encountered an issue searching for matching sarees: {error_msg}"
                self.history.append(ChatMessage(role="assistant", content=reply))
                return reply, None

            results = tool_output.get("results", [])
            self.last_search_results = results

            # Formulate response
            reply = self._generate_search_summary_response(user_message, tool_output)
            self.history.append(ChatMessage(role="assistant", content=reply))
            return reply, results

        # 2. COMPARISON INTENT
        elif intent == "COMPARISON":
            reply = self._generate_comparison_response(user_message, self.last_search_results)
            self.history.append(ChatMessage(role="assistant", content=reply))
            return reply, self.last_search_results

        # 3. CONVERSATIONAL INTENT
        else:
            reply = self._generate_conversational_response(user_message)
            self.history.append(ChatMessage(role="assistant", content=reply))
            return reply, None

    def _generate_search_summary_response(self, user_query: str, tool_output: Dict[str, Any]) -> str:
        """Synthesize natural language response summarizing visual matches."""
        results = tool_output.get("results", [])
        if not results:
            return (
                "I analyzed your query image through our vector index and multi-stage reranker, "
                "but couldn't find close matches meeting the similarity threshold."
            )

        top = results[0]
        top_pct = top.get("score_percentage", "N/A")
        top_fabric = top.get("attributes", {}).get("fabric", "Silk")
        top_color = top.get("attributes", {}).get("primary_color", "Multicolor")
        top_weave = top.get("attributes", {}).get("weave", "traditional weave")
        top_border = top.get("attributes", {}).get("border", "ornate border")

        text = (
            f"✨ I've analyzed your saree using our multi-stage computer vision pipeline! "
            f"Here are the top **{len(results)} visual matches** ranked by fine-grained color, weave texture, and border alignment:\n\n"
            f"🏆 **Top Match (Rank 1 — {top_pct} Match)**:\n"
            f"- **Style & Fabric**: {top_color} {top_fabric} featuring {top_weave}.\n"
            f"- **Craftsmanship**: {top_border}.\n"
            f"- **Visual Relevance**: {top.get('visual_explanation')}\n\n"
            f"Browse the visual gallery below to inspect the full score breakdowns, color histograms, and structural pallu details."
        )
        return text

    def _generate_comparison_response(self, user_query: str, results: Optional[List[Dict[str, Any]]]) -> str:
        """Provide detailed visual comparison between top results."""
        if not results or len(results) < 2:
            return (
                "Based on the visual retrieval, the top match is the most relevant saree with the highest "
                "overall harmony in primary hues, fabric texture, and border styling."
            )

        r1 = results[0]
        r2 = results[1]

        text = (
            f"🔍 **Visual Comparison between Top Matches**:\n\n"
            f"• **Rank 1 ({r1.get('score_percentage')} match - {r1.get('attributes', {}).get('fabric', 'Silk')})**:\n"
            f"  Leading match with high color fidelity ({r1.get('similarity_breakdown', {}).get('color_similarity', 0)*100:.0f}%) "
            f"and matching {r1.get('attributes', {}).get('weave', 'weave')}.\n\n"
            f"• **Rank 2 ({r2.get('score_percentage')} match - {r2.get('attributes', {}).get('fabric', 'Silk')})**:\n"
            f"  Alternative option emphasizing {r2.get('attributes', {}).get('primary_color', 'color')} tones "
            f"with {r2.get('similarity_breakdown', {}).get('texture_similarity', 0)*100:.0f}% weave texture alignment.\n\n"
            f"Both pieces share complementary drape characteristics and traditional ornamentation."
        )
        return text

    def _generate_conversational_response(self, user_query: str) -> str:
        """Handle general saree inquiries, styling tips, and conversational greetings."""
        q = user_query.lower()
        if any(w in q for w in ["hello", "hi", "hey", "namaste"]):
            return (
                "Hello! Welcome to **TailorTalk** — your visual saree similarity search and styling agent.\n\n"
                "You can:\n"
                "1. 📸 **Upload or link a saree photo** to find visually matching sarees in our catalog.\n"
                "2. 🎨 **Explore fine-grained similarity** across colors, zari brocade, weaves, and border styles.\n"
                "3. 💬 **Ask styling questions** about Banarasi, Kanjeevaram, Chanderi, Bandhani, or Kalamkari sarees.\n\n"
                "How may I assist your saree search today?"
            )

        if "banarasi" in q:
            return (
                "**Banarasi Sarees** are legendary handcrafted textiles from Varanasi, celebrated for their opulent "
                "gold and silver metallic *zari* brocade, fine silk (*kathan*), and intricate floral *jangla* or *kalga* motifs. "
                "They are timeless choices for weddings and festive occasions."
            )

        if "kanjeevaram" in q or "kanchipuram" in q:
            return (
                "**Kanjeevaram Sarees** from Tamil Nadu are woven from pure mulberry silk with three-ply silk yarn "
                "and heavy gold zari. They are distinguished by their contrasting *korvai* borders with temple (*gopuram*) motifs "
                "and solid jewel-tone color palettes."
            )

        if "chanderi" in q:
            return (
                "**Chanderi Sarees** from Madhya Pradesh combine silk and cotton with sheer, lightweight transparency, "
                "glossy texture, and delicate gold zari *bootis*. Perfect for summer festivities and day events."
            )

        if "bandhani" in q or "bandhej" in q:
            return (
                "**Bandhani Sarees** are traditional tie-dye textiles from Gujarat and Rajasthan featuring intricate "
                "dotted resist patterns, vibrant red-yellow-green festive palettes, and flowing georgette or silk fabrics."
            )

        return (
            "I'm here to help you discover and compare Indian sarees! You can upload an image of any saree you love, "
            "and I will perform a fine-grained visual search across our catalog analyzing dominant hues, weave density, "
            "and border craftsmanship."
        )
