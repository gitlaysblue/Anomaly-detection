# Project: Financial Transaction Anomaly Detector
# Enhanced, robust version for resume/portfolio
# Interactive, colorful, student-friendly but professional

import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
import plotly.express as px

# ---- Page Config ----
st.set_page_config(
    page_title="Transaction Anomaly Detector",
    layout="wide",
    page_icon="💳",
    initial_sidebar_state="expanded"
)

# ---- Sidebar Navigation ----
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home", "Upload & Analyze"])

# ---- Home Page ----
if menu == "Home":
    st.markdown("<h1 style='color:#2E86C1'>💳 Financial Anomaly Detection App</h1>", unsafe_allow_html=True)
    st.write("Welcome! This app detects unusual or potentially fraudulent financial transactions from a CSV file.")
    st.markdown("""
        **Features:**  
        - Upload CSV of transactions  
        - Detect anomalies (Isolation Forest)  
        - Interactive charts & metrics  
        - Download flagged anomalies  
    """)
    st.markdown("<p style='color:gray;font-size:12px'>Made by laysBlue</p>", unsafe_allow_html=True)

# ---- Upload & Analyze Page ----
elif menu == "Upload & Analyze":
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            st.stop()

        st.subheader("📂 Data Preview")
        st.dataframe(df.head())

        # Check numeric columns
        numeric_cols = df.select_dtypes(include=['int64', 'float64'])
        if numeric_cols.shape[1] == 0:
            st.error("No numeric columns found for analysis!")
        else:
            # ---- Anomaly Detection ----
            try:
                model = IsolationForest(contamination=0.05, random_state=42)
                df["anomaly_flag"] = model.fit_predict(numeric_cols)
                df["anomaly_flag"] = df["anomaly_flag"].map({1: "Normal", -1: "Anomaly"})
            except Exception as e:
                st.error(f"Error during anomaly detection: {e}")
                st.stop()

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

            # ---- Transaction Amount Distribution ----
            st.subheader("📊 Transaction Amount Distribution")
            if "amount" in df.columns:
                try:
                    fig = px.histogram(
                        df,
                        x="amount",
                        color="anomaly_flag",
                        barmode="overlay",
                        labels={"amount":"Transaction Amount","anomaly_flag":"Flag"},
                        title="Transaction Amounts: Normal vs Anomaly"
                    )
                    fig.update_layout(
                        xaxis_title="Amount",
                        yaxis_title="Count",
                        legend_title="Flag",
                        autosize=True
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error plotting histogram: {e}")
            else:
                st.info("No 'amount' column to plot.")

            # ---- Transactions Over Time ----
            st.subheader("📈 Transactions Over Time")
            if "date" in df.columns:
                try:
                    df["date"] = pd.to_datetime(df["date"], errors='coerce')
                    df_time = df.dropna(subset=["date"])
                    fig2 = px.line(
                        df_time,
                        x="date",
                        y="amount",
                        color="anomaly_flag",
                        labels={"date":"Date","amount":"Amount","anomaly_flag":"Flag"},
                        title="Transaction Trends Over Time"
                    )
                    fig2.update_layout(
                        xaxis_title="Date",
                        yaxis_title="Amount",
                        legend_title="Flag",
                        autosize=True
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                except Exception as e:
                    st.error(f"Error plotting time-series: {e}")
            else:
                st.info("No 'date' column to plot.")

            # ---- Show Anomalies Table ----
            st.subheader("🔍 Flagged Anomalies")
            anomalies_df = df[df["anomaly_flag"]=="Anomaly"]
            st.dataframe(anomalies_df)

            # ---- Download Anomalies CSV ----
            try:
                csv = anomalies_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Anomalies CSV",
                    data=csv,
                    file_name="anomalies.csv",
                    mime="text/csv",
                )
            except Exception as e:
                st.error(f"Error creating download: {e}")

            # ---- Subtle Credit ----
            st.markdown("<p style='color:gray;font-size:12px'>Made by laysBlue</p>", unsafe_allow_html=True)
