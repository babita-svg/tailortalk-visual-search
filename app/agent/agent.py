"""Conversational Agent for TailorTalk.

Implements genuine LLM function/tool calling architecture with Gemini API / OpenCLIP-FAISS
search tool, handling visual similarity search requests, comparative styling reasoning,
and conversational textile guidance.
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
    """Intelligent saree stylist and visual retrieval agent powered by genuine tool calling."""

    def __init__(
        self,
        search_tool: Optional[VisualSareeSimilaritySearchTool] = None,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
    ) -> None:
        self.search_tool = search_tool or VisualSareeSimilaritySearchTool()
        self.api_key = api_key or config.agent.gemini_api_key or os.getenv("GEMINI_API_KEY", "")
        self.model_name = model_name or config.agent.model_name or "gemini-3.7-flash"
        self.history: List[ChatMessage] = []
        self.last_query_image: Optional[Union[str, bytes, Image.Image]] = None
        self.last_search_results: Optional[List[Dict[str, Any]]] = None

    def reset_conversation(self) -> None:
        """Clear conversation history and session state."""
        self.history.clear()
        self.last_query_image = None
        self.last_search_results = None

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Return standardized OpenAI/Gemini tool declaration schema for search_similar_sarees."""
        return [
            {
                "name": "search_similar_sarees",
                "description": (
                    "Search the saree catalog for visually similar sarees based on color distribution, "
                    "weave texture, border motifs, and pallu layout. Call this tool whenever the user wants "
                    "to find matches, search the catalogue, retrieve visually similar items, or analyze an image."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "top_k": {
                            "type": "integer",
                            "description": "Number of top matching sarees to return (default 6, range 1-20).",
                            "default": 6,
                        },
                        "query_description": {
                            "type": "string",
                            "description": "Optional textual focus or description of what visual attributes to prioritize (e.g. 'gold zari border', 'red silk').",
                        },
                    },
                    "required": [],
                },
            }
        ]

    def _call_llm_with_tools(
        self,
        user_message: str,
        has_image: bool,
        top_k: int = config.retrieval.default_top_k,
    ) -> Dict[str, Any]:
        """Query the LLM with function declarations and conversation history to obtain tool call decisions."""
        if not self.api_key:
            return {"mode": "fallback"}

        try:
            # Attempt to use google.genai or standard Gemini REST endpoints
            import requests

            tools_payload = [
                {
                    "function_declarations": [
                        {
                            "name": "search_similar_sarees",
                            "description": (
                                "Execute fine-grained visual similarity search on the saree catalog. "
                                "Call this tool whenever the user asks to find, match, search, recommend, "
                                "or retrieve sarees visually similar to an uploaded/provided image."
                            ),
                            "parameters": {
                                "type": "OBJECT",
                                "properties": {
                                    "top_k": {
                                        "type": "INTEGER",
                                        "description": "Number of top results to return (1-20).",
                                    },
                                    "aspect_focus": {
                                        "type": "STRING",
                                        "description": "Specific visual attribute focus (e.g. 'color', 'weave', 'border', 'overall').",
                                    },
                                },
                            },
                        }
                    ]
                }
            ]

            # Build messages contents
            contents = []
            for h in self.history[-6:]:
                role = "user" if h.role == "user" else "model"
                contents.append({"role": role, "parts": [{"text": h.content}]})

            # Append current user prompt with multimodal context note if image present
            current_text = user_message
            if has_image:
                current_text += "\n[Context: User has uploaded/provided a query saree image in the current session]"

            contents.append({"role": "user", "parts": [{"text": current_text}]})

            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
            payload = {
                "contents": contents,
                "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
                "tools": tools_payload,
                "toolConfig": {
                    "functionCallingConfig": {"mode": "AUTO"}
                },
                "generationConfig": {
                    "temperature": 0.2,
                    "maxOutputTokens": 800,
                },
            }

            resp = requests.post(endpoint, json=payload, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    for part in parts:
                        if "functionCall" in part:
                            fc = part["functionCall"]
                            args = fc.get("args", {})
                            requested_k = args.get("top_k", top_k)
                            return {
                                "mode": "tool_call",
                                "tool_name": fc.get("name"),
                                "tool_args": args,
                                "top_k": int(requested_k) if requested_k else top_k,
                            }
                        if "text" in part and part["text"].strip():
                            return {
                                "mode": "direct_text",
                                "text": part["text"].strip(),
                            }

        except Exception as e:
            logger.warning(f"LLM tool calling API invocation failed, transitioning to deterministic classifier: {e}")

        return {"mode": "fallback"}

    def _call_llm_post_search(
        self,
        user_message: str,
        tool_results: List[Dict[str, Any]],
    ) -> Optional[str]:
        """Synthesize natural language response using LLM based on actual structured search tool results."""
        if not self.api_key or not tool_results:
            return None

        try:
            import requests

            prompt = (
                f"User asked: '{user_message}'\n\n"
                f"The visual search tool `search_similar_sarees` returned the following genuine top catalog matches:\n"
                f"{json.dumps(tool_results[:4], indent=2)}\n\n"
                f"Synthesize an expert, concise, fashion-stylist summary explaining why these top matches were retrieved, "
                f"highlighting specific color harmonies, weave textures, border styles, and zari details from the results. "
                f"Do not hallucinate products or fabrics not in the result set."
            )

            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
            payload = {
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
                "generationConfig": {"temperature": 0.3, "maxOutputTokens": 600},
            }

            resp = requests.post(endpoint, json=payload, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    for p in parts:
                        if "text" in p and p["text"].strip():
                            return p["text"].strip()
        except Exception as e:
            logger.warning(f"Post-search LLM synthesis failed: {e}")

        return None

    def process_message(
        self,
        user_message: str,
        image_input: Optional[Union[str, bytes, Image.Image]] = None,
        top_k: int = config.retrieval.default_top_k,
    ) -> Tuple[str, Optional[List[Dict[str, Any]]]]:
        """Process user input through genuine LLM agent tool calling loop.

        Flow:
            1. User Prompt + Optional Image Context
            2. LLM determines if `search_similar_sarees` tool is needed (or semantic fallback)
            3. If tool called: executes SareeSearchEngine (FAISS + Reranker)
            4. Feeds structured retrieval results back to formulate response
            5. Returns assistant text and structured results.
        """
        # Store user query image if provided
        if image_input is not None:
            self.last_query_image = image_input

        has_image = bool(image_input or self.last_query_image)

        # 1. Ask LLM with Function Declarations
        llm_decision = self._call_llm_with_tools(user_message, has_image=has_image, top_k=top_k)

        # 2. Tool Execution Branch
        if llm_decision.get("mode") == "tool_call":
            call_k = llm_decision.get("top_k", top_k)
            query_img = image_input or self.last_query_image

            if not query_img:
                reply = (
                    "I would be glad to search for matching sarees! Please upload an image or provide "
                    "a direct image URL so the visual search pipeline can analyze its colors, weave, and border patterns."
                )
                self.history.append(ChatMessage(role="assistant", content=reply))
                return reply, None

            # Execute tool
            tool_output = self.search_tool.run(image_reference=query_img, top_k=call_k)
            if tool_output.get("status") == "error":
                error_msg = tool_output.get("error_message", "Unknown error during visual search.")
                reply = f"⚠️ Visual search encountered an issue: {error_msg}"
                self.history.append(ChatMessage(role="assistant", content=reply))
                return reply, None

            results = tool_output.get("results", [])
            self.last_search_results = results

            # Formulate response using LLM or structured template
            llm_text = self._call_llm_post_search(user_message, results)
            reply = llm_text if llm_text else self._generate_search_summary_response(user_message, tool_output)
            self.history.append(ChatMessage(role="assistant", content=reply))
            return reply, results

        # 3. Direct LLM Text Response Branch (Conversational / Stylist Q&A)
        elif llm_decision.get("mode") == "direct_text":
            reply = llm_decision.get("text", "")
            self.history.append(ChatMessage(role="assistant", content=reply))
            return reply, None

        # 4. Fallback Reasoning (Used when offline or no API key configured)
        return self._handle_fallback_pipeline(user_message, image_input, top_k)

    def _handle_fallback_pipeline(
        self,
        user_message: str,
        image_input: Optional[Union[str, bytes, Image.Image]],
        top_k: int,
    ) -> Tuple[str, Optional[List[Dict[str, Any]]]]:
        """Deterministic agent pipeline for offline or API-independent environments."""
        msg = user_message.lower().strip()
        query_img = image_input or self.last_query_image
        has_img = bool(query_img)

        # Check comparison intent
        is_comparison = any(
            phrase in msg
            for phrase in ["which one", "compare", "difference", "explain top", "why is this", "most similar", "rank 1"]
        ) and bool(self.last_search_results)

        # Check visual search intent
        is_search = (
            has_img
            and (
                any(w in msg for w in ["similar", "find", "search", "match", "closest", "look like", "recommend", "show me"])
                or not msg
                or msg == "find sarees visually similar to this image."
            )
        )

        if is_comparison:
            reply = self._generate_comparison_response(user_message, self.last_search_results)
            self.history.append(ChatMessage(role="assistant", content=reply))
            return reply, self.last_search_results

        if is_search:
            tool_output = self.search_tool.run(image_reference=query_img, top_k=top_k)
            if tool_output.get("status") == "error":
                reply = f"⚠️ Visual search failed: {tool_output.get('error_message')}"
                self.history.append(ChatMessage(role="assistant", content=reply))
                return reply, None

            results = tool_output.get("results", [])
            self.last_search_results = results
            reply = self._generate_search_summary_response(user_message, tool_output)
            self.history.append(ChatMessage(role="assistant", content=reply))
            return reply, results

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
            f"Browse the visual gallery below to inspect the full score breakdowns, color histograms, and structural details."
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
                "**Banarasi Sarees** are celebrated handcrafted textiles from Varanasi, recognized for their opulent "
                "gold and silver metallic *zari* brocade, fine silk (*kathan*), and intricate floral *jangla* or *kalga* motifs. "
                "They are classic choices for weddings and formal festivities."
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

