# uv: the Python project manager used in this series

A practical guide and command cheat sheet. Introduced in [Episode 2](../../ep02-setup/) and used in every episode after.

> [HTML version of this guide](https://amitpnk.github.io/genai-zero-to-production/guides/uv/)

## What is uv?

**uv is one fast tool that replaces several:** `pip`, `venv`, `pip-tools`, `pyenv` and `pipx`. It's made by Astral, the team behind the Ruff linter.

| Job | Old way | With uv |
| --- | --- | --- |
| Install Python versions | pyenv, python.org installer | `uv python install 3.12` |
| Create a virtual environment | `python -m venv .venv` | done for you by `uv sync` |
| Install packages | `pip install …` | `uv add …` |
| Pin exact versions | `pip freeze > requirements.txt` | `uv.lock`, automatically |
| Run a command in the env | activate, then run | `uv run …`, no activation |
| Run a CLI tool once | `pipx run …` | `uvx …` |

**Why this series uses it:** it's much faster than pip, it installs Python for you (handy if your system Python is too old), and the **lock file** means everyone who clones the repo gets exactly the same package versions.

## How a uv project fits together

```text
genai-zero-to-production/
├── .python-version   ← which Python to use (3.12)        you edit via: uv python pin
├── pyproject.toml    ← what you depend on (anthropic...)  you edit via: uv add / uv remove
├── uv.lock           ← exact versions of everything       uv writes it; commit it
└── .venv/            ← the installed environment          uv creates it; never commit it
```

- You **describe** what you want in `pyproject.toml` (by running `uv add`).
- uv **resolves** exact versions into `uv.lock`.
- `uv sync` **makes `.venv` match** the lock file.
- `uv run` makes sure everything's in sync, then **runs your command inside `.venv`**.

---

## 1. Install uv

| OS | Command |
| --- | --- |
| **macOS / Linux** | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **Windows (PowerShell)** | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| **Any OS, if you have pip** | `pip install uv` |

Close and reopen your terminal, then check it:

```bash
uv --version            # e.g. uv 0.13.1
```

Keep it current:

```bash
uv self update          # only if you used the standalone installer above
```

## 2. The five commands you'll use every day

```bash
uv sync                          # make .venv match uv.lock (run after git pull)
uv run python script.py          # run anything inside the project's environment
uv add httpx                     # add a package (updates pyproject.toml + uv.lock)
uv remove httpx                  # remove a package
uv tree --depth 1                # what does this project depend on?
```

Real output of `uv tree --depth 1` in this repo:

```text
genai-zero-to-production v0.1.0
├── anthropic v1.15.0
├── boto3 v1.43.114
├── google-genai v2.31.0
├── openai v3.35.1
├── python-dotenv v1.2.4
├── tiktoken v0.14.0
├── ipykernel v7.4.0 (group: dev)
└── ruff v0.17.1 (group: dev)
```

---

## 3. Command cheat sheet

### Projects and dependencies

| Command | What it does |
| --- | --- |
| `uv init my-app --python 3.12` | Create a new project: `pyproject.toml`, `.python-version`, README, `.gitignore`, a `src/` folder and a git repo |
| `uv add anthropic openai` | Add packages; updates `pyproject.toml` and `uv.lock`, installs them |
| `uv add "openai>=2,<3"` | Add with a version range |
| `uv add --dev ruff pytest` | Add development-only tools (the `dev` group) |
| `uv remove openai` | Remove a package |
| `uv sync` | Install exactly what `uv.lock` says into `.venv` |
| `uv sync --no-dev` | Install without dev tools (e.g. in production) |
| `uv lock` | Re-resolve `uv.lock` without installing |
| `uv lock --upgrade-package openai` | Upgrade one package to its newest allowed version |
| `uv lock --upgrade` | Upgrade everything (then re-run your tests) |
| `uv tree` | Show the dependency tree |
| `uv export --format requirements-txt` | Produce a `requirements.txt` for tools that need one |

### Running things

| Command | What it does |
| --- | --- |
| `uv run python script.py` | Run a script in the project's environment, no activation needed |
| `uv run python` | Open a Python shell with the project's packages |
| `uv run --with rich python script.py` | Add a package **for this one run only** |
| `uvx ruff check .` | Run a CLI tool without installing it (`uvx` = `uv tool run`) |
| `uv tool install ruff` | Install a CLI tool permanently, isolated from your projects |
| `uv tool list` | List installed tools |

### Python versions

| Command | What it does |
| --- | --- |
| `uv python install 3.12` | Download and install Python 3.12 (no admin rights needed) |
| `uv python list --only-installed` | Every Python uv can see on this machine |
| `uv python pin 3.12` | Write `.python-version` so this project uses 3.12 |
| `uv python find` | Which Python would be used here? |
| `uv python uninstall 3.11` | Remove a uv-installed Python |

Real output of `uv python list --only-installed` on a laptop where the system Python is too old:

```text
cpython-3.12.15-windows-x86_64-none    ...\uv\python\cpython-3.12.15-...\python.exe   ← installed by uv
cpython-3.8.2-windows-x86_64-none      C:\Program Files\Python38\python.exe           ← old system Python
```

Both live side by side. Projects pinned to 3.12 use 3.12; nothing else on the machine changes.

### Housekeeping

| Command | What it does |
| --- | --- |
| `uv cache size --human` | How much disk the download cache uses (e.g. 340.9 MiB) |
| `uv cache clean` | Clear the cache (safe; packages re-download when needed) |
| `uv cache prune` | Remove only unused cache entries |
| `uv self update` | Update uv itself (standalone installs) |
| `uv help <command>` | Full help for any command |

---

## 4. pip and venv habits → uv

| You used to type | Now type |
| --- | --- |
| `python -m venv .venv` + activate | nothing: `uv sync` creates `.venv` |
| `pip install requests` | `uv add requests` |
| `pip install -r requirements.txt` | `uv sync` (or `uv pip install -r requirements.txt` in a non-uv project) |
| `pip freeze > requirements.txt` | nothing: `uv.lock` is kept up to date for you |
| `python script.py` (after activating) | `uv run python script.py` |
| `pipx run black .` | `uvx black .` |

> **Still need plain pip?** `uv pip install …` gives you a pip-compatible interface that's much faster. Handy for old projects without a `pyproject.toml`.

---

## 5. Commit or not?

| File | Commit it? | Why |
| --- | --- | --- |
| `pyproject.toml` | ✅ Yes | What the project needs |
| `uv.lock` | ✅ **Yes** | Everyone gets identical versions |
| `.python-version` | ✅ Yes | Everyone uses the same Python |
| `.venv/` | ❌ **Never** | Machine-specific, huge, rebuilt by `uv sync` (it's in `.gitignore`) |

## 6. Using it with VS Code

1. Run `uv sync` once so `.venv` exists.
2. `Ctrl+Shift+P` → **Python: Select Interpreter** → pick the one inside `.venv`.
3. Red squiggles under imports? You picked the wrong interpreter, or haven't run `uv sync` yet.

---

## 7. Troubleshooting

| Problem | Fix |
| --- | --- |
| `uv: command not found` / not recognized | Close and reopen the terminal. Still missing? Run the installer again, or `uv python update-shell` / check `~/.local/bin` is on your `PATH` |
| `ModuleNotFoundError` when running a script | Use `uv run python …`, not plain `python …`; or run `uv sync` |
| `python --version` still shows an old version | Normal: that's your system Python. `uv run python --version` shows the project's |
| `No solution found when resolving dependencies` | Two packages need conflicting versions: loosen a version range in `pyproject.toml`, then `uv lock` |
| Lock file out of date after `git pull` | `uv sync` (it re-locks if needed) |
| Running out of disk | `uv cache clean` |
| Corporate proxy or certificate errors | Set `UV_NATIVE_TLS=1` (uses your system's certificates), or set `HTTPS_PROXY` |

## 8. Clean start

If an environment gets into a strange state, rebuild it. It's safe: `.venv` is just a copy of what `uv.lock` describes.

```bash
rm -rf .venv          # Windows PowerShell: Remove-Item -Recurse -Force .venv
uv sync
```
