import requests
import os

input_file = "/data/email.txt"
output_file = "/data/email-sender.txt"

AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
AIPROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

try:
    with open(input_file, "r") as f:
        email_content = f.read()

    response = requests.post(
        AIPROXY_URL,
        headers={"Authorization": f"Bearer {AIPROXY_TOKEN}", "Content-Type": "application/json"},
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": f"Extract sender's email from this:\n{email_content}"}]
        }
    )

    email_address = response.json()["choices"][0]["message"]["content"].strip()

    with open(output_file, "w") as f:
        f.write(email_address)

    print("Extracted email successfully.")

except Exception as e:
    print(f"Error extracting email: {e}")
