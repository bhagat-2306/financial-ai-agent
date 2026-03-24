import json
from datetime import datetime

LOG_FILE = "outputs/audit_logs.json"
REPORT_FILE = "outputs/compliance_report.txt"

def generate_report():
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except:
        return None

    if len(logs) == 0:
        return None

    report_lines = []
    report_lines.append("FINANCIAL COMPLIANCE REPORT")
    report_lines.append("=" * 50)
    report_lines.append(f"Generated at: {datetime.now()}")
    report_lines.append(f"Total Anomalies: {len(logs)}")
    report_lines.append("")

    for log in logs:
        report_lines.append(f"Transaction ID: {log['transaction_id']}")
        report_lines.append(f"User ID: {log['user_id']}")
        report_lines.append(f"Amount: ₹{log['amount']}")
        report_lines.append(f"Location: {log['location']}")
        report_lines.append(f"Rules Triggered: {log['rules_triggered']}")
        report_lines.append(f"Explanation: {log['llm_explanation']}")
        report_lines.append("-" * 50)

    report_text = "\n".join(report_lines)

    with open(REPORT_FILE, "w") as f:
        f.write(report_text)

    return REPORT_FILE