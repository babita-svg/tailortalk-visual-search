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
                    "texture profile, and spatial layout. Call this tool whenever the user wants "
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
                        "candidate_k": {
                            "type": "integer",
                            "description": "Stage-1 vector candidate pool size (default 30, range 1-100).",
                            "default": 30,
                        },
                        "query_description": {
                            "type": "string",
                            "description": "Optional textual focus or description of what visual attributes to prioritize.",
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
        candidate_k: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Query the LLM with function declarations and conversation history to obtain tool call decisions."""
        if not self.api_key:
            return {"mode": "fallback"}

        try:
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
                                    "candidate_k": {
                                        "type": "INTEGER",
                                        "description": "Stage-1 vector candidate pool size.",
                                    },
                                    "aspect_focus": {
                                        "type": "STRING",
                                        "description": "Specific visual attribute focus (e.g. 'color', 'texture', 'spatial', 'overall').",
                                    },
                                },
                            },
                        }
                    ]
                }
            ]

            contents = []
            for h in self.history[-6:]:
                role = "user" if h.role == "user" else "model"
                contents.append({"role": role, "parts": [{"text": h.content}]})

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
                            requested_cand_k = args.get("candidate_k", candidate_k)
                            return {
                                "mode": "tool_call",
                                "tool_name": fc.get("name"),
                                "tool_args": args,
                                "top_k": int(requested_k) if requested_k else top_k,
                                "candidate_k": int(requested_cand_k) if requested_cand_k else candidate_k,
                            }
                        if "text" in part and part["text"].strip():
                            return {
                                "mode": "direct_text",
                                "text": part["text"].strip(),
                            }
        except Exception as e:
            logger.warning(f"LLM tool calling request failed: {e}. Switching to semantic fallback.")

        return {"mode": "fallback"}

    def _call_llm_post_search(
        self,
        user_message: str,
        results: List[Dict[str, Any]],
    ) -> Optional[str]:
        """Ask LLM to summarize search results concisely for the user."""
        if not self.api_key or not results:
            return None

        try:
            import requests

            summary_items = []
            for r in results[:4]:
                attrs = r.get("attributes", {})
                breakdown = r.get("similarity_breakdown", {})
                summary_items.append({
                    "rank": r.get("rank"),
                    "score_percentage": r.get("score_percentage"),
                    "fabric": attrs.get("fabric") if attrs.get("fabric") != "Unknown" else "Not specified",
                    "color": attrs.get("primary_color") if attrs.get("primary_color") != "Unknown" else "Not specified",
                    "color_sim": breakdown.get("color_similarity"),
                    "texture_sim": breakdown.get("texture_similarity"),
                    "spatial_sim": breakdown.get("composition_similarity"),
                    "explanation": r.get("visual_explanation"),
                })

            prompt = (
                f"User asked: '{user_message}'\n\n"
                f"Visual Search Results from catalogue:\n{json.dumps(summary_items, indent=2)}\n\n"
                f"Provide a natural, structured summary highlighting the top match and why it was selected based on "
                f"color harmony, texture profile, and spatial layout. Do not fabricate textile details not present in the data."
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
        candidate_k: Optional[int] = None,
    ) -> Tuple[str, Optional[List[Dict[str, Any]]]]:
        """Process user input through genuine LLM agent tool calling loop.

        Flow:
            1. User Prompt + Optional Image Context
            2. LLM determines if `search_similar_sarees` tool is needed (or semantic fallback)
            3. If tool called: executes SareeSearchEngine (FAISS + Reranker)
            4. Feeds structured retrieval results back to formulate response
            5. Returns assistant text and structured results.
        """
        if image_input is not None:
            self.last_query_image = image_input

        has_image = bool(image_input or self.last_query_image)

        # 1. Ask LLM with Function Declarations
        llm_decision = self._call_llm_with_tools(
            user_message,
            has_image=has_image,
            top_k=top_k,
            candidate_k=candidate_k,
        )

        # 2. Tool Execution Branch
        if llm_decision.get("mode") == "tool_call":
            call_k = llm_decision.get("top_k", top_k)
            call_cand_k = llm_decision.get("candidate_k", candidate_k)
            query_img = image_input or self.last_query_image

            if not query_img:
                reply = (
                    "I would be glad to search for matching sarees! Please upload an image or provide "
                    "a direct image URL so the visual search pipeline can analyze its colors, texture, and spatial composition."
                )
                self.history.append(ChatMessage(role="assistant", content=reply))
                return reply, None

            # Execute tool with candidate_k propagation
            tool_output = self.search_tool.run(image_reference=query_img, top_k=call_k, candidate_k=call_cand_k)
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
        return self._handle_fallback_pipeline(user_message, image_input, top_k, candidate_k)

    def _handle_fallback_pipeline(
        self,
        user_message: str,
        image_input: Optional[Union[str, bytes, Image.Image]],
        top_k: int,
        candidate_k: Optional[int] = None,
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
            tool_output = self.search_tool.run(image_reference=query_img, top_k=top_k, candidate_k=candidate_k)
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
        """Synthesize natural language response summarizing visual matches truthfully without unsupported defaults."""
        results = tool_output.get("results", [])
        if not results:
            return (
                "I analyzed your query image through our vector index and multi-stage reranker, "
                "but couldn't find close matches meeting the similarity threshold."
            )

        top = results[0]
        top_pct = top.get("score_percentage", "N/A")
        attrs = top.get("attributes", {})
        top_fabric = attrs.get("fabric") if attrs.get("fabric") != "Unknown" else "Catalog item"
        top_color = attrs.get("primary_color") if attrs.get("primary_color") != "Unknown" else "Matched"
        top_weave = attrs.get("weave") if attrs.get("weave") != "Unknown" else None
        top_border = attrs.get("border") if attrs.get("border") != "Unknown" else None

        details = []
        if top_weave:
            details.append(f"Weave pattern: {top_weave}")
        if top_border:
            details.append(f"Border style: {top_border}")

        details_str = f"- **Textile Details**: {', '.join(details)}\n" if details else ""

        text = (
            f"✨ I've analyzed your saree using our multi-stage computer vision pipeline! "
            f"Here are the top **{len(results)} visual matches** ranked by fine-grained color distribution, texture profile, and spatial layout:\n\n"
            f"🏆 **Top Match (Rank 1 — {top_pct} Match)**:\n"
            f"- **Item**: {top_color} {top_fabric}\n"
            f"{details_str}"
            f"- **Visual Relevance**: {top.get('visual_explanation')}\n\n"
            f"Browse the visual gallery below to inspect the full score breakdowns and similarity metrics."
        )
        return text

    def _generate_comparison_response(self, user_query: str, results: Optional[List[Dict[str, Any]]]) -> str:
        """Provide detailed visual comparison between top results."""
        if not results or len(results) < 2:
            return (
                "Based on the visual retrieval, the top match is the most relevant saree with the highest "
                "overall harmony in color distribution, texture profile, and spatial composition."
            )

        r1 = results[0]
        r2 = results[1]
        a1 = r1.get("attributes", {})
        a2 = r2.get("attributes", {})

        f1 = a1.get("fabric") if a1.get("fabric") != "Unknown" else "Item"
        f2 = a2.get("fabric") if a2.get("fabric") != "Unknown" else "Item"

        text = (
            f"🔍 **Visual Comparison between Top Matches**:\n\n"
            f"• **Rank 1 ({r1.get('score_percentage')} match - {f1})**:\n"
            f"  Leading match with {r1.get('similarity_breakdown', {}).get('color_similarity', 0)*100:.0f}% color fidelity "
            f"and {r1.get('similarity_breakdown', {}).get('texture_similarity', 0)*100:.0f}% texture alignment.\n\n"
            f"• **Rank 2 ({r2.get('score_percentage')} match - {f2})**:\n"
            f"  Alternative match with {r2.get('similarity_breakdown', {}).get('color_similarity', 0)*100:.0f}% color fidelity "
            f"and {r2.get('similarity_breakdown', {}).get('composition_similarity', 0)*100:.0f}% spatial layout alignment.\n\n"
            f"Both pieces share high visual harmony with the query image."
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
                "2. 🎨 **Explore fine-grained similarity** across colors, texture profiles, and spatial composition.\n"
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
            "and I will perform a fine-grained visual search across our catalog analyzing dominant hues, texture profile, "
            "and spatial composition."
        )
