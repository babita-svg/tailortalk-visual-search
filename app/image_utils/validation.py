"""Image validation utilities.

Validates image formats, byte sizes, dimensions, path safety, and URL formats
to prevent invalid operations, resource exhaustion, and security vulnerabilities.
"""

from io import BytesIO
import os
from pathlib import Path
from typing import Optional, Set, Tuple
from urllib.parse import urlparse
from PIL import Image

from app.config import config
from app.exceptions import InvalidImageError


class ImageValidator:
    """Security and integrity validator for saree images."""

    ALLOWED_FORMATS: Set[str] = {"JPEG", "JPG", "PNG", "WEBP"}
    ALLOWED_EXTENSIONS: Set[str] = {".jpg", ".jpeg", ".png", ".webp"}
    MIN_DIMENSION: int = 32
    MAX_DIMENSION: int = 8192
    MAX_FILE_BYTES: int = config.storage.max_upload_size_mb * 1024 * 1024

    @classmethod
    def validate_file_path(cls, path_input: str | Path, base_dir: Optional[Path] = None) -> Path:
        """Validate that a local file path exists, is a safe path, and is an allowed image type."""
        path = Path(path_input).resolve()
        
        # Path traversal guard if base_dir is enforced
        if base_dir is not None:
            base = Path(base_dir).resolve()
            if not str(path).startswith(str(base)):
                raise InvalidImageError(f"Security: Path '{path_input}' is outside authorized directory '{base}'.")

        if not path.exists():
            raise InvalidImageError(f"Image file does not exist: {path_input}")
        
        if not path.is_file():
            raise InvalidImageError(f"Path is not a regular file: {path_input}")

        if path.suffix.lower() not in cls.ALLOWED_EXTENSIONS:
            raise InvalidImageError(
                f"Unsupported image extension '{path.suffix}'. Allowed extensions: {', '.join(cls.ALLOWED_EXTENSIONS)}"
            )

        file_size = path.stat().st_size
        if file_size == 0:
            raise InvalidImageError(f"Image file is empty (0 bytes): {path_input}")
        if file_size > cls.MAX_FILE_BYTES:
            raise InvalidImageError(
                f"Image file size ({file_size / (1024*1024):.1f} MB) exceeds maximum permitted limit ({config.storage.max_upload_size_mb} MB)."
            )

        return path

    @classmethod
    def is_valid_url(cls, url: str) -> bool:
        """Check whether a URL is a valid http/https image URL without raising exceptions."""
        try:
            cls.validate_url(url)
            return True
        except Exception:
            return False

    @classmethod
    def validate_bytes(cls, image_bytes: bytes, max_size_mb: Optional[int] = None) -> Image.Image:
        """Validate and verify raw byte stream as a valid PIL image with optional custom max size."""
        if not image_bytes:
            raise InvalidImageError("Received empty byte buffer for image validation.")

        limit = (max_size_mb * 1024 * 1024) if max_size_mb is not None else cls.MAX_FILE_BYTES
        if len(image_bytes) > limit:
            raise InvalidImageError(
                f"Byte size ({len(image_bytes) / (1024*1024):.1f} MB) exceeds limit ({limit / (1024*1024):.1f} MB)."
            )

        return cls.validate_raw_bytes(image_bytes)

    @classmethod
    def validate_url(cls, url: str) -> str:
        """Validate format and scheme of an image URL."""
        if not url or not isinstance(url, str):
            raise InvalidImageError("Invalid URL: URL cannot be empty.")

        url = url.strip()
        parsed = urlparse(url)
        if parsed.scheme.lower() not in {"http", "https"}:
            raise InvalidImageError(f"Invalid URL scheme '{parsed.scheme}'. Only HTTP and HTTPS are permitted.")
        
        if not parsed.netloc:
            raise InvalidImageError("Invalid URL: Missing domain/network location.")

        return url

    @classmethod
    def validate_pil_image(cls, img: Image.Image) -> Image.Image:
        """Validate an in-memory PIL Image instance."""
        if not isinstance(img, Image.Image):
            raise InvalidImageError(f"Expected PIL Image, received {type(img)}.")

        width, height = img.size
        if width < cls.MIN_DIMENSION or height < cls.MIN_DIMENSION:
            raise InvalidImageError(
                f"Image resolution ({width}x{height}) is below minimum viable threshold ({cls.MIN_DIMENSION}x{cls.MIN_DIMENSION})."
            )
        
        if width > cls.MAX_DIMENSION or height > cls.MAX_DIMENSION:
            raise InvalidImageError(
                f"Image resolution ({width}x{height}) exceeds maximum permitted dimension ({cls.MAX_DIMENSION}x{cls.MAX_DIMENSION})."
            )

        return img

    @classmethod
    def validate_raw_bytes(cls, image_bytes: bytes) -> Image.Image:
        """Validate and verify raw byte stream as a valid PIL image."""
        if not image_bytes:
            raise InvalidImageError("Received empty byte buffer for image validation.")

        if len(image_bytes) > cls.MAX_FILE_BYTES:
            raise InvalidImageError(
                f"Byte size ({len(image_bytes) / (1024*1024):.1f} MB) exceeds limit ({config.storage.max_upload_size_mb} MB)."
            )

        try:
            stream = BytesIO(image_bytes)
            img = Image.open(stream)
            img.verify()  # Verifies file integrity
            
            # Reopen after verify because verify() exhausts/mangles the stream in PIL
            stream.seek(0)
            img = Image.open(stream)
            img.load()
            return cls.validate_pil_image(img)
        except Exception as e:
            raise InvalidImageError(f"Failed to decode or verify image bytes: {str(e)}") from e
