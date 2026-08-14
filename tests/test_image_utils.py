"""Unit tests for image loading, preprocessing, and validation utilities."""

import io
from pathlib import Path
import pytest
from PIL import Image
import numpy as np

from app.image_utils.loader import ImageLoader
from app.image_utils.validation import ImageValidator
from app.exceptions import InvalidImageError, CorruptedImageError


@pytest.fixture
def valid_rgb_image():
    """Create a temporary valid RGB test image."""
    img = Image.new("RGB", (300, 400), color=(180, 50, 60))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf.getvalue()


@pytest.fixture
def valid_rgba_image():
    """Create a temporary valid RGBA image."""
    img = Image.new("RGBA", (200, 200), color=(50, 150, 200, 255))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()


def test_validate_valid_image(valid_rgb_image):
    """Test that a valid JPEG image passes validation."""
    ImageValidator.validate_bytes(valid_rgb_image)


def test_validate_corrupted_image():
    """Test that invalid/random bytes raise InvalidImageError or CorruptedImageError."""
    junk_data = b"NOT_AN_IMAGE_FILE_HEADER_1234567890"
    with pytest.raises((InvalidImageError, CorruptedImageError)):
        ImageValidator.validate_bytes(junk_data)


def test_validate_oversized_image():
    """Test that payload exceeding max bytes is rejected."""
    huge_data = b"0" * (30 * 1024 * 1024)  # 30MB
    with pytest.raises(InvalidImageError):
        ImageValidator.validate_bytes(huge_data, max_size_mb=10)


def test_load_pil_image(valid_rgba_image):
    """Test that RGBA images are properly converted to RGB."""
    img = ImageLoader.load(valid_rgba_image)
    assert isinstance(img, Image.Image)
    assert img.mode == "RGB"
    assert img.size == (200, 200)


def test_url_validation():
    """Test URL scheme and format validation."""
    assert ImageValidator.is_valid_url("https://example.com/saree.jpg") is True
    assert ImageValidator.is_valid_url("http://images.unsplash.com/photo-123.png") is True
    assert ImageValidator.is_valid_url("file:///etc/passwd") is False
    assert ImageValidator.is_valid_url("ftp://server/img.jpg") is False
    assert ImageValidator.is_valid_url("not-a-url") is False
