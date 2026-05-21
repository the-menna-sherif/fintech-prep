````markdown
# Earnings Intelligence Engine

A hybrid financial search system that ingests public company earnings filings, extracts structured data, and answers natural language queries using both SQL and vector search.

---

## Overview

This project covers two core competencies for AI engineering in fintech:

- **Financial data processing** — pulling, parsing, and structuring SEC filings (10-Q/10-K) into queryable formats
- **Retrieval and search systems** — building a hybrid retrieval pipeline (dense + sparse) with a query router that decides whether a question needs SQL, vector search, or both

---

## Architecture

```
User Query
    │
    ▼
Query Router (classifier)
    ├── Structured? ──► Postgres (SQL) ──────────┐
    └── Semantic?  ──► Qdrant (vector + BM25) ───┤
                                                  ▼
                                           Answer synthesis
                                          (Anthropic API)
```

---

## Directory Structure

High level structure, subject to change.

```
earnings-intelligence-engine/
│
├── data/
│   ├── raw/                    # Downloaded SEC filings (.htm, .xml)
│   └── processed/              # Cleaned text chunks + extracted tables
│
├── ingestion/
│   ├── sec_downloader.py       # Pulls filings via sec-edgar-downloader
│   ├── parser.py               # Extracts text + tables (pdfplumber / unstructured)
│   ├── chunker.py              # Splits text into embed-ready chunks
│   └── embedder.py             # Embeds chunks and upserts to Qdrant
│
├── storage/
│   ├── postgres/
│   │   ├── schema.sql          # Tables: companies, filings, financials
│   │   └── loader.py           # Inserts structured numeric data
│   └── qdrant/
│       └── client.py           # Vector DB setup and upsert helpers
│
├── retrieval/
│   ├── router.py               # Classifies query → sql / vector / hybrid
│   ├── sql_retriever.py        # Generates + runs SQL for numeric questions
│   ├── vector_retriever.py     # Dense + sparse (BM25) hybrid search
│   └── reranker.py             # Optional cross-encoder reranking step
│
├── pipeline/
│   └── query_pipeline.py       # Orchestrates router → retrieval → synthesis
│
├── eval/
│   ├── eval_set.json           # Ground-truth Q&A pairs for scoring
│   ├── run_eval.py             # Computes recall@k, faithfulness (RAGAS)
│   └── results/                # Eval output logs
│
├── api/
│   └── main.py                 # FastAPI endpoint: POST /query
│
├── notebooks/
│   ├── 01_ingestion_demo.ipynb
│   ├── 02_retrieval_experiments.ipynb
│   └── 03_eval_results.ipynb
│
├── docker-compose.yml          # Spins up Qdrant + Postgres locally
├── requirements.txt
├── .env.example                # ANTHROPIC_API_KEY, DB_URL, etc.
└── README.md
```

---

## Stack

| Layer | Tool |
|---|---|
| Filing ingestion | `sec-edgar-downloader` |
| Parsing | `pdfplumber`, `unstructured` |
| Embeddings | Anthropic / OpenAI embeddings |
| Vector DB | Qdrant (local Docker) |
| Relational DB | Postgres |
| Orchestration | Anthropic SDK or LangChain |
| API | FastAPI |
| Evaluation | RAGAS + custom eval harness |

---

## Scope (1–2 weeks)

1. **Week 1** — Ingestion pipeline end-to-end: download → parse → embed → store (5 tickers, 10-Q only)
2. **Week 2** — Query router + retrieval + FastAPI endpoint + eval harness with results

---

## Example Queries

- *"What was Apple's gross margin in Q3 2024?"* → SQL
- *"What risks did management flag around interest rates?"* → vector search
- *"How did revenue growth compare to guidance?"* → hybrid