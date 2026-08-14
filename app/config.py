"""Application configuration for TailorTalk.

Defines all paths, model identifiers, retrieval parameters, reranking weights,
and server settings with environment variable override capabilities.
"""

from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import Dict, List, Tuple
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass
class ModelConfig:
    """Vision embedding model configuration."""

    # Default OpenCLIP model: ViT-B-32 with OpenAI pretrained weights
    # Fast inference (30ms on CPU), 512-dim normalized vectors, high visual semantic alignment
    model_name: str = os.getenv("EMBEDDING_MODEL_NAME", "ViT-B-32")
    pretrained: str = os.getenv("EMBEDDING_MODEL_PRETRAINED", "openai")
    embedding_dim: int = int(os.getenv("EMBEDDING_DIM", "512"))
    batch_size: int = int(os.getenv("EMBEDDING_BATCH_SIZE", "16"))
    device: str = os.getenv("MODEL_DEVICE", "cpu")
    cache_dir: Path = BASE_DIR / "data" / "models"


@dataclass
class StorageConfig:
    """Data paths and vector index storage configuration."""

    base_dir: Path = BASE_DIR
    images_dir: Path = BASE_DIR / "data" / "images"
    index_dir: Path = BASE_DIR / "data" / "index"
    faiss_index_file: Path = BASE_DIR / "data" / "index" / "saree_faiss.index"
    metadata_file: Path = BASE_DIR / "data" / "index" / "saree_metadata.json"
    supported_extensions: Tuple[str, ...] = (".jpg", ".jpeg", ".png", ".webp")
    max_upload_size_mb: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
    url_request_timeout_seconds: int = int(os.getenv("URL_REQUEST_TIMEOUT", "8"))


@dataclass
class RetrievalConfig:
    """Multi-stage retrieval and reranking configuration."""

    # Stage 1: Initial candidate retrieval size
    candidate_top_k: int = int(os.getenv("CANDIDATE_TOP_K", "30"))
    
    # Final top-k results returned to agent / UI
    default_top_k: int = int(os.getenv("DEFAULT_TOP_K", "6"))
    max_top_k: int = int(os.getenv("MAX_TOP_K", "20"))
    
    # Distance metric: 'cosine' (FAISS Inner Product on L2-normalized embeddings)
    distance_metric: str = "cosine"
    
    # Fine-grained Reranking Weights (Sum must equal 1.0)
    # 1. Base semantic/visual embedding similarity: captures overall category, drape, style
    weight_embedding: float = float(os.getenv("WEIGHT_EMBEDDING", "0.50"))
    # 2. Color harmony & dominant hue distribution (HSV/Lab histogram intersection)
    weight_color: float = float(os.getenv("WEIGHT_COLOR", "0.25"))
    # 3. Spatial texture and high-frequency weave pattern density (Sobel/Laplacian gradient energy)
    weight_texture: float = float(os.getenv("WEIGHT_TEXTURE", "0.15"))
    # 4. Structural border & pallu layout correlation (Upper/Lower/Side zone distributions)
    weight_composition: float = float(os.getenv("WEIGHT_COMPOSITION", "0.10"))


@dataclass
class AgentConfig:
    """Agent and LLM configuration."""

    agent_name: str = "TailorTalk Assistant"
    # Optional Gemini / OpenAI API key if available; system functions fully with deterministic CV pipeline
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    model_name: str = os.getenv("AGENT_MODEL_NAME", "gemini-2.5-flash")
    temperature: float = 0.2


@dataclass
class AppConfig:
    """Master application configuration aggregating all components."""

    model: ModelConfig = field(default_factory=ModelConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    retrieval: RetrievalConfig = field(default_factory=RetrievalConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)

    def ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        self.storage.images_dir.mkdir(parents=True, exist_ok=True)
        self.storage.index_dir.mkdir(parents=True, exist_ok=True)
        self.model.cache_dir.mkdir(parents=True, exist_ok=True)


config = AppConfig()
config.ensure_directories()
