"""Metadata extraction for dataset saree images."""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
from PIL import Image

from app.schemas import SareeMetadata


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB integers to hex string."""
    return f"#{r:02x}{g:02x}{b:02x}"


def extract_dominant_color_palette(img: Image.Image, num_colors: int = 5) -> List[str]:
    """Extract top dominant hex colors from image pixels."""
    small = img.convert("RGB").resize((64, 64), Image.Resampling.NEAREST)
    arr = np.asarray(small, dtype=np.int32).reshape(-1, 3)
    # Quantize to 32-step buckets
    quantized = (arr // 32) * 32
    colors, counts = np.unique(quantized, axis=0, return_counts=True)
    sorted_idx = np.argsort(counts)[::-1]
    palette = []
    for idx in sorted_idx[:num_colors]:
        c = colors[idx]
        palette.append(rgb_to_hex(int(c[0]), int(c[1]), int(c[2])))
    return palette


def estimate_saree_attributes_from_filename(filename: str) -> Dict[str, Optional[str]]:
    """Derive semantic attributes from catalog filename patterns without fabricating unsupported defaults."""
    clean = filename.lower().replace("-", " ").replace("_", " ")

    # Fabric heuristics
    fabrics = [
        "banarasi", "kanjeevaram", "chanderi", "bandhani", "patola", "tussar",
        "georgette", "cotton", "kasavu", "silk", "organza", "crepe", "linen", "paithani", "sambalpuri", "kalamkari"
    ]
    fabric_type: Optional[str] = None
    for f in fabrics:
        if f in clean:
            fabric_type = f.title()
            break

    # Weave & Pattern heuristics
    weaves = [
        "zari brocade", "temple border", "tie-dye", "leheriya", "ikat", "floral print",
        "digital print", "embroidered", "plain woven", "geometric", "block print",
        "buta", "booti", "kantha", "tribal weave", "tree of life", "chevron", "elephant", "parrot", "peacock"
    ]
    weave_style: Optional[str] = None
    for w in weaves:
        if w in clean:
            weave_style = w.title()
            break

    # Color heuristics
    colors = [
        "crimson red", "ruby red", "red", "emerald green", "mint green", "green",
        "royal navy blue", "navy blue", "powder blue", "indigo blue", "peacock blue", "blue",
        "mustard yellow", "mustard gold", "yellow", "gold", "rose pink", "pink", "magenta",
        "purple", "violet", "orange", "rust orange", "terracotta", "maroon", "deep maroon",
        "black", "offwhite", "ivory", "white", "beige", "golden beige", "teal", "turquoise", "peach", "lavender"
    ]
    primary_color: Optional[str] = None
    for c in colors:
        if c in clean:
            primary_color = c.title()
            break

    # Border heuristics
    border_type: Optional[str] = None
    if "zari border" in clean or ("gold" in clean and "border" in clean):
        border_type = "Zari Border"
    elif "silver zari" in clean:
        border_type = "Silver Zari Border"
    elif "border" in clean:
        border_type = "Contrasting Border"

    # Pallu heuristics
    pallu_style: Optional[str] = None
    if "pallu" in clean:
        if "mor" in clean or "peacock" in clean:
            pallu_style = "Peacock Motif Pallu"
        elif "brocade" in clean:
            pallu_style = "Brocade Pallu"
        else:
            pallu_style = "Embellished Pallu"

    return {
        "fabric_type": fabric_type,
        "weave_style": weave_style,
        "primary_color": primary_color,
        "border_type": border_type,
        "pallu_style": pallu_style,
    }


def extract_metadata_for_image(image_path: Path, dataset_root: Path) -> SareeMetadata:
    """Generate comprehensive SareeMetadata object for an image file."""
    rel_path = str(image_path.relative_to(dataset_root))
    file_size = image_path.stat().st_size
    image_id = image_path.stem

    with Image.open(image_path) as img:
        dims = img.size
        palette = extract_dominant_color_palette(img)

    attrs = estimate_saree_attributes_from_filename(image_path.name)

    # Build truthful summary description from available attributes
    desc_parts = []
    if attrs["primary_color"]:
        desc_parts.append(attrs["primary_color"])
    if attrs["fabric_type"]:
        desc_parts.append(attrs["fabric_type"])
    desc_parts.append("saree")
    if attrs["weave_style"]:
        desc_parts.append(f"with {attrs['weave_style']}")
    if attrs["border_type"]:
        desc_parts.append(f"and {attrs['border_type']}")

    desc_str = " ".join(desc_parts) + "."

    return SareeMetadata(
        image_id=image_id,
        filename=image_path.name,
        relative_path=rel_path,
        file_size_bytes=file_size,
        dimensions=dims,
        color_palette=palette,
        primary_color=attrs["primary_color"] or "Unknown",
        fabric_type=attrs["fabric_type"] or "Unknown",
        weave_style=attrs["weave_style"] or "Unknown",
        border_type=attrs["border_type"] or "Unknown",
        pallu_style=attrs["pallu_style"] or "Unknown",
        description=desc_str,
    )
