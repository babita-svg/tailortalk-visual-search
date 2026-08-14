"""Metadata extraction for dataset saree images."""

from pathlib import Path
from typing import Dict, List, Tuple
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


def estimate_saree_attributes_from_filename(filename: str) -> Dict[str, str]:
    """Derive semantic attributes from catalog filename patterns."""
    clean = filename.lower().replace("-", " ").replace("_", " ")

    # Fabric heuristics
    fabrics = ["banarasi", "kanjeevaram", "chanderi", "bandhani", "patola", "tussar", "georgette", "cotton", "kasavu", "silk", "organza", "crepe", "linen"]
    fabric_type = "Silk"
    for f in fabrics:
        if f in clean:
            fabric_type = f.title()
            break

    # Weave & Pattern heuristics
    weaves = ["zari brocade", "temple border", "tie-dye", "ikat", "floral print", "digital print", "embroidered", "plain woven", "geometric", "block print", "buta"]
    weave_style = "Handloom Weave"
    for w in weaves:
        if w in clean:
            weave_style = w.title()
            break

    # Color heuristics
    colors = ["crimson red", "red", "ruby", "emerald green", "green", "royal blue", "navy", "blue", "mustard yellow", "yellow", "gold", "pink", "magenta", "purple", "violet", "orange", "maroon", "black", "ivory", "white", "teal", "turquoise", "peach", "lavender"]
    primary_color = "Multicolor"
    for c in colors:
        if c in clean:
            primary_color = c.title()
            break

    # Border heuristics
    border_type = "Zari Border" if ("zari" in clean or "gold" in clean or "border" in clean) else "Contrasting Border"
    pallu_style = "Heavy Brocade Pallu" if ("banarasi" in clean or "kanjeevaram" in clean) else "Embellished Pallu"

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

    return SareeMetadata(
        image_id=image_id,
        filename=image_path.name,
        relative_path=rel_path,
        file_size_bytes=file_size,
        dimensions=dims,
        color_palette=palette,
        primary_color=attrs["primary_color"],
        fabric_type=attrs["fabric_type"],
        weave_style=attrs["weave_style"],
        border_type=attrs["border_type"],
        pallu_style=attrs["pallu_style"],
        description=f"{attrs['primary_color']} {attrs['fabric_type']} saree with {attrs['weave_style']} and {attrs['border_type']}.",
    )
