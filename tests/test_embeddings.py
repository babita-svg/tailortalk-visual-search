"""Unit tests for pretrained image embeddings generation and normalization."""

import numpy as np
import pytest
from PIL import Image

from app.embeddings.image_encoder import ImageEncoder
from app.config import config


def test_encoder_singleton_and_dimension():
    """Test loading the image encoder and verifying output dimensions."""
    encoder = ImageEncoder(allow_test_fallback=True)
    assert encoder.dimension == config.model.embedding_dim


def test_encode_image_shape_and_normalization():
    """Test encoding a synthetic PIL image produces unit-norm (L2 norm ~1.0) vectors."""
    encoder = ImageEncoder(allow_test_fallback=True)
    img = Image.new("RGB", (224, 224), color=(100, 150, 200))
    
    vec = encoder.encode_image(img)
    
    assert isinstance(vec, np.ndarray)
    assert vec.shape == (512,)
    assert vec.dtype == np.float32
    
    l2_norm = np.linalg.norm(vec)
    assert pytest.approx(l2_norm, abs=1e-3) == 1.0


def test_deterministic_embeddings():
    """Test that identical images produce identical embedding vectors."""
    encoder = ImageEncoder(allow_test_fallback=True)
    img1 = Image.new("RGB", (224, 224), color=(200, 40, 80))
    img2 = Image.new("RGB", (224, 224), color=(200, 40, 80))
    
    vec1 = encoder.encode_image(img1)
    vec2 = encoder.encode_image(img2)
    
    np.testing.assert_allclose(vec1, vec2, atol=1e-5)


def test_batch_encoding():
    """Test batch encoding multiple images."""
    encoder = ImageEncoder(allow_test_fallback=True)
    images = [
        Image.new("RGB", (224, 224), color=(i * 20, 100, 150))
        for i in range(3)
    ]
    batch_vecs = encoder.encode_batch(images)
    
    assert batch_vecs.shape == (3, 512)
    norms = np.linalg.norm(batch_vecs, axis=1)
    np.testing.assert_allclose(norms, np.ones(3), atol=1e-3)
