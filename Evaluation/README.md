# Banking LLM Evaluation Framework

End-to-end evaluation framework for a banking-focused LLM assistant that answers questions on policies & regulatory guidance, with a focus on measuring answer quality and reliability.

## Overview
This project combines a simple RAG-based chatbot with automated and systematic evaluation pipelines to assess performance, factual accuracy, and robustness.

## Components

### 1. RAG Chatbot
- Retrieval-Augmented Generation over a small corpus of banking policy documents (PDF/Markdown)
- Answers user queries with grounded, document-based responses

### 2. Automated Evaluation
Evaluates responses using:
- BLEU / ROUGE / METEOR
- LLM-as-a-judge scoring
- Factuality checks
- Inter-rater agreement metrics
- Structured output validation

### 3. Bias & Robustness Analysis
Tests the assistant for:
- Position bias
- Verbosity bias
- Self-enhancement bias
- Prompt sensitivity (variation tests)

## Goal
Provide a reproducible framework to measure correctness, reliability, and consistency of LLM outputs in regulated banking scenarios.

## Status
### Done
Ingested docs
### Doing
1 -- the chatbot
### To do
2 & 3
