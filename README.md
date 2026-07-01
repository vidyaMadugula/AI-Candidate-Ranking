# 🎯 SignalRank AI: Explainable Candidate Ranking System

## Overview

SignalRank AI is an explainable AI-powered candidate ranking system designed to emulate the decision-making process of experienced recruiters.

Instead of relying solely on keyword matching, the system combines semantic retrieval, lexical retrieval, behavioral intelligence, career analysis, profile quality signals, and anomaly detection to identify the strongest candidates for a given role.

Developed for the **Redrob Hiring Intelligence Challenge**, the system is designed to rank candidates at scale while remaining fully explainable and reproducible.

---

## 🚀 Key Features

* Hybrid Retrieval (FAISS + BM25)
* Semantic Candidate Matching
* Career Intelligence Scoring
* Behavioral Signal Scoring
* Profile Quality Assessment
* Mandatory Skill Penalties
* Honeypot Candidate Detection
* Diversity Re-ranking
* Explainable Rankings
* Dynamic Skill Vocabulary Generation
* CPU-Optimized Inference
* End-to-End Reproducible Pipeline

---

## 🏗️ System Architecture

```text
Candidates (.jsonl)
        │
        ▼
Feature Engineering
        │
        ▼
Candidate Text Builder
        │
        ▼
Sentence Embeddings
(all-MiniLM-L6-v2)
        │
        ├──────────────┐
        ▼              ▼
FAISS Retrieval     BM25 Retrieval
        │              │
        └──────┬───────┘
               ▼
        Hybrid Retrieval
               ▼
        Hybrid Scoring
               │
               ├─ Semantic Similarity
               ├─ Skill Matching
               ├─ Experience Alignment
               ├─ Behavioral Signals
               ├─ Career Intelligence
               ├─ Profile Quality
               ├─ Mandatory Skill Penalties
               └─ Honeypot Detection
               ▼
      Diversity Re-ranking
               ▼
       Explainability Layer
               ▼
       Top Ranked Candidates
```

---

## 📂 Repository Structure

```text
Recruiter-AI/
│
├── app.py
├── rank.py
├── preprocess.py
├── build_index.py
├── create_sample.py
├── requirements.txt
├── README.md
├── submission_metadata.yaml
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample_candidates.jsonl
│
├── src/
│   ├── preprocessing/
│   ├── embeddings/
│   ├── retrieval/
│   ├── scoring/
│   ├── explainability/
│   ├── validation/
│   └── reranking/
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/vidyaMadugula/AI-Candidate-Ranking.git
cd recruiter-ai
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate environment:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / Mac**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔧 Preprocessing Pipeline

Generate candidate features and embeddings:

```bash
python preprocess.py
```

Build the FAISS index:

```bash
python build_index.py
```

Preprocessing is performed once and stored locally for fast inference.

---

## 🏆 Running the Ranking Pipeline

Generate ranked candidates:

```bash
python rank.py --candidates ./candidates.jsonl --out ./submission.csv
```

The command produces:

```text
submission.csv
```

containing:

```text
candidate_id,rank,score,reasoning
```

---

## 🖥️ Live Demo

A lightweight Streamlit application demonstrates the ranking pipeline on a curated sample dataset derived from the full candidate pool.

The application ranks candidates end-to-end and displays the Top candidates with detailed explainability.

Run locally:

```bash
streamlit run app.py
```

The demo:

* Loads a sample candidate dataset
* Runs the ranking pipeline end-to-end
* Displays ranked candidates
* Shows explainable recommendations
* Allows CSV export

---

## 🧠 Methodology

The ranking score combines multiple independent signals.

### 1. Hybrid Retrieval

Candidate retrieval combines:

* Dense semantic retrieval using Sentence Transformers + FAISS
* Sparse lexical retrieval using BM25

```text
Hybrid Score =
0.6 × Semantic Score +
0.4 × BM25 Score
```

---

### 2. Career Intelligence

Career fit scoring considers:

Career fit scoring considers:

* Seniority alignment (5–9 years preferred)
* Evidence of production retrieval/ranking systems
* Search, recommendation and matching experience
* Product-company experience
* Career trajectory and title relevance
* Detection of keyword stuffing without career evidence
* Penalties for irrelevant domains and titles

---

### 3. Behavioral Signals

Behavior score includes:

* Open-to-work status
* Notice period
* Recruiter response rate
* Interview completion
* GitHub activity
* Recent profile activity

---
### 4. Skill Verification

The system validates claimed expertise using additional profile signals:

* Skill assessment scores
* Endorsements received
* LinkedIn connectivity
* Expert-skill consistency checks
* Detection of unrealistic expert claims

This reduces the impact of skill stuffing and improves ranking reliability.
---

### 5. Profile Quality

Profile quality evaluates:

* Profile completeness
* Endorsements
* Search appearances
* Recruiter saves
* Connection strength

---

### 6. Honeypot Detection

The system penalizes suspicious or inconsistent profiles.

Examples:

* Senior titles with very low experience
* Unrealistic skill durations
* Excessive expert claims
* Skill stuffing
* Timeline inconsistencies
* Title-skill mismatches

This reduces the likelihood of ranking synthetic or misleading profiles.

---

### 7. Diversity Re-ranking

A diversity layer prevents highly similar candidates from dominating the final shortlist.

This improves candidate variety while preserving relevance.

---

## 💡 Explainability Example

```text
✓ Strong semantic alignment with the job description

✓ Demonstrates production experience in retrieval and ranking systems

✓ Matches critical skills including FAISS, RAG and semantic search

✓ Exceeds the minimum experience requirement with 6.5 years of experience
```

## 📈 Compute Constraints

* CPU-only inference
* No network access during ranking
* Precomputed embeddings
* Designed for 16 GB RAM environments
* Ranking pipeline optimized for challenge constraints

---

## 🔁 Reproducibility

Official reproduction command:

```bash
python rank.py --candidates ./candidates.jsonl --out ./submission.csv
```

The pipeline executes end-to-end and generates the final ranked CSV.

---


## 📜 License

MIT License
