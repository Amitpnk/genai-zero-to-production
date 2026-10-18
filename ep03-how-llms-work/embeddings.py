"""Embeddings: words with similar meanings get similar vectors."""

import math
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()  # reads GEMINI_API_KEY

words = ["cat", "dog", "kitten", "banana", "apple", "laptop", "king", "queen", "man", "woman"]
result = client.models.embed_content(model=os.environ["GEMINI_EMBEDDING_MODEL"], contents=words)
vectors = {w: e.values for w, e in zip(words, result.embeddings)}


def cosine(a, b):
    """1.0 = same direction (same meaning), lower = less related."""
    dot = sum(x * y for x, y in zip(a, b))
    return dot / math.sqrt(sum(x * x for x in a) * sum(y * y for y in b))


print(f"Each word is now a list of {len(vectors['cat'])} numbers.")
print("First 5 numbers for 'cat':", [round(x, 3) for x in vectors["cat"][:5]], "\n")

print("Most similar to 'cat':")
ranked = sorted((cosine(vectors["cat"], vectors[w]), w) for w in words if w != "cat")
for score, word in reversed(ranked):
    print(f"  {word:<8} {score:.3f}  {'#' * round((score - 0.5) * 60)}")

# The classic trick: meaning behaves a bit like arithmetic.
target = [k - m + w for k, m, w in zip(vectors["king"], vectors["man"], vectors["woman"])]
best = max((w for w in words if w not in ("king", "man", "woman")), key=lambda w: cosine(target, vectors[w]))
print(f"\nking - man + woman  ~  {best}")
