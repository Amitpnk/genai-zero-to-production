"""A multi-turn chat in plain Python. The API has no memory, so we keep the history ourselves.

    uv run python ep07-calling-llm-apis/chat.py                 # chat interactively (/reset, /exit)
    uv run python ep07-calling-llm-apis/chat.py --demo          # scripted demo, with and without history
    uv run python ep07-calling-llm-apis/chat.py --provider gemini
"""

import sys

from shared.llm import provider_from_args, stream

SYSTEM = "You are a friendly, concise assistant. Keep answers under 3 sentences."


def ask(history, text, provider, remember=True):
    """Add the user's message, stream the reply, and (optionally) remember both."""
    messages = history + [{"role": "user", "content": text}]
    reply = ""
    for piece in stream(messages, system=SYSTEM, provider=provider, max_tokens=300):
        print(piece, end="", flush=True)
        reply += piece
    print()
    if remember:
        history += [{"role": "user", "content": text}, {"role": "assistant", "content": reply}]
    return history


def demo(provider):
    script = ["Hi! My name is Asha and I'm learning GenAI.", "What's my name, and what am I learning?"]
    for remember in (True, False):
        print(f"\n===== {'WITH' if remember else 'WITHOUT'} history =====")
        history = []
        for text in script:
            print(f"\nYou: {text}\nAI:  ", end="")
            history = ask(history, text, provider, remember)
            print(f"     (messages sent next turn: {len(history) + 1})")


def interactive(provider):
    print(f"Chatting with {provider}. Commands: /reset, /exit\n")
    history = []
    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if text == "/exit":
            break
        if text == "/reset":
            history = []
            print("(history cleared)\n")
            continue
        if not text:
            continue
        print("AI:  ", end="")
        history = ask(history, text, provider)
        print(f"     ({len(history)} messages in history)\n")


if __name__ == "__main__":
    provider = provider_from_args()
    demo(provider) if "--demo" in sys.argv else interactive(provider)
