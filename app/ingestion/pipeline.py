"""Dataset ingestion and vector index creation pipeline."""

import argparse
import logging
from pathlib import Path
import time
from typing import List, Optional
import numpy as np
from PIL import Image

from app.config import config
from app.embeddings.image_encoder import get_image_encoder
from app.exceptions import IngestionError
from app.image_utils.loader import ImageLoader
from app.image_utils.validation import ImageValidator
from app.ingestion.metadata import extract_metadata_for_image
from app.retrieval.vector_store import FAISSVectorStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("TailorTalk.Ingestion")


class IngestionPipeline:
    """Discovers images, generates normalized embeddings, extracts metadata, and populates FAISS."""

    def __init__(
        self,
        images_dir: Optional[Path] = None,
        index_dir: Optional[Path] = None,
        batch_size: int = config.model.batch_size,
    ) -> None:
        self.images_dir = images_dir or config.storage.images_dir
        self.index_dir = index_dir or config.storage.index_dir
        self.batch_size = batch_size
        self.encoder = get_image_encoder()
        self.vector_store = FAISSVectorStore(
            dimension=self.encoder.embedding_dim,
            index_file=self.index_dir / "saree_faiss.index",
            metadata_file=self.index_dir / "saree_metadata.json",
        )

    def discover_images(self) -> List[Path]:
        """Recursively scan image directory and filter supported extensions."""
        if not self.images_dir.exists():
            logger.warning(f"Images directory '{self.images_dir}' does not exist.")
            return []

        found: List[Path] = []
        for ext in config.storage.supported_extensions:
            found.extend(self.images_dir.rglob(f"*{ext}"))
            found.extend(self.images_dir.rglob(f"*{ext.upper()}"))

        # Deduplicate paths and sort for deterministic order
        unique_images = sorted(list(set(found)))
        logger.info(f"Discovered {len(unique_images)} candidate images in '{self.images_dir}'")
        return unique_images

    def run(self, force_reindex: bool = False) -> int:
        """Execute the ingestion pipeline with strict duplicate prevention and clean reindexing."""
        start_time = time.time()
        logger.info(f"Starting TailorTalk Saree Ingestion Pipeline (force_reindex={force_reindex})...")

        if force_reindex:
            logger.info("force_reindex=True: resetting vector index and clearing previous state.")
            self.vector_store.clear()

        image_paths = self.discover_images()
        if not image_paths:
            logger.warning("No images found to index. Dataset directory is currently empty.")
            return 0

        # Validate images and filter out corrupt ones, deduplicating by stem (image ID)
        valid_paths: List[Path] = []
        seen_ids = set()
        for p in image_paths:
            try:
                ImageValidator.validate_file_path(p)
                with Image.open(p) as img:
                    img.verify()
                img_id = p.stem
                if img_id in seen_ids:
                    logger.warning(f"Duplicate image ID '{img_id}' encountered at '{p}'. Skipping duplicate.")
                    continue
                seen_ids.add(img_id)
                valid_paths.append(p)
            except Exception as e:
                logger.warning(f"Skipping invalid/corrupt image '{p.name}': {str(e)}")

        logger.info(f"Verified {len(valid_paths)} unique valid images for indexing.")

        if not valid_paths:
            raise IngestionError("No valid images available for indexing.")

        # Batch encode and extract metadata
        all_vectors = []
        all_ids = []
        all_metadata = []

        total_batches = (len(valid_paths) + self.batch_size - 1) // self.batch_size

        for b_idx in range(total_batches):
            batch_paths = valid_paths[b_idx * self.batch_size : (b_idx + 1) * self.batch_size]
            batch_images: List[Image.Image] = []
            batch_valid_paths: List[Path] = []

            for path in batch_paths:
                try:
                    img = ImageLoader.load_from_path(path)
                    batch_images.append(img)
                    batch_valid_paths.append(path)
                except Exception as e:
                    logger.warning(f"Error loading image '{path.name}': {str(e)}")

            if not batch_images:
                continue

            # Generate batch embeddings
            vectors = self.encoder.encode_batch(batch_images)

            for path, vec in zip(batch_valid_paths, vectors):
                meta = extract_metadata_for_image(path, self.images_dir)
                all_vectors.append(vec)
                all_ids.append(meta.image_id)
                all_metadata.append(meta.model_dump())

            logger.info(f"Processed batch {b_idx + 1}/{total_batches} ({len(all_vectors)} images prepared)")

        # Populate and persist vector store
        if all_vectors:
            vectors_array = np.array(all_vectors, dtype=np.float32)
            self.vector_store.add(vectors_array, all_ids, all_metadata)
            self.vector_store.save()

        elapsed = time.time() - start_time
        logger.info(
            f"Ingestion completed successfully! Indexed {len(all_vectors)} sarees in {elapsed:.2f}s."
        )
        return len(all_vectors)


def main():
    parser = argparse.ArgumentParser(description="TailorTalk Saree Dataset Ingestion CLI")
    parser.add_argument("--images-dir", type=Path, default=config.storage.images_dir, help="Directory containing saree images")
    parser.add_argument("--index-dir", type=Path, default=config.storage.index_dir, help="Directory to save FAISS index and metadata")
    parser.add_argument("--batch-size", type=int, default=config.model.batch_size, help="Embedding generation batch size")
    parser.add_argument("--force", action="store_true", help="Force reindexing of all images")

    args = parser.parse_args()
    pipeline = IngestionPipeline(
        images_dir=args.images_dir,
        index_dir=args.index_dir,
        batch_size=args.batch_size,
    )
    count = pipeline.run(force_reindex=args.force)
    print(f"Indexed {count} saree images.")


if __name__ == "__main__":
    main()
