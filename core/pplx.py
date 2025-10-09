# core/pplx.py
import os, requests

PPLX_URL = "https://api.perplexity.ai/chat/completions"
PPLX_KEY = os.getenv("PPLX_API_KEY")

def ask_pplx(system, user):
    headers = {"Authorization": f"Bearer {PPLX_KEY}", "Content-Type": "application/json"}
    body = {
      "model": "sonar-pro",
      "messages": [
        {"role":"system","content":system},
        {"role":"user","content":user}
      ]
    }
    r = requests.post(PPLX_URL, headers=headers, json=body, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]
