import json
import os
from datetime import datetime

LOG_FILE = "outputs/audit_logs.json"

def log_audit(transaction, reason, explanation):
    log_entry = {
        "transaction_id": transaction["transaction_id"],
        "user_id": transaction["user_id"],
        "amount": transaction["amount"],
        "location": transaction["location"],
        "timestamp": str(transaction["timestamp"]),
        "rules_triggered": reason,
        "llm_explanation": explanation,
        "logged_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Create file if not exists
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    # Append log
    with open(LOG_FILE, "r+") as f:
        data = json.load(f)
        data.append(log_entry)
        f.seek(0)
        json.dump(data, f, indent=4)