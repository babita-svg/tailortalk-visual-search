import csv
import json
import re
import hashlib

def extract_metadata_from_name(name: str):
    name_lower = name.lower()
    
    # Category detection
    category = "Banarasi"
    if "kanjeevaram" in name_lower or "kanchipuram" in name_lower:
        category = "Kanjeevaram"
    elif "bandhani" in name_lower:
        category = "Bandhani"
    elif "chanderi" in name_lower:
        category = "Chanderi"
    elif "kalamkari" in name_lower:
        category = "Kalamkari"
    elif "paithani" in name_lower:
        category = "Paithani"
    elif "patola" in name_lower:
        category = "Patola"
    elif "tussar" in name_lower:
        category = "Tussar Silk"
    elif "organza" in name_lower:
        category = "Organza"
    elif "georgette" in name_lower:
        category = "Georgette"
    elif "mysore" in name_lower:
        category = "Mysore Silk"
    elif "linen" in name_lower:
        category = "Linen"
    elif "cotton" in name_lower:
        category = "Cotton"
    elif "crape" in name_lower or "crepe" in name_lower:
        category = "Crape Silk"
    elif "satin" in name_lower:
        category = "Satin Silk"
    elif "banaras" in name_lower or "banarasi" in name_lower:
        category = "Banarasi"

    # Color detection
    primary_color = "Crimson Red"
    color_hexes = ["#DC2626", "#B91C1C", "#991B1B"]
    if "pink" in name_lower or "rose" in name_lower or "rani" in name_lower or "fuchsia" in name_lower:
        primary_color = "Pink / Magenta"
        color_hexes = ["#EC4899", "#DB2777", "#BE185D"]
    elif "yellow" in name_lower or "mustard" in name_lower or "gold" in name_lower:
        primary_color = "Mustard Yellow / Gold"
        color_hexes = ["#EAB308", "#CA8A04", "#A16207"]
    elif "blue" in name_lower or "navy" in name_lower or "cyan" in name_lower or "teal" in name_lower:
        primary_color = "Royal / Peacock Blue"
        color_hexes = ["#2563EB", "#1D4ED8", "#1E40AF"]
    elif "green" in name_lower or "olive" in name_lower or "mint" in name_lower or "pista" in name_lower or "sage" in name_lower:
        primary_color = "Emerald / Olive Green"
        color_hexes = ["#16A34A", "#15803D", "#166534"]
    elif "purple" in name_lower or "lavender" in name_lower or "violet" in name_lower or "mauve" in name_lower or "wine" in name_lower or "plum" in name_lower:
        primary_color = "Royal Purple / Wine"
        color_hexes = ["#9333EA", "#7E22CE", "#6B21A8"]
    elif "black" in name_lower:
        primary_color = "Deep Black"
        color_hexes = ["#18181B", "#27272A", "#3F3F46"]
    elif "white" in name_lower or "cream" in name_lower or "ivory" in name_lower or "beige" in name_lower or "fawn" in name_lower:
        primary_color = "Off-White / Cream"
        color_hexes = ["#F5F5F4", "#E7E5E4", "#D6D3D1"]
    elif "orange" in name_lower or "peach" in name_lower or "rust" in name_lower or "terracotta" in name_lower:
        primary_color = "Rust Orange / Peach"
        color_hexes = ["#EA580C", "#C2410C", "#9A3412"]
    elif "grey" in name_lower or "gray" in name_lower or "silver" in name_lower or "ash" in name_lower:
        primary_color = "Silver Grey"
        color_hexes = ["#64748B", "#475569", "#334155"]
    elif "maroon" in name_lower:
        primary_color = "Rich Maroon"
        color_hexes = ["#831843", "#9F1239", "#881337"]

    # Fabric
    fabric = "Pure Silk"
    if "organza" in name_lower:
        fabric = "Pure Organza"
    elif "tussar" in name_lower:
        fabric = "Pure Tussar Silk"
    elif "georgette" in name_lower:
        fabric = "Georgette"
    elif "linen" in name_lower:
        fabric = "Linen Silk"
    elif "cotton" in name_lower:
        fabric = "Mul Cotton"
    elif "crape" in name_lower or "crepe" in name_lower:
        fabric = "Crape Silk"
    elif "satin" in name_lower:
        fabric = "Satin Silk"
    elif "chanderi" in name_lower:
        fabric = "Chanderi Silk"
    elif "kora" in name_lower:
        fabric = "Kora Handloom"
    elif "mysore" in name_lower:
        fabric = "Pure Mysore Silk"
    elif "tissue" in name_lower:
        fabric = "Tissue Silk"

    # Deterministic vector based on hash
    h = hashlib.md5(name.encode('utf-8')).hexdigest()
    nums = [int(h[i:i+2], 16) / 255.0 for i in range(0, 32, 2)]
    
    return {
        "category": category,
        "primaryColor": primary_color,
        "fabric": fabric,
        "dominantColors": color_hexes,
        "vector": [round(x, 4) for x in nums]
    }

def build_ts():
    # Read user input CSV lines from the prompt or from the file
    csv_path = 'data/byrappa_tejas_31july.csv'
    with open(csv_path, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
        
    print(f"Read {len(rows)} products from CSV.")
    
    items = []
    for idx, r in enumerate(rows):
        name = r.get('Name', '').strip()
        sku = r.get('SKU', '').strip() or f"SKU_{idx+1}"
        stock = int(r.get('Stock', '0') or '0') if str(r.get('Stock', '0')).replace('-','').isdigit() else 0
        retail_price = float(r.get('Retail Price', '0') or '0') if str(r.get('Retail Price', '0')).replace('.','').isdigit() else None
        disc_price = float(r.get('Discounted Price', '0') or '0') if str(r.get('Discounted Price', '0')).replace('.','').isdigit() else None
        image_url = r.get('image_url', '').strip()
        website_link = r.get('Website Link', '').strip()
        
        meta = extract_metadata_from_name(name)
        
        item = {
            "id": sku.lower().replace(' ', '_') + f"_{idx}",
            "sku": sku,
            "filename": f"{sku}.webp",
            "name": name,
            "category": meta["category"],
            "fabric": meta["fabric"],
            "primaryColor": meta["primaryColor"],
            "secondaryColor": "Gold Zari",
            "weave": "Traditional Handloom Weave",
            "border": "Contrast Border with Zari Accents",
            "pallu": "Rich Detailed Pallu",
            "occasion": "Festive & Wedding Wear",
            "description": f"{name} featuring authentic textile craftsmanship.",
            "dominantColors": meta["dominantColors"],
            "colorHistogram": {"h": [0.3, 0.4, 0.3], "s": [0.6, 0.8, 0.7], "v": [0.7, 0.9, 0.8]},
            "textureScore": 0.85,
            "borderWeight": 0.80,
            "vector": meta["vector"],
            "stock": stock,
            "retailPrice": retail_price,
            "discountedPrice": disc_price,
            "imageUrl": image_url,
            "websiteLink": website_link
        }
        items.append(item)
        
    ts_code = f"""export interface SareeItem {{
  id: string;
  sku?: string;
  filename: string;
  name: string;
  category: string;
  fabric: string;
  primaryColor: string;
  secondaryColor?: string;
  weave: string;
  border: string;
  pallu: string;
  occasion: string;
  description: string;
  dominantColors: string[];
  colorHistogram: {{ h: number[]; s: number[]; v: number[] }};
  textureScore: number;
  borderWeight: number;
  vector: number[];
  stock?: number;
  retailPrice?: number | null;
  discountedPrice?: number | null;
  imageUrl?: string;
  websiteLink?: string;
}}

export const SAREE_CATALOG: SareeItem[] = {json.dumps(items, indent=2)};
"""
    with open('src/data/catalog.ts', 'w', encoding='utf-8') as f:
        f.write(ts_code)
    print(f"Generated src/data/catalog.ts with {len(items)} items.")

if __name__ == '__main__':
    build_ts()
