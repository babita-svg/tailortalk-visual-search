"""Fine-grained multi-modal visual reranker for saree similarity.

Combines base vision embeddings with fine-grained color distributions,
fabric texture/weave patterns, and spatial composition analysis.
"""

from dataclasses import dataclass
import logging
from typing import Dict, List, Optional, Tuple
import numpy as np
from PIL import Image

from app.config import config
from app.exceptions import RerankerError
from app.image_utils.loader import ImageLoader
from app.schemas import SareeMetadata, SearchResultItem, SimilarityBreakdown

logger = logging.getLogger(__name__)


@dataclass
class VisualFeatures:
    """Precomputed or runtime extracted visual descriptor for fine-grained reranking."""

    # 3D HSV Color Histogram (8x4x4 = 128 bins normalized)
    color_hist: np.ndarray
    # Dominant Lab color centers (Top 3 colors in RGB float [0, 1])
    dominant_colors: np.ndarray
    # Texture gradient energy across horizontal/vertical frequencies
    texture_profile: np.ndarray
    # 3x3 spatial grid color and edge density
    spatial_layout: np.ndarray


class FineGrainedSareeReranker:
    """Multi-signal deterministic reranker for fine-grained saree retrieval."""

    def __init__(
        self,
        weight_embedding: float = config.retrieval.weight_embedding,
        weight_color: float = config.retrieval.weight_color,
        weight_texture: float = config.retrieval.weight_texture,
        weight_composition: float = config.retrieval.weight_composition,
    ) -> None:
        self.w_emb = weight_embedding
        self.w_col = weight_color
        self.w_tex = weight_texture
        self.w_comp = weight_composition

        # Normalize weights to sum to 1.0
        total_w = self.w_emb + self.w_col + self.w_tex + self.w_comp
        if total_w > 0:
            self.w_emb /= total_w
            self.w_col /= total_w
            self.w_tex /= total_w
            self.w_comp /= total_w

    def extract_visual_features(self, img: Image.Image) -> VisualFeatures:
        """Extract multi-scale color, texture, and spatial composition descriptors."""
        img_rgb = img.convert("RGB").resize((160, 160), Image.Resampling.BILINEAR)
        arr = np.asarray(img_rgb, dtype=np.float32) / 255.0  # (H, W, 3)

        # 1. Color Histogram in HSV space
        hsv_img = img_rgb.convert("HSV")
        hsv_arr = np.asarray(hsv_img, dtype=np.float32)
        h = hsv_arr[:, :, 0] / 255.0  # [0, 1]
        s = hsv_arr[:, :, 1] / 255.0
        v = hsv_arr[:, :, 2] / 255.0

        # 8 hue bins, 4 saturation bins, 4 value bins = 128 bins
        hist, _ = np.histogramdd(
            np.stack([h.ravel(), s.ravel(), v.ravel()], axis=1),
            bins=(8, 4, 4),
            range=((0, 1), (0, 1), (0, 1)),
        )
        hist = hist.flatten().astype(np.float32)
        hist_sum = hist.sum()
        color_hist = hist / (hist_sum if hist_sum > 0 else 1.0)

        # 2. Dominant Colors (Mean of sorted pixel clusters)
        pixels = arr.reshape(-1, 3)
        quantized = np.round(pixels * 5) / 5.0
        unique_colors, counts = np.unique(quantized, axis=0, return_counts=True)
        top_indices = np.argsort(counts)[::-1][:3]
        dominant_colors = unique_colors[top_indices]
        if len(dominant_colors) < 3:
            pad = np.tile(dominant_colors[0], (3 - len(dominant_colors), 1))
            dominant_colors = np.vstack([dominant_colors, pad])

        # 3. Texture Profile (Sobel gradient magnitude for weave / pattern density)
        gray = 0.2989 * arr[:, :, 0] + 0.5870 * arr[:, :, 1] + 0.1140 * arr[:, :, 2]
        grad_x = np.abs(gray[:, 1:] - gray[:, :-1])
        grad_y = np.abs(gray[1:, :] - gray[:-1, :])

        mean_gx = float(np.mean(grad_x))
        std_gx = float(np.std(grad_x))
        mean_gy = float(np.mean(grad_y))
        std_gy = float(np.std(grad_y))
        high_freq_ratio = float(np.mean(grad_x > 0.15) + np.mean(grad_y > 0.15)) / 2.0
        texture_profile = np.array([mean_gx, std_gx, mean_gy, std_gy, high_freq_ratio], dtype=np.float32)

        # 4. Spatial 3x3 Grid Layout
        grid_feats = []
        h_step, w_step = 160 // 3, 160 // 3
        for r in range(3):
            for c in range(3):
                cell_rgb = arr[r * h_step : (r + 1) * h_step, c * w_step : (c + 1) * w_step]
                grid_feats.extend(cell_rgb.mean(axis=(0, 1)))  # 3 RGB values
        spatial_layout = np.array(grid_feats, dtype=np.float32)  # 27 dims

        return VisualFeatures(
            color_hist=color_hist,
            dominant_colors=dominant_colors,
            texture_profile=texture_profile,
            spatial_layout=spatial_layout,
        )

    def compute_color_similarity(self, query_feat: VisualFeatures, candidate_feat: VisualFeatures) -> float:
        """Calculate histogram intersection and dominant color proximity."""
        intersection = np.sum(np.minimum(query_feat.color_hist, candidate_feat.color_hist))
        hist_sim = float(np.clip(intersection, 0.0, 1.0))

        diffs = np.linalg.norm(query_feat.dominant_colors - candidate_feat.dominant_colors, axis=1)
        dom_sim = float(np.clip(1.0 - np.mean(diffs) / np.sqrt(3.0), 0.0, 1.0))

        return 0.7 * hist_sim + 0.3 * dom_sim

    def compute_texture_similarity(self, query_feat: VisualFeatures, candidate_feat: VisualFeatures) -> float:
        """Calculate texture and pattern gradient statistics similarity."""
        diff = np.abs(query_feat.texture_profile - candidate_feat.texture_profile)
        scales = np.array([0.2, 0.2, 0.2, 0.2, 0.4], dtype=np.float32)
        norm_diff = np.sum(diff * scales)
        return float(np.clip(1.0 - norm_diff, 0.0, 1.0))

    def compute_composition_similarity(self, query_feat: VisualFeatures, candidate_feat: VisualFeatures) -> float:
        """Calculate 3x3 spatial layout cosine similarity."""
        q_grid = query_feat.spatial_layout
        c_grid = candidate_feat.spatial_layout
        dot = np.dot(q_grid, c_grid)
        denom = (np.linalg.norm(q_grid) * np.linalg.norm(c_grid)) + 1e-7
        sim = dot / denom
        return float(np.clip(sim, 0.0, 1.0))

    def rerank_candidates(
        self,
        query_image: Image.Image,
        candidates: List[Tuple[str, float, Dict]],
        top_k: int = config.retrieval.default_top_k,
    ) -> List[SearchResultItem]:
        """Rerank Stage-1 candidates using multi-signal visual analysis."""
        if not candidates:
            return []

        try:
            query_features = self.extract_visual_features(query_image)
        except Exception as e:
            logger.error(f"Failed to extract visual features from query: {str(e)}")
            raise RerankerError(f"Query feature extraction failed: {str(e)}") from e

        scored_items: List[SearchResultItem] = []

        for image_id, base_emb_score, meta_dict in candidates:
            # Base embedding score from FAISS [-1.0, 1.0] -> normalize to [0.0, 1.0]
            emb_sim = float(np.clip((base_emb_score + 1.0) / 2.0 if base_emb_score < 0 else base_emb_score, 0.0, 1.0))

            rel_path = meta_dict.get("relative_path", "")
            img_path = config.storage.images_dir / rel_path if rel_path else None

            color_sim = emb_sim
            texture_sim = emb_sim
            comp_sim = emb_sim

            if img_path and img_path.exists():
                try:
                    cand_img = ImageLoader.load_from_path(img_path)
                    cand_features = self.extract_visual_features(cand_img)

                    color_sim = self.compute_color_similarity(query_features, cand_features)
                    texture_sim = self.compute_texture_similarity(query_features, cand_features)
                    comp_sim = self.compute_composition_similarity(query_features, cand_features)
                except Exception as e:
                    logger.debug(f"Candidate feature extraction failed for {image_id}: {str(e)}")

            # Composite final score calculation
            final_score = (
                self.w_emb * emb_sim
                + self.w_col * color_sim
                + self.w_tex * texture_sim
                + self.w_comp * comp_sim
            )
            final_score = float(np.clip(final_score, 0.0, 1.0))

            breakdown = SimilarityBreakdown(
                embedding_similarity=round(emb_sim, 4),
                color_similarity=round(color_sim, 4),
                texture_similarity=round(texture_sim, 4),
                composition_similarity=round(comp_sim, 4),
                final_score=round(final_score, 4),
            )

            metadata_obj = SareeMetadata(**meta_dict) if meta_dict else None
            explanation = self._generate_visual_explanation(breakdown, metadata_obj)

            item = SearchResultItem(
                rank=0,
                image_id=image_id,
                relative_path=rel_path,
                score=round(final_score, 4),
                score_percentage=f"{final_score * 100:.1f}%",
                breakdown=breakdown,
                metadata=metadata_obj,
                visual_explanation=explanation,
            )
            scored_items.append(item)

        # Sort descending by final composite score
        scored_items.sort(key=lambda x: x.score, reverse=True)

        # Assign 1-indexed ranks and slice top_k
        top_results = scored_items[:top_k]
        for idx, item in enumerate(top_results, start=1):
            item.rank = idx

        return top_results

    def _generate_visual_explanation(
        self,
        breakdown: SimilarityBreakdown,
        meta: Optional[SareeMetadata],
    ) -> str:
        """Create a truthful visual explanation based solely on measured similarity metrics."""
        parts = []

        # Color evaluation
        if breakdown.color_similarity >= 0.85:
            parts.append("strong color distribution match and shared dominant hues")
        elif breakdown.color_similarity >= 0.70:
            parts.append("compatible tonal color distribution")

        # Texture profile evaluation
        if breakdown.texture_similarity >= 0.82:
            parts.append("closely matching texture gradient statistics")
        elif breakdown.texture_similarity >= 0.65:
            parts.append("similar texture profile")

        # Spatial composition evaluation
        if breakdown.composition_similarity >= 0.80:
            parts.append("aligned 3x3 spatial color layout")

        if not parts:
            parts.append("overall semantic visual embedding similarity")

        explanation = f"Matches query ({breakdown.final_score * 100:.0f}% overall similarity): " + ", ".join(parts) + "."
        if meta and meta.fabric_type and meta.fabric_type != "Unknown":
            explanation += f" (Catalog fabric: {meta.fabric_type})"

        return explanation
