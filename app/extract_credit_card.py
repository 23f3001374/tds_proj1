import requests
import os

input_file = "/data/credit-card.png"
output_file = "/data/credit-card.txt"

AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
AIPROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

try:
    with open(input_file, "rb") as img_file:
        files = {"file": img_file}
        response = requests.post(
            AIPROXY_URL,
            headers={"Authorization": f"Bearer {AIPROXY_TOKEN}"},
            files=files
        )

    card_number = response.json()["choices"][0]["message"]["content"].replace(" ", "")

    with open(output_file, "w") as f:
        f.write(card_number)

    print("Extracted credit card number successfully.")

except Exception as e:
    print(f"Error extracting card number: {e}")
