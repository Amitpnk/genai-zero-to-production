"""Measure tokens, cost and latency for a short and a long answer with Gemini."""

import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()  # reads GEMINI_API_KEY

# EXAMPLE prices in US$ per 1 million tokens, to show the maths only.
# Prices change often: copy the real ones from your provider's pricing page.
PRICE_IN, PRICE_OUT = 0.50, 3.00


def run(prompt):
    start = time.perf_counter()
    first_token_at = None
    usage = None
    stream = client.models.generate_content_stream(
        model=os.environ["GEMINI_MODEL"],
        contents=prompt,
        config=types.GenerateContentConfig(max_output_tokens=4000),
    )
    for chunk in stream:
        if first_token_at is None and chunk.text:
            first_token_at = time.perf_counter() - start
        usage = chunk.usage_metadata or usage
    total = time.perf_counter() - start

    tokens_in = usage.prompt_token_count
    tokens_out = usage.candidates_token_count or 0
    thinking = usage.thoughts_token_count or 0  # hidden reasoning, billed as output
    cost = (tokens_in * PRICE_IN + (tokens_out + thinking) * PRICE_OUT) / 1_000_000

    print(f"Prompt: {prompt!r}")
    print(f"  input tokens      {tokens_in:>6}")
    print(f"  output tokens     {tokens_out:>6}")
    print(f"  thinking tokens   {thinking:>6}   (hidden, still billed as output)")
    print(f"  first text after  {first_token_at:>6.1f} s")
    print(f"  total time        {total:>6.1f} s")
    print(f"  example cost      ${cost:.5f}\n")


run("Describe the ocean in about 20 words.")
run("Describe the ocean in about 400 words.")

print("Longer output = more tokens = more time and more money.")
