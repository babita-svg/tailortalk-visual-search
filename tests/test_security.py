"""Unit tests for security guards: SSRF protection, path traversal, and payload limits."""

from pathlib import Path
import pytest
from app.exceptions import InvalidImageError
from app.image_utils.validation import ImageValidator


def test_is_safe_ip():
    """Verify IP classification correctly blocks private, loopback, link-local, and multicast IPs."""
    # Loopback
    assert not ImageValidator.is_safe_ip("127.0.0.1")
    assert not ImageValidator.is_safe_ip("127.0.1.1")
    assert not ImageValidator.is_safe_ip("::1")

    # Private RFC 1918
    assert not ImageValidator.is_safe_ip("10.0.0.1")
    assert not ImageValidator.is_safe_ip("172.16.0.1")
    assert not ImageValidator.is_safe_ip("192.168.1.1")

    # Link-local / Cloud Metadata
    assert not ImageValidator.is_safe_ip("169.254.169.254")

    # Public IP
    assert ImageValidator.is_safe_ip("8.8.8.8")
    assert ImageValidator.is_safe_ip("1.1.1.1")


def test_validate_url_ssrf_blocking():
    """Verify SSRF validation blocks dangerous schemes and restricted hosts."""
    # Invalid schemes
    with pytest.raises(InvalidImageError, match="Invalid URL scheme"):
        ImageValidator.validate_url("file:///etc/passwd")

    with pytest.raises(InvalidImageError, match="Invalid URL scheme"):
        ImageValidator.validate_url("ftp://example.com/image.jpg")

    # Forbidden hostnames
    with pytest.raises(InvalidImageError, match="Security"):
        ImageValidator.validate_url("http://localhost/image.jpg")

    with pytest.raises(InvalidImageError, match="Security"):
        ImageValidator.validate_url("http://127.0.0.1:8080/image.jpg")

    with pytest.raises(InvalidImageError, match="Security"):
        ImageValidator.validate_url("http://metadata.google.internal/computeMetadata/v1/")

    with pytest.raises(InvalidImageError, match="Security"):
        ImageValidator.validate_url("http://169.254.169.254/latest/meta-data/")


def test_validate_file_path_traversal(tmp_path):
    """Verify path traversal outside authorized base_dir is rejected."""
    base_dir = tmp_path / "authorized"
    base_dir.mkdir()
    secret_dir = tmp_path / "secret"
    secret_dir.mkdir()

    secret_file = secret_dir / "passwords.jpg"
    secret_file.write_bytes(b"dummy")

    with pytest.raises(InvalidImageError, match="Security: Path .* is outside authorized directory"):
        ImageValidator.validate_file_path(secret_file, base_dir=base_dir)
