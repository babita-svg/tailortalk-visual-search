"""Vision embedding encoder module.

Generates normalized high-dimensional visual embeddings using OpenCLIP / Vision Transformers.
Embeddings are L2-normalized to ensure that cosine similarity directly corresponds to dot product.
"""

from abc import ABC, abstractmethod
import logging
from typing import List, Union
import numpy as np
from PIL import Image
import torch

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
    ) -> None:
        self._model_name = model_name
        self._pretrained = pretrained
        self._device = torch.device(device if torch.cuda.is_available() and device == "cuda" else "cpu")
        self._model = None
        self._preprocess = None
        self._dim = config.model.embedding_dim
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
            logger.warning(
                f"Failed to load OpenCLIP weights ({str(e)}). Falling back to deterministic feature extractor."
            )
            self._model = None

    @property
    def embedding_dim(self) -> int:
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
                tensors = [self._preprocess(img.convert("RGB")) for img in images]
                batch_tensor = torch.stack(tensors).to(self._device)

                with torch.no_grad():
                    features = self._model.encode_image(batch_tensor)
                    # Convert to CPU numpy
                    features_np = features.cpu().numpy().astype(np.float32)

                # Explicit L2 normalization: vector / ||vector||_2
                norms = np.linalg.norm(features_np, axis=1, keepdims=True)
                norms = np.where(norms == 0, 1.0, norms)
                normalized_features = features_np / norms
                return normalized_features.astype(np.float32)
            except Exception as e:
                logger.error(f"Error during OpenCLIP batch encoding: {str(e)}")
                raise EmbeddingGenerationError(f"OpenCLIP inference failed: {str(e)}") from e

        # Fallback deterministic visual encoder (used if model weight download is offline)
        return self._fallback_encode_batch(images)

    def _fallback_encode_batch(self, images: List[Image.Image]) -> np.ndarray:
        """Multi-frequency spatial color and texture encoder for testing or offline environments."""
        embeddings = []
        for img in images:
            rgb = img.convert("RGB").resize((128, 128), Image.Resampling.BILINEAR)
            arr = np.asarray(rgb, dtype=np.float32) / 255.0  # (128, 128, 3)

            # Spatial 4x4 grid color means and stds (16 * 6 = 96 dims)
            grid_feats = []
            for r in range(4):
                for c in range(4):
                    cell = arr[r * 32 : (r + 1) * 32, c * 32 : (c + 1) * 32]
                    grid_feats.extend(cell.mean(axis=(0, 1)))
                    grid_feats.extend(cell.std(axis=(0, 1)))

            # Color histogram in RGB (8x8x8 = 512 bins or truncated to target dim)
            hist, _ = np.histogramdd(arr.reshape(-1, 3), bins=(8, 8, 8), range=((0, 1), (0, 1), (0, 1)))
            hist_feat = hist.flatten()[: (self._dim - len(grid_feats))]

            combined = np.concatenate([grid_feats, hist_feat])
            if len(combined) < self._dim:
                combined = np.pad(combined, (0, self._dim - len(combined)))
            elif len(combined) > self._dim:
                combined = combined[: self._dim]

            norm = np.linalg.norm(combined)
            norm = 1.0 if norm == 0 else norm
            embeddings.append(combined / norm)

        return np.array(embeddings, dtype=np.float32)


# Singleton instance container
_GLOBAL_ENCODER: Union[BaseImageEncoder, None] = None


def get_image_encoder() -> BaseImageEncoder:
    """Retrieve or lazily initialize the singleton vision encoder."""
    global _GLOBAL_ENCODER
    if _GLOBAL_ENCODER is None:
        _GLOBAL_ENCODER = OpenCLIPImageEncoder()
    return _GLOBAL_ENCODER
