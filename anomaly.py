import pandas as pd

def detect_anomalies(df):
    df = df.copy()

    # Calculate average amount per user
    user_avg = df.groupby("user_id")["amount"].mean().to_dict()

    anomaly_flags = []
    reasons = []

    for _, row in df.iterrows():
        user = row["user_id"]
        amount = row["amount"]

        reason = []

        # Rule 1: High value transaction
        if amount > 100000:
            reason.append("High-value transaction")

        # Rule 2: Deviation from user's average behavior
        if amount > 3 * user_avg[user]:
            reason.append("Deviation from normal behavior")

        # Final flag
        if len(reason) > 0:
            anomaly_flags.append(1)
            reasons.append(", ".join(reason))
        else:
            anomaly_flags.append(0)
            reasons.append("Normal")

    df["is_anomaly"] = anomaly_flags
    df["reason"] = reasons

    return df