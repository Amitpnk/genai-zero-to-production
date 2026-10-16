# Episode 02: Dev Environment Setup

Python, uv, VS Code, API keys for Anthropic, OpenAI and AWS Bedrock, and how to never leak them.

## Run the smoke tests

From the repo root:

```bash
uv sync
cp .env.example .env      # then paste real values
uv run python ep02-setup/hello_anthropic.py
uv run python ep02-setup/hello_openai.py
uv run python ep02-setup/hello_bedrock.py
```

## If it fails

| Error | Fix |
| --- | --- |
| `401` / auth error | Check the key in `.env` |
| `AccessDenied` (Bedrock) | Request model access in your region, or check IAM permissions |
| `KeyError` | The variable is missing from `.env` |

For Bedrock, sign in first with `aws sso login --profile genai-course`, then confirm with `aws sts get-caller-identity`.

## Five rules for API keys

1. Never hardcode a key in a `.py` file or notebook, not even for a test.
2. `.env` goes in `.gitignore` before you create the file.
3. Commit a `.env.example` with names and fake values only.
4. Least privilege and limits: one key per project, spend caps, short-lived AWS credentials.
5. Leaked? Revoke immediately. Deleting the commit isn't enough.
