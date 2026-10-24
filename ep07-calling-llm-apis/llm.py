"""One small helper so every demo can call Gemini or a local Ollama model the same way.

Messages use the common shape every provider understands in some form:
    [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}, ...]
The system prompt is passed separately, just like Anthropic's Messages API.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Reply:
    text: str
    finish_reason: str
    input_tokens: int
    output_tokens: int


def default_provider():
    return os.getenv("LLM_PROVIDER", "ollama")


# ---------- Ollama (OpenAI-compatible Chat Completions) ----------
def _ollama_client():
    from openai import OpenAI

    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    return OpenAI(base_url=f"{host}/v1", api_key="ollama")


def _ollama_messages(messages, system):
    return ([{"role": "system", "content": system}] if system else []) + messages


# ---------- Gemini (google-genai) ----------
def _gemini_contents(messages):
    from google.genai import types

    # Gemini calls the assistant role "model".
    return [
        types.Content(role="model" if m["role"] == "assistant" else "user", parts=[types.Part(text=m["content"])])
        for m in messages
    ]


def _gemini_config(system, max_tokens):
    from google.genai import types

    return types.GenerateContentConfig(system_instruction=system, max_output_tokens=max_tokens)


def chat(messages, system=None, provider=None, max_tokens=2000):
    """Send the whole conversation, get one reply back."""
    provider = provider or default_provider()
    if provider == "ollama":
        resp = _ollama_client().chat.completions.create(
            model=os.environ["OLLAMA_MODEL"], messages=_ollama_messages(messages, system), max_tokens=max_tokens
        )
        choice = resp.choices[0]
        return Reply(choice.message.content, choice.finish_reason, resp.usage.prompt_tokens, resp.usage.completion_tokens)
    if provider == "gemini":
        from google import genai

        resp = genai.Client().models.generate_content(
            model=os.environ["GEMINI_MODEL"], contents=_gemini_contents(messages), config=_gemini_config(system, max_tokens)
        )
        usage = resp.usage_metadata
        return Reply(resp.text or "", resp.candidates[0].finish_reason.name, usage.prompt_token_count,
                     (usage.candidates_token_count or 0) + (usage.thoughts_token_count or 0))
    raise ValueError(f"Unknown provider {provider!r}: use 'ollama' or 'gemini'")


def stream(messages, system=None, provider=None, max_tokens=2000):
    """Yield the reply piece by piece as it's generated."""
    provider = provider or default_provider()
    if provider == "ollama":
        chunks = _ollama_client().chat.completions.create(
            model=os.environ["OLLAMA_MODEL"], messages=_ollama_messages(messages, system),
            max_tokens=max_tokens, stream=True,
        )
        for chunk in chunks:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
        return
    if provider == "gemini":
        from google import genai

        for chunk in genai.Client().models.generate_content_stream(
            model=os.environ["GEMINI_MODEL"], contents=_gemini_contents(messages), config=_gemini_config(system, max_tokens)
        ):
            if chunk.text:
                yield chunk.text
        return
    raise ValueError(f"Unknown provider {provider!r}: use 'ollama' or 'gemini'")


def provider_from_args():
    """Read --provider ollama|gemini from the command line (default: LLM_PROVIDER or ollama)."""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=["ollama", "gemini"], default=default_provider())
    args, _ = parser.parse_known_args()
    return args.provider
