"""Run the same small test set on several models and compare quality, speed and tokens.

Usage (model ids are provider:model):
  uv run python ep06-model-landscape/compare_models.py
  uv run python ep06-model-landscape/compare_models.py ollama:gemma3:1b gemini:gemini-3.5-flash-lite
"""

import json
import os
import re
import sys
import time
import urllib.request

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# A tiny "eval set": each task has a prompt and a check for the right answer.
TASKS = [
    ("sentiment", "Classify the sentiment as positive, negative or neutral. Reply with one word.\n"
                  "Review: The battery died after two days and support never replied.",
     lambda a: "negative" in a.lower()),
    ("letters", "How many times does the letter r appear in 'strawberry'? Reply with just the number.",
     lambda a: a.strip().startswith("3")),
    ("maths", "I have 3 boxes. Each box has 4 bags. Each bag has 5 marbles. I give away 17 marbles. "
              "How many marbles are left? Reply with just the number.",
     lambda a: "43" in a),
    ("logic", "Tom is older than Ana. Ana is older than Raj. Raj is older than Lee. "
              "Who is the second youngest? Reply with just the name.",
     lambda a: "raj" in a.lower()),
    ("extract", 'Return JSON with keys "item" and "qty" (a number) for this order: '
                '"Hi, please send me three blue mugs by Friday."',
     lambda a: parse_json(a).get("qty") == 3),
    ("date", "Today is Monday 12 October. What is the date 10 days from today? Reply as 'Weekday DD Month'.",
     lambda a: "thursday 22 october" in a.lower()),
]


def parse_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    try:
        return json.loads(match.group(0)) if match else {}
    except json.JSONDecodeError:
        return {}


def ask_ollama(model, prompt):
    body = {"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False,
            "options": {"temperature": 0}}
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    req = urllib.request.Request(f"{host}/api/chat", json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        result = json.load(resp)
    return result["message"]["content"], result.get("eval_count", 0)


gemini = None


def ask_gemini(model, prompt):
    global gemini
    gemini = gemini or genai.Client()
    reply = gemini.models.generate_content(
        model=model, contents=prompt,
        config=types.GenerateContentConfig(temperature=0, max_output_tokens=4000),
    )
    usage = reply.usage_metadata
    return reply.text or "", (usage.candidates_token_count or 0) + (usage.thoughts_token_count or 0)


models = sys.argv[1:] or [f"ollama:{os.environ['OLLAMA_MODEL']}", f"gemini:{os.environ['GEMINI_MODEL']}"]
print(f"{'model':<34}{'score':>7}{'time':>8}{'out tokens':>12}   per task")
for spec in models:
    provider, model = spec.split(":", 1)
    ask = ask_ollama if provider == "ollama" else ask_gemini
    passed, tokens, marks = 0, 0, []
    start = time.perf_counter()
    for name, prompt, check in TASKS:
        answer, used = ask(model, prompt)
        ok = check(answer)
        passed += ok
        tokens += used
        marks.append(f"{name} {'✓' if ok else '✗'}")
    elapsed = time.perf_counter() - start
    print(f"{spec:<34}{passed:>4}/{len(TASKS)}{elapsed:>7.1f}s{tokens:>12}   {'  '.join(marks)}")

print("\nPick the smallest, cheapest model that passes YOUR tests, not the one at the top of a leaderboard.")
