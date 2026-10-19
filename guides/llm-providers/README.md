# LLM provider cheat sheet

The same jobs in Anthropic, OpenAI, Google Gemini, AWS Bedrock and Ollama: install, sign in, first call, system prompts, streaming, chat, parameters and errors.

> **Draft** · Supports Episodes 2, 5 and 7 · The Ollama example was run live; the Gemini calls match the ones run in Episodes 2–6. Anthropic, OpenAI and Bedrock examples follow each SDK's documented API but weren't run here (no keys). SDKs change: check the current docs.

## At a glance

| | Anthropic | OpenAI | Gemini | Bedrock | Ollama |
| --- | --- | --- | --- | --- | --- |
| **Package** | `anthropic` | `openai` | `google-genai` | `boto3` | none (HTTP) or `openai` |
| **Auth** | `ANTHROPIC_API_KEY` | `OPENAI_API_KEY` | `GEMINI_API_KEY` | AWS profile (`AWS_PROFILE`) | none (local) |
| **Main call** | `messages.create` | `responses.create` | `models.generate_content` | `converse` | `POST /api/chat` |
| **System prompt** | `system=` | `instructions=` | `system_instruction=` (in config) | `system=[{"text": ...}]` | a `system` message |
| **Max output** | `max_tokens` (**required**) | `max_output_tokens` | `max_output_tokens` | `inferenceConfig.maxTokens` | `options.num_predict` |
| **Why it stopped** | `stop_reason` | `status` / `incomplete_details` | `finish_reason` | `stopReason` | `done_reason` |
| **Token usage** | `usage.input_tokens` / `output_tokens` | `usage.input_tokens` / `output_tokens` | `usage_metadata` | `usage.inputTokens` / `outputTokens` | `prompt_eval_count` / `eval_count` |

Install everything used in this course:

```bash
uv add anthropic openai google-genai boto3 python-dotenv
```

---

## Anthropic (Claude)

```python
import os
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

msg = client.messages.create(
    model=os.environ["ANTHROPIC_MODEL"],
    max_tokens=500,                      # required
    system="You are a concise assistant.",
    messages=[{"role": "user", "content": "Explain tokens in one sentence."}],
)
print(msg.content[0].text)
print(msg.stop_reason, msg.usage.input_tokens, msg.usage.output_tokens)
```

**Streaming:**

```python
with client.messages.stream(
    model=os.environ["ANTHROPIC_MODEL"], max_tokens=500,
    messages=[{"role": "user", "content": "Write a haiku about Python."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

**Multi-turn:** send the whole history each time, alternating `user` and `assistant` messages.

**Count tokens before sending:** `client.messages.count_tokens(model=..., messages=[...]).input_tokens`

## OpenAI (GPT)

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()  # reads OPENAI_API_KEY

response = client.responses.create(
    model=os.environ["OPENAI_MODEL"],
    instructions="You are a concise assistant.",
    input="Explain tokens in one sentence.",
    max_output_tokens=500,
)
print(response.output_text)
print(response.usage.input_tokens, response.usage.output_tokens)
```

**Streaming:**

```python
stream = client.responses.create(model=os.environ["OPENAI_MODEL"], input="Write a haiku about Python.", stream=True)
for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
```

**Multi-turn:** pass a list of `{"role": ..., "content": ...}` items as `input`, or continue with `previous_response_id=response.id`.

> The older **Chat Completions** API (`client.chat.completions.create(messages=[...])`) is still widely used and is what many other tools copy (including Ollama's compatible endpoint).

## Google Gemini

```python
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()  # reads GEMINI_API_KEY

reply = client.models.generate_content(
    model=os.environ["GEMINI_MODEL"],
    contents="Explain tokens in one sentence.",
    config=types.GenerateContentConfig(
        system_instruction="You are a concise assistant.",
        max_output_tokens=2000,           # includes hidden thinking on reasoning models
    ),
)
print(reply.text)
print(reply.candidates[0].finish_reason, reply.usage_metadata)
```

**Streaming:**

```python
for chunk in client.models.generate_content_stream(model=os.environ["GEMINI_MODEL"], contents="Write a haiku about Python."):
    print(chunk.text or "", end="", flush=True)
```

**Multi-turn:** `chat = client.chats.create(model=...)`, then `chat.send_message("...")` keeps the history for you.

**Count tokens before sending:** `client.models.count_tokens(model=..., contents=...)` (free).

## AWS Bedrock

```python
import os
import boto3
from dotenv import load_dotenv

load_dotenv()
session = boto3.Session(profile_name=os.getenv("AWS_PROFILE"), region_name=os.environ["AWS_REGION"])
bedrock = session.client("bedrock-runtime")

resp = bedrock.converse(
    modelId=os.environ["BEDROCK_MODEL_ID"],
    system=[{"text": "You are a concise assistant."}],
    messages=[{"role": "user", "content": [{"text": "Explain tokens in one sentence."}]}],
    inferenceConfig={"maxTokens": 500, "temperature": 0.3},
)
print(resp["output"]["message"]["content"][0]["text"])
print(resp["stopReason"], resp["usage"])
```

**Streaming:** `converse_stream(...)`, then read `contentBlockDelta` events from `resp["stream"]`.

> The **Converse API** uses the same request shape for every Bedrock model, so switching models is just a new `modelId`. Setup help: [AWS CLI and Bedrock setup](../aws-bedrock/).

## Ollama (local)

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
reply = client.chat.completions.create(
    model="gemma3:1b",
    messages=[{"role": "system", "content": "You are a concise assistant."},
              {"role": "user", "content": "Explain tokens in one sentence."}],
)
print(reply.choices[0].message.content)
```

More in the [Ollama cheat sheet](../ollama/).

---

## Common errors by provider

| Problem | Anthropic | OpenAI | Gemini | Bedrock |
| --- | --- | --- | --- | --- |
| Bad or missing key | `401 authentication_error` | `401 invalid_api_key` | `400 API key not valid` | `UnrecognizedClientException` / expired SSO token |
| No access to model | `403` / `404 not_found_error` | `404 model_not_found` | `404 NOT_FOUND` | `AccessDeniedException` |
| Too many requests | `429 rate_limit_error` | `429 rate_limit_exceeded` | `429 RESOURCE_EXHAUSTED` | `ThrottlingException` |
| Provider busy | `529 overloaded_error` | `500` / `503` | `503 UNAVAILABLE` | `ServiceUnavailableException` |

What to do about each: [API errors and rate limits](../api-errors/).

## Tips that apply everywhere

- Keep **model IDs in `.env`**, never in code.
- Always **check the stop reason**: a length stop means a cut-off answer.
- **Log token usage** from every response.
- The Anthropic and OpenAI SDKs **retry some errors automatically** (2 retries by default; change with `max_retries=`).
