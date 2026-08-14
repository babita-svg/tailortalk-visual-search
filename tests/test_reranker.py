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
