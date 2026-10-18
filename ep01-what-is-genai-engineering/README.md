# Episode 01: What is GenAI Engineering?

How it differs from ML engineering and data science, and the roadmap for this playlist.

> **No code in this episode.** Read these notes, then set up your environment in [Episode 02](../ep02-setup/).

## What you'll learn

- Define GenAI Engineering in one sentence
- Tell a GenAI engineer apart from a data scientist and an ML engineer
- Name the six things a GenAI engineer does
- Know the layers of a GenAI application and the path this playlist follows

---

## 1. The big idea

**You don't need to train a model to build serious AI products.**
You need to engineer around one: context, tools, evaluation and production.

A few years ago, a feature that could read documents or answer questions needed a research team and a custom model. Today, one engineer can ship it in a week by building on top of an existing model.

## 2. Definition

> **GenAI Engineering** is building reliable, production-ready applications on top of foundation models.

The key words are *on top of*. Companies like Anthropic, OpenAI, Google, Meta and Mistral build the models. Your job is everything around the model.

```
Foundation model  +  Your data  +  Tools  +  Evaluation  =  A product
```

**The model is the engine. You build the car.**

## 3. Three roles, three starting points

|  | Data Scientist | ML Engineer | GenAI Engineer |
| --- | --- | --- | --- |
| **Starts with** | A business question | Data and a prediction task | A pre-trained foundation model |
| **Core work** | Analysis, statistics, experiments | Feature pipelines, training, serving | Context, RAG, tools, agents, evals |
| **Typical output** | Insights, dashboards, reports | A trained model in production | An AI app or agent |
| **Key question** | What does the data tell us? | How accurate can the model get? | Does the system work reliably? |

These roles overlap. Many strong GenAI engineers come from software engineering, not ML.

## 4. Where the effort goes

| Classic ML: *training the model* | GenAI Engineering: *everything around the model* |
| --- | --- |
| Labeling and cleaning data | Context and retrieval |
| Feature engineering | Tools and agents |
| Training and tuning | Evals, cost and guardrails |

- In classic ML you ask: *"How do I make the model more accurate?"*
- In GenAI engineering you ask: *"How do I give the model the right information and tools, and prove it's working?"*

**If you can write Python and call an API, you can start today.**

## 5. Six things a GenAI engineer does

| # | Skill | What it means |
| --- | --- | --- |
| 1 | **Prompt & context design** | What the model sees: instructions, examples, output formats |
| 2 | **Retrieval (RAG)** | Ground answers in your own documents and data instead of guessing |
| 3 | **Agents & tools** | Let the model call APIs, query databases, plug in MCP servers |
| 4 | **Evaluation** | Measure quality. This is the step that turns a demo into a product |
| 5 | **Deployment** | APIs, scaling and monitoring on platforms like AWS |
| 6 | **Cost & guardrails** | Token spend, latency, prompt injection, sensitive data |

> Skill 4 is the one most people skip. If you can't measure it, you can't ship it.

## 6. The GenAI application stack

Read it bottom to top:

| Layer | Examples |
| --- | --- |
| **Application** | Chat UI, APIs, Slack bots |
| **Orchestration** | Chains, agents, LangGraph |
| **Context** | RAG, vector DBs, knowledge graphs, MCP |
| **Models** | Claude, GPT, Bedrock, open-weight models |
| **Infrastructure** | AWS compute, containers, secrets |

**Evaluation & observability** runs alongside every layer: traces, evals and cost dashboards.

Every module in this playlist maps to one layer. By the end, you'll have built each one yourself.

## 7. Who this for

- **Software developers** who want to add AI to what they already build
- **ML and data folks** moving from training models to building with them
- **Students and career switchers** who want a structured path, not random tutorials
- **Interview prep** for AI Engineer and Forward Deployed Engineer (FDE) roles

**You need:** basic Python and comfort with APIs. No PhD, no GPU.

## 8. The roadmap: 10 modules + capstone

| Module | Topic | Episodes |
| --- | --- | --- |
| 01 | LLM Foundations | 3–7 |
| 02 | Prompt Engineering | 8–11 |
| 03 | Embeddings & Vector DBs | 12–15 |
| 04 | RAG & Graph RAG | 16–21 |
| 05 | Fine-tuning & Open Models | 22–24 |
| 06 | Multimodal GenAI | 25–26 |
| 07 | Agentic AI Fundamentals | 27–31 |
| 08 | MCP & Multi-Agent | 32–35 |
| 09 | Evals & Observability | 36–38 |
| 10 | Production on AWS | 39–41 |
| **Capstone** | Ship an ask-your-docs agent on AWS | 42 |

**Where we end up:** a production AI agent with RAG + MCP tools + evals + tracing, deployed on AWS with Bedrock and ECS Fargate. Not a notebook demo.

## 9. How every episode works

1. **Hook:** the why, in seconds
2. **Concept:** explained visually
3. **Live code:** build it together
4. **Recap:** lock in the idea
5. **Next:** what's coming up

All code lives in this repo, one folder per episode (`ep02-setup/`, `ep03-how-llms-work/`, ...).

---

## Interview question (AI Engineer / FDE)

> **"How is GenAI engineering different from ML engineering?"**

**A 30-second answer:**

> ML engineering trains and serves task-specific models on your own data. GenAI engineering starts from a pre-trained foundation model and builds everything around it: context and retrieval, tools, agent orchestration and evaluation. The core risk shifts from model accuracy to system reliability: hallucinations, cost, latency and safety.

Practise it: say it out loud in your own words before moving on.

## Recap

- GenAI Engineering = building reliable products **on top of** foundation models.
- The work moves from **training** to **context, tools and evaluation**.
- Ten modules plus a capstone take you from your first API call to a deployed agent.

## Next up

**[Episode 02: Dev Environment Setup](../ep02-setup/):** Python, uv, VS Code and API keys, so you're ready to write code from Episode 3.
