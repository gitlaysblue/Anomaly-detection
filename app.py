# Project: Financial Transaction Anomaly Detector
# Enhanced Version - Dynamic & Interactive
# Student-style but impressive

import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
import plotly.express as px

# ---- Page Config ----
st.set_page_config(page_title="Transaction Anomaly Detector", layout="wide", page_icon="💳")

# ---- Sidebar ----
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home", "Upload & Analyze"])

# ---- Home Page ----
if menu == "Home":
    st.markdown("<h1 style='color:#2E86C1'>💳 Financial Anomaly Detection App</h1>", unsafe_allow_html=True)
    st.write("Welcome! This app helps you detect unusual or potentially fraudulent transactions from a CSV file.")
    st.markdown("""
        **Features:**  
        - Upload CSV of transactions  
        - Detect anomalies (Isolation Forest)  
        - Interactive charts & metrics  
        - Download flagged anomalies  
    """)
    st.markdown("<p style='color:gray;font-size:12px'>Made with ❤️ by Your Name</p>", unsafe_allow_html=True)

# ---- Upload & Analyze Page ----
elif menu == "Upload & Analyze":
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.subheader("📂 Data Preview")
        st.dataframe(df.head())

        numeric_cols = df.select_dtypes(include=['int64', 'float64'])
        if numeric_cols.shape[1] == 0:
            st.error("No numeric columns to analyze!")
        else:
            # Anomaly Detection
            model = IsolationForest(contamination=0.05, random_state=42)
            df["anomaly_flag"] = model.fit_predict(numeric_cols)
            df["anomaly_flag"] = df["anomaly_flag"].map({1: "Normal", -1: "Anomaly"})

            st.success("✅ Anomaly Detection Complete!")

            # ---- Metrics ----
            total_txn = len(df)
            anomaly_count = len(df[df["anomaly_flag"]=="Anomaly"])
            anomaly_pct = round(anomaly_count/total_txn*100,2)

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Transactions", total_txn)
            col2.metric("Anomalies Found", anomaly_count)
            col3.metric("Anomaly %", f"{anomaly_pct}%")
            if "amount" in df.columns:
                col4.metric("Max Transaction", df["amount"].max())

            # ---- Interactive Charts ----
            st.subheader("📊 Transaction Amount Distribution")
            if "amount" in df.columns:
                fig = px.histogram(df, x="amount", color="anomaly_flag", barmode="overlay",
                                   labels={"amount":"Transaction Amount","anomaly_flag":"Flag"},
                                   title="Transaction Amounts: Normal vs Anomaly")
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("📈 Transactions Over Time")
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                fig2 = px.line(df, x="date", y="amount", color="anomaly_flag",
                               labels={"date":"Date","amount":"Amount","anomaly_flag":"Flag"},
                               title="Transaction Trends Over Time")
                st.plotly_chart(fig2, use_container_width=True)

            # ---- Show Anomalies Table ----
            st.subheader("🔍 Flagged Anomalies")
            anomalies_df = df[df["anomaly_flag"]=="Anomaly"]
            st.dataframe(anomalies_df)

            # ---- Download Anomalies CSV ----
            csv = anomalies_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Anomalies CSV",
                data=csv,
                file_name="anomalies.csv",
                mime="text/csv",
            )

            # ---- Subtle Credit ----
            st.markdown("<p style='color:gray;font-size:12px'>Made with ❤️ by Your Name</p>", unsafe_allow_html=True)
