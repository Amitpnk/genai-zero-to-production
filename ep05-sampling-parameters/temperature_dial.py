"""How temperature and top-p reshape the next-token choice. Runs locally with Ollama.

We get the model's real top-10 next tokens, then apply temperature and top-p
ourselves so you can see the maths.
"""

import json
import math
import os
import urllib.request

from dotenv import load_dotenv

load_dotenv()
MODEL = os.environ["OLLAMA_MODEL"]
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
PROMPT = "My favourite ice cream flavour is"

body = {
    "model": MODEL, "prompt": PROMPT, "raw": True, "stream": False,
    "logprobs": True, "top_logprobs": 10,
    "options": {"num_predict": 1, "temperature": 0},
}
req = urllib.request.Request(f"{HOST}/api/generate", json.dumps(body).encode(), {"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=120) as resp:
    top = json.load(resp)["logprobs"][0]["top_logprobs"]
tokens = [t["token"] for t in top]
logprobs = [t["logprob"] for t in top]


def with_temperature(temp):
    """Temperature divides the scores before softmax: low = sharper, high = flatter."""
    scaled = [lp / temp for lp in logprobs]
    biggest = max(scaled)
    weights = [math.exp(s - biggest) for s in scaled]
    total = sum(weights)
    return [w / total for w in weights]  # renormalised over the top 10


print(f"Prompt: {PROMPT!r}   (top 10 next tokens, renormalised)\n")
temps = (0.2, 1.0, 2.0)
print(f"{'token':<14}" + "".join(f"{'T=' + str(t):>10}" for t in temps))
dists = [with_temperature(t) for t in temps]
for i, tok in enumerate(tokens):
    print(f"{tok!r:<14}" + "".join(f"{d[i]:>10.1%}" for d in dists))

# Top-p (nucleus): keep the smallest set of tokens whose probabilities add up to p.
p = 0.9
probs = dists[1]
kept, running = [], 0.0
for tok, prob in zip(tokens, probs):
    if running >= p:
        break
    kept.append(tok)
    running += prob
print(f"\nTop-p = {p} at T=1.0 keeps {len(kept)} of {len(tokens)}: {kept}")
print("Everything else can never be picked.")
