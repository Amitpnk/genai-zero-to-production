# Ollama: run LLMs on your own machine

A practical guide and command cheat sheet. Used in [Episode 3](../../ep03-how-llms-work/) (`next_token.py`) and again in Module 5 (Running models locally).

> [HTML version of this guide](https://amitpnk.github.io/genai-zero-to-production/guides/ollama/)

## What is Ollama?

**Ollama runs open-weight LLMs (Gemma, Llama, Qwen, Mistral and more) locally on your laptop.** No API key, no cloud bill, and your data never leaves your machine.

| Why use it | Why not (always) |
| --- | --- |
| Free and works offline | Small local models are less capable than Claude, GPT or Gemini |
| Private: prompts stay on your machine | Big models need lots of RAM, ideally a GPU |
| Great for learning and quick experiments | You manage the downloads and memory |

## How it works

```text
 ┌──────────────┐     HTTP on localhost:11434     ┌────────────────────────┐
 │  ollama CLI  │ ──────────────────────────────▶ │  Ollama server         │
 │  your Python │                                 │  (runs in background)  │
 │  any app     │ ◀────────────────────────────── │  loads models into RAM │
 └──────────────┘          responses              └────────────────────────┘
```

- Installing Ollama starts a **background server** on `http://localhost:11434`.
- The `ollama` command, your Python code and other apps all talk to that server.
- A model is **downloaded once** (disk), **loaded into memory** on first use, and **unloaded after 5 minutes idle** by default.

---

## 1. Install

| OS | How |
| --- | --- |
| **Windows** | Download from [ollama.com/download](https://ollama.com/download), or `winget install Ollama.Ollama` |
| **macOS** | Download from [ollama.com/download](https://ollama.com/download), or `brew install ollama` |
| **Linux** | `curl -fsSL https://ollama.com/install.sh \| sh` |

Check it worked:

```bash
ollama --version
```

## 2. Your first model

```bash
ollama pull gemma3:1b        # download once (~815 MB)
ollama run gemma3:1b         # chat with it; type /bye to exit
```

✅ **Done when:** the model answers in your terminal.

---

## 3. Command cheat sheet

### Download and manage models

| Command | What it does |
| --- | --- |
| `ollama pull gemma3:1b` | Download a model (or update it) |
| `ollama list` | **List all downloaded models**, with size and date |
| `ollama show gemma3:1b` | Model details: parameters, context length, quantization |
| `ollama cp gemma3:1b my-gemma` | Copy a model under a new name |
| `ollama rm gemma3:1b` | **Delete a model** and free its disk space |

### Run models

| Command | What it does |
| --- | --- |
| `ollama run gemma3:1b` | Start an interactive chat (downloads first if needed) |
| `ollama run gemma3:1b "Why is the sky blue?"` | One question, one answer, then exit |
| `ollama run gemma3:1b --verbose` | Also show speed: tokens per second, load time |
| `ollama run gemma3:1b --keepalive 30m` | Keep it in memory for 30 minutes after use |
| `ollama run gemma3:1b --format json "..."` | Ask for a JSON response |

### See what's running, and stop it

| Command | What it does |
| --- | --- |
| `ollama ps` | **What's loaded right now**: model, memory used, CPU/GPU, time until unload |
| `ollama stop gemma3:1b` | **Unload a model** from memory immediately |
| `ollama ps` (again) | Empty list = nothing using memory |

Example `ollama ps` output (measured on a laptop):

```text
NAME         ID              SIZE      PROCESSOR    CONTEXT    UNTIL
gemma3:1b    8648f39daa8f    883 MB    100% CPU     4096       4 minutes from now
```

### Inside an interactive chat (`ollama run ...`)

| Type | What it does |
| --- | --- |
| `/?` | Show all chat commands |
| `/bye` | Exit the chat (or press `Ctrl+D`) |
| `/clear` | Forget the conversation so far |
| `/show info` | Show details of the current model |
| `/set system "You are a pirate."` | Set a system prompt |
| `/set parameter temperature 0.2` | Change a setting for this session (Episode 5 covers temperature) |
| `/set parameter num_ctx 8192` | Use a bigger context window (uses more memory) |

> These slash commands only work **inside the interactive chat**. If you pipe text in (`echo "/bye" | ollama run ...`), the model treats it as a normal prompt.

### Stop or start the Ollama server

`ollama stop` unloads a **model**. To stop the **whole server**:

| OS | Stop the server | Start it again |
| --- | --- | --- |
| **Windows** | Right-click the llama icon in the system tray → **Quit Ollama**<br>or PowerShell: `Stop-Process -Name "ollama app", "ollama"` | Open **Ollama** from the Start menu |
| **macOS** | Menu bar llama icon → **Quit Ollama** | Open the Ollama app |
| **Linux** | `sudo systemctl stop ollama` | `sudo systemctl start ollama` |
| **Any OS** (manual) | `Ctrl+C` in the terminal running it | `ollama serve` |

Check whether the server is up:

```bash
curl http://localhost:11434/api/version
# {"version":"0.40.5"}
```

---

## 4. Use Ollama from code

### Native API (what `next_token.py` uses)

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "gemma3:1b",
  "messages": [{"role": "user", "content": "Say hello in five words."}],
  "stream": false
}'
```

<details>
<summary><b>On Windows PowerShell?</b> Use this instead</summary>

```powershell
$body = @{ model = "gemma3:1b"; stream = $false
           messages = @(@{ role = "user"; content = "Say hello in five words." }) } | ConvertTo-Json -Depth 5
Invoke-RestMethod http://localhost:11434/api/chat -Method Post -Body $body -ContentType "application/json"
```

In Windows PowerShell, `curl` is an alias for `Invoke-WebRequest`, so the `curl` example above doesn't work as written.

</details>

### OpenAI-compatible API

Ollama speaks the OpenAI API, so the same `openai` package from Episode 2 works. Just point it at Ollama:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")  # any non-empty key
reply = client.chat.completions.create(
    model="gemma3:1b",
    messages=[{"role": "user", "content": "Say hello in five words."}],
)
print(reply.choices[0].message.content)
```

This is handy for testing code locally for free, then switching `base_url` and `model` to a cloud provider.

### Useful endpoints

| Endpoint | Does |
| --- | --- |
| `POST /api/chat` | Chat with messages |
| `POST /api/generate` | Plain text completion (supports `logprobs`, used in Episode 3) |
| `POST /api/embed` | Embeddings (with an embedding model, e.g. `nomic-embed-text`) |
| `GET /api/tags` | Downloaded models (same as `ollama list`) |
| `GET /api/ps` | Loaded models (same as `ollama ps`) |
| `/v1/...` | OpenAI-compatible endpoints |

---

## 5. Memory: how much do I need?

**Disk** is used once per downloaded model. **RAM** (or GPU memory) is used only while a model is loaded.

| Model size | Example | RAM while loaded (approx.) | Runs well on |
| --- | --- | --- | --- |
| ~1B | `gemma3:1b` | **~0.9 GB** (measured) | Any laptop with 8 GB |
| ~4B | small general models | ~3–4 GB | 8–16 GB laptop |
| ~12B | mid-size models | ~8–10 GB | 16 GB+ or a GPU |
| ~27B+ | large models | 17 GB+ | 32 GB+ or a big GPU |

*Approximate for the default 4-bit (`Q4_K_M`) downloads. A bigger context window (`num_ctx`) needs more memory.*

**Tips to save memory:**

- `ollama stop <model>` when you're done, instead of waiting 5 minutes.
- Run one model at a time.
- Prefer smaller models for experiments; you'll compare sizes properly in Module 5.

---

## 6. Settings (environment variables)

Set these **before starting** the server (on Windows: *System Properties → Environment Variables*, then restart Ollama).

| Variable | Default | Use it to |
| --- | --- | --- |
| `OLLAMA_KEEP_ALIVE` | `5m` | Keep models loaded longer (`30m`) or unload right away (`0`) |
| `OLLAMA_MODELS` | see below | Store models on another drive |
| `OLLAMA_HOST` | `127.0.0.1:11434` | Change the address or port |
| `OLLAMA_CONTEXT_LENGTH` | depends on hardware | Default context window for all models |
| `OLLAMA_MAX_LOADED_MODELS` | auto | Limit how many models stay loaded at once |

**Where models are stored:**

| OS | Folder |
| --- | --- |
| Windows | `%USERPROFILE%\.ollama\models` |
| macOS | `~/.ollama/models` |
| Linux | `/usr/share/ollama/.ollama/models` (system service) |

---

## 7. Troubleshooting

| Problem | Fix |
| --- | --- |
| `could not connect to ollama server` / `ConnectionRefusedError` | The server isn't running: open the Ollama app, or run `ollama serve` |
| `model 'gemma3:1b' not found` | `ollama pull gemma3:1b` |
| Very slow replies | The model is too big for your machine; try a smaller one, and close other apps |
| Laptop runs out of memory | `ollama ps`, then `ollama stop <model>`; use a smaller model |
| Disk filling up | `ollama list`, then `ollama rm <model>` for ones you don't need |
| Port 11434 already in use | Another Ollama is running; quit it first (see "Stop the server") |

## 8. Clean up

```bash
ollama ps                  # anything loaded?
ollama stop gemma3:1b      # unload it
ollama list                # what's on disk?
ollama rm gemma3:1b        # delete it (frees ~815 MB)
```

To remove Ollama completely, uninstall the app as normal and delete the models folder above.
