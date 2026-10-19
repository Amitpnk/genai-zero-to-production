# Tracing LLM apps

See every step of an LLM app (prompts, model calls, tool calls, tokens, latency and cost) so you can debug it and improve it.

> **Draft** · Preview of Module 9 (Evals & Observability) · Tool-specific setup will be finalised in Module 9; SDKs change often, so follow each tool's current quick start.

## Why tracing

A single user question in a RAG or agent app can trigger many steps. Without tracing, you only see the final answer. With it, you see **which step went wrong**:

```text
trace: "What's our refund policy for damaged items?"      2.8 s · $0.0031
├── span: embed question                       0.2 s
├── span: vector search (top 5)                0.1 s
├── span: LLM call (gemini-3.5-flash-lite)     2.3 s · 1,840 in / 96 out tokens
└── span: format answer                        0.0 s
```

| Term | Meaning |
| --- | --- |
| **Trace** | Everything that happened for one request |
| **Span** | One step inside it (an LLM call, a retrieval, a tool call) |
| **Attributes** | Details on a span: model, tokens, cost, prompt, output |
| **Session** | Several traces from one conversation or user |

## What to record on every LLM call

- Model ID and parameters (temperature, max tokens)
- Input and output (redact personal data and secrets)
- Token usage: input, output, thinking
- Latency: time to first token and total
- Finish reason and any error or retry
- A **version** for your prompt, so you can compare changes

## Tools

| Tool | Notes |
| --- | --- |
| **Langfuse** | Open source; self-host or cloud; traces, prompt management, evals |
| **LangSmith** | From the LangChain team; works with or without LangChain |
| **OpenTelemetry** | The vendor-neutral standard, with emerging **GenAI semantic conventions**; send traces to many backends |
| **Cloud native** | e.g. Amazon CloudWatch / X-Ray for apps on AWS (Module 10) |

## Start simple: structured logs

Before adopting a tool, a few lines of logging already help:

```python
import json
import logging
import time

log = logging.getLogger("llm")


def traced_call(name, model, call):
    start = time.perf_counter()
    result = call()
    usage = result.usage_metadata                       # Gemini; other SDKs: result.usage
    log.info(json.dumps({
        "span": name,
        "model": model,
        "input_tokens": usage.prompt_token_count,
        "output_tokens": usage.candidates_token_count,
        "thinking_tokens": usage.thoughts_token_count,
        "seconds": round(time.perf_counter() - start, 2),
    }))
    return result
```

Then move to a tracing tool when you have multi-step flows, several people debugging, or need dashboards.

## Habits

- **Trace in development, not only production**: it's the fastest way to understand an agent.
- **Sample** in high-traffic production if cost or volume is a concern.
- **Redact** personal data before it leaves your system.
- **Link traces to evals** (Module 9): when a test fails, open its trace.
