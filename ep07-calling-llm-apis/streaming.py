"""Streaming vs waiting: same request, but streaming shows the first words much sooner."""

import time

from shared.llm import chat, provider_from_args, stream

provider = provider_from_args()
messages = [{"role": "user", "content": "Explain what an API is to a 10-year-old, in about 80 words."}]

print(f"Provider: {provider}\n")
chat([{"role": "user", "content": "Hi"}], provider=provider, max_tokens=5)   # warm-up: load the model first, so timings are fair

print("1) Without streaming: nothing appears until the whole answer is ready...")
start = time.perf_counter()
reply = chat(messages, provider=provider)
waited = time.perf_counter() - start
print(f"   ...{waited:.1f} s later, all {reply.output_tokens} tokens arrive at once.\n")

print("2) With streaming: text appears as it's generated:\n")
start = time.perf_counter()
first = None
for piece in stream(messages, provider=provider):
    if first is None:
        first = time.perf_counter() - start
    print(piece, end="", flush=True)
total = time.perf_counter() - start

print(f"\n\n   first words after {first:.1f} s, finished after {total:.1f} s (vs {waited:.1f} s without streaming)")
print("   Streaming doesn't make the model faster; the user just starts reading much sooner.")
