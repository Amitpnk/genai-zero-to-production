"""Max tokens and stop sequences: two ways an answer ends early. Runs locally with Ollama."""

import json
import os
import urllib.request

from dotenv import load_dotenv

load_dotenv()
MODEL = os.environ["OLLAMA_MODEL"]
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")


def generate(prompt, **options):
    body = {"model": MODEL, "prompt": prompt, "raw": True, "stream": False,
            "options": {"temperature": 0, **options}}
    req = urllib.request.Request(f"{HOST}/api/generate", json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        result = json.load(resp)
    return result["response"], result["done_reason"], result["eval_count"]


print("1) max tokens = 12  (num_predict in Ollama)")
text, reason, count = generate("Explain photosynthesis:", num_predict=12)
print(f"   output: {text.strip()!r}")
print(f"   stopped because: {reason!r} after {count} tokens  <- cut mid-sentence\n")

print('2) stop sequence = "\\n3."  (stop generating when this text appears)')
text, reason, count = generate("List three fruits:\n1.", num_predict=60, stop=["\n3."])
print(f"   output: {text!r}")
print(f"   stopped because: {reason!r}  <- the stop text itself is not included")
