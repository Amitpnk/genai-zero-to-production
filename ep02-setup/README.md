# Episode 02: Dev Environment Setup

Python, uv, VS Code, API keys for Anthropic, OpenAI and AWS Bedrock, and how to never leak them.

## What you'll have at the end

One Python project that calls **Anthropic**, **OpenAI** and **AWS Bedrock**, with every key stored safely in `.env`. You're done when three smoke-test scripts each print a reply.

## Before you start

- A laptop running Windows, macOS or Linux
- A [GitHub](https://github.com) account
- A payment card for API billing (all providers are pay-as-you-go)
- An [AWS account](https://aws.amazon.com) (for Bedrock)

> Already have some of this? Skip ahead, but **don't skip Step 6** (`.env` hygiene).

## Steps at a glance

| Step | What | Done when |
| --- | --- | --- |
| 1 | Check Python | `python --version` shows 3.11+ (or you'll let uv install it) |
| 2 | Install uv | `uv --version` works |
| 3 | Get the code | `uv sync` finishes without errors |
| 4 | Set up VS Code | Status bar shows `.venv` |
| 5 | Get API keys | You have two keys and an AWS profile |
| 6 | Create `.env` | `.env` exists with real values and Git ignores it |
| 7 | Run smoke tests | All three scripts print a reply |

---

## Step 1: Check Python

This series needs **Python 3.11 or newer** (the videos use 3.12).

```bash
python --version        # macOS / Linux: python3 --version
```

Older or missing? That's fine. uv installs Python for you in Step 3.

## Step 2: Install uv

Every project needs its own isolated environment, so one project's packages don't break another's. There are two ways to do it:

|  | venv + pip | **uv** (used in this series) |
| --- | --- | --- |
| Comes from | Built into Python | Astral, a single install |
| Python versions | Install them yourself | `uv python install 3.12` |
| Dependencies | pip + `requirements.txt` | `pyproject.toml` + `uv.lock` |
| Reproducible | Only if you pin manually | Yes, via the lock file |
| Speed | Standard | Much faster installs |

Install uv:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen your terminal, then check it:

```bash
uv --version
```

## Step 3: Get the code

Clone this repo and install everything:

```bash
git clone <repo-url>
cd genai-zero-to-production
uv python install 3.12
uv sync
```

`uv sync` creates a `.venv` folder and installs the exact versions pinned in `uv.lock`. You never need to activate it: `uv run <command>` runs inside the environment for you.

<details>
<summary><b>Want to build a project from scratch instead?</b> (what the video shows)</summary>

```bash
uv init genai-engineering --python 3.12
cd genai-engineering
uv add anthropic openai boto3 python-dotenv
uv run python --version
```

This creates `.venv`, `pyproject.toml` and `uv.lock`.

</details>

<details>
<summary><b>Prefer classic venv + pip?</b></summary>

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install anthropic openai boto3 python-dotenv
```

With venv, run scripts with `python ...` instead of `uv run python ...`.

</details>

## Step 4: Set up VS Code

1. Install [VS Code](https://code.visualstudio.com/).
2. Open the project:
   ```bash
   code .
   ```
3. Install these extensions. VS Code will suggest them when you open this repo, because they're listed in `.vscode/extensions.json`:

   | Extension | Why |
   | --- | --- |
   | **Python + Pylance** | Run, debug, type-aware autocomplete |
   | **Jupyter** | Notebooks for quick experiments |
   | **Ruff** | Fast linter and formatter |
   | **DotENV** (optional) | Highlighting for `.env` files |

4. **Select the interpreter.** This is the step everyone forgets:
   - Press `Ctrl+Shift+P` (`Cmd+Shift+P` on Mac)
   - Type **Python: Select Interpreter**
   - Pick the one inside `.venv`

✅ **Check:** the bottom status bar shows `.venv`.

> **Red squiggles under imports?** You picked the wrong interpreter. Repeat step 4.

Format on save with Ruff is already turned on in `.vscode/settings.json`.

## Step 5: Get your API keys

Three providers, three ways to sign in:

| Provider | How you sign in | Variable in `.env` |
| --- | --- | --- |
| Anthropic | API key from the Console | `ANTHROPIC_API_KEY` |
| OpenAI | API key from the Platform | `OPENAI_API_KEY` |
| AWS Bedrock | Your AWS identity (no single key) | `AWS_PROFILE` |

> 💰 **Set a spending limit on every account today.** The experiments are small, but limits protect you if a key ever leaks.

### 5a. Anthropic

1. Sign in at [console.anthropic.com](https://console.anthropic.com) and add billing.
2. Go to **API Keys → Create Key** and name it `genai-course-dev`.
3. **Copy it now.** You only see it once.
4. Under **Limits**, set a monthly spend limit.
5. Pick a model from the [Anthropic models page](https://docs.anthropic.com/en/docs/about-claude/models) and note its model ID.

### 5b. OpenAI

1. Sign in at [platform.openai.com](https://platform.openai.com) and add billing.
2. Create a dedicated **project** for this course.
3. Go to **API keys → Create new secret key** and copy it once.
4. Set a budget under your organization's limits.
5. Note the model ID you want to use from the [OpenAI models page](https://platform.openai.com/docs/models).

### 5c. AWS Bedrock (three steps)

Bedrock has no single API key. You sign in with your AWS identity.

**1. Credentials:** install the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), then create a profile named `genai-course`:

```bash
aws configure sso --profile genai-course      # preferred: short-lived credentials
# or, for a personal dev account:
aws configure --profile genai-course          # access key + secret

aws sts get-caller-identity --profile genai-course   # confirms who you are
```

> Use `--profile genai-course` exactly. It must match `AWS_PROFILE` in your `.env`.

**2. Region and model access:** pick a Bedrock region (the videos use `us-east-1`). In the Bedrock console, check **model access** for the models you want. Some providers need a one-time access request or use-case form.

**3. Model ID:** copy the model ID or inference profile ID from the Bedrock model catalog. It goes in `.env`, never in code.

> **Why are model names in `.env`?** Model versions change often. You should never have to edit code just to switch models.

## Step 6: Create your `.env` (don't skip this)

### Five rules for API keys

1. **Never hardcode a key** in a `.py` file or notebook, not even for a test.
2. **`.env` goes in `.gitignore`** *before* you create the file.
3. **Commit a `.env.example`** with names and fake values only.
4. **Least privilege and limits:** one key per project, spend caps, short-lived AWS credentials.
5. **Leaked? Revoke immediately.** Deleting the commit isn't enough: Git history and forks keep it.

### The two files that protect you

This repo already has both:

- **`.gitignore`** lists `.env`, `.venv/`, `__pycache__/` and `.ipynb_checkpoints/`.
- **`.env.example`** is committed and has no secrets:

```ini
ANTHROPIC_API_KEY=your-anthropic-key
ANTHROPIC_MODEL=model-id-from-anthropic-docs
OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=model-id-from-openai-docs
AWS_PROFILE=genai-course
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=model-id-from-bedrock-catalog
```

### Create your own `.env`

```bash
cp .env.example .env
```

Open `.env` and replace every placeholder with your real keys and the model IDs from Step 5.

✅ **Check:** Git must not see `.env`:

```bash
git status          # .env must NOT appear in the list
git check-ignore .env   # should print: .env
```

The Anthropic and OpenAI SDKs read their keys from the environment automatically, and boto3 picks up `AWS_PROFILE`. Your code never touches the secret directly.

## Step 7: Run the smoke tests

Each script sends one small prompt and prints the reply. Run them from the **repo root**:

```bash
uv run python ep02-setup/hello_anthropic.py
uv run python ep02-setup/hello_openai.py
uv run python ep02-setup/hello_bedrock.py
```

If you're using SSO for AWS and your session has expired, sign in again first:

```bash
aws sso login --profile genai-course
```

✅ **Done when:** three providers give three replies, with zero secrets in code. 🎉

| File | Provider | API used |
| --- | --- | --- |
| [`hello_anthropic.py`](hello_anthropic.py) | Anthropic | Messages API |
| [`hello_openai.py`](hello_openai.py) | OpenAI | Responses API |
| [`hello_bedrock.py`](hello_bedrock.py) | AWS Bedrock | Converse API (same request shape for every Bedrock model) |

### If it fails

| Error | Likely cause | Fix |
| --- | --- | --- |
| `401` / `authentication_error` | Wrong or missing key | Check the key in `.env` |
| `AccessDeniedException` (Bedrock) | No model access or IAM permission | Request model access in your region, or check IAM |
| `KeyError: 'ANTHROPIC_MODEL'` (etc.) | Variable missing from `.env` | Add it, copying the name from `.env.example` |
| `ModuleNotFoundError` | Not running inside the project env | Use `uv run ...`, or run `uv sync` again |
| Token expired / SSO errors | AWS session timed out | `aws sso login --profile genai-course` |

Still stuck? Drop the error in the video comments, or open an issue on this repo.

---

## Interview question (FDE)

> **"A customer pushed an LLM API key to a public GitHub repo. What do you do?"**

Answer in this order:

1. **Revoke and rotate.** This stops the damage now.
2. **Check usage.** Look at logs and billing for anything unexpected.
3. **Clean history** with `git-filter-repo`, knowing that forks may still have the key.
4. **Prevent repeats:** `.env` in `.gitignore`, push protection and secret scanning on the repo, and a pre-commit scanner.

> **What interviewers listen for:** rotation comes **before** cleanup.

## Final checklist

- [ ] Python 3.11+ available (or installed by uv)
- [ ] `uv --version` works
- [ ] Repo cloned and `uv sync` succeeded
- [ ] VS Code shows `.venv` as the interpreter
- [ ] Spend limits set on Anthropic, OpenAI and AWS
- [ ] `.env` created from `.env.example`, and `git status` doesn't show it
- [ ] All three smoke tests print a reply

## Staying up to date

```bash
git pull
uv sync
```

## Next up

**[Episode 03: How LLMs actually work](../ep03-how-llms-work/):** tokens, embeddings and attention, without heavy maths.
