import streamlit as st
import pandas as pd
from anomaly import detect_anomalies
from explain import generate_explanation
from audit import log_audit
from report import generate_report
# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Financial AI Agent", layout="wide")

st.title("💰 Explainable Financial Anomaly Agent")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/transactions.csv")
        return df
    except:
        return None

df = load_data()

if df is not None:
    df=detect_anomalies(df)

# -----------------------------
# DISPLAY DATA
# -----------------------------
st.subheader("📊 Transaction Dataset")

if df is not None:
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No dataset found. Please add transactions.csv in data folder.")

# -----------------------------
# ANOMALY SECTION
# -----------------------------
if df is not None:
    st.subheader("🚨 Detected Anomalies")

    anomalies = df[df["is_anomaly"] == 1]

    if len(anomalies) > 0:
        for idx, row in anomalies.iterrows():
            with st.expander(f"Transaction {row['transaction_id']}"):
                st.write(f"**Amount:** ₹{row['amount']}")
                st.write(f"**Location:** {row['location']}")
                st.write(f"**Reason:** {row['reason']}")

                if st.button(f"Explain {row['transaction_id']}", key=idx):
                    explanation = generate_explanation(row, row["reason"])

                    # Log audit
                    log_audit(row, row["reason"], explanation)

                    st.success(explanation)
    else:
        st.success("No anomalies detected")

# -----------------------------
# BASIC STATS
# -----------------------------
if df is not None:
    st.subheader("📈 Basic Insights")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Transactions", len(df))
    col2.metric("Unique Users", df["user_id"].nunique())
    col3.metric("Total Amount", f"₹ {df['amount'].sum():,.0f}")

# -----------------------------
# FILTER OPTION
# -----------------------------
if df is not None:
    st.subheader("🔍 Filter by User")

    users = df["user_id"].unique()
    selected_user = st.selectbox("Select User", users)

    filtered_df = df[df["user_id"] == selected_user]

    st.dataframe(filtered_df, use_container_width=True)


# -----------------------------
# AUDIT TRAIL VIEWER
# -----------------------------
import json

st.subheader("📜 Audit Trail Logs")

if st.button("View Audit Logs"):
    try:
        with open("outputs/audit_logs.json", "r") as f:
            logs = json.load(f)
            st.json(logs)
    except:
        st.warning("No audit logs found yet.")


# -----------------------------
# REPORT GENERATION
# -----------------------------
st.subheader("📄 Generate Compliance Report")

if st.button("Generate Report"):
    report_path = generate_report()

    if report_path:
        with open(report_path, "r") as f:
            st.download_button(
                label="Download Report",
                data=f,
                file_name="compliance_report.txt",
                mime="text/plain"
            )
    else:
        st.warning("No audit logs available to generate report.")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Prototype: Financial Close & Anomaly AI Agent")