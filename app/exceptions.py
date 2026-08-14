"""Custom exceptions for TailorTalk visual search and agent framework."""


class TailorTalkError(Exception):
    """Base exception for all TailorTalk domain errors."""
    pass


class InvalidImageError(TailorTalkError):
    """Raised when an input image cannot be validated, read, or decoded."""
    pass


class CorruptedImageError(InvalidImageError):
    """Raised when an input image is corrupted or truncated."""
    pass


class ImageDownloadError(TailorTalkError):
    """Raised when downloading an image from a URL fails or times out."""
    pass


class EmbeddingGenerationError(TailorTalkError):
    """Raised when the vision embedding model fails to encode an image."""
    pass


class VectorStoreIndexError(TailorTalkError):
    """Raised when the vector store is uninitialized, missing, or corrupt."""
    pass


class RerankerError(TailorTalkError):
    """Raised when fine-grained reranking fails."""
    pass


class IngestionError(TailorTalkError):
    """Raised during dataset ingestion and indexing failures."""
    pass


class AgentToolExecutionError(TailorTalkError):
    """Raised when an agent tool receives invalid arguments or fails to execute."""
    pass
