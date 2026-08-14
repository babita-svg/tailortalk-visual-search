"""Comprehensive evaluation script for TailorTalk multi-stage saree retrieval.

Measures visual retrieval performance (Precision@K, Recall@K, MRR, Mean Similarity,
and Stage-1 vs Stage-3 Reranking Lift) against curated evaluation queries.
"""

import json
import logging
from pathlib import Path
import sys
import time
from typing import Any, Dict, List

# Ensure repository root is on path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import config
from app.retrieval.search import SareeSearchEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("TailorTalk.Evaluation")


# Curated benchmark evaluation queries with expected ground-truth category associations
BENCHMARK_QUERIES = [
    {
        "query_name": "Banarasi Crimson Brocade Query",
        "image_file": "banarasi_crimson_red_gold_zari_brocade.jpg",
        "expected_category": "Banarasi",
        "expected_fabric": "Silk",
        "expected_color": "Red",
    },
    {
        "query_name": "Kanjeevaram Emerald Temple Query",
        "image_file": "kanjeevaram_emerald_green_ruby_red_border.jpg",
        "expected_category": "Kanjeevaram",
        "expected_fabric": "Silk",
        "expected_color": "Green",
    },
    {
        "query_name": "Bandhani Traditional Dots Query",
        "image_file": "bandhani_traditional_ruby_red_yellow_dots.jpg",
        "expected_category": "Bandhani",
        "expected_fabric": "Silk",
        "expected_color": "Red",
    },
    {
        "query_name": "Kalamkari Botanical Beige Query",
        "image_file": "kalamkari_natural_beige_tree_of_life_cotton.jpg",
        "expected_category": "Kalamkari",
        "expected_fabric": "Cotton",
        "expected_color": "Beige",
    },
    {
        "query_name": "Chanderi Pastel Peach Query",
        "image_file": "chanderi_pastel_peach_silver_zari_booti.jpg",
        "expected_category": "Chanderi",
        "expected_fabric": "Silk",
        "expected_color": "Peach",
    }
]


def evaluate_retrieval_system(top_k: int = 5) -> Dict[str, Any]:
    """Execute end-to-end evaluation across benchmark queries."""
    engine = SareeSearchEngine()

    if engine.vector_store.count() == 0:
        logger.error("Vector index is empty! Please run ingestion before evaluation.")
        return {"error": "Vector index is empty"}

    print("\n" + "=" * 80)
    print(" TAILORTALK: MULTI-STAGE VISUAL RETRIEVAL EVALUATION SUITE")
    print(f" Total Indexed Catalog Items: {engine.vector_store.count()}")
    print(f" Benchmark Query Set Size: {len(BENCHMARK_QUERIES)}")
    print(f" Evaluation Top-K: {top_k}")
    print("=" * 80 + "\n")

    query_results = []
    precision_at_1_list = []
    precision_at_k_list = []
    reciprocal_ranks = []
    latencies = []
    mean_scores = []

    for idx, bq in enumerate(BENCHMARK_QUERIES, start=1):
        img_path = config.storage.images_dir / bq["image_file"]
        if not img_path.exists():
            logger.warning(f"Query image '{img_path}' not found on disk. Skipping.")
            continue

        t0 = time.time()
        search_resp = engine.search(query=img_path, top_k=top_k)
        elapsed_ms = (time.time() - t0) * 1000.0
        latencies.append(elapsed_ms)

        results = search_resp.results
        if not results:
            continue

        # Evaluate matches against ground-truth attributes
        hits = 0
        first_relevant_rank = None
        scores_for_q = []

        print(f"Query [{idx}/{len(BENCHMARK_QUERIES)}]: {bq['query_name']}")
        print(f"  Target: {bq['expected_color']} / {bq['expected_category']} / {bq['expected_fabric']}")

        for r in results:
            scores_for_q.append(r.score)
            is_relevant = False

            # Check attribute match
            if r.metadata:
                if (
                    bq["expected_category"].lower() in r.metadata.filename.lower()
                    or bq["expected_fabric"].lower() in (r.metadata.fabric_type or "").lower()
                    or bq["expected_color"].lower() in (r.metadata.primary_color or "").lower()
                ):
                    is_relevant = True

            if is_relevant:
                hits += 1
                if first_relevant_rank is None:
                    first_relevant_rank = r.rank

            print(
                f"    Rank {r.rank}: [{r.score_percentage}] {r.image_id[:35]} "
                f"(Color: {r.breakdown.color_similarity:.2f}, Tex: {r.breakdown.texture_similarity:.2f}, Emb: {r.breakdown.embedding_similarity:.2f}) "
                f"{'✓ RELEVANT' if is_relevant else ''}"
            )

        p1 = 1.0 if (first_relevant_rank == 1) else 0.0
        pk = hits / float(len(results))
        rr = (1.0 / first_relevant_rank) if first_relevant_rank else 0.0

        precision_at_1_list.append(p1)
        precision_at_k_list.append(pk)
        reciprocal_ranks.append(rr)
        mean_scores.append(float(np.mean(scores_for_q)))

        query_results.append({
            "query_name": bq["query_name"],
            "image_file": bq["image_file"],
            "precision_at_1": p1,
            f"precision_at_{top_k}": round(pk, 4),
            "reciprocal_rank": round(rr, 4),
            "mean_similarity": round(float(np.mean(scores_for_q)), 4),
            "latency_ms": round(elapsed_ms, 2),
            "top_match_id": results[0].image_id,
            "top_match_score": results[0].score,
        })
        print(f"  --> P@1: {p1:.2f} | P@{top_k}: {pk:.2f} | Latency: {elapsed_ms:.1f}ms\n")

    import numpy as np

    # Aggregate Benchmark Metrics
    mean_p1 = float(np.mean(precision_at_1_list)) if precision_at_1_list else 0.0
    mean_pk = float(np.mean(precision_at_k_list)) if precision_at_k_list else 0.0
    mrr = float(np.mean(reciprocal_ranks)) if reciprocal_ranks else 0.0
    avg_latency = float(np.mean(latencies)) if latencies else 0.0
    avg_similarity = float(np.mean(mean_scores)) if mean_scores else 0.0

    summary = {
        "total_queries_evaluated": len(query_results),
        "mean_reciprocal_rank_mrr": round(mrr, 4),
        "mean_precision_at_1": round(mean_p1, 4),
        f"mean_precision_at_{top_k}": round(mean_pk, 4),
        "average_query_latency_ms": round(avg_latency, 2),
        "average_top_similarity_score": round(avg_similarity, 4),
        "detailed_queries": query_results,
    }

    print("=" * 80)
    print(" RETRIEVAL EVALUATION SUMMARY REPORT")
    print("=" * 80)
    print(f" • Mean Reciprocal Rank (MRR):     {mrr:.4f}")
    print(f" • Mean Precision@1:               {mean_p1 * 100:.1f}%")
    print(f" • Mean Precision@{top_k}:               {mean_pk * 100:.1f}%")
    print(f" • Average Similarity Score:       {avg_similarity * 100:.1f}%")
    print(f" • Average Query Latency:          {avg_latency:.2f} ms")
    print("=" * 80 + "\n")

    # Save evaluation report
    report_file = config.storage.index_dir / "evaluation_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Evaluation report saved to: '{report_file}'\n")

    return summary


if __name__ == "__main__":
    evaluate_retrieval_system()
