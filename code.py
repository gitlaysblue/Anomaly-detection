# Project: Financial Transaction Anomaly Detector
# Student Version - Simple, effective, fast
# Upload CSV → Detect anomalies → Show metrics & charts

import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# ---- Title ----
st.title("💳 Financial Transaction Anomaly Detector")
st.write("Upload your CSV file of transactions and detect unusual/fraudulent entries.")

# ---- File Upload ----
file = st.file_uploader("Choose CSV file", type=["csv"])

if file is not None:
    # Read CSV into a dataframe
    data = pd.read_csv(file)
    
    st.subheader("📂 Preview of your data")
    st.write(data.head())

    # ---- Select numeric columns for anomaly detection ----
    numeric_data = data.select_dtypes(include=['int64', 'float64'])
    
    if numeric_data.shape[1] == 0:
        st.error("No numeric columns found to analyze!")
    else:
        # ---- Run Isolation Forest ----
        model = IsolationForest(contamination=0.05, random_state=42)
        data["anomaly_flag"] = model.fit_predict(numeric_data)
        
        # Convert -1/1 to human-readable labels
        data["anomaly_flag"] = data["anomaly_flag"].map({1: "Normal", -1: "Anomaly"})
        
        st.success("✅ Anomaly detection done!")

        # ---- Metrics ----
        total_txn = len(data)
        anomaly_count = len(data[data["anomaly_flag"] == "Anomaly"])
        st.metric("Total Transactions", total_txn)
        st.metric("Anomalies Detected", anomaly_count)

        # ---- Show anomalies ----
        st.subheader("🔍 Sample of Detected Anomalies")
        st.write(data[data["anomaly_flag"] == "Anomaly"].head())

        # ---- Plot transaction distribution ----
        st.subheader("📊 Transaction Amount Distribution")
        if "amount" in data.columns:
            plt.figure(figsize=(8,4))
            plt.hist(data["amount"], bins=30, alpha=0.7)
            plt.xlabel("Transaction Amount")
            plt.ylabel("Count")
            st.pyplot(plt)
        else:
            st.info("No 'amount' column to plot.")
