"""Script to generate a rich, authentic catalog of saree images with diverse fabrics, weaves, borders, and pallus."""

import math
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

OUTPUT_DIR = Path("data/images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SAREE_CATALOG = [
    {
        "filename": "banarasi_crimson_red_gold_zari_brocade.jpg",
        "primary_color": (180, 20, 35),
        "secondary_color": (235, 190, 60),
        "pattern": "floral_brocade",
        "border_width": 38,
        "pallu_width": 75,
        "texture": "silk_sheen",
    },
    {
        "filename": "banarasi_royal_navy_blue_silver_zari.jpg",
        "primary_color": (15, 30, 95),
        "secondary_color": (210, 220, 235),
        "pattern": "kalga_buta",
        "border_width": 35,
        "pallu_width": 70,
        "texture": "silk_sheen",
    },
    {
        "filename": "kanjeevaram_emerald_green_ruby_red_border.jpg",
        "primary_color": (10, 105, 55),
        "secondary_color": (175, 15, 45),
        "pattern": "temple_motifs",
        "border_width": 48,
        "pallu_width": 80,
        "texture": "heavy_silk",
    },
    {
        "filename": "kanjeevaram_mustard_gold_peacock_blue_border.jpg",
        "primary_color": (215, 165, 30),
        "secondary_color": (10, 75, 140),
        "pattern": "peacock_checks",
        "border_width": 45,
        "pallu_width": 80,
        "texture": "heavy_silk",
    },
    {
        "filename": "chanderi_pastel_peach_silver_zari_booti.jpg",
        "primary_color": (250, 190, 165),
        "secondary_color": (220, 225, 230),
        "pattern": "fine_booti",
        "border_width": 24,
        "pallu_width": 50,
        "texture": "sheer_cotton_silk",
    },
    {
        "filename": "chanderi_mint_green_geometric_zari.jpg",
        "primary_color": (160, 220, 190),
        "secondary_color": (225, 195, 75),
        "pattern": "geometric_diamond",
        "border_width": 26,
        "pallu_width": 52,
        "texture": "sheer_cotton_silk",
    },
    {
        "filename": "bandhani_traditional_ruby_red_yellow_dots.jpg",
        "primary_color": (200, 25, 40),
        "secondary_color": (245, 220, 30),
        "pattern": "tie_dye_dots",
        "border_width": 30,
        "pallu_width": 65,
        "texture": "crinkled_georgette",
    },
    {
        "filename": "bandhani_deep_maroon_white_leheriya.jpg",
        "primary_color": (120, 15, 30),
        "secondary_color": (250, 250, 250),
        "pattern": "diagonal_leheriya",
        "border_width": 28,
        "pallu_width": 60,
        "texture": "crinkled_georgette",
    },
    {
        "filename": "patola_double_ikat_maroon_black_elephant.jpg",
        "primary_color": (130, 20, 35),
        "secondary_color": (25, 25, 25),
        "pattern": "double_ikat_grid",
        "border_width": 40,
        "pallu_width": 75,
        "texture": "patola_silk",
    },
    {
        "filename": "patola_emerald_and_mustard_geometric_parrot.jpg",
        "primary_color": (15, 110, 65),
        "secondary_color": (220, 160, 25),
        "pattern": "double_ikat_grid",
        "border_width": 38,
        "pallu_width": 70,
        "texture": "patola_silk",
    },
    {
        "filename": "kalamkari_natural_beige_tree_of_life_cotton.jpg",
        "primary_color": (225, 210, 180),
        "secondary_color": (140, 45, 35),
        "pattern": "hand_painted_botanical",
        "border_width": 32,
        "pallu_width": 90,
        "texture": "matte_cotton",
    },
    {
        "filename": "kalamkari_indigo_blue_mythological_motifs.jpg",
        "primary_color": (30, 55, 110),
        "secondary_color": (215, 195, 155),
        "pattern": "hand_painted_botanical",
        "border_width": 34,
        "pallu_width": 85,
        "texture": "matte_cotton",
    },
    {
        "filename": "tussar_silk_raw_golden_beige_kantha_embroidery.jpg",
        "primary_color": (210, 185, 140),
        "secondary_color": (160, 30, 45),
        "pattern": "kantha_running_stitch",
        "border_width": 30,
        "pallu_width": 65,
        "texture": "slub_tussar",
    },
    {
        "filename": "tussar_silk_rust_orange_tribal_weave.jpg",
        "primary_color": (195, 80, 35),
        "secondary_color": (50, 40, 35),
        "pattern": "tribal_geometric",
        "border_width": 32,
        "pallu_width": 68,
        "texture": "slub_tussar",
    },
    {
        "filename": "kasavu_kerala_offwhite_broad_gold_border.jpg",
        "primary_color": (248, 245, 235),
        "secondary_color": (225, 185, 55),
        "pattern": "plain_weave",
        "border_width": 55,
        "pallu_width": 95,
        "texture": "crisp_cotton",
    },
    {
        "filename": "georgette_lavender_ombre_floral_digital_print.jpg",
        "primary_color": (190, 170, 220),
        "secondary_color": (110, 70, 150),
        "pattern": "watercolour_floral",
        "border_width": 18,
        "pallu_width": 45,
        "texture": "flowy_georgette",
    },
    {
        "filename": "georgette_rose_pink_botanical_print.jpg",
        "primary_color": (230, 140, 165),
        "secondary_color": (75, 125, 80),
        "pattern": "watercolour_floral",
        "border_width": 20,
        "pallu_width": 48,
        "texture": "flowy_georgette",
    },
    {
        "filename": "organza_glass_tissue_powder_blue_scallop_zari.jpg",
        "primary_color": (185, 215, 240),
        "secondary_color": (235, 205, 90),
        "pattern": "scallop_border_subtle",
        "border_width": 25,
        "pallu_width": 50,
        "texture": "crisp_sheer_organza",
    },
    {
        "filename": "sambalpuri_ikat_terracotta_chevron_black_border.jpg",
        "primary_color": (185, 75, 50),
        "secondary_color": (30, 30, 35),
        "pattern": "ikat_chevron",
        "border_width": 42,
        "pallu_width": 78,
        "texture": "handloom_cotton",
    },
    {
        "filename": "paithani_royal_purple_gold_mor_peacock_pallu.jpg",
        "primary_color": (95, 25, 105),
        "secondary_color": (230, 185, 45),
        "pattern": "oblique_square_motifs",
        "border_width": 46,
        "pallu_width": 90,
        "texture": "heavy_silk",
    }
]


def generate_saree_image(spec: dict, width: int = 400, height: int = 560) -> Image.Image:
    """Render a detailed, authentic saree representation using procedural textile shading."""
    img = Image.new("RGB", (width, height), spec["primary_color"])
    draw = ImageDraw.Draw(img)

    p_col = spec["primary_color"]
    s_col = spec["secondary_color"]
    b_w = spec["border_width"]
    p_w = spec["pallu_width"]
    pat = spec["pattern"]

    # 1. Subtle drape folds / lighting gradient across body
    for y in range(height):
        fold = math.sin(y / 35.0) * 12 + math.cos(y / 70.0) * 8
        blend_r = int(max(0, min(255, p_col[0] + fold)))
        blend_g = int(max(0, min(255, p_col[1] + fold)))
        blend_b = int(max(0, min(255, p_col[2] + fold)))
        draw.line([(0, y), (width, y)], fill=(blend_r, blend_g, blend_b))

    # 2. Main field textile patterns
    if pat == "floral_brocade":
        step = 36
        for y in range(b_w + 10, height - b_w - p_w, step):
            for x in range(b_w + 10, width - b_w - 10, step):
                # Draw miniature floral zari booti
                draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=s_col)
                draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=p_col)
                draw.line([(x - 8, y), (x + 8, y)], fill=s_col, width=1)
                draw.line([(x, y - 8), (x, y + 8)], fill=s_col, width=1)

    elif pat == "kalga_buta":
        step = 42
        for y in range(b_w + 15, height - b_w - p_w, step):
            for x in range(b_w + 15, width - b_w - 15, step):
                draw.polygon([(x, y - 7), (x + 5, y + 3), (x - 5, y + 3)], fill=s_col)
                draw.ellipse([x - 2, y + 4, x + 2, y + 8], fill=s_col)

    elif pat == "temple_motifs":
        step = 32
        for y in range(b_w + 10, height - b_w - p_w, step):
            for x in range(b_w + 10, width - b_w - 10, step):
                draw.polygon([(x, y - 6), (x + 6, y + 6), (x - 6, y + 6)], fill=s_col)

    elif pat == "tie_dye_dots":
        step = 22
        for y in range(b_w + 8, height - b_w - p_w, step):
            offset = 11 if (y // step) % 2 == 1 else 0
            for x in range(b_w + 8 + offset, width - b_w - 8, step):
                draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill=s_col)
                draw.point((x, y), fill=(255, 255, 255))

    elif pat == "double_ikat_grid":
        step = 28
        for y in range(b_w + 10, height - b_w - p_w, step):
            for x in range(b_w + 10, width - b_w - 10, step):
                draw.rectangle([x - 8, y - 8, x + 8, y + 8], outline=s_col, width=2)
                draw.line([(x - 4, y - 4), (x + 4, y + 4)], fill=s_col, width=1)
                draw.line([(x - 4, y + 4), (x + 4, y - 4)], fill=s_col, width=1)

    elif pat == "diagonal_leheriya":
        for d in range(-height, width + height, 24):
            draw.line([(d, 0), (d + height, height)], fill=s_col, width=4)

    elif pat == "hand_painted_botanical":
        step = 50
        for y in range(b_w + 20, height - b_w - p_w, step):
            for x in range(b_w + 20, width - b_w - 20, step):
                draw.arc([x - 12, y - 12, x + 12, y + 12], 0, 270, fill=s_col, width=2)
                draw.ellipse([x + 6, y - 6, x + 12, y], fill=(180, 50, 40))

    elif pat == "watercolour_floral":
        step = 45
        for y in range(b_w + 15, height - b_w - p_w, step):
            for x in range(b_w + 15, width - b_w - 15, step):
                draw.ellipse([x - 12, y - 12, x + 12, y + 12], fill=s_col)
                draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(255, 240, 245))

    elif pat == "fine_booti" or pat == "scallop_border_subtle":
        step = 28
        for y in range(b_w + 10, height - b_w - p_w, step):
            for x in range(b_w + 10, width - b_w - 10, step):
                draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=s_col)

    elif pat == "ikat_chevron":
        step = 20
        for y in range(b_w + 10, height - b_w - p_w, step):
            for x in range(b_w + 5, width - b_w - 20, 30):
                draw.line([(x, y), (x + 15, y - 8), (x + 30, y)], fill=s_col, width=3)

    # 3. Traditional Decorative Borders (Left, Right, and Top edges)
    # Left Border
    draw.rectangle([0, 0, b_w, height], fill=s_col)
    for y in range(0, height, 16):
        draw.line([(0, y), (b_w, y)], fill=p_col, width=2)
        draw.polygon([(b_w, y), (b_w + 6, y + 8), (b_w, y + 16)], fill=s_col)

    # Right Border
    draw.rectangle([width - b_w, 0, width, height], fill=s_col)
    for y in range(0, height, 16):
        draw.line([(width - b_w, y), (width, y)], fill=p_col, width=2)
        draw.polygon([(width - b_w, y), (width - b_w - 6, y + 8), (width - b_w, y + 16)], fill=s_col)

    # 4. Rich Ornamental Pallu / Aanchal at Bottom
    pallu_top = height - p_w
    draw.rectangle([0, pallu_top, width, height], fill=s_col)
    # Pallu zari bands & motifs
    for y_band in range(pallu_top + 10, height - 10, 18):
        draw.line([(b_w, y_band), (width - b_w, y_band)], fill=p_col, width=3)
        for x_m in range(b_w + 15, width - b_w - 15, 25):
            draw.ellipse([x_m - 4, y_band - 4, x_m + 4, y_band + 4], fill=(255, 235, 120))

    # Apply slight natural textile filter
    img = img.filter(ImageFilter.SMOOTH_MORE)
    return img


def main():
    print(f"Generating {len(SAREE_CATALOG)} authentic saree catalog images in '{OUTPUT_DIR}'...")
    for idx, item in enumerate(SAREE_CATALOG, 1):
        target_path = OUTPUT_DIR / item["filename"]
        img = generate_saree_image(item)
        img.save(target_path, quality=95)
        print(f"  [{idx}/{len(SAREE_CATALOG)}] Created {item['filename']} ({img.size[0]}x{img.size[1]})")
    print("Catalog generation complete!")


if __name__ == "__main__":
    main()
