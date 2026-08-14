#!/usr/bin/env python3
"""Catalogue verification and integrity script."""

import csv
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

CATALOG_PATH = Path("data/byrappa_tejas_31july.csv")

def verify():
    if not CATALOG_PATH.exists():
        print(f"ERROR: Catalogue file {CATALOG_PATH} not found!")
        sys.exit(1)

    with open(CATALOG_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    total_rows = len(rows)
    print(f"Total CSV rows: {total_rows}")

    valid_rows = 0
    invalid_rows = 0
    duplicate_skus = set()
    seen_skus = set()
    missing_images = 0
    missing_links = 0
    invalid_prices = 0

    for idx, r in enumerate(rows):
        name = r.get("Name", "").strip()
        sku = r.get("SKU", "").strip()
        stock = r.get("Stock", "").strip()
        retail = r.get("Retail Price", "").strip()
        discounted = r.get("Discounted Price", "").strip()
        image_url = r.get("image_url", "").strip()
        website_link = r.get("Website Link", "").strip()

        if not name or not sku:
            invalid_rows += 1
            continue

        if sku in seen_skus:
            duplicate_skus.add(sku)
        seen_skus.add(sku)

        if not image_url:
            missing_images += 1
        if not website_link:
            missing_links += 1

        try:
            if retail:
                float(retail)
            if discounted:
                float(discounted)
        except ValueError:
            invalid_prices += 1

        valid_rows += 1

    print(f"Valid product rows: {valid_rows}")
    print(f"Invalid product rows: {invalid_rows}")
    print(f"Unique SKUs: {len(seen_skus)}")
    print(f"Duplicate SKU instances: {len(duplicate_skus)}")
    print(f"Missing images: {missing_images}")
    print(f"Missing website links: {missing_links}")
    print(f"Invalid price fields: {invalid_prices}")

    report = {
        "total_records": total_rows,
        "valid_records": valid_rows,
        "invalid_records": invalid_rows,
        "unique_skus": len(seen_skus),
        "missing_images": missing_images,
        "missing_website_links": missing_links,
    }

    os.makedirs("data/catalog", exist_ok=True)
    with open("data/catalog/ingestion_report.json", "w", encoding="utf-8") as out:
        json.dump(report, out, indent=2)

    print("Generated data/catalog/ingestion_report.json")
    print("VERIFICATION COMPLETED SUCCESSFULLY.")

if __name__ == "__main__":
    verify()
