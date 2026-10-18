"""Count the same text with different tokenizers. Each model family counts differently."""

import os

import tiktoken
from dotenv import load_dotenv
from google import genai

load_dotenv()
openai_enc = tiktoken.get_encoding("o200k_base")  # recent OpenAI models, runs locally
gemini = genai.Client()  # reads GEMINI_API_KEY; counting tokens is free

# Claude counts via the API too, but only if you've set a real Anthropic key.
anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
claude = None
if anthropic_key and not anthropic_key.startswith("your-"):
    import anthropic

    claude = anthropic.Anthropic()

samples = {
    "English": "The quick brown fox jumps over the lazy dog. Large language models read text as tokens.",
    "Hindi": "तेज़ भूरी लोमड़ी आलसी कुत्ते के ऊपर कूदती है। बड़े भाषा मॉडल टेक्स्ट को टोकन के रूप में पढ़ते हैं।",
    "Code": "def add(a: int, b: int) -> int:\n    return a + b\n\nprint(add(2, 3))",
    "JSON": '{"user_id": 48213, "name": "Asha", "tags": ["admin", "beta"], "active": true}',
    "Numbers": "3.14159 2.71828 1.41421 1234567890 98765.4321",
}

header = f"{'Text':<9}{'chars':>6}{'OpenAI':>8}{'Gemini':>8}"
print(header + (f"{'Claude':>8}" if claude else ""))
print("-" * len(header + ("        " if claude else "")))

for name, text in samples.items():
    openai_count = len(openai_enc.encode(text))
    gemini_count = gemini.models.count_tokens(model=os.environ["GEMINI_MODEL"], contents=text).total_tokens
    row = f"{name:<9}{len(text):>6}{openai_count:>8}{gemini_count:>8}"
    if claude:
        claude_count = claude.messages.count_tokens(
            model=os.environ["ANTHROPIC_MODEL"], messages=[{"role": "user", "content": text}]
        ).input_tokens
        row += f"{claude_count:>8}"
    print(row)

print("\nSame text, different counts: always measure with the tokenizer of the model you use.")
