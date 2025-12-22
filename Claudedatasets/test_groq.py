import os
import requests
from dotenv import load_dotenv

load_dotenv()  # must be called before os.getenv

key = os.getenv("GROQ_API_KEY")
print("KEY:", key)

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "llama-3.1-8b-instant",
    "messages": [{"role": "user", "content": "say hi"}]
}

r = requests.post(url, headers=headers, json=payload)
print(r.status_code)
print(r.text)
