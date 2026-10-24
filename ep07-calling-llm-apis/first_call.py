"""The anatomy of one LLM API call: what you send, and what comes back."""

import json

from llm import chat, provider_from_args

provider = provider_from_args()

system = "You are a concise assistant. Answer in one sentence."
messages = [{"role": "user", "content": "What is a context window?"}]

print(f"Provider: {provider}\n")
print("What we send:")
print(json.dumps({"system": system, "messages": messages}, indent=2))

reply = chat(messages, system=system, provider=provider)

print("\nWhat comes back:")
print(f"  text:          {reply.text.strip()}")
print(f"  finish reason: {reply.finish_reason}")
print(f"  tokens:        {reply.input_tokens} in, {reply.output_tokens} out")
