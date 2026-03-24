from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def generate_explanation(transaction, reason):
    prompt = f"""
    You are a financial compliance AI.

    A transaction has been flagged with the following details:
    - User ID: {transaction['user_id']}
    - Amount: {transaction['amount']}
    - Location: {transaction['location']}
    - Timestamp: {transaction['timestamp']}

    Detected issues:
    {reason}

    Explain clearly why this transaction is suspicious in a professional, audit-friendly manner.
    Do not hallucinate. Stick only to given reasons.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content