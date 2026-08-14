"""Image loading and normalization module.

Handles safe ingestion of images from file paths, raw bytes, base64 strings,
and external HTTP/HTTPS URLs with defensive timeout, content-type, and size controls.
"""

import base64
from io import BytesIO
import logging
from pathlib import Path
from typing import Union
from PIL import Image, ImageOps
import requests

from app.config import config
from app.exceptions import ImageDownloadError, InvalidImageError
from app.image_utils.validation import ImageValidator

logger = logging.getLogger(__name__)


class ImageLoader:
    """Safe loader and normalizer for saree query and dataset images."""

    DEFAULT_USER_AGENT = "TailorTalk-VisualSearch/1.0 (Vision Evaluation Bot)"

    @classmethod
    def load_from_path(cls, file_path: Union[str, Path]) -> Image.Image:
        """Load and normalize an image from a local filesystem path."""
        valid_path = ImageValidator.validate_file_path(file_path)
        try:
            with Image.open(valid_path) as img:
                return cls.normalize_image(img)
        except Exception as e:
            raise InvalidImageError(f"Unable to read or parse image at '{file_path}': {str(e)}") from e

    @classmethod
    def load_from_bytes(cls, image_bytes: bytes) -> Image.Image:
        """Load and normalize an image from in-memory byte buffer."""
        img = ImageValidator.validate_raw_bytes(image_bytes)
        return cls.normalize_image(img)

    @classmethod
    def load_from_base64(cls, base64_str: str) -> Image.Image:
        """Load and normalize an image from a base64 encoded data URI or raw base64 string."""
        if not base64_str:
            raise InvalidImageError("Base64 image string is empty.")

        try:
            if "," in base64_str:
                # Strip data:image/...;base64, prefix
                base64_str = base64_str.split(",", 1)[1]

            decoded_bytes = base64.b64decode(base64_str)
            return cls.load_from_bytes(decoded_bytes)
        except Exception as e:
            raise InvalidImageError(f"Failed to decode base64 image data: {str(e)}") from e

    @classmethod
    def load_from_url(cls, url: str) -> Image.Image:
        """Download and normalize an image from an HTTP/HTTPS URL with strict timeout and size limits."""
        valid_url = ImageValidator.validate_url(url)
        headers = {"User-Agent": cls.DEFAULT_USER_AGENT, "Accept": "image/*"}

        try:
            response = requests.get(
                valid_url,
                headers=headers,
                timeout=config.storage.url_request_timeout_seconds,
                stream=True,
            )
            response.raise_for_status()

            # Validate Content-Type header if provided
            content_type = response.headers.get("Content-Type", "").lower()
            if content_type and not content_type.startswith("image/"):
                raise ImageDownloadError(
                    f"URL returned non-image content type '{content_type}'. Expected 'image/*'."
                )

            # Enforce max content length header check
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > ImageValidator.MAX_FILE_BYTES:
                raise ImageDownloadError(
                    f"Remote image exceeds size limit ({int(content_length) / (1024*1024):.1f} MB)."
                )

            # Stream download with byte counter to prevent zip-bomb / unbounded download
            downloaded = bytearray()
            for chunk in response.iter_content(chunk_size=65536):
                downloaded.extend(chunk)
                if len(downloaded) > ImageValidator.MAX_FILE_BYTES:
                    raise ImageDownloadError(
                        f"Streamed image exceeds maximum allowed download size of {config.storage.max_upload_size_mb} MB."
                    )

            return cls.load_from_bytes(bytes(downloaded))

        except requests.exceptions.Timeout as e:
            raise ImageDownloadError(f"Request timed out while fetching image from '{valid_url}'.") from e
        except requests.exceptions.RequestException as e:
            raise ImageDownloadError(f"Network error while fetching image from '{valid_url}': {str(e)}") from e
        except Exception as e:
            if isinstance(e, (ImageDownloadError, InvalidImageError)):
                raise
            raise ImageDownloadError(f"Failed to process remote image: {str(e)}") from e

    @classmethod
    def load(cls, source: Union[str, Path, bytes, Image.Image]) -> Image.Image:
        """Polymorphic loader resolving paths, URLs, byte buffers, or existing PIL Images."""
        if isinstance(source, Image.Image):
            return cls.normalize_image(source)
        if isinstance(source, bytes):
            return cls.load_from_bytes(source)
        if isinstance(source, (str, Path)):
            s = str(source).strip()
            if s.startswith("http://") or s.startswith("https://"):
                return cls.load_from_url(s)
            if s.startswith("data:image/") or (len(s) > 100 and ";" not in s and " " not in s):
                try:
                    return cls.load_from_base64(s)
                except InvalidImageError:
                    pass  # Fall through to path check
            return cls.load_from_path(source)

        raise InvalidImageError(f"Unsupported image input type: {type(source)}")

    @classmethod
    def normalize_image(cls, img: Image.Image) -> Image.Image:
        """Correct EXIF orientation and convert any color mode (RGBA, P, L, CMYK) to standard RGB."""
        # Auto-rotate based on EXIF tags
        try:
            img = ImageOps.exif_transpose(img)
        except Exception:
            pass

        if img.mode == "RGB":
            return img.copy()

        if img.mode in ("RGBA", "LA"):
            # Blend on clean white background
            background = Image.new("RGB", img.size, (255, 255, 255))
            alpha = img.split()[-1]
            background.paste(img, mask=alpha)
            return background

        if img.mode == "P":
            return img.convert("RGBA").convert("RGB")

        return img.convert("RGB")
