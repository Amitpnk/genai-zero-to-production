# Jupyter notebooks with uv

Use notebooks for quick experiments, with the project's `.venv` as the kernel so every course package is available.

> **Draft** · Useful from Module 3 onwards · `ipykernel` is already in this repo's dev dependencies.

## Option A: notebooks inside VS Code (recommended)

1. Make sure the environment exists (this installs `ipykernel` from the dev group):
   ```bash
   uv sync
   ```
2. Install the **Jupyter** extension in VS Code (it's in `.vscode/extensions.json`).
3. Create a file ending in `.ipynb`, or `Ctrl+Shift+P` → **Create: New Jupyter Notebook**.
4. Click **Select Kernel** (top right) → **Python Environments** → pick the one in **`.venv`**.
5. Run a cell:
   ```python
   import anthropic, openai, google.genai, tiktoken
   print("course packages ready")
   ```

## Option B: JupyterLab in the browser

Run JupyterLab without adding it to the project:

```bash
uv run --with jupyter jupyter lab
```

`uv run` makes the project's packages available, and `--with jupyter` adds JupyterLab just for this session.

## Loading `.env` in a notebook

Notebooks don't load `.env` automatically. Put this in the first cell:

```python
from dotenv import load_dotenv
load_dotenv()          # finds .env in the repo root
```

## Good notebook habits

| Do | Why |
| --- | --- |
| **Restart and run all** before trusting a result | Cells run out of order hide bugs |
| Keep notebooks for **exploring**; move working code into `.py` files | Scripts are easier to test, review and reuse |
| **Clear outputs** before committing | Outputs bloat Git and can contain data or keys |
| Never print API keys | Outputs are saved inside the `.ipynb` file |

`.ipynb_checkpoints/` is already in `.gitignore`.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `.venv` doesn't appear as a kernel | Run `uv sync`; reload VS Code; check `ipykernel` is installed (`uv tree`) |
| `ModuleNotFoundError` in a notebook | Wrong kernel selected: pick the `.venv` one |
| `KeyError` for an env variable | Add `load_dotenv()` in the first cell |
| Kernel keeps dying | Out of memory: restart the kernel, or use smaller data or models |
