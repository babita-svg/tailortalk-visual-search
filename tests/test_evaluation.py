"""Unit tests for retrieval evaluation metrics and benchmark harness."""

import json
from pathlib import Path
import pytest

from scripts.evaluate_retrieval import (
    calculate_dcg,
    calculate_ndcg,
    calculate_mrr,
    calculate_recall_at_k,
    evaluate_retrieval_system,
)
from app.embeddings.image_encoder import MockTestImageEncoder
from app.retrieval.reranker import FineGrainedSareeReranker
from app.retrieval.search import SareeSearchEngine
from app.retrieval.vector_store import FAISSVectorStore


def test_calculate_dcg():
    """Test Discounted Cumulative Gain computation."""
    gains = [3, 2, 1, 0, 0]
    dcg = calculate_dcg(gains)
    assert dcg > 0.0
    # Gain 0 should yield 0
    assert calculate_dcg([0, 0, 0]) == 0.0


def test_calculate_ndcg():
    """Test Normalized Discounted Cumulative Gain metric."""
    # Perfect ranking
    ranked_relevant = [3, 2, 1, 0]
    ideal_relevant = [3, 2, 1, 0]
    ndcg = calculate_ndcg(ranked_relevant, ideal_relevant, k=4)
    assert pytest.approx(ndcg, 0.001) == 1.0

    # Non-perfect ranking
    suboptimal = [0, 1, 2, 3]
    ndcg_sub = calculate_ndcg(suboptimal, ideal_relevant, k=4)
    assert 0.0 <= ndcg_sub < 1.0

    # Empty
    assert calculate_ndcg([], [], k=5) == 0.0


def test_calculate_mrr():
    """Test Mean Reciprocal Rank metric."""
    # First item is relevant
    assert calculate_mrr(["a", "b", "c"], {"a"}) == 1.0

    # Second item is relevant
    assert pytest.approx(calculate_mrr(["x", "a", "c"], {"a"}), 0.01) == 0.5

    # Third item is relevant
    assert pytest.approx(calculate_mrr(["x", "y", "a"], {"a"}), 0.01) == 0.3333

    # No relevant item
    assert calculate_mrr(["x", "y", "z"], {"a"}) == 0.0


def test_calculate_recall_at_k():
    """Test Recall@K calculation."""
    retrieved = ["a", "b", "c", "d", "e"]
    relevant = {"a", "b", "x", "y"}

    # k=2: retrieved {"a", "b"}, 2 out of 4 relevant -> 0.5
    assert pytest.approx(calculate_recall_at_k(retrieved, relevant, k=2), 0.01) == 0.5

    # k=5: retrieved {"a", "b"}, 2 out of 4 relevant -> 0.5
    assert pytest.approx(calculate_recall_at_k(retrieved, relevant, k=5), 0.01) == 0.5

    # Empty relevant set
    assert calculate_recall_at_k(retrieved, set(), k=5) == 0.0
