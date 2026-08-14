"""TailorTalk - Streamlit Web Application.

A modern, responsive interface for conversational saree styling and fine-grained
visual similarity retrieval with multi-stage vector search and reranking.
"""

from io import BytesIO
import json
import logging
from pathlib import Path
import sys
import time
from typing import Any, Dict, List, Optional
from PIL import Image
import streamlit as st

# Ensure root workspace is accessible
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app.agent.agent import TailorTalkAgent
from app.config import config
from app.image_utils.loader import ImageLoader
from app.ingestion.metadata import extract_dominant_color_palette
from app.ingestion.pipeline import IngestionPipeline
from app.retrieval.search import SareeSearchEngine

# Configure page
st.set_page_config(
    page_title="TailorTalk — Saree Visual Search Agent",
    page_icon="🥻",
    layout="wide",
    initial_sidebar_state="expanded",
)

logger = logging.getLogger("TailorTalk.UI")


# Initialize session state singletons
if "agent" not in st.session_state:
    st.session_state.agent = TailorTalkAgent()

if "search_engine" not in st.session_state:
    st.session_state.search_engine = SareeSearchEngine()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Namaste! Welcome to **TailorTalk** — your AI fashion stylist and visual saree search assistant. "
                "Upload a saree photo, provide an image URL, or choose a sample from the sidebar to find "
                "closest matching sarees based on fine-grained weave texture, color harmony, and border craftsmanship."
            ),
            "results": None,
        }
    ]

if "current_query_image" not in st.session_state:
    st.session_state.current_query_image = None

if "current_query_source" not in st.session_state:
    st.session_state.current_query_source = None

if "search_results" not in st.session_state:
    st.session_state.search_results = None


def render_sidebar():
    """Render catalog status, hyperparameters, and sample gallery."""
    with st.sidebar:
        st.header("🥻 Catalog & Settings")
        
        # Index status
        count = st.session_state.search_engine.vector_store.count()
        if count > 0:
            st.success(f"**Vector Index Active**: {count} Sarees Indexed")
        else:
            st.warning("**Index Empty**: Click below to build index.")

        with st.expander("📊 Index & Model Details", expanded=False):
            st.write(f"**Embedding Model**: `{config.model.model_name}`")
            st.write(f"**Pretrained Weights**: `{config.model.pretrained}`")
            st.write(f"**Vector Dimension**: `{config.model.embedding_dim}`")
            st.write(f"**Distance Metric**: `Cosine Similarity (IndexFlatIP)`")
            
            if st.button("🔄 Rebuild Catalog Index", use_container_width=True):
                with st.spinner("Indexing saree catalog..."):
                    pipeline = IngestionPipeline()
                    indexed_count = pipeline.run(force_reindex=True)
                    st.session_state.search_engine = SareeSearchEngine()
                    st.success(f"Indexed {indexed_count} sarees successfully!")
                    st.rerun()

        st.markdown("---")
        st.subheader("🎯 Retrieval Parameters")
        top_k = st.slider("Top Results (K)", min_value=1, max_value=12, value=config.retrieval.default_top_k)
        candidate_k = st.slider("Stage-1 Candidates", min_value=10, max_value=50, value=config.retrieval.candidate_top_k)

        with st.expander("⚖️ Fine-Grained Reranking Weights", expanded=False):
            st.caption("Adjust multi-signal reranking contributions (normalized automatically):")
            w_emb = st.slider("Base Embedding (CLIP)", 0.0, 1.0, config.retrieval.weight_embedding, 0.05)
            w_col = st.slider("Color Distribution (HSV/Lab)", 0.0, 1.0, config.retrieval.weight_color, 0.05)
            w_tex = st.slider("Weave / Texture Gradient", 0.0, 1.0, config.retrieval.weight_texture, 0.05)
            w_comp = st.slider("Border & Pallu Layout", 0.0, 1.0, config.retrieval.weight_composition, 0.05)
            
            # Apply weights dynamically
            st.session_state.search_engine.reranker.w_emb = w_emb
            st.session_state.search_engine.reranker.w_col = w_col
            st.session_state.search_engine.reranker.w_tex = w_tex
            st.session_state.search_engine.reranker.w_comp = w_comp

        st.markdown("---")
        st.subheader("🖼️ Sample Query Gallery")
        st.caption("Click any sample saree to test visual similarity retrieval:")

        sample_images = sorted(list(config.storage.images_dir.glob("*.jpg")))[:6]
        for img_p in sample_images:
            col1, col2 = st.columns([1, 2])
            with col1:
                try:
                    s_img = Image.open(img_p)
                    st.image(s_img, width=60)
                except Exception:
                    pass
            with col2:
                label = img_p.stem.replace("_", " ")[:24] + "..."
                if st.button(label, key=f"sample_{img_p.name}", use_container_width=True):
                    st.session_state.current_query_image = img_p
                    st.session_state.current_query_source = img_p.name
                    trigger_search(img_p, top_k, candidate_k)
                    st.rerun()

        st.markdown("---")
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.agent.reset_conversation()
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Conversation cleared. How can I assist you with your saree search?",
                    "results": None,
                }
            ]
            st.session_state.current_query_image = None
            st.session_state.current_query_source = None
            st.session_state.search_results = None
            st.rerun()

    return top_k, candidate_k


def trigger_search(image_source: Any, top_k: int, candidate_k: int) -> None:
    """Execute retrieval solely via UI -> Agent -> Tool -> SearchEngine -> Agent -> UI."""
    try:
        with st.spinner("Analyzing colors, weave textures, and borders through Agent..."):
            # Update search engine candidate size if changed in sidebar
            st.session_state.agent.search_tool.search_engine.reranker.candidate_k = candidate_k

            # Sole retrieval execution: routed through the Agent's tool calling loop
            agent_reply, results_list = st.session_state.agent.process_message(
                user_message="Find sarees visually similar to this image.",
                image_input=image_source,
                top_k=top_k,
            )

            # Record in chat & store results
            st.session_state.messages.append({
                "role": "user",
                "content": "Find sarees visually similar to this image.",
                "image": image_source,
                "results": None,
            })

            st.session_state.messages.append({
                "role": "assistant",
                "content": agent_reply,
                "results": results_list,
            })

            st.session_state.search_results = results_list
    except Exception as e:
        st.error(f"Search failed: {str(e)}")


def render_query_preview(query_img: Optional[Any]):
    """Display active query image with extracted color palette chips."""
    if query_img is None:
        return

    try:
        loaded_img = ImageLoader.load(query_img)
        palette = extract_dominant_color_palette(loaded_img, num_colors=5)

        col_img, col_info = st.columns([1, 3])
        with col_img:
            st.image(loaded_img, caption="Active Query Saree", width=180)
        with col_info:
            st.markdown("#### 🎨 Query Visual Signature")
            st.write(f"**Resolution**: `{loaded_img.size[0]} x {loaded_img.size[1]} px`")
            st.write("**Extracted Dominant Color Palette**:")
            
            # Render color chips
            chips_html = "".join([
                f"<span style='display:inline-block; background-color:{c}; width:28px; height:28px; "
                f"border-radius:6px; margin-right:8px; border:1px solid #ccc;' title='{c}'></span>"
                for c in palette
            ])
            st.markdown(chips_html, unsafe_allow_html=True)
            st.caption("Extracted via HSV multi-bin quantization and Sobel spatial gradient analysis.")
    except Exception as e:
        st.warning(f"Could not render query image preview: {str(e)}")


def render_results_gallery(results: List[Any]):
    """Render high-contrast visual match cards with score breakdown and textile tags."""
    if not results:
        return

    st.markdown("### 🏆 Top Matched Sarees (Multi-Stage Reranked)")
    
    # 3 columns for card gallery
    cols = st.columns(3)
    for idx, item in enumerate(results):
        col = cols[idx % 3]
        with col:
            # Handle dictionary or SearchResultItem object
            if isinstance(item, dict):
                rank = item.get("rank", idx + 1)
                score = item.get("score", 0.0)
                score_pct = item.get("score_percentage", f"{score*100:.1f}%")
                rel_path = item.get("image_path", "")
                attrs = item.get("attributes", {}) or {}
                breakdown = item.get("similarity_breakdown", {}) or {}
                explanation = item.get("visual_explanation", "")
                primary_color = attrs.get("primary_color", "Saree")
                fabric_type = attrs.get("fabric", "Silk")
                weave_style = attrs.get("weave", "Traditional")
                border_type = attrs.get("border", "Zari")
                emb_sim = breakdown.get("embedding_similarity", 0.0)
                col_sim = breakdown.get("color_similarity", 0.0)
                tex_sim = breakdown.get("texture_similarity", 0.0)
                comp_sim = breakdown.get("composition_similarity", 0.0)
            else:
                rank = item.rank
                score = item.score
                score_pct = item.score_percentage
                rel_path = item.relative_path
                meta = item.metadata
                primary_color = meta.primary_color if meta else "Saree"
                fabric_type = meta.fabric_type if meta else "Silk"
                weave_style = meta.weave_style if meta else "Traditional"
                border_type = meta.border_type if meta else "Zari"
                emb_sim = item.breakdown.embedding_similarity
                col_sim = item.breakdown.color_similarity
                tex_sim = item.breakdown.texture_similarity
                comp_sim = item.breakdown.composition_similarity
                explanation = item.visual_explanation

            img_path = config.storage.images_dir / rel_path
            if img_path.exists():
                try:
                    s_img = Image.open(img_path)
                    st.image(s_img, use_container_width=True)
                except Exception:
                    st.error("Image render error")

            # Rank and Score badge
            score_color = "#16a34a" if score >= 0.80 else "#2563eb" if score >= 0.65 else "#d97706"
            st.markdown(
                f"<div style='display:flex; justify-content:space-between; align-items:center; margin-top:4px;'>"
                f"<span style='background:#f1f5f9; color:#0f172a; padding:2px 8px; border-radius:4px; font-weight:600; font-size:12px;'>Rank #{rank}</span>"
                f"<span style='background:{score_color}; color:#fff; padding:2px 8px; border-radius:4px; font-weight:700; font-size:13px;'>{score_pct} Match</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

            # Metadata attributes
            st.markdown(
                f"**{primary_color or 'Saree'} {fabric_type or 'Silk'}**\n\n"
                f"• **Weave**: {weave_style or 'Traditional'}\n"
                f"• **Border**: {border_type or 'Zari'}"
            )

            # Score breakdown expandable
            with st.expander("🔍 Similarity Breakdown", expanded=False):
                st.progress(float(emb_sim), text=f"Base Vision Embedding: {emb_sim*100:.1f}%")
                st.progress(float(col_sim), text=f"Color Harmony: {col_sim*100:.1f}%")
                st.progress(float(tex_sim), text=f"Weave / Texture: {tex_sim*100:.1f}%")
                st.progress(float(comp_sim), text=f"Spatial Composition: {comp_sim*100:.1f}%")

            if explanation:
                st.caption(f"💡 *{explanation}*")
            st.markdown("---")


def main():
    st.title("🥻 TailorTalk — Visual Saree Similarity Search Agent")
    st.markdown(
        "A fine-grained computer vision retrieval system that analyzes **dominant colors, weave texture, "
        "border motifs, and pallu craftsmanship** using OpenCLIP embeddings, FAISS vector indexing, and multi-signal reranking."
    )

    top_k, candidate_k = render_sidebar()

    # Input Area Tabs: File Upload vs URL
    st.markdown("#### 📥 Query Image Input")
    tab_upload, tab_url = st.tabs(["📁 Upload Image File", "🔗 Image Web URL"])

    query_to_process = None

    with tab_upload:
        uploaded_file = st.file_uploader(
            "Upload a saree photo (JPEG, PNG, WEBP, up to 10MB)",
            type=["jpg", "jpeg", "png", "webp"],
            key="file_uploader_input",
        )
        if uploaded_file is not None:
            bytes_data = uploaded_file.read()
            if st.button("🔍 Search Matching Sarees for Upload", type="primary", use_container_width=True):
                st.session_state.current_query_image = bytes_data
                st.session_state.current_query_source = uploaded_file.name
                trigger_search(bytes_data, top_k, candidate_k)
                st.rerun()

    with tab_url:
        url_input = st.text_input("Enter direct image URL (e.g. https://example.com/saree.jpg)", key="url_input")
        if url_input:
            if st.button("🔍 Search Matching Sarees from URL", type="primary", use_container_width=True):
                st.session_state.current_query_image = url_input.strip()
                st.session_state.current_query_source = url_input.strip()
                trigger_search(url_input.strip(), top_k, candidate_k)
                st.rerun()

    # Render active query image preview if present
    if st.session_state.current_query_image is not None:
        st.markdown("---")
        render_query_preview(st.session_state.current_query_image)

    # Render Visual Match Gallery if search results exist
    if st.session_state.search_results and st.session_state.search_results.results:
        st.markdown("---")
        render_results_gallery(st.session_state.search_results.results)

    # Interactive Conversational Chat Area
    st.markdown("---")
    st.markdown("### 💬 Conversational Saree Stylist")
    st.caption("Ask questions about fabrics, compare matches, or ask for styling advice:")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("image"):
                try:
                    img_to_show = ImageLoader.load(msg["image"])
                    st.image(img_to_show, width=120)
                except Exception:
                    pass

    # Chat Input
    if user_prompt := st.chat_input("Ask about saree styling, weaves, or compare matches..."):
        # Add user message to state
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Agent processing
        with st.chat_message("assistant"):
            with st.spinner("TailorTalk is thinking..."):
                reply, results_dict = st.session_state.agent.process_message(
                    user_message=user_prompt,
                    image_input=st.session_state.current_query_image,
                    top_k=top_k,
                )
                st.markdown(reply)
                
                # If tool was called in chat, update search results
                if results_dict:
                    # Sync with latest search response
                    if st.session_state.agent.search_tool.search_engine:
                        pass
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply,
                    "results": results_dict,
                })


if __name__ == "__main__":
    main()
