# GenAI Engineering: Zero to Production

Companion code for the GenAI Engineering YouTube series: from your first API call to a production AI agent on AWS.

## Get started

You need Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone <repo-url>
cd genai-zero-to-production
uv sync
cp .env.example .env      # then paste real values
uv run python ep02-setup/hello_anthropic.py
```

Fell behind? Run `git pull`, then `uv sync`. Found a bug? Open an issue.

## Repo layout

```
genai-zero-to-production/
├── README.md          # this episode index
├── pyproject.toml     # dependencies
├── uv.lock            # pinned versions (created by uv sync)
├── .env.example       # variable names, fake values; copy to .env
├── .gitignore
├── shared/            # helpers reused across episodes
├── ep01-what-is-genai-engineering/
├── ep02-setup/
├── ep03-how-llms-work/
└── ...                # one folder per episode
```

## Episodes

| # | Episode | Folder |
| --- | --- | --- |
| 01 | What is GenAI Engineering? | [ep01-what-is-genai-engineering](ep01-what-is-genai-engineering/) |
| 02 | Dev Environment Setup | [ep02-setup](ep02-setup/) |
| 03 | How LLMs actually work | [ep03-how-llms-work](ep03-how-llms-work/) |
| 04 | Tokens and context windows | [ep04-tokens-and-context-windows](ep04-tokens-and-context-windows/) |
| 05 | Sampling parameters | [ep05-sampling-parameters](ep05-sampling-parameters/) |
| 06 | The model landscape | [ep06-model-landscape](ep06-model-landscape/) |

## Syllabus: 42 episodes, 10 modules + capstone

Each episode is 10–20 minutes, builds on the one before, and ends with a hands-on demo in this repo. Modules end with an interview question for AI Engineer and Forward Deployed Engineer (FDE) roles.

### At a glance

| Module | Topic | Episodes |
| --- | --- | --- |
| 0 | Orientation | 1–2 |
| 1 | LLM Foundations | 3–7 |
| 2 | Prompt Engineering | 8–11 |
| 3 | Embeddings and Vector Databases | 12–15 |
| 4 | RAG: Retrieval-Augmented Generation | 16–21 |
| 5 | Fine-tuning and Open Models | 22–24 |
| 6 | Multimodal GenAI | 25–26 |
| 7 | Agentic AI Fundamentals | 27–31 |
| 8 | MCP and Multi-Agent Systems | 32–35 |
| 9 | Evaluation and Observability | 36–38 |
| 10 | Production and Deployment on AWS | 39–41 |
| Capstone | Ship an Ask-your-docs agent on AWS | 42 |


### Module 0: Orientation (2 episodes)

| Ep | Title | What it covers |
| --- | --- | --- |
| 1 | What is GenAI Engineering? | How it differs from ML engineering and data science, what the playlist covers, and the roadmap |
| 2 | Dev setup | Python, uv/venv, VS Code, API keys (Anthropic, OpenAI, Google Gemini, AWS Bedrock), .env hygiene, and the companion GitHub repo walkthrough |

### Module 1: LLM Foundations (5 episodes)

| Ep | Title | What it covers |
| --- | --- | --- |
| 3 | How LLMs work, intuitively | Tokens, embeddings, attention, next-token prediction without the heavy math |
| 4 | Tokenization and context windows | Why token counts matter for cost, latency, and truncation |
| 5 | Sampling parameters | Temperature, top-p, max tokens, stop sequences, with live side-by-side outputs |
| 6 | The model landscape | Closed vs open-weight models, model families, and how to choose for a use case |
| 7 | Calling LLM APIs | Messages API, system prompts, streaming, multi-turn chat in pure Python |

> **Interview angle (FDE):** "Explain attention to a non-technical customer in 60 seconds."

### Module 2: Prompt Engineering (4 episodes)

| Ep | Title | What it covers |
| --- | --- | --- |
| 8 | Prompt anatomy | Role, context, task, constraints, examples, output format |
| 9 | Prompting techniques | Zero-shot, few-shot, chain-of-thought, and when each actually helps |
| 10 | Structured outputs | JSON mode, schemas with Pydantic, validation and retries |
| 11 | Prompt injection and jailbreak basics | How attacks work and defensive patterns |

> **Interview angle (FDE):** "A customer's prompt works 80% of the time. How do you debug it?"

### Module 3: Embeddings and Vector Databases (4 episodes)

| Ep | Title | What it covers |
| --- | --- | --- |
| 12 | Embeddings explained | Semantic similarity, cosine distance, visualizing vector space |
| 13 | Vector DBs compared | FAISS, Chroma, pgvector, Pinecone, OpenSearch |
| 14 | Chunking strategies | Fixed, recursive, semantic, document-aware |
| 15 | Hands-on: semantic search | Build a semantic search engine over your own PDFs |

### Module 4: RAG: Retrieval-Augmented Generation (6 episodes)

| Ep | Title | What it covers |
| --- | --- | --- |
| 16 | Why RAG | Hallucinations, freshness, grounding, RAG vs fine-tuning |
| 17 | Naive RAG from scratch | Build RAG without any framework |
| 18 | RAG with LangChain / LlamaIndex | When frameworks help and when they hide too much |
| 19 | Advanced retrieval | Hybrid search (BM25 + vectors), re-ranking, query rewriting, HyDE |
| 20 | Graph RAG vs Vector RAG | Knowledge graphs with Neo4j / Amazon Neptune, and when relationships beat similarity |
| 21 | Evaluating RAG | Faithfulness, context precision/recall, RAGAS, building a golden dataset |

> **Interview angle (FDE):** "Design a RAG system for 10M legal documents."

### Module 5: Fine-tuning and Open Models (3 episodes)

| Ep | Title | What it covers |
| --- | --- | --- |
| 22 | When to fine-tune (and when you shouldn't) | Cost, data needs, alternatives |
| 23 | LoRA / QLoRA hands-on | Fine-tune a small open model with Hugging Face |
| 24 | Running models locally | Ollama, quantization, latency trade-offs |

### Module 6: Multimodal GenAI (2 episodes)

| Ep | Title | What it covers |
| --- | --- | --- |
| 25 | Vision + language | Image understanding, document/OCR extraction, chart reading |
| 26 | Speech pipelines | Whisper transcription + LLM summarization |

### Module 7: Agentic AI Fundamentals (5 episodes)

| Ep | Title | What it covers |
| --- | --- | --- |
| 27 | What is an agent? | The LLM + tools + loop + memory mental model |
| 28 | Tool / function calling | Build tool calling from scratch |
| 29 | Agent patterns | ReAct, plan-and-execute, reflection, routing |
| 30 | Agent memory | Short-term, long-term, vector and graph memory |
| 31 | Build a research agent | End to end |

### Module 8: MCP and Multi-Agent Systems (4 episodes)

| Ep | Title | What it covers |
| --- | --- | --- |
| 32 | Model Context Protocol explained | Hosts, clients, servers, tools/resources/prompts |
| 33 | Build your own MCP server | e.g., Jira or GitHub tools, connected to Claude |
| 34 | Multi-agent orchestration | LangGraph, CrewAI, supervisor vs swarm patterns |
| 35 | Human-in-the-loop and guardrails | Controls for agents taking real actions |

> **Interview angle (FDE):** "A customer wants agents to touch production systems. What controls do you propose?"

### Module 9: Evaluation and Observability (3 episodes)

| Ep | Title | What it covers |
| --- | --- | --- |
| 36 | LLM evals 101 | Offline vs online, LLM-as-judge, rubric design |
| 37 | Agent evaluation | Trajectory evals, tool-call accuracy, task success rates |
| 38 | Observability | Tracing with LangSmith / Langfuse / OpenTelemetry, cost and latency dashboards |

### Module 10: Production and Deployment on AWS (3 episodes)

| Ep | Title | What it covers |
| --- | --- | --- |
| 39 | Serving GenAI apps | FastAPI, streaming responses, caching, rate limits |
| 40 | Deploy to AWS | Bedrock for models, ECS Fargate vs App Runner for the app, secrets and IAM |
| 41 | Cost optimization and security | Prompt caching, model routing, PII handling, responsible AI |

### Capstone (1–2 episodes)

| Ep | Title | What it covers |
| --- | --- | --- |
| 42 | Build and ship | An enterprise "Ask-your-docs" agent with RAG + MCP tools + evals, deployed on AWS, with a full architecture walkthrough |

## Keep your keys safe

Never commit `.env`. It is already in `.gitignore`. If a key leaks, revoke it first, then clean up.
