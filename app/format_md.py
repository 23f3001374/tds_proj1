import subprocess

file_path = "/data/format.md"
try:
    subprocess.run(["npx", "prettier@3.4.2", "--write", file_path], check=True)
    print(f"Formatted {file_path}")
except Exception as e:
    print(f"Error formatting file: {e}")
