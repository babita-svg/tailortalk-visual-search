# TailorTalk — Fine-Grained Visual Saree Similarity Search & Conversational Stylist

TailorTalk is an intelligent visual retrieval and conversational fashion styling system designed for Indian sarees. It combines deep vision models, vector similarity indexing, and multi-signal reranking with an LLM-powered agent to deliver accurate visual recommendations based on weave texture, color harmony, zari patterns, and border motifs.

---

## Architecture Overview

```
                                  [ User Input ]
                         (Image Upload / URL / Text Query)
                                        │
                                        ▼
                           ┌─────────────────────────┐
                           │   Input Sanitization    │
                           │     & Validation        │
                           └────────────┬────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    ▼                                       ▼
         [ Visual Similarity Search ]               [ Conversational Agent ]
                    │                                       │
        ┌───────────┴───────────┐                           │
        ▼                       ▼                           │
  [ OpenCLIP ViT ]      [ Visual Feature Engine ]           │
  (512-dim Vector)     (HSV, Texture, Composition)          │
        │                       │                           │
        ▼                       │                           │
 ┌──────────────┐               │                           │
 │ FAISS Index  │               │                           │
 │ (Stage-1 IP) │               │                           │
 └──────┬───────┘               │                           │
        │ Candidate IDs         │                           │
        ▼                       ▼                           │
 ┌──────────────────────────────────────┐                   │
 │       Stage-2 Fine-Grained           │                   │
 │             Reranker                 │                   │
 └──────────────────┬───────────────────┘                   │
                    │ Ranked Matches & Similarity           │
                    ▼                                       │
         [ Structured Response ] ◄──────────────────────────┘
                    │            (Tool Invocation & Reasoning)
                    ▼
         [ Web / Streamlit UI ]
```

---

## Key Features

1. **Multi-Stage Retrieval Engine**:
   - **Stage 1 (High-Recall Candidate Retrieval)**: Generates 512-dimensional L2-normalized embeddings via OpenCLIP (ViT-B-32) and performs inner-product cosine search in FAISS (`IndexFlatIP`).
   - **Stage 2 (Fine-Grained Visual Reranking)**: Scores candidates using a weighted multi-signal visual metric:
     $$\text{Score} = w_{\text{emb}} \cdot S_{\text{emb}} + w_{\text{col}} \cdot S_{\text{col}} + w_{\text{tex}} \cdot S_{\text{tex}} + w_{\text{comp}} \cdot S_{\text{comp}}$$
     - **Color Distribution ($S_{\text{col}}$)**: Multi-channel HSV/Lab color histograms with Bhattacharyya distance.
     - **Weave Texture ($S_{\text{tex}}$)**: High-frequency Sobel gradient magnitude profiles capturing fine zari and jacquard weaves.
     - **Spatial Composition ($S_{\text{comp}}$)**: $3 \times 3$ sub-region grid layout matching pallu, body, and border placements.

2. **Conversational Stylist Agent**:
   - Genuine function/tool-calling architecture via `VisualSareeSimilaritySearchTool`.
   - Distinguishes conversational styling questions from visual search requests.
   - Provides comparative analysis explaining similarities in weave, fabric, and zari work.

3. **Production Web Interface**:
   - Live visual search with instant preview, extracted dominant color palette chips, and score breakdowns.
   - Sample query gallery for immediate evaluation across authentic saree categories (Banarasi, Kanjeevaram, Chanderi, Bandhani, Kalamkari, Patola, Paithani, Tussar, Organza).
   - Real-time conversational interface with interactive chat.

4. **Security & Validation**:
   - Strict image dimension, size (max 10MB), and format validation (JPEG, PNG, WEBP).
   - URL scheme validation with SSRF safeguards.
   - Path traversal prevention.

---

## Directory Structure

```
├── app/
│   ├── agent/                 # Conversational agent & tool definitions
│   │   ├── agent.py           # Core agent orchestrator
│   │   ├── prompts.py         # System and styling prompt templates
│   │   └── tools.py           # Visual similarity search tool definition
│   ├── embeddings/            # Vision embedding extractors
│   │   └── image_encoder.py   # OpenCLIP ViT-B-32 embedding encoder
│   ├── image_utils/           # Image validation, security, and loading
│   │   ├── loader.py          # Robust image loader (file, bytes, URL)
│   │   └── validation.py      # Format, dimension, and URL validator
│   ├── ingestion/             # Catalog discovery, metadata & indexing
│   │   ├── metadata.py        # Color palette & attribute extraction
│   │   └── pipeline.py        # End-to-end ingestion pipeline
│   ├── retrieval/             # Multi-stage retrieval and reranking
│   │   ├── reranker.py        # Fine-grained multi-signal reranker
│   │   ├── search.py          # SareeSearchEngine orchestrator
│   │   └── vector_store.py    # FAISS vector store & persistence
│   ├── config.py              # Centralized configuration dataclasses
│   ├── exceptions.py          # Domain-specific exception hierarchy
│   └── schemas.py             # Pydantic data contracts and models
├── data/
│   ├── images/                # High-resolution authentic saree dataset
│   └── index/                 # FAISS binary index & metadata JSON
├── scripts/
│   ├── build_index.py         # CLI tool to build/rebuild vector index
│   └── evaluate_retrieval.py  # Precision, MRR, and latency evaluation suite
├── tests/                     # Unit and integration test suite
├── ui/
│   └── streamlit_app.py       # Streamlit web application
├── src/                       # React frontend application
├── server.ts                  # Express server & API routes
└── requirements.txt           # Python dependencies
```

---

## Getting Started

### 1. Installation

Install Python dependencies:

```bash
pip install -r requirements.txt
```

### 2. Build the Visual Vector Index

Index the saree dataset into the FAISS vector database:

```bash
python scripts/build_index.py
```

### 3. Run the Streamlit Application

```bash
streamlit run app.py
```

### 4. Run the Full-Stack Web Application

```bash
npm run build
node dist/server.cjs
```

---

## Evaluation & Benchmarking

Execute the evaluation benchmark across curated query sets:

```bash
python scripts/evaluate_retrieval.py
```

Metrics evaluated:
- **Precision@1 & Precision@K**: Correct fabric/weave category alignment.
- **Mean Reciprocal Rank (MRR)**: Retrieval ranking quality.
- **Query Latency (ms)**: End-to-end inference and reranking time.
- **Similarity Breakdown**: Contribution of CLIP embeddings vs. fine-grained visual signals.

---

## License

MIT License.
