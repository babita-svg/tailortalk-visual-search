"""Ingestion pipeline for byrappa_tejas_31july.csv catalogue."""

import csv
import io
import json
import logging
from pathlib import Path
import re
import socket
import time
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse
import requests
from PIL import Image
import numpy as np

from app.config import config
from app.schemas import SareeMetadata
from app.image_utils.validation import ImageValidator
from app.embeddings.image_encoder import get_image_encoder
from app.retrieval.reranker import FineGrainedSareeReranker
from app.retrieval.vector_store import FAISSVectorStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CatalogueIngestion")


def is_safe_url(url: str) -> bool:
    """Validate URL scheme and block SSRF, loopback, private networks."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        hostname = parsed.hostname
        if not hostname:
            return False
        if hostname in ("localhost", "127.0.0.1", "0.0.0.0", "::1"):
            return False
        ip = socket.gethostbyname(hostname)
        parts = [int(p) for p in ip.split(".")]
        if len(parts) == 4:
            if parts[0] == 10:
                return False
            if parts[0] == 172 and 16 <= parts[1] <= 31:
                return False
            if parts[0] == 192 and parts[1] == 168:
                return False
            if parts[0] == 127:
                return False
            if parts[0] == 169 and parts[1] == 254:
                return False
        return True
    except Exception:
        return False


def parse_numeric(val: Any) -> Optional[float]:
    """Safely parse price or float value."""
    if val is None:
        return None
    cleaned = re.sub(r"[^\d.-]", "", str(val).strip())
    try:
        return float(cleaned) if cleaned else None
    except ValueError:
        return None


def parse_int(val: Any) -> Optional[int]:
    """Safely parse integer stock value."""
    if val is None:
        return None
    cleaned = re.sub(r"[^\d-]", "", str(val).strip())
    try:
        return int(cleaned) if cleaned else None
    except ValueError:
        return None


class CatalogueIngestor:
    def __init__(self, csv_path: Path, output_images_dir: Path, index_dir: Path):
        self.csv_path = csv_path
        self.output_images_dir = output_images_dir
        self.index_dir = index_dir
        self.output_images_dir.mkdir(parents=True, exist_ok=True)
        self.index_dir.mkdir(parents=True, exist_ok=True)

    def load_csv(self) -> List[Dict[str, str]]:
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        rows = []
        with open(self.csv_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append(r)
        return rows

    def download_image(self, image_url: str, dest_path: Path, timeout: int = 10) -> bool:
        if not is_safe_url(image_url):
            logger.warning(f"Unsafe URL rejected: {image_url}")
            return False
        try:
            resp = requests.get(image_url, timeout=timeout, headers={"User-Agent": "TailorTalk/1.0"})
            if resp.status_code != 200:
                logger.warning(f"HTTP {resp.status_code} for {image_url}")
                return False
            data = resp.content
            if len(data) > 15 * 1024 * 1024:
                logger.warning(f"Image exceeded max size: {image_url}")
                return False
            img = Image.open(io.BytesIO(data))
            img.verify()
            img = Image.open(io.BytesIO(data))
            img.save(dest_path)
            return True
        except Exception as e:
            logger.warning(f"Failed to download {image_url}: {e}")
            return False


if __name__ == "__main__":
    print("Catalogue Ingestion Helper Module Loaded.")
