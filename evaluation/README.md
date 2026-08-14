# TailorTalk Visual Retrieval Evaluation Framework

## Overview
This evaluation suite benchmarks the performance of TailorTalk's multi-stage visual retrieval architecture across curated query sarees and catalog items.

## Methodology & Invariants

1. **Leave-One-Out Evaluation (Self-Retrieval Exclusion)**:
   When evaluating a catalog image as a query, the exact query image is strictly excluded from its own candidate result set before calculating ranking metrics (Recall@K, MRR, nDCG@5). This guarantees that self-matches do not artificially inflate benchmark scores.

2. **Explicit Ground-Truth Manifest (`ground_truth.json`)**:
   Relevance is determined via manually curated visual relevance associations between queries and catalogue IDs, rather than heuristic filename keyword matching.

3. **Metrics Evaluated**:
   - **Recall@1**: Proportion of queries where a relevant catalog item is ranked at position 1.
   - **Recall@5**: Proportion of queries where at least one relevant catalog item is found within the top 5 results.
   - **Recall@10**: Proportion of queries where at least one relevant catalog item is found within the top 10 results.
   - **MRR (Mean Reciprocal Rank)**: The average of reciprocal ranks of the first relevant item retrieved.
   - **nDCG@5 (Normalized Discounted Cumulative Gain at 5)**: Position-discounted ranking quality metric evaluating whether relevant items appear near the top of the ranked list.

4. **Limitations**:
   - Current sample catalog size is 20 diverse Indian saree handlooms.
   - Visual similarity is multi-faceted (color harmony, weave texture, spatial layout). As the catalogue expands, ground-truth annotations can be scaled accordingly.
