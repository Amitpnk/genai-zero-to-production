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

## Roadmap: 10 modules + capstone

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
| Capstone | Ship an ask-your-docs agent on AWS | 42 |

## Keep your keys safe

Never commit `.env`. It is already in `.gitignore`. If a key leaks, revoke it first, then clean up.
