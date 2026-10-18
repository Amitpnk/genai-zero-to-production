"""Same prompt, different temperatures, side by side. Runs locally with Ollama."""

import json
import os
import urllib.request

from dotenv import load_dotenv

load_dotenv()
MODEL = os.environ["OLLAMA_MODEL"]
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
PROMPT = "Write a one-sentence slogan for a coffee shop:"


def generate(**options):
    body = {"model": MODEL, "prompt": PROMPT, "raw": True, "stream": False,
            "options": {"num_predict": 30, **options}}
    req = urllib.request.Request(f"{HOST}/api/generate", json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        text = json.load(resp)["response"].strip()
    return text.splitlines()[0] if text else ""


print(f"Prompt: {PROMPT!r}\n")
for temp in (0, 0.8, 1.8):
    print(f"temperature = {temp}")
    for run in range(3):
        print(f"   run {run + 1}: {generate(temperature=temp)}")
    print()

print("Same seed, temperature 1.0, twice:")
for run in range(2):
    print(f"   run {run + 1}: {generate(temperature=1.0, seed=42)}")
