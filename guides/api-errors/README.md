# API errors and rate limits

What 400, 401, 403, 404, 429 and 5xx errors mean when calling LLM APIs, which ones to retry, and how to retry safely.

> **Draft** · Used in every episode · The 429 examples are real errors hit while building Episodes 3–6.

## The one rule

> **Retry the temporary errors (429, 5xx, timeouts). Fix the permanent ones (400, 401, 403, 404).** Retrying a bad key just wastes time.

## Status codes at a glance

| Code | Meaning | Retry? | Usual fix |
| --- | --- | --- | --- |
| **400** | Bad request: invalid parameter, prompt too long, bad JSON | ❌ | Read the message; fix the request |
| **401** | Not authenticated: missing or wrong key | ❌ | Check `.env`; is the key revoked? |
| **403** | Authenticated, but not allowed | ❌ | Model access, IAM permission, or region |
| **404** | Model or endpoint not found | ❌ | Check the model ID; it may be retired or not available to you |
| **408 / timeout** | Took too long | ✅ | Retry; consider streaming or a smaller request |
| **429** | Rate limit or quota exceeded | ✅ (with backoff) | Slow down, wait, or raise your limit |
| **500 / 502 / 503 / 529** | Provider-side problem or overloaded | ✅ (with backoff) | Retry; fall back to another model if it persists |

## Real 429s from this course

**Daily free-tier quota used up** (Gemini, while testing Episodes 3–6):

```text
429 RESOURCE_EXHAUSTED ... Quota exceeded for metric:
generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-3.8-flash
Please retry in 7h50m
```

**Model not on the free tier at all** (Gemini Pro): also `429 RESOURCE_EXHAUSTED`. Retrying never helps here: you need billing or a different model.

> **Read the message, not just the code.** A per-minute rate limit clears in seconds; a daily quota or a "no free tier" limit doesn't. Many providers include a `Retry-After` header or a retry delay in the error.

## Kinds of limits

| Limit | Example | What it means |
| --- | --- | --- |
| **Requests per minute (RPM)** | 15 requests/minute | Too many calls too fast |
| **Tokens per minute (TPM)** | 1M input tokens/minute | Big prompts hit this before RPM |
| **Requests per day (RPD)** | 20 requests/day (free tier) | Resets daily, not in seconds |
| **Spend limit** | $50/month cap | Calls fail until the next period or you raise it |

Limits are usually **per model** and depend on your **tier** (free, paid, higher usage tiers). Check each provider's rate-limit page.

## Retry with exponential backoff and jitter

Wait longer after each failure (1 s, 2 s, 4 s…), plus a little randomness so many clients don't retry at the same moment:

```python
import random
import time

RETRYABLE = {408, 429, 500, 502, 503, 504, 529}


def call_with_retries(make_call, max_attempts=5):
    for attempt in range(max_attempts):
        try:
            return make_call()
        except Exception as error:
            status = getattr(error, "status_code", None) or getattr(error, "code", None)
            if status not in RETRYABLE or attempt == max_attempts - 1:
                raise                                   # permanent error, or out of attempts
            delay = min(2 ** attempt, 30) + random.uniform(0, 1)
            print(f"Got {status}, retrying in {delay:.1f}s...")
            time.sleep(delay)
```

Usage: `call_with_retries(lambda: client.models.generate_content(model=..., contents=...))`

**Built-in retries:** the Anthropic and OpenAI SDKs already retry connection errors, 408, 409, 429 and 5xx twice by default (`max_retries=` to change). Don't stack your own retry loop on top without thinking about the total wait.

> For production, the `tenacity` package gives you retries, backoff and jitter as a decorator.

## Avoid hitting limits in the first place

- **Cache** answers to repeated questions.
- **Batch** work instead of firing hundreds of calls at once; providers offer cheaper **batch APIs** for non-urgent jobs.
- Use **smaller prompts and smaller models** where they pass your tests ([Episode 6](../../ep06-model-landscape/)).
- **Limit concurrency**: a queue with a few workers beats 100 parallel requests.
- **Fallback:** if the main model is overloaded, try a second model or provider.

## Provider-specific errors

| | Rate limited | Overloaded | Bad key | No access |
| --- | --- | --- | --- | --- |
| **Anthropic** | `rate_limit_error` (429) | `overloaded_error` (529) | `authentication_error` (401) | `permission_error` (403), `not_found_error` (404) |
| **OpenAI** | `rate_limit_exceeded` / `insufficient_quota` (429) | 500 / 503 | `invalid_api_key` (401) | `model_not_found` (404) |
| **Gemini** | `RESOURCE_EXHAUSTED` (429) | `UNAVAILABLE` (503) | `API key not valid` (400) | `NOT_FOUND` (404) |
| **Bedrock** | `ThrottlingException` | `ServiceUnavailableException`, `ModelNotReadyException` | `UnrecognizedClientException`, expired SSO token | `AccessDeniedException` |
| **Ollama** | (none: local) | slow, not an error | (none) | `model not found` → `ollama pull` |

> `insufficient_quota` from OpenAI means **out of credit**, not "too fast": add billing rather than retrying.
