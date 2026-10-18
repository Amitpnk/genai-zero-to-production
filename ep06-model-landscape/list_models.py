"""Discover the models you can use right now, instead of trusting a list that goes stale."""

import json
import os
import urllib.request

from dotenv import load_dotenv
from google import genai

load_dotenv()

print("Cloud: Gemini models your key can call (listing is free)\n")
print(f"   {'model':<28}{'context (in)':>14}{'max out':>10}")
client = genai.Client()  # reads GEMINI_API_KEY
for model in client.models.list():
    name = model.name.removeprefix("models/")
    actions = model.supported_actions or []
    # Keep the main text models; skip previews, aliases and special-purpose variants.
    if "generateContent" not in actions or not name.startswith("gemini-"):
        continue
    if any(word in name for word in ("preview", "latest", "tts", "image", "banana", "robotics", "computer", "transcribe")):
        continue
    print(f"   {name:<28}{model.input_token_limit:>14,}{model.output_token_limit:>10,}")
print("   Listed doesn't always mean callable: older models can be closed to new users.")

host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
print("\nLocal: open-weight models you've downloaded with Ollama\n")
try:
    with urllib.request.urlopen(f"{host}/api/tags", timeout=10) as resp:
        local = json.load(resp)["models"]
    print(f"   {'model':<20}{'parameters':>12}{'quantization':>14}{'on disk':>10}")
    for m in local:
        d = m["details"]
        print(f"   {m['name']:<20}{d['parameter_size']:>12}{d['quantization_level']:>14}{m['size'] / 1e9:>8.1f} GB")
except OSError:
    print("   Ollama isn't running (see the Ollama cheat sheet).")
