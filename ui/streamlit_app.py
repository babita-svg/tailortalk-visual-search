"""TailorTalk - Streamlit Web Application.

A modern, responsive interface for conversational saree styling and fine-grained
visual similarity retrieval with multi-stage vector search, reranking, and full catalogue browsing.
"""

import csv
from io import BytesIO
import json
import logging
import math
from pathlib import Path
import sys
import time
from typing import Any, Dict, List, Optional
from PIL import Image
import streamlit as st

# Ensure root workspace is accessible
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.agent.agent import TailorTalkAgent
from app.agent.tools import VisualSareeSimilaritySearchTool
from app.config import config
from app.image_utils.loader import ImageLoader
from app.image_utils.validation import ImageValidator
from app.ingestion.metadata import extract_dominant_color_palette
from app.ingestion.pipeline import IngestionPipeline
from app.retrieval.search import SareeSearchEngine, get_search_engine

# Configure Streamlit page immediately so the UI shell mounts instantly
st.set_page_config(
    page_title="TailorTalk — Saree Visual Search Agent",
    page_icon="🥻",
    layout="wide",
    initial_sidebar_state="expanded",
)

logger = logging.getLogger("TailorTalk.UI")


# --- Resource Caching for Production Deployment ---

@st.cache_resource(show_spinner="Initializing OpenCLIP vision model & FAISS search engine...")
def get_cached_search_engine() -> SareeSearchEngine:
    """Initialize and cache the singleton search engine and vision encoder across Streamlit sessions."""
    return get_search_engine()


@st.cache_resource(show_spinner="Initializing TailorTalk Stylist Agent...")
def get_cached_agent() -> TailorTalkAgent:
    """Initialize and cache the conversational agent with the visual similarity search tool."""
    engine = get_cached_search_engine()
    tool = VisualSareeSimilaritySearchTool(search_engine=engine)
    return TailorTalkAgent(search_tool=tool)


@st.cache_data
def load_catalog_data() -> List[Dict[str, Any]]:
    """Load and parse the authoritative 83-record catalogue CSV with robust type conversion."""
    csv_path = config.storage.base_dir / "data" / "byrappa_tejas_31july.csv"
    if not csv_path.exists():
        return []
    items: List[Dict[str, Any]] = []
    try:
        with open(csv_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                name = (row.get("Name") or "").strip()
                sku = (row.get("SKU") or "").strip()
                stock_str = (row.get("Stock") or "").strip()
                retail_str = (row.get("Retail Price") or "").strip()
                disc_str = (row.get("Discounted Price") or "").strip()
                img_url = (row.get("image_url") or "").strip()
                link = (row.get("Website Link") or "").strip()

                try:
                    stock_val = int(float(stock_str)) if stock_str else None
                except Exception:
                    stock_val = None

                try:
                    retail_val = float(retail_str) if retail_str else None
                except Exception:
                    retail_val = None

                try:
                    disc_val = float(disc_str) if disc_str else None
                except Exception:
                    disc_val = None

                items.append({
                    "id": idx,
                    "name": name or f"Saree {sku}",
                    "sku": sku or "Unknown",
                    "stock": stock_val,
                    "retail_price": retail_val,
                    "discounted_price": disc_val,
                    "image_url": img_url,
                    "website_link": link,
                })
    except Exception as e:
        logger.error(f"Failed to read catalog CSV '{csv_path}': {e}")
    return items


def init_session_state():
    """Initialize state variables safely."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Namaste! Welcome to **TailorTalk** — your fashion stylist and visual saree search assistant. "
                    "Upload a saree photo, provide an image URL, or choose a sample to find "
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


init_session_state()


def render_sidebar():
    """Render catalog status, hyperparameters, and sample gallery."""
    with st.sidebar:
        st.header("🥻 Catalog & Settings")

        # Safely obtain search engine
        search_engine = None
        try:
            search_engine = get_cached_search_engine()
        except Exception as e:
            st.warning(f"⚠️ Vision model loading: {e}")

        # Index status
        if search_engine and search_engine.vector_store:
            count = search_engine.vector_store.count()
            if count > 0:
                st.success(f"**Vector Index Active**: {count} Sarees Indexed")
            else:
                st.info("**Vector Index**: 83 Catalogue items ready. Click below to index.")
        else:
            st.info("**Vector Index**: Initializing...")

        with st.expander("📊 Index & Model Details", expanded=False):
            st.write(f"**Embedding Model**: `{config.model.model_name}`")
            st.write(f"**Pretrained Weights**: `{config.model.pretrained}`")
            st.write(f"**Vector Dimension**: `{config.model.embedding_dim}`")
            st.write(f"**Distance Metric**: `Cosine Similarity (IndexFlatIP)`")

            if st.button("🔄 Rebuild Catalog Index", use_container_width=True):
                with st.spinner("Indexing saree catalog..."):
                    try:
                        pipeline = IngestionPipeline()
                        indexed_count = pipeline.run(force_reindex=True)
                        st.cache_resource.clear()
                        st.success(f"Indexed {indexed_count} sarees successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Rebuild failed: {e}")

        st.markdown("---")
        st.subheader("🎯 Retrieval Parameters")
        top_k = st.slider("Top Results (K)", min_value=1, max_value=12, value=config.retrieval.default_top_k)
        candidate_k = st.slider("Stage-1 Candidates", min_value=10, max_value=50, value=config.retrieval.candidate_top_k)

        with st.expander("⚖️ Fine-Grained Reranking Weights", expanded=False):
            st.caption("Adjust multi-signal reranking contributions (normalized automatically):")
            w_emb = st.slider("Base Embedding (CLIP)", 0.0, 1.0, config.retrieval.weight_embedding, 0.05)
            w_col = st.slider("Color Distribution (HSV/Lab)", 0.0, 1.0, config.retrieval.weight_color, 0.05)
            w_tex = st.slider("Gradient-based Texture Statistics", 0.0, 1.0, config.retrieval.weight_texture, 0.05)
            w_comp = st.slider("Spatial Composition Similarity", 0.0, 1.0, config.retrieval.weight_composition, 0.05)

            # Apply weights dynamically if engine available
            if search_engine and search_engine.reranker:
                search_engine.reranker.w_emb = w_emb
                search_engine.reranker.w_col = w_col
                search_engine.reranker.w_tex = w_tex
                search_engine.reranker.w_comp = w_comp

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
            try:
                agent = get_cached_agent()
                agent.reset_conversation()
            except Exception:
                pass
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
        agent = get_cached_agent()
        with st.spinner("Analyzing colors, weave textures, and borders through Agent..."):
            if agent.search_tool and agent.search_tool.search_engine:
                agent.search_tool.search_engine.reranker.candidate_k = candidate_k

            # Sole retrieval execution: routed through the Agent's tool calling loop
            agent_reply, results_list = agent.process_message(
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
        logger.error(f"Search failed: {e}", exc_info=True)
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
            st.caption("Extracted via HSV multi-bin quantization and adjacent-pixel gradient statistics.")
    except Exception as e:
        st.warning(f"Could not render query image preview: {str(e)}")


def render_results_gallery(results: List[Any]):
    """Render high-contrast visual match cards with score breakdown and textile tags."""
    if not results:
        return

    st.markdown("### 🏆 Top Matched Sarees (Multi-Stage Reranked)")

    cols = st.columns(3)
    for idx, item in enumerate(results):
        col = cols[idx % 3]
        with col:
            if isinstance(item, dict):
                rank = item.get("rank", idx + 1)
                score = item.get("score", 0.0)
                score_pct = item.get("score_percentage", f"{score*100:.1f}%")
                rel_path = item.get("image_path", "")
                attrs = item.get("attributes", {}) or {}
                breakdown = item.get("similarity_breakdown", {}) or {}
                explanation = item.get("visual_explanation", "")
                sku = attrs.get("sku") or item.get("sku") or "Unknown"
                prod_name = attrs.get("product_name") or item.get("product_name") or None
                stock = attrs.get("stock") if attrs.get("stock") is not None else item.get("stock")
                retail_price = attrs.get("retail_price") or item.get("retail_price")
                disc_price = attrs.get("discounted_price") or item.get("discounted_price")
                website_link = attrs.get("website_link") or item.get("website_link")
                primary_color = attrs.get("primary_color", "Unknown")
                fabric_type = attrs.get("fabric", "Unknown")
                weave_style = attrs.get("weave", "Unknown")
                border_type = attrs.get("border", "Unknown")
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
                sku = meta.sku if meta and meta.sku else "Unknown"
                prod_name = meta.product_name if meta and meta.product_name else None
                stock = meta.stock if meta and meta.stock is not None else None
                retail_price = meta.retail_price if meta else None
                disc_price = meta.discounted_price if meta else None
                website_link = meta.website_link if meta else None
                primary_color = meta.primary_color if meta and meta.primary_color else "Unknown"
                fabric_type = meta.fabric_type if meta and meta.fabric_type else "Unknown"
                weave_style = meta.weave_style if meta and meta.weave_style else "Unknown"
                border_type = meta.border_type if meta and meta.border_type else "Unknown"
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

            # Product Name & SKU
            display_title = prod_name if prod_name else (f"{primary_color} {fabric_type} Saree" if (primary_color != "Unknown" or fabric_type != "Unknown") else "Catalog Saree")
            st.markdown(f"**{display_title}**")
            st.caption(f"SKU: `{sku}`")

            # Price & Stock
            price_parts = []
            if disc_price is not None:
                price_parts.append(f"<strong style='font-size:15px; color:#0f172a;'>₹{disc_price:,.0f}</strong>")
            if retail_price is not None and (disc_price is None or retail_price != disc_price):
                price_parts.append(f"<span style='text-decoration:line-through; color:#64748b; font-size:13px;'>₹{retail_price:,.0f}</span>")

            stock_str = f"{stock} in stock" if (stock is not None and stock >= 0) else ("Out of stock" if stock == 0 else "Unknown")
            stock_badge = f"<span style='font-size:12px; color:{'#16a34a' if stock and stock > 0 else '#64748b'};'>• {stock_str}</span>"

            if price_parts:
                st.markdown(f"<div>{' '.join(price_parts)} {stock_badge}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div><span style='color:#64748b; font-size:13px;'>Price: Unknown</span> {stock_badge}</div>", unsafe_allow_html=True)

            # Direct Website Link button using ImageValidator.is_valid_url
            if website_link and ImageValidator.is_valid_url(website_link):
                st.markdown(f"<a href='{website_link}' target='_blank' style='display:inline-block; margin-top:6px; margin-bottom:6px; padding:4px 12px; background:#0284c7; color:#ffffff; text-decoration:none; border-radius:4px; font-size:12px; font-weight:600;'>🔗 View Product</a>", unsafe_allow_html=True)

            # Score breakdown expandable
            with st.expander("🔍 Similarity Breakdown", expanded=False):
                st.progress(float(emb_sim), text=f"Base Vision Embedding: {emb_sim*100:.1f}%")
                st.progress(float(col_sim), text=f"Color Harmony: {col_sim*100:.1f}%")
                st.progress(float(tex_sim), text=f"Texture Statistics: {tex_sim*100:.1f}%")
                st.progress(float(comp_sim), text=f"Spatial Composition: {comp_sim*100:.1f}%")

            if explanation:
                st.caption(f"💡 *{explanation}*")
            st.markdown("---")


def render_catalog_browser(top_k: int, candidate_k: int):
    """Render the full 83-record catalogue browser with live filtering, pagination, and visual search triggers."""
    catalog_items = load_catalog_data()
    st.subheader(f"📖 Saree Catalogue ({len(catalog_items)} Total Products)")
    st.caption("Authoritative Byrappa Silks catalogue dataset (`data/byrappa_tejas_31july.csv`).")

    col_search, col_filter, col_page_size = st.columns([3, 2, 1])
    with col_search:
        search_query = st.text_input("🔍 Search by Name or SKU", placeholder="e.g. Banarasi, Pink, QS204820", key="cat_search").strip().lower()
    with col_filter:
        stock_filter = st.selectbox("Filter Stock", ["All Items", "In Stock Only", "Out of Stock"], key="cat_stock_filter")
    with col_page_size:
        page_size = st.selectbox("Page Size", [12, 24, 48, 83], index=0, key="cat_page_size")

    # Filter items
    filtered = []
    for it in catalog_items:
        if search_query:
            match_name = search_query in it["name"].lower()
            match_sku = search_query in it["sku"].lower()
            if not (match_name or match_sku):
                continue

        if stock_filter == "In Stock Only":
            if it["stock"] is None or it["stock"] <= 0:
                continue
        elif stock_filter == "Out of Stock":
            if it["stock"] is not None and it["stock"] > 0:
                continue

        filtered.append(it)

    st.write(f"Showing **{len(filtered)}** of **{len(catalog_items)}** sarees")

    if not filtered:
        st.info("No sarees match your search criteria.")
        return

    # Pagination
    total_pages = max(1, math.ceil(len(filtered) / page_size))
    page_num = 1
    if total_pages > 1:
        page_num = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1, key="cat_page_num")

    start_idx = (page_num - 1) * page_size
    end_idx = min(start_idx + page_size, len(filtered))
    current_batch = filtered[start_idx:end_idx]

    # Grid display
    cols = st.columns(3)
    for idx, it in enumerate(current_batch):
        col = cols[idx % 3]
        with col:
            # Saree image
            if it["image_url"]:
                st.image(it["image_url"], use_container_width=True)

            st.markdown(f"**{it['name']}**")
            st.caption(f"SKU: `{it['sku']}`")

            # Price & Stock
            price_parts = []
            if it["discounted_price"] is not None:
                price_parts.append(f"<strong style='font-size:15px; color:#0f172a;'>₹{it['discounted_price']:,.0f}</strong>")
            if it["retail_price"] is not None and (it["discounted_price"] is None or it["retail_price"] != it["discounted_price"]):
                price_parts.append(f"<span style='text-decoration:line-through; color:#64748b; font-size:13px;'>₹{it['retail_price']:,.0f}</span>")

            stk = it["stock"]
            stock_str = f"{stk} in stock" if (stk is not None and stk >= 0) else ("Out of stock" if stk == 0 else "Unknown")
            stock_badge = f"<span style='font-size:12px; color:{'#16a34a' if stk and stk > 0 else '#64748b'};'>• {stock_str}</span>"

            if price_parts:
                st.markdown(f"<div>{' '.join(price_parts)} {stock_badge}</div>", unsafe_allow_html=True)

            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if it["website_link"] and ImageValidator.is_valid_url(it["website_link"]):
                    st.markdown(f"<a href='{it['website_link']}' target='_blank' style='display:block; text-align:center; padding:4px 8px; background:#0284c7; color:#ffffff; text-decoration:none; border-radius:4px; font-size:12px; font-weight:600;'>🔗 View Page</a>", unsafe_allow_html=True)
            with c_btn2:
                if it["image_url"] and st.button("🔍 Find Similar", key=f"cat_find_{it['sku']}_{it['id']}", use_container_width=True):
                    st.session_state.current_query_image = it["image_url"]
                    st.session_state.current_query_source = f"{it['name']} ({it['sku']})"
                    trigger_search(it["image_url"], top_k, candidate_k)
                    st.rerun()

            st.markdown("---")


def main():
    st.title("🥻 TailorTalk — Visual Saree Similarity Search Agent")
    st.markdown(
        "A fine-grained computer vision retrieval system that analyzes **dominant color distributions, "
        "gradient-based texture statistics, and spatial composition** using OpenCLIP embeddings, FAISS vector indexing, and multi-signal reranking."
    )

    top_k, candidate_k = render_sidebar()

    # Primary Application Tabs
    tab_search, tab_catalog = st.tabs(["🔍 Visual Similarity Search & Stylist", "📖 Catalogue Browser (83 Sarees)"])

    with tab_search:
        # Input Area Tabs: File Upload vs URL
        st.markdown("#### 📥 Query Image Input")
        tab_upload, tab_url = st.tabs(["📁 Upload Image File", "🔗 Image Web URL"])

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
                    try:
                        agent = get_cached_agent()
                        reply, results_dict = agent.process_message(
                            user_message=user_prompt,
                            image_input=st.session_state.current_query_image,
                            top_k=top_k,
                        )
                    except Exception as e:
                        reply = f"I encountered an issue processing your request: {e}"
                        results_dict = None

                    st.markdown(reply)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": reply,
                        "results": results_dict,
                    })

    with tab_catalog:
        render_catalog_browser(top_k, candidate_k)


if __name__ == "__main__":
    main()
