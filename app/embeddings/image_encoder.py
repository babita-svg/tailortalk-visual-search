"""Vision embedding encoder module.

Generates normalized high-dimensional visual embeddings using OpenCLIP / Vision Transformers.
Embeddings are L2-normalized to ensure that cosine similarity directly corresponds to dot product.
"""

from abc import ABC, abstractmethod
import logging
from typing import List, Optional, Union
import numpy as np
from PIL import Image

from app.config import config
from app.exceptions import EmbeddingGenerationError

logger = logging.getLogger(__name__)


class BaseImageEncoder(ABC):
    """Abstract Base Class for image feature extractors."""

    @abstractmethod
    def encode_image(self, image: Image.Image) -> np.ndarray:
        """Encode a single PIL image into a 1D L2-normalized numpy embedding."""
        pass

    @abstractmethod
    def encode_batch(self, images: List[Image.Image]) -> np.ndarray:
        """Encode a batch of PIL images into a 2D (N, D) L2-normalized numpy array."""
        pass

    @property
    @abstractmethod
    def embedding_dim(self) -> int:
        """Return the vector dimensionality of output embeddings."""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the model identifier."""
        pass


class OpenCLIPImageEncoder(BaseImageEncoder):
    """OpenCLIP-based vision encoder supporting ViT architectures."""

    def __init__(
        self,
        model_name: str = config.model.model_name,
        pretrained: str = config.model.pretrained,
        device: str = config.model.device,
        allow_test_fallback: bool = False,
    ) -> None:
        self._model_name = model_name
        self._pretrained = pretrained
        self._allow_test_fallback = allow_test_fallback
        self._device = None
        self._model = None
        self._preprocess = None
        self._dim = config.model.embedding_dim

        # Setup device
        try:
            import torch
            self._device = torch.device(device if torch.cuda.is_available() and device == "cuda" else "cpu")
        except Exception:
            if not self._allow_test_fallback:
                raise EmbeddingGenerationError("PyTorch is required for OpenCLIP image encoding but is not available.")

        self._initialize_model()

    def _initialize_model(self) -> None:
        """Load pretrained OpenCLIP model and transformation pipeline."""
        try:
            import open_clip

            logger.info(
                f"Loading OpenCLIP vision encoder: model={self._model_name}, "
                f"pretrained={self._pretrained}, device={self._device}"
            )
            model, _, preprocess = open_clip.create_model_and_transforms(
                self._model_name,
                pretrained=self._pretrained,
                device=self._device,
            )
            model.eval()
            self._model = model
            self._preprocess = preprocess

            # Dynamically infer output dimension
            if hasattr(model, "visual") and hasattr(model.visual, "output_dim"):
                self._dim = model.visual.output_dim
            logger.info(f"OpenCLIP model initialized successfully with embedding_dim={self._dim}")
        except Exception as e:
            if not self._allow_test_fallback:
                logger.error(f"Failed to load OpenCLIP weights: {str(e)}")
                raise EmbeddingGenerationError(
                    f"Failed to load OpenCLIP model '{self._model_name}' (pretrained='{self._pretrained}'): {str(e)}. "
                    f"Production search requires the configured OpenCLIP model."
                ) from e
            logger.warning(
                f"Failed to load OpenCLIP weights ({str(e)}). Test fallback enabled explicitly."
            )
            self._model = None

    @property
    def embedding_dim(self) -> int:
        return self._dim

    @property
    def dimension(self) -> int:
        return self._dim

    @property
    def model_name(self) -> str:
        return f"OpenCLIP-{self._model_name}-{self._pretrained}"

    def encode_image(self, image: Image.Image) -> np.ndarray:
        """Encode a single PIL image into a 1D L2-normalized float32 numpy vector."""
        batch_res = self.encode_batch([image])
        return batch_res[0]

    def encode_batch(self, images: List[Image.Image]) -> np.ndarray:
        """Encode a list of PIL images into an (N, D) float32 L2-normalized matrix."""
        if not images:
            return np.empty((0, self._dim), dtype=np.float32)

        if self._model is not None and self._preprocess is not None:
            try:
                import torch
                tensors = [self._preprocess(img.convert("RGB")) for img in images]
                batch_tensor = torch.stack(tensors).to(self._device)

                with torch.no_grad():
                    features = self._model.encode_image(batch_tensor)
                    features_np = features.cpu().numpy().astype(np.float32)

                # Explicit L2 normalization: vector / ||vector||_2
                norms = np.linalg.norm(features_np, axis=1, keepdims=True)
                norms = np.where(norms == 0, 1.0, norms)
                normalized_features = features_np / norms
                return normalized_features.astype(np.float32)
            except Exception as e:
                logger.error(f"Error during OpenCLIP batch encoding: {str(e)}")
                raise EmbeddingGenerationError(f"OpenCLIP inference failed: {str(e)}") from e

        if self._allow_test_fallback:
            return self._fallback_encode_batch(images)

        raise EmbeddingGenerationError("OpenCLIP vision model is not initialized and test fallback is disabled.")

    def _fallback_encode_batch(self, images: List[Image.Image]) -> np.ndarray:
        """Deterministic feature extractor used ONLY in test fixtures when explicitly configured."""
        embeddings = []
        for img in images:
            rgb = img.convert("RGB").resize((128, 128), Image.Resampling.BILINEAR)
            arr = np.asarray(rgb, dtype=np.float32) / 255.0  # (128, 128, 3)

            # Spatial grid pooling 4x4 -> 16 cells * 3 channels = 48 dims
            grid_means = []
            for r in range(4):
                for c in range(4):
                    cell = arr[r * 32 : (r + 1) * 32, c * 32 : (c + 1) * 32]
                    grid_means.extend(cell.mean(axis=(0, 1)))

            # Color histogram in RGB (4x4x4 = 64 bins)
            hist, _ = np.histogramdd(
                arr.reshape(-1, 3),
                bins=(4, 4, 4),
                range=((0, 1), (0, 1), (0, 1)),
            )
            hist_flat = hist.flatten() / (arr.shape[0] * arr.shape[1])

            # Gradient texture features
            gray = 0.2989 * arr[:, :, 0] + 0.5870 * arr[:, :, 1] + 0.1140 * arr[:, :, 2]
            dx = np.abs(gray[:, 1:] - gray[:, :-1])
            dy = np.abs(gray[1:, :] - gray[:-1, :])
            grad_feats = [float(np.mean(dx)), float(np.std(dx)), float(np.mean(dy)), float(np.std(dy))]

            combined = np.concatenate([grid_means, hist_flat, grad_feats])  # 48 + 64 + 4 = 116 dims

            # Deterministic projection to target self._dim (512 dims)
            np.random.seed(42)
            projection_matrix = np.random.randn(len(combined), self._dim).astype(np.float32)
            projected = np.dot(combined, projection_matrix)

            # L2 normalization
            norm = np.linalg.norm(projected)
            projected = projected / (norm if norm > 0 else 1.0)
            embeddings.append(projected.astype(np.float32))

        return np.array(embeddings, dtype=np.float32)


class MockTestImageEncoder(BaseImageEncoder):
    """Dedicated test encoder class for fast, deterministic unit test fixtures."""

    def __init__(self, dimension: int = config.model.embedding_dim) -> None:
        self._dim = dimension

    @property
    def embedding_dim(self) -> int:
        return self._dim

    @property
    def model_name(self) -> str:
        return f"MockTestEncoder-{self._dim}d"

    def encode_image(self, image: Image.Image) -> np.ndarray:
        return self.encode_batch([image])[0]

    def encode_batch(self, images: List[Image.Image]) -> np.ndarray:
        if not images:
            return np.empty((0, self._dim), dtype=np.float32)
        results = []
        for img in images:
            arr = np.asarray(img.convert("RGB").resize((16, 16)), dtype=np.float32).flatten()
            padded = np.zeros(self._dim, dtype=np.float32)
            padded[:min(len(arr), self._dim)] = arr[:min(len(arr), self._dim)]
            norm = np.linalg.norm(padded)
            padded = padded / (norm if norm > 0 else 1.0)
            results.append(padded)
        return np.array(results, dtype=np.float32)


# Convenience alias
ImageEncoder = OpenCLIPImageEncoder

# Singleton instance container
_GLOBAL_ENCODER: Union[BaseImageEncoder, None] = None


def get_image_encoder(allow_test_fallback: bool = False) -> BaseImageEncoder:
    """Retrieve or lazily initialize the singleton vision encoder."""
    global _GLOBAL_ENCODER
    if _GLOBAL_ENCODER is None:
        try:
            _GLOBAL_ENCODER = OpenCLIPImageEncoder(allow_test_fallback=allow_test_fallback)
        except Exception:
            if allow_test_fallback:
                _GLOBAL_ENCODER = OpenCLIPImageEncoder(allow_test_fallback=True)
            else:
                raise
    return _GLOBAL_ENCODER
