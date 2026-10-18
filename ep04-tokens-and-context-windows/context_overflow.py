"""What happens when a prompt doesn't fit the context window? Runs locally with Ollama.

We hide a secret at the very start of a long prompt, then ask for it back
with a big context window and with a small one.
"""

import json
import os
import urllib.request

from dotenv import load_dotenv

load_dotenv()
MODEL = os.environ["OLLAMA_MODEL"]
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

filler = " ".join(
    f"Note {i}: the weather report for the coastal town was calm, mild and uneventful today."
    for i in range(60)
)
prompt = (
    "Remember this: the secret code is BLUE-TIGER-42.\n\n"
    + filler
    + "\n\nQuestion: what is the secret code? Answer with just the code."
)


def ask(num_ctx):
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"num_ctx": num_ctx, "temperature": 0},  # num_ctx = context window size
    }
    req = urllib.request.Request(
        f"{HOST}/api/chat", json.dumps(body).encode(), {"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        result = json.load(resp)
    return result["prompt_eval_count"], result["message"]["content"].strip()


for num_ctx in (4096, 512):
    seen, reply = ask(num_ctx)
    print(f"Context window {num_ctx:>5} tokens -> model saw {seen:>5} prompt tokens -> reply: {reply!r}")

print("\nWith the small window, the start of the prompt (and the secret) was silently cut off.")
