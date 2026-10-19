# Docker for Python AI apps

Package a uv-based Python app into a container so it runs the same everywhere: your laptop, CI and AWS (ECS Fargate in Module 10).

> **Draft** · Preview of Module 10 (Production on AWS) · Dockerfile pattern follows uv's documented Docker integration; will be built and tested in Module 10.

## Key ideas

| Term | Meaning |
| --- | --- |
| **Image** | A packaged, read-only snapshot of your app and everything it needs |
| **Container** | A running instance of an image |
| **Dockerfile** | The recipe that builds an image |
| **Registry** | Where images are stored (Docker Hub, Amazon ECR) |

## A Dockerfile for a uv project

```dockerfile
FROM python:3.12-slim

# Bring in uv (pin a version you've tested)
COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /uvx /bin/

WORKDIR /app

# 1) Install dependencies first (cached unless pyproject/uv.lock change)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# 2) Then copy the app code
COPY . .
RUN uv sync --frozen --no-dev

# Run as a non-root user
RUN useradd --create-home app
USER app

CMD ["uv", "run", "--no-sync", "python", "app.py"]
```

- `--frozen` uses `uv.lock` exactly, and fails if it's out of date: reproducible builds.
- Copying `pyproject.toml` + `uv.lock` **before** the code means dependency installs are cached between builds.
- `--no-dev` leaves out notebooks, linters and test tools.

## .dockerignore (just as important)

```text
.env
.venv/
__pycache__/
.git/
_content/
*.ipynb
.ipynb_checkpoints/
```

> **Never bake secrets into an image.** `.env` must be in `.dockerignore`. Pass keys at runtime instead.

## Build and run

```bash
docker build -t genai-app .
docker run --rm --env-file .env genai-app          # keys come from .env at runtime, not in the image
docker run --rm -p 8000:8000 --env-file .env genai-app   # for a web API on port 8000
```

## Useful commands

| Command | What it does |
| --- | --- |
| `docker ps` | Running containers |
| `docker logs -f <container>` | Follow a container's output |
| `docker exec -it <container> sh` | Open a shell inside it |
| `docker images` | Images on this machine |
| `docker system prune` | Clean up unused images and containers |

## Secrets in production

On AWS, keep keys in **Secrets Manager** or **SSM Parameter Store** and inject them as environment variables at runtime; better still, use an **IAM role** so Bedrock calls need no keys at all (Module 10).
