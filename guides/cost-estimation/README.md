# Estimating LLM costs

Work out what an LLM feature will cost before you ship it, and the levers that bring the bill down.

> **Draft** · Builds on Episodes 4 and 6; full detail in Module 10 · All prices here are **examples** to show the maths. Always use your provider's current pricing page.

## The formula

```text
cost per request = input_tokens  × input_price  / 1,000,000
                 + output_tokens × output_price / 1,000,000      (output includes hidden thinking)

monthly cost     = cost per request × requests per user per day × users × 30
```

## Worked example

A support chatbot. Example prices: **$0.50** per million input tokens, **$3.00** per million output tokens.

| Item | Value |
| --- | --- |
| System prompt + tools | 800 tokens |
| Average chat history sent | 1,500 tokens |
| Retrieved documents | 2,000 tokens |
| User question | 50 tokens |
| **Input per request** | **4,350 tokens** |
| Visible answer | 200 tokens |
| Hidden thinking | 300 tokens |
| **Output per request** | **500 tokens** |

```text
input  = 4,350 × $0.50 / 1M = $0.0022
output =   500 × $3.00 / 1M = $0.0015
per request                 = $0.0037

1,000 users × 10 requests/day × 30 days = 300,000 requests
monthly ≈ 300,000 × $0.0037 ≈ $1,100
```

Notice where the money goes: **input dominates** here because history and documents are resent on every request ([Episode 4](../../ep04-tokens-and-context-windows/)).

## Estimate it in code

```python
PRICE_IN, PRICE_OUT = 0.50, 3.00          # EXAMPLE prices per 1M tokens


def monthly_cost(tokens_in, tokens_out, users, requests_per_day, days=30):
    per_request = (tokens_in * PRICE_IN + tokens_out * PRICE_OUT) / 1_000_000
    return per_request * users * requests_per_day * days


print(f"${monthly_cost(4350, 500, users=1000, requests_per_day=10):,.0f} per month")   # $1,102 per month
```

Use **real token counts** from the `usage` field of actual responses, not guesses.

## Levers, roughly in order of impact

| Lever | Typical effect | Where |
| --- | --- | --- |
| **Smaller model / tier** | Often several times cheaper | [Episode 6](../../ep06-model-landscape/) |
| **Send less context** | Fewer input tokens on every call | RAG (Module 4), trimming history |
| **Prompt caching** | Repeated prompt prefixes billed at a discount | Module 10 |
| **Batch API** | Discounted price for non-urgent jobs, results within hours | Module 10 |
| **Cap output** | `max_tokens`, ask for brevity, limit thinking | [Episode 5](../../ep05-sampling-parameters/) |
| **Cache whole answers** | Zero cost for repeated questions | Module 10 |
| **Route by difficulty** | Small model first, escalate only when needed | Module 10 |

## Don't forget

- **Embeddings** for indexing documents (usually cheap, but it adds up at scale)
- **Retries** after errors resend the whole request
- **Evals** in CI run the model on your test set every time
- **Free tiers** have daily limits; plan for paid limits in production ([API errors guide](../api-errors/))
- **Set budget alerts** on every account
