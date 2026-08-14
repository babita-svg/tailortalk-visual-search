"""Script entry point to build or rebuild the FAISS vector index."""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.ingestion.pipeline import IngestionPipeline


def main():
    print("=" * 60)
    print(" TailorTalk: Building Saree Visual Vector Index")
    print("=" * 60)
    pipeline = IngestionPipeline()
    count = pipeline.run(force_reindex=True)
    print(f"Successfully indexed {count} sarees into FAISS vector database!")


if __name__ == "__main__":
    main()
