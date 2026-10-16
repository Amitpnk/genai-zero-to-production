"""Load .env once and read required settings with a helpful error."""

import os

from dotenv import load_dotenv

load_dotenv()


def require_env(name: str) -> str:
    """Return an environment variable, or fail with a hint about .env."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"{name} is not set. Copy .env.example to .env and fill in a real value."
        )
    return value
