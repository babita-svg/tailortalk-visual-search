"""Unit tests for fine-grained multi-signal visual reranking and score calibration."""

import numpy as np
import pytest
from PIL import Image

from app.retrieval.reranker import FineGrainedSareeReranker, VisualFeatures


@pytest.fixture
def sample_query_image():
    """Create a sample query image (crimson red with gold stripes)."""
    arr = np.zeros((300, 300, 3), dtype=np.uint8)
    arr[:, :] = [180, 20, 40]  # Crimson
    arr[100:150, :] = [230, 190, 40]  # Gold band
    return Image.fromarray(arr)


@pytest.fixture
def sample_candidate_image():
    """Create a sample candidate image (similar crimson red)."""
    arr = np.zeros((300, 300, 3), dtype=np.uint8)
    arr[:, :] = [175, 25, 45]  # Very close crimson
    arr[90:140, :] = [225, 185, 35]  # Gold band
    return Image.fromarray(arr)


@pytest.fixture
def dissimilar_candidate_image():
    """Create a completely dissimilar image (bright blue/green)."""
    arr = np.zeros((300, 300, 3), dtype=np.uint8)
    arr[:, :] = [20, 120, 220]  # Blue
    return Image.fromarray(arr)


def test_reranker_weights_normalization():
    """Test that custom reranking weights sum properly to 1.0."""
    reranker = FineGrainedSareeReranker(
        weight_embedding=0.40,
        weight_color=0.30,
        weight_texture=0.15,
        weight_composition=0.15,
    )
    assert pytest.approx(reranker.w_emb + reranker.w_col + reranker.w_tex + reranker.w_comp) == 1.0


def test_extract_visual_features(sample_query_image):
    """Test extracting visual features returns valid VisualFeatures dataclass."""
    reranker = FineGrainedSareeReranker()
    features = reranker.extract_visual_features(sample_query_image)
    
    assert isinstance(features, VisualFeatures)
    assert features.color_hist.shape == (128,)
    assert features.dominant_colors.shape == (3, 3)
    assert features.texture_profile.shape == (5,)
    assert features.spatial_layout.shape == (27,)


def test_reranking_score_bounds_and_similarity(sample_query_image, sample_candidate_image, dissimilar_candidate_image):
    """Test that reranking produces scores in [0, 1] and calculates higher color similarity for matching hues."""
    reranker = FineGrainedSareeReranker()
    
    feat_query = reranker.extract_visual_features(sample_query_image)
    feat_similar = reranker.extract_visual_features(sample_candidate_image)
    feat_dissimilar = reranker.extract_visual_features(dissimilar_candidate_image)
    
    col_sim_close = reranker.compute_color_similarity(feat_query, feat_similar)
    col_sim_diff = reranker.compute_color_similarity(feat_query, feat_dissimilar)
    
    assert 0.0 <= col_sim_close <= 1.0
    assert 0.0 <= col_sim_diff <= 1.0
    assert col_sim_close > col_sim_diff


def test_visual_features_serialization_roundtrip(sample_query_image):
    """Test VisualFeatures to_dict and from_dict produce identical arrays."""
    reranker = FineGrainedSareeReranker()
    features = reranker.extract_visual_features(sample_query_image)
    
    serialized = features.to_dict()
    assert isinstance(serialized, dict)
    assert "color_hist" in serialized
    assert "dominant_colors" in serialized
    assert "texture_profile" in serialized
    assert "spatial_layout" in serialized

    restored = VisualFeatures.from_dict(serialized)
    np.testing.assert_allclose(features.color_hist, restored.color_hist, rtol=1e-5)
    np.testing.assert_allclose(features.dominant_colors, restored.dominant_colors, rtol=1e-5)
    np.testing.assert_allclose(features.texture_profile, restored.texture_profile, rtol=1e-5)
    np.testing.assert_allclose(features.spatial_layout, restored.spatial_layout, rtol=1e-5)


def test_rerank_candidates_with_cached_features(sample_query_image, sample_candidate_image):
    """Test reranking executes efficiently when visual_features dictionary is cached in candidate metadata."""
    reranker = FineGrainedSareeReranker()
    feat_cand = reranker.extract_visual_features(sample_candidate_image)

    candidates = [
        ("cand_01", 0.90, {
            "image_id": "cand_01",
            "filename": "cand_01.jpg",
            "relative_path": "cand_01.jpg",
            "file_size_bytes": 1000,
            "dimensions": [300, 300],
            "primary_color": "Red",
            "fabric_type": "Silk",
            "weave_style": "Zari",
            "border_type": "Gold",
            "pallu_style": "Brocade",
            "visual_features": feat_cand.to_dict(),
        })
    ]

    results = reranker.rerank_candidates(sample_query_image, candidates, top_k=1)
    assert len(results) == 1
    assert results[0].image_id == "cand_01"
    assert results[0].breakdown.color_similarity > 0.5
    assert results[0].breakdown.texture_similarity > 0.5
    assert results[0].breakdown.final_score > 0.5


def test_rerank_candidates_honest_fallback_when_features_unavailable(sample_query_image):
    """Test truthful fallback when candidate visual features are missing and cannot be loaded."""
    reranker = FineGrainedSareeReranker()
    
    candidates = [
        ("missing_img_01", 0.85, {
            "image_id": "missing_img_01",
            "filename": "missing_img_01.jpg",
            "relative_path": "non_existent_path.jpg",
            "file_size_bytes": 1000,
            "dimensions": [300, 300],
            "primary_color": "Unknown",
            "fabric_type": "Unknown",
            "weave_style": "Unknown",
            "border_type": "Unknown",
            "pallu_style": "Unknown",
        })
    ]

    results = reranker.rerank_candidates(sample_query_image, candidates, top_k=1)
    assert len(results) == 1
    # Check that color, texture, and composition are 0.0, NOT fabricated from 0.85
    assert results[0].breakdown.color_similarity == 0.0
    assert results[0].breakdown.texture_similarity == 0.0
    assert results[0].breakdown.composition_similarity == 0.0
    assert results[0].breakdown.embedding_similarity == 0.85
    assert "fine-grained visual features were unavailable" in results[0].visual_explanation
