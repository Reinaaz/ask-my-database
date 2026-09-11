import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen2.5:7b",
        "prompt": "What is SQL in one simple sentence?",
        "stream": False
    }
)

print(response.json()["response"])