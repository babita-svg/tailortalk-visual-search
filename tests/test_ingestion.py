"""Unit tests for ingestion pipeline, metadata extraction, and attribute heuristics."""

from pathlib import Path
import numpy as np
from PIL import Image
import pytest

from app.ingestion.metadata import (
    estimate_saree_attributes_from_filename,
    extract_dominant_color_palette,
    extract_metadata_for_image,
    rgb_to_hex,
)
from app.ingestion.pipeline import IngestionPipeline


def test_rgb_to_hex():
    """Verify RGB integer conversion to standard hex code."""
    assert rgb_to_hex(255, 0, 0) == "#ff0000"
    assert rgb_to_hex(0, 255, 0) == "#00ff00"
    assert rgb_to_hex(0, 0, 255) == "#0000ff"
    assert rgb_to_hex(0, 0, 0) == "#000000"
    assert rgb_to_hex(255, 255, 255) == "#ffffff"


def test_estimate_saree_attributes_from_filename():
    """Test truthful heuristic extraction of saree attributes without fabrication."""
    # Banarasi Crimson Red Zari Brocade
    attrs = estimate_saree_attributes_from_filename("banarasi_crimson_red_gold_zari_brocade.jpg")
    assert attrs["fabric_type"] == "Banarasi"
    assert attrs["primary_color"] == "Crimson Red"
    assert attrs["weave_style"] == "Zari Brocade"
    assert attrs["border_type"] == "Zari Border"

    # Kanjeevaram Royal Navy Blue Gold Zari Border
    attrs2 = estimate_saree_attributes_from_filename("kanjeevaram_royal_navy_blue_gold_zari_border.jpg")
    assert attrs2["fabric_type"] == "Kanjeevaram"
    assert attrs2["primary_color"] == "Royal Navy Blue"
    assert attrs2["border_type"] == "Zari Border"

    # Unknown unstructured filename
    attrs3 = estimate_saree_attributes_from_filename("sample_photo_999.jpg")
    assert attrs3["fabric_type"] is None
    assert attrs3["primary_color"] is None


def test_extract_dominant_color_palette(tmp_path):
    """Test extracting dominant color palette from image."""
    img = Image.new("RGB", (64, 64), color=(200, 50, 50))
    palette = extract_dominant_color_palette(img, num_colors=3)
    assert len(palette) >= 1
    assert palette[0].startswith("#")


def test_extract_metadata_for_image(tmp_path):
    """Test full SareeMetadata generation for an image file."""
    dataset_dir = tmp_path / "dataset"
    dataset_dir.mkdir()
    img_path = dataset_dir / "banarasi_crimson_red_gold_zari_brocade.jpg"
    img = Image.new("RGB", (100, 100), color=(180, 20, 20))
    img.save(img_path)

    metadata = extract_metadata_for_image(img_path, dataset_dir)
    assert metadata.image_id == "banarasi_crimson_red_gold_zari_brocade"
    assert metadata.fabric_type == "Banarasi"
    assert metadata.primary_color == "Crimson Red"
    assert len(metadata.color_palette) > 0
    assert metadata.dimensions == (100, 100)
