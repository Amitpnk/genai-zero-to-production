"""See how text becomes tokens. Runs locally: no API key needed."""

import tiktoken

# The tokenizer used by recent OpenAI models. Claude and Gemini use their own,
# so the exact pieces and counts differ by model, but the idea is the same.
enc = tiktoken.get_encoding("o200k_base")

examples = [
    "Hello world",
    "unbelievable",
    "GenAI engineering is fun!",
    "ChatGPT, Claude and Gemini",
    "नमस्ते दुनिया",  # "Hello world" in Hindi
]

for text in examples:
    ids = enc.encode(text)
    pieces = [enc.decode([i]) for i in ids]
    print(f"{text!r}  ->  {len(ids)} tokens")
    print("   pieces:", " | ".join(repr(p) for p in pieces))
    print("   ids:   ", ids)
    print()
