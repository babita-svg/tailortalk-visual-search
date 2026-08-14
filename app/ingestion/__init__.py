"""Dataset ingestion module."""

from app.ingestion.metadata import extract_metadata_for_image
from app.ingestion.pipeline import IngestionPipeline

__all__ = ["IngestionPipeline", "extract_metadata_for_image"]
