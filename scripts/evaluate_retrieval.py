"""Comprehensive evaluation script for TailorTalk multi-stage saree retrieval.

Measures visual retrieval performance (Recall@1, Recall@5, Recall@10, MRR, and nDCG@5)
against explicit ground-truth associations with strict self-retrieval exclusion.
"""

import json
import logging
import math
from pathlib import Path
import sys
import time
from typing import Any, Dict, List, Optional
import numpy as np

# Ensure repository root is on path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import config
from app.retrieval.search import SareeSearchEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("TailorTalk.Evaluation")


def load_ground_truth(manifest_path: Optional[Path] = None) -> Dict[str, Any]:
    """Load explicit query-to-relevant-IDs ground truth manifest."""
    gt_file = manifest_path or (config.storage.base_dir / "evaluation" / "ground_truth.json")
    if not gt_file.exists():
        logger.warning(f"Ground truth manifest '{gt_file}' not found.")
        return {}
    with open(gt_file, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_dcg(gains: List[float]) -> float:
    """Compute Discounted Cumulative Gain for a list of relevance scores."""
    dcg = 0.0
    for idx, gain in enumerate(gains, start=1):
        if gain > 0:
            dcg += float(gain) / math.log2(idx + 1)
    return float(dcg)


def calculate_ndcg(retrieved_items: List[Any], relevant_items: Any, k: int = 5) -> float:
    """Compute Normalized Discounted Cumulative Gain at rank K (nDCG@K)."""
    if not retrieved_items or not relevant_items:
        return 0.0

    # If numeric gains list is passed
    if isinstance(retrieved_items, list) and len(retrieved_items) > 0 and isinstance(retrieved_items[0], (int, float)):
        dcg = calculate_dcg(retrieved_items[:k])
        # Sort ideal gains descending
        ideal_gains = sorted(relevant_items if isinstance(relevant_items, list) else retrieved_items, reverse=True)[:k]
        idcg = calculate_dcg(ideal_gains)
        return float(dcg / idcg) if idcg > 0 else 0.0

    # If ID lists are passed
    rel_set = set(relevant_items)
    gains = [1.0 if item in rel_set else 0.0 for item in retrieved_items[:k]]
    dcg = calculate_dcg(gains)
    ideal_hits = min(len(relevant_items), k)
    if ideal_hits == 0:
        return 0.0
    idcg = sum(1.0 / math.log2(i + 1) for i in range(1, ideal_hits + 1))
    return float(dcg / idcg) if idcg > 0 else 0.0


def calculate_mrr(retrieved_ids: List[str], relevant_ids: Any) -> float:
    """Compute Reciprocal Rank of first relevant item."""
    rel_set = set(relevant_ids)
    for idx, item in enumerate(retrieved_ids, start=1):
        if item in rel_set:
            return 1.0 / float(idx)
    return 0.0


def calculate_recall_at_k(retrieved_ids: List[str], relevant_ids: Any, k: int = 5) -> float:
    """Compute Recall@K (fraction of relevant items retrieved in top K)."""
    rel_set = set(relevant_ids)
    if not rel_set:
        return 0.0
    retrieved_k = set(retrieved_ids[:k])
    hits = len(retrieved_k.intersection(rel_set))
    return float(hits / len(rel_set))


def evaluate_retrieval_system(top_k: int = 5) -> Dict[str, Any]:
    """Execute end-to-end evaluation across benchmark queries with self-exclusion."""
    engine = SareeSearchEngine()

    if engine.vector_store.count() == 0:
        logger.error("Vector index is empty! Please run ingestion before evaluation.")
        return {"error": "Vector index is empty"}

    ground_truth = load_ground_truth()
    if not ground_truth:
        logger.error("No ground truth queries found.")
        return {"error": "No ground truth available"}

    print("\n" + "=" * 80)
    print(" TAILORTALK: MULTI-STAGE VISUAL RETRIEVAL EVALUATION SUITE")
    print(f" Total Indexed Catalog Items: {engine.vector_store.count()}")
    print(f" Benchmark Query Set Size: {len(ground_truth)}")
    print(f" Evaluation Top-K: {top_k}")
    print(" Note: Self-retrieval is strictly excluded for every query evaluation.")
    print("=" * 80 + "\n")

    query_results = []
    recall_at_1_list = []
    recall_at_5_list = []
    recall_at_10_list = []
    reciprocal_ranks = []
    ndcg_at_5_list = []
    latencies = []
    mean_scores = []

    for idx, (query_file, query_data) in enumerate(ground_truth.items(), start=1):
        img_path = config.storage.images_dir / query_file
        if not img_path.exists():
            logger.warning(f"Query image '{img_path}' not found on disk. Skipping.")
            continue

        query_id = img_path.stem
        relevant_ids = set(query_data.get("relevant_ids", []))
        query_name = query_data.get("query_name", query_file)

        # Retrieve candidates: top_k + 1 to account for self-exclusion
        t0 = time.time()
        search_resp = engine.search(query=img_path, top_k=max(10, top_k + 1), candidate_k=30)
        elapsed_ms = (time.time() - t0) * 1000.0
        latencies.append(elapsed_ms)

        # P0-2: Self-exclusion - exclude the exact query image from candidates
        filtered_results = [
            r for r in search_resp.results
            if r.image_id != query_id and r.relative_path != query_file
        ]

        # Re-rank filtered results
        for rank_idx, r in enumerate(filtered_results, start=1):
            r.rank = rank_idx

        results = filtered_results[:top_k]
        results_10 = filtered_results[:10]

        if not results:
            continue

        retrieved_ids_5 = [r.image_id for r in results]
        retrieved_ids_10 = [r.image_id for r in results_10]

        first_relevant_rank = None
        scores_for_q = [r.score for r in results]

        print(f"Query [{idx}/{len(ground_truth)}]: {query_name} ({query_file})")
        print(f"  Target Relevant IDs: {list(relevant_ids)}")

        for r in results:
            is_relevant = r.image_id in relevant_ids
            if is_relevant and first_relevant_rank is None:
                first_relevant_rank = r.rank

            print(
                f"    Rank {r.rank}: [{r.score_percentage}] {r.image_id[:40]} "
                f"(Color: {r.breakdown.color_similarity:.2f}, Tex: {r.breakdown.texture_similarity:.2f}, Emb: {r.breakdown.embedding_similarity:.2f}) "
                f"{'✓ RELEVANT' if is_relevant else ''}"
            )

        # Metrics computation
        r1 = 1.0 if (first_relevant_rank == 1) else 0.0
        r5 = 1.0 if any(rid in relevant_ids for rid in retrieved_ids_5) else 0.0
        r10 = 1.0 if any(rid in relevant_ids for rid in retrieved_ids_10) else 0.0
        rr = (1.0 / first_relevant_rank) if first_relevant_rank else 0.0
        ndcg_5 = calculate_ndcg(retrieved_ids_5, list(relevant_ids), k=5)

        recall_at_1_list.append(r1)
        recall_at_5_list.append(r5)
        recall_at_10_list.append(r10)
        reciprocal_ranks.append(rr)
        ndcg_at_5_list.append(ndcg_5)
        mean_scores.append(float(np.mean(scores_for_q)))

        query_results.append({
            "query_name": query_name,
            "query_file": query_file,
            "recall_at_1": r1,
            "recall_at_5": r5,
            "recall_at_10": r10,
            "reciprocal_rank": round(rr, 4),
            "ndcg_at_5": round(ndcg_5, 4),
            "latency_ms": round(elapsed_ms, 2),
            "top_match_id": results[0].image_id if results else None,
            "top_match_score": results[0].score if results else 0.0,
        })
        print(f"  --> R@1: {r1:.2f} | R@5: {r5:.2f} | MRR: {rr:.2f} | nDCG@5: {ndcg_5:.2f} | Latency: {elapsed_ms:.1f}ms\n")

    # Aggregate Benchmark Metrics
    mean_r1 = float(np.mean(recall_at_1_list)) if recall_at_1_list else 0.0
    mean_r5 = float(np.mean(recall_at_5_list)) if recall_at_5_list else 0.0
    mean_r10 = float(np.mean(recall_at_10_list)) if recall_at_10_list else 0.0
    mrr = float(np.mean(reciprocal_ranks)) if reciprocal_ranks else 0.0
    mean_ndcg_5 = float(np.mean(ndcg_at_5_list)) if ndcg_at_5_list else 0.0
    avg_latency = float(np.mean(latencies)) if latencies else 0.0
    avg_similarity = float(np.mean(mean_scores)) if mean_scores else 0.0

    summary = {
        "total_queries_evaluated": len(query_results),
        "mean_reciprocal_rank_mrr": round(mrr, 4),
        "recall_at_1": round(mean_r1, 4),
        "recall_at_5": round(mean_r5, 4),
        "recall_at_10": round(mean_r10, 4),
        "ndcg_at_5": round(mean_ndcg_5, 4),
        "average_query_latency_ms": round(avg_latency, 2),
        "average_top_similarity_score": round(avg_similarity, 4),
        "detailed_queries": query_results,
    }

    print("=" * 80)
    print(" RETRIEVAL EVALUATION SUMMARY REPORT")
    print("=" * 80)
    print(f" • Recall@1:                       {mean_r1 * 100:.1f}%")
    print(f" • Recall@5:                       {mean_r5 * 100:.1f}%")
    print(f" • Recall@10:                      {mean_r10 * 100:.1f}%")
    print(f" • Mean Reciprocal Rank (MRR):     {mrr:.4f}")
    print(f" • nDCG@5:                         {mean_ndcg_5:.4f}")
    print(f" • Average Similarity Score:       {avg_similarity * 100:.1f}%")
    print(f" • Average Query Latency:          {avg_latency:.2f} ms")
    print("=" * 80 + "\n")

    # Save evaluation report
    report_file = config.storage.index_dir / "evaluation_report.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Evaluation report saved to: '{report_file}'\n")

    return summary


if __name__ == "__main__":
    evaluate_retrieval_system()
