"""Two surprises with a cloud reasoning model (Gemini)."""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()  # reads GEMINI_API_KEY
MODEL = os.environ["GEMINI_MODEL"]
PROMPT = "Write a one-sentence slogan for a coffee shop."

print("Gotcha 1: max_output_tokens also has to cover hidden thinking\n")
for limit in (50, 300, 2000):
    reply = client.models.generate_content(
        model=MODEL, contents=PROMPT, config=types.GenerateContentConfig(max_output_tokens=limit)
    )
    usage = reply.usage_metadata
    print(f"   limit {limit:>4}: thinking {usage.thoughts_token_count or 0:>4} + answer {usage.candidates_token_count or 0:>3} "
          f"-> {reply.candidates[0].finish_reason.name:<10} {(reply.text or '').strip()!r}")

print("\nGotcha 2: temperature 0 is not a determinism guarantee\n")
for run in range(3):
    reply = client.models.generate_content(
        model=MODEL, contents=PROMPT,
        config=types.GenerateContentConfig(temperature=0, max_output_tokens=2000),
    )
    print(f"   run {run + 1}: {reply.text.strip()}")
