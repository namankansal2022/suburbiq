# 🏙️ SuburbIQ — Business Survival Intelligence Platform

> **Find where businesses like yours survive — before you sign a lease.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-suburbiq.streamlit.app-00e5a0?style=for-the-badge)](https://suburbiq.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 📖 Overview

SuburbIQ is a business location intelligence platform that maps **historical business survival rates** across 144,000 suburb-category pairs spanning the US, Canada, Australia and the UK.

Most location tools show you where competitors exist *today*. SuburbIQ answers a fundamentally different question:

> *Where have businesses like mine historically survived — and where have they gone to die?*

Built in 24 hours for the **SUDATA × COMM-STEM Datathon 2026** on the Foursquare Open Source Places dataset.

---

## ✨ Features

**Business Survival Map**
Every suburb is scored and colour-coded by a weighted survival metric — from red (high risk) to green (prime opportunity). Powered by real historical POI data.

**SuburbIQ Score**
A composite score combining survival rate (60%) and inverse competition density (40%), giving entrepreneurs a single actionable number per suburb.

**Suburb Deep Dive**
Click any suburb to see its full survival profile — active businesses, historical closures, survival rate vs state average, average business lifespan, and a plain-English verdict.

**Interactive Location Map**
Real GPS coordinates for every suburb, rendered on a dark Mapbox map with colour-coded markers and hover tooltips.

**Suburb Comparison**
Compare up to 3 suburbs side by side across survival rate, competition density and SuburbIQ score.

**AI Location Advisor**
Describe your business situation in plain English. SuburbIQ AI — powered by Claude — analyses 144,000 data points and recommends specific suburbs with scores, survival rates and reasoning grounded in real data.

---

## 🔬 The Core Insight

The Foursquare Open Source Places dataset ships three fields that most teams scroll past:

```
date_created    — when a business first opened
date_closed     — when it shut down
unresolved_flags — community-flagged closures and non-existent venues
```

Combined, these fields encode the **complete lifecycle of every business** in the dataset. We used them to compute:

```
survival_rate = active_businesses / total_businesses_ever_recorded
```

This produces something no existing free tool offers — a **business mortality map** showing not just where businesses exist, but where they have historically survived.

---

## 🏗️ Architecture

```
foursquare/fsq-os-places (HuggingFace)
        │
        ▼
  Streaming Pipeline (Polars + PyArrow)
  Filter → 6.1M POIs (US, CA, AU, GB)
        │
        ▼
  Survival Rate Calculator
  144,590 suburb-category pairs
  SuburbIQ Score = Survival(60%) + Inv.Density(40%)
        │
        ▼
  Streamlit App
  ├── Interactive Map (Mapbox)
  ├── Suburb Deep Dive
  ├── Comparison Charts (Plotly)
  └── AI Advisor (Claude API)
        │
        ▼
  Streamlit Cloud (suburbiq.streamlit.app)
```

---

## 🚀 Getting Started

### Prerequisites

```bash
python 3.11+
pip
```

### Installation

```bash
git clone https://github.com/namankansal2022/suburbiq.git
cd suburbiq
pip install -r requirements.txt
```

### Data Setup

The processed survival scores file is included in the repo (`data/survival_scores.parquet`). To regenerate from the raw Foursquare dataset:

```bash
# Step 1: Stream and filter POI data (requires HuggingFace token)
python notebooks/explore.py

# Step 2: Compute survival rates and SuburbIQ scores
python notebooks/process.py
```

### Running Locally

```bash
streamlit run app/main.py
```

Open `http://localhost:8501` in your browser.

### Environment Variables

Create a `.streamlit/secrets.toml` file:

```toml
MAPBOX_TOKEN = "your_mapbox_token"
ANTHROPIC_KEY = "your_anthropic_api_key"
```

---

## 📊 Data

| Source | Description |
|--------|-------------|
| [Foursquare Open Source Places](https://huggingface.co/datasets/foursquare/fsq-os-places) | 114M global POIs, monthly refresh |
| Filtered dataset | 6.1M POIs across US, Canada, Australia, UK |
| Processed output | 144,590 suburb-category survival scores |
| Geographic coverage | 24,619 unique localities |
| Category coverage | 409 business categories |

### Key Schema Fields Used

| Field | Type | Usage |
|-------|------|-------|
| `date_created` | Date | Business opening date |
| `date_closed` | Date | Business closure date |
| `unresolved_flags` | Array | Quality flags (closed, doesnt_exist) |
| `fsq_category_labels` | Array | 6-level category hierarchy |
| `latitude / longitude` | Decimal | Real GPS coordinates |
| `locality` | String | Suburb/city level grouping |
| `region` | String | State/province level grouping |

---

## 🧮 Scoring Methodology

**Step 1 — Tag active vs closed**
```python
is_closed = date_closed.notna() OR unresolved_flags contains ["closed", "doesnt_exist"]
```

**Step 2 — Compute survival rate per suburb-category pair**
```python
survival_rate = active_count / (active_count + closed_count)
# Only computed for pairs with ≥ 5 historical businesses
```

**Step 3 — Compute competition density rank**
```python
density_rank = percentile_rank(active_count) within category
inverse_density = 1 - density_rank
```

**Step 4 — SuburbIQ composite score**
```python
suburbiq_score = (survival_rate * 0.6 + inverse_density * 0.4) * 100
```

---

## 🤖 AI Location Advisor

The AI advisor uses the **Anthropic Claude API** with structured context injection. For each query, the top 50 matching suburb-category pairs are formatted into a structured prompt and passed to Claude, which reasons over the real data to produce specific, defensible recommendations.

This ensures recommendations are grounded in actual survival statistics rather than general knowledge.

---

## 🗂️ Project Structure

```
suburbiq/
├── app/
│   └── main.py              # Streamlit application
├── data/
│   ├── survival_scores.parquet   # Processed survival data (1.9MB)
│   └── suburb_coords.parquet     # Real GPS coordinates per suburb
├── notebooks/
│   ├── explore.py           # Data streaming pipeline
│   └── process.py           # Survival rate computation
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.13 |
| Data Processing | Polars, PyArrow, Pandas |
| Frontend | Streamlit |
| Visualisation | Plotly, Mapbox |
| AI | Anthropic Claude (claude-sonnet-4) |
| Data Source | Foursquare OS Places via HuggingFace |
| Deployment | Streamlit Cloud |
| Version Control | GitHub |

---

## 👥 Team

Built by **Team: Fire the Hole** for the SUDATA × COMM-STEM Datathon 2026, University of Sydney.

Judges: Blackbird Ventures, Microsoft, Airtree, Quantium, One Ventures.

---

## 📄 License

This project is licensed under the MIT License. The underlying Foursquare Open Source Places dataset is licensed under [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0).

---

## 🔮 What's Next

- Expand Australian and New Zealand coverage with additional Foursquare data files
- Integrate ABS census demographic overlays for richer opportunity scoring
- Add survival trend over time — showing whether a suburb is improving or declining
- Build an API layer for proptech platforms and franchise networks
- Mobile-optimised interface for on-the-go location scouting
