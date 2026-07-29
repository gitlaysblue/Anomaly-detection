# 💳 Financial Transaction Anomaly Detection Dashboard

## Objective

An interactive dashboard that flags potentially fraudulent or unusual financial transactions from any uploaded CSV file, using unsupervised anomaly detection — no labeled fraud data required.

## Technologies

- **Language:** Python
- **ML:** Scikit-learn (Isolation Forest)
- **Dashboard:** Streamlit
- **Visualization:** Plotly

## How It Works

1. **Upload** — user uploads a CSV of transactions (any numeric transaction data works; `amount` and `date` columns unlock additional charts).
2. **Anomaly Detection** — an Isolation Forest model (5% contamination rate) is fit on the numeric columns of the uploaded data and flags each transaction as `Normal` or `Anomaly`.
3. **Interactive Results:**
   - Summary metrics: total transactions, anomalies found, anomaly %, max transaction value
   - Transaction amount distribution (histogram, normal vs. anomaly overlay)
   - Transactions over time (if a `date` column is present)
   - Full table of flagged anomalies
   - One-click CSV export of just the flagged anomalies

## Why Isolation Forest

Isolation Forest is an unsupervised algorithm — it doesn't need pre-labeled "fraud" vs. "not fraud" examples to train on. Instead, it isolates outliers by randomly partitioning the data and identifying points that are easier to separate from the rest, which tend to be the anomalous ones. This makes it well suited to real-world fraud detection, where labeled fraud examples are often scarce or unavailable, and where fraud patterns evolve over time.

## Project Structure

```
financial-anomaly-detection/
├── app.py              # Streamlit app: UI, anomaly detection, visualizations
└── requirements.txt
```

## Setup

```bash
pip install streamlit pandas scikit-learn plotly

streamlit run app.py
```

Then open the local URL Streamlit prints, upload a transactions CSV, and view results instantly.

## Key Features

- Works with any transaction CSV — no fixed schema required beyond numeric columns
- Graceful handling of missing `amount`/`date` columns (charts adapt or are skipped with a clear message)
- Robust error handling at every stage (CSV parsing, model fitting, chart rendering, CSV export)
- Downloadable results — flagged anomalies can be exported directly for further review

## Talking Points for CV / Interview

- Built a real-time anomaly detection system using Isolation Forest to flag suspicious transactions across simulated financial data, with no labeled fraud examples required.
- Deployed as an interactive Streamlit dashboard with dynamic metrics, distribution and time-series visualizations, and a one-click export of flagged results.
- Designed for robustness — the app validates input data at each step and degrades gracefully (informative messages instead of crashes) when expected columns are missing.
