from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import requests
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "script_runner",
            "description": "Run a Python script with provided arguments.",
            "parameters": {
                "type": "object",
                "properties": {
                    "script_name": {
                        "type": "string",
                        "description": "The name of the script inside the /app/ directory."
                    },
                    "args": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "List of arguments to pass to the script."
                    }
                },
                "required": ["script_name", "args"]
            }
        }
    }
]

@app.get("/")
def home():
    return {"message": "TDS Automation API is running!"}

@app.get("/read")
def read_file(path: str):
    try:
        with open(path, "r") as f:
            return {"data": f.read()}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/run")
def task_runner(task: str):
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": task},
            {
                "role": "system",
                "content": """
You are an assistant that determines which script to run for a given task.
You must return the script name and any arguments it requires in JSON format.
                """
            }
        ],
        "tools": TOOLS,
        "tool_choice": "auto"
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    try:
        script_name = response_data["choices"][0]["message"]["content"]["script_name"]
        args = response_data["choices"][0]["message"]["content"].get("args", [])
    except (KeyError, IndexError, TypeError):
        raise HTTPException(status_code=500, detail="AI response format error")

    return execute_script(script_name, args)

def execute_script(script_name: str, args: list):
    script_path = f"./app/{script_name}.py"

    if not os.path.exists(script_path):
        raise HTTPException(status_code=404, detail=f"Script {script_name}.py not found.")

    try:
        result = subprocess.run(
            ["python3", script_path, *args],
            capture_output=True,
            text=True,
            check=True
        )
        return {"output": result.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=e.stderr)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
