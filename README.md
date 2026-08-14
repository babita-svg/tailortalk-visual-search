# TailorTalk Visual Search

## 1. Overview

TailorTalk is a fine-grained visual search and conversational styling system tailored for Indian sarees. Given a query image or image URL, TailorTalk retrieves visually and stylistically harmonious sarees from a structured catalog using a multi-stage pipeline: semantic embedding retrieval followed by fine-grained visual reranking based on color distributions, weave textures, and spatial composition. It also provides an agentic tool-calling conversational assistant to answer drape, occasion, and textile styling questions.

## 2. Key Capabilities

- **Visual Similarity Search**: Dual-stage retrieval matching query images against catalog inventory using normalized OpenCLIP visual vectors and fine-grained visual signals.
- **Fine-Grained Visual Reranking**: Composite scoring combining semantic embeddings, HSV color histograms, gradient-based texture statistics, and 3x3 spatial composition similarity.
- **Conversational Styling Agent**: LLM agent with structured tool-calling (`VisualSareeSimilaritySearchTool`) that distinguishes styling advice queries from visual similarity searches.
- **Defensive Ingestion & SSRF Protection**: Comprehensive input validation blocking private RFC 1918 IPs, loopbacks, link-local metadata endpoints, path traversals, and oversized payloads.
- **Quantitative Retrieval Benchmark**: Automated evaluation framework computing Recall@1, Recall@5, Recall@10, MRR, and nDCG@5 with self-retrieval exclusion.

## 3. Architecture

```
User Input (Image Upload / URL / Text)
  │
  ▼
Input Sanitization & SSRF Defense
  │
  ├─────────────────────────────────────────────┐
  ▼                                             ▼
Visual Similarity Search Engine           Conversational Agent
  │                                             │
  ├───────────────────────┐                     │ Function Calling
  ▼                       ▼                     │
OpenCLIP ViT-B/32   Visual Feature Engine       │
(512-dim Embedding) (HSV, Texture, 3x3 Grid)    │
  │                       │                     │
  ▼                       │                     │
FAISS IndexFlatIP         │                     │
(Stage-1 Candidate Top-K) │                     │
  │                       │                     │
  └───────────┬───────────┘                     │
              ▼                                 │
     Stage-2 Fine-Grained                       │
           Reranker                             │
              │                                 │
              ▼                                 │
      Ranked Results & Similarity ──────────────┘
              │
              ▼
    Streamlit Web Application (ui/streamlit_app.py)
```

## 4. Retrieval Pipeline

1. **Stage 1 — Semantic Embedding Retrieval**:
   - Query image is preprocessed and encoded into a 512-dimensional unit-normalized vector using OpenCLIP (`ViT-B-32` trained on `laion2b_s34b_b79k`).
   - FAISS `IndexFlatIP` performs fast inner-product search (cosine similarity on L2-normalized vectors) across catalog embeddings to retrieve the top `candidate_k` candidates (default: 20-50).

2. **Stage 2 — Fine-Grained Visual Reranking**:
   - Computes weighted multi-signal similarity scores over the candidate set:
     $$\text{Score} = w_{\text{emb}} \cdot S_{\text{emb}} + w_{\text{col}} \cdot S_{\text{col}} + w_{\text{tex}} \cdot S_{\text{tex}} + w_{\text{comp}} \cdot S_{\text{comp}}$$
   - Normalizes scores into a deterministic 0–100 visual similarity metric and generates grounded visual explanations.

## 5. Fine-Grained Similarity Signals

- **Embedding Similarity ($S_{\text{emb}}$)**: Cosine similarity between 512-dimensional OpenCLIP visual embeddings.
- **Color Similarity ($S_{\text{col}}$)**: 3D HSV histogram correlation and dominant RGB color proximity across hue, saturation, and value distributions.
- **Texture Similarity ($S_{\text{tex}}$)**: Gradient-based texture statistics across horizontal and vertical image intensity variations measuring local surface texture structure.
- **Spatial Composition ($S_{\text{comp}}$)**: $3 \times 3$ spatial grid color layout matching comparing corresponding image regions.

## 6. Agent / Tool Architecture

- The system implements an agent orchestrator with declared tool schemas (`VisualSareeSimilaritySearchTool`).
- When a user provides an image or requests visual matching, the agent invokes the tool with `image_reference`, `top_k`, and `candidate_k`.
- Tool responses return structured `SearchResponse` objects containing similarity breakdowns, fabric metadata, and grounded visual reasoning.
- Non-search styling queries (e.g., blouse pairing, draping techniques, jewellery selection) are answered directly using fashion domain system prompts.

## 7. Dataset / Catalogue

- **Authoritative Catalogue Source**: `data/byrappa_tejas_31july.csv` contains the 83 handloom saree catalogue records supplied by the assignment package.
- **Fields Preserved**: `Name`, `SKU`, `Stock`, `Retail Price`, `Discounted Price`, `image_url`, and `Website Link`.
- **Integrity**: Attribute values strictly match the CSV source. Missing or unspecified attributes are handled transparently as `Unknown` without synthetic fabrication.
- **Catalogue Verification**: Run `python3 scripts/verify_catalog.py` to validate row counts, SKU uniqueness, URL formatting, and pricing integrity.

## 8. Evaluation

The evaluation suite (`scripts/evaluate_retrieval.py`) benchmarks retrieval precision against ground-truth query-target pairs (`evaluation/ground_truth.json`).

- **Query Set**: Curated representative queries across distinct textile categories.
- **Self-Retrieval Exclusion**: Query images are explicitly removed from retrieved candidate sets to prevent trivial 1.0 matches.
- **Metrics**: Recall@1, Recall@5, Recall@10, Mean Reciprocal Rank (MRR), and nDCG@5.

## 9. Security

- **SSRF Defense**: Validates URL schemes (`http`, `https`), enforces timeouts (10s), and resolves hostnames to reject private networks (RFC 1918), loopbacks (`127.0.0.0/8`, `::1`), link-local metadata endpoints (`169.254.169.254`), and broadcast addresses.
- **Payload Limits**: Enforces 10 MB maximum image file size and 25,000,000 maximum pixel limit to prevent decompression bombs.
- **Path Traversal Protection**: Ensures file paths resolve within authorized directory boundaries.

## 10. Testing

Test suite organized under `tests/`:
- `test_embeddings.py`: OpenCLIP encoding, unit L2 normalization, dimension guarantees.
- `test_vector_store.py`: FAISS vector store indexing, deduplication, search, and persistence.
- `test_reranker.py`: Color histograms, gradient-based texture statistics, 3x3 spatial grid composition, and composite scoring.
- `test_search.py`: End-to-end `SareeSearchEngine` retrieval flows.
- `test_image_utils.py` & `test_security.py`: Image loading, SSRF prevention, IP validation, dimension bounds.
- `test_agent.py` & `test_agent_tools.py`: Tool calling, conversational routing, prompt formatting.
- `test_evaluation.py`: Mathematical metrics (DCG, nDCG, MRR, Recall@K).
- `test_ingestion.py`: Metadata extraction, color palette analysis, attribute heuristics.

## 11. Installation

```bash
# Install Python dependencies
pip install -r requirements.txt
```

## 12. Configuration

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

Available environment variables:
- `GEMINI_API_KEY`: Optional API key for conversational agent capabilities (graceful fallback included).
- `DEVICE`: Processing device (`cpu` or `cuda`, default: `cpu`).
- `DATASET_DIR`: Path to saree image dataset directory (default: `data/images`).
- `INDEX_DIR`: Path to vector store index directory (default: `data/index`).

## 13. Build Index

Index catalog images into FAISS binary index and metadata cache:

```bash
python scripts/build_index.py
```

## 14. Run Application

To launch the Streamlit web application on port 3000:

```bash
streamlit run app.py --server.port=3000 --server.address=0.0.0.0
```

## 15. Production Deployment (Render)

TailorTalk is configured for single-click deployment on **Render** as a Python Web Service.

### Quick Setup Steps
1. Push repository to GitHub: `babita-svg/tailortalk-visual-search`
2. In the Render Dashboard, select **New +** → **Web Service**
3. Connect the GitHub repository
4. Set configurations:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true`
5. Click **Deploy Web Service**

Alternatively, Render automatically detects the root `render.yaml` Blueprint specification.

## 16. Run Tests

Execute the unit and integration test suite:

```bash
pytest
```

## 17. Run Evaluation

Run the quantitative retrieval evaluation benchmark:

```bash
python scripts/evaluate_retrieval.py
```

## 18. Project Structure

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
│   │   └── validation.py      # Format, dimension, and SSRF validator
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
│   ├── images/                # Saree image catalogue
│   └── index/                 # FAISS binary index & metadata JSON
├── evaluation/
│   ├── ground_truth.json      # Ground truth query-relevance benchmark
│   └── README.md              # Evaluation methodology and metrics guide
├── scripts/
│   ├── build_index.py         # CLI tool to build/rebuild vector index
│   ├── evaluate_retrieval.py  # Precision, MRR, and nDCG evaluation suite
│   └── generate_sample_sarees.py # Catalog generator
├── tests/                     # Unit and integration test suite
├── ui/
│   └── streamlit_app.py       # Streamlit web application
└── requirements.txt           # Python dependencies
```

## 18. Limitations

- **Model Scale**: Currently runs OpenCLIP `ViT-B-32` on CPU/GPU. Larger backbones (`ViT-L-14`) offer higher textile fine-grain sensitivity but require greater GPU VRAM.
- **Lighting & Angle Sensitivity**: Extreme shadows or angled flat-lays may skew spatial composition matching ($S_{\text{comp}}$).
- **Metadata Availability**: Visual attributes not present in the catalog schema are classified as `Unknown` rather than synthetically guessed.

## 19. Future Improvements

- Incorporate dedicated textile segmentation masks to isolate the pallu and border prior to spatial grid calculation.
- Support multi-modal text + image hybrid queries (e.g., "Find this Kanjeevaram design in emerald green").
- Add batch vector search optimization for catalogs exceeding 100,000 SKU items.

---

## License

MIT License.
