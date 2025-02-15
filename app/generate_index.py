import os
import json

docs_dir = "/data/docs/"
output_file = "/data/docs/index.json"

index = {}

try:
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    for line in f:
                        if line.startswith("# "):
                            index[file] = line.strip("# ").strip()
                            break

    with open(output_file, "w") as f:
        json.dump(index, f, indent=2)

    print("Generated Markdown index successfully.")

except Exception as e:
    print(f"Error generating index: {e}")
