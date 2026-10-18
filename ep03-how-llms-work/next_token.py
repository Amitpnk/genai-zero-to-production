"""Watch an LLM predict the next token, one step at a time.

Runs a small open model locally with Ollama (free, offline):
  1. Install Ollama: https://ollama.com/download
  2. ollama pull gemma3:1b
"""

import json
import math
import os
import urllib.request

from dotenv import load_dotenv

load_dotenv()
MODEL = os.environ["OLLAMA_MODEL"]
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")


def next_token(text):
    """Ask the model for exactly one token and its top-5 alternatives."""
    body = {
        "model": MODEL,
        "prompt": text,
        "raw": True,  # no chat template: plain "continue this text"
        "stream": False,
        "logprobs": True,
        "top_logprobs": 5,
        "options": {"num_predict": 1, "temperature": 0},
    }
    req = urllib.request.Request(
        f"{HOST}/api/generate", json.dumps(body).encode(), {"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        step = json.load(resp)["logprobs"][0]
    options = [(t["token"], math.exp(t["logprob"])) for t in step["top_logprobs"]]
    return step["token"], options


text = "The capital of France is"
print(f"Prompt: {text!r}\n")

for i in range(6):
    chosen, options = next_token(text)
    print(f"Step {i + 1}: the model's top guesses")
    for token, prob in options:
        mark = "  <- picked" if token == chosen else ""
        print(f"   {token!r:<14} {prob:6.1%}  {'#' * round(prob * 40)}{mark}")
    text += chosen
    print(f"   text so far: {text!r}\n")
