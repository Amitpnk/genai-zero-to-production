# MCP: build, test and connect tools

The Model Context Protocol (MCP) is a standard way to give AI apps tools and data. This guide covers the pieces, a minimal Python server, testing with the MCP Inspector, and connecting it to Claude.

> **Draft** · Preview of Module 8 (MCP & Multi-Agent) · Uses the official `mcp` Python SDK (version 2). The server example was run and its tool listed and called; the Inspector and Claude connection steps follow the docs and will be finalised in Module 8.

## The pieces

```text
Host (Claude Desktop, Claude Code, an IDE, your app)
  └─ MCP client  ──(stdio or HTTP)──▶  MCP server  ──▶  your API, database, files
```

| Term | Meaning |
| --- | --- |
| **Host** | The AI app the user talks to |
| **Client** | The connector inside the host, one per server |
| **Server** | Your program exposing capabilities |
| **Tools** | Functions the model can call (e.g. `create_ticket`) |
| **Resources** | Data the app can read (e.g. a file or record) |
| **Prompts** | Reusable prompt templates the server offers |
| **Transport** | How they talk: **stdio** (local process) or **Streamable HTTP** (remote) |

## A minimal server in Python

```bash
uv add "mcp[cli]"
```

```python
# weather_server.py
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("weather")


@mcp.tool()
def get_forecast(city: str) -> str:
    """Get a short weather forecast for a city."""
    return f"{city}: sunny, 24°C"          # call a real API here


if __name__ == "__main__":
    mcp.run()                               # stdio transport by default
```

The **docstring and type hints** become the tool's description and schema: that's what the model reads when deciding to call it, so write them well.

> **Checked with `mcp` 2.3.0.** In version 2 the server class is `MCPServer` (from `mcp.server.mcpserver`). Older tutorials use the version 1 name, `FastMCP` (from `mcp.server.fastmcp`): same idea, renamed. Pin `"mcp<2"` if you need to run old code.

## Test it with the MCP Inspector

The Inspector is a web UI for calling your server's tools by hand, no AI needed (requires Node.js):

```bash
npx @modelcontextprotocol/inspector uv run python weather_server.py
```

Open the URL it prints, connect, list the tools, and call `get_forecast` with a city.

## Connect it to Claude

**Claude Code:**

```bash
claude mcp add weather -- uv run --directory /full/path/to/project python weather_server.py
claude mcp list
```

**Claude Desktop:** edit `claude_desktop_config.json`, then restart Claude Desktop.

| OS | Config file |
| --- | --- |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": ["run", "--directory", "/full/path/to/project", "python", "weather_server.py"]
    }
  }
}
```

Use **full paths**: the host doesn't start in your project folder.

## Debugging checklist

| Symptom | Check |
| --- | --- |
| Server doesn't appear | JSON syntax; full paths; restart the host |
| Server starts then dies | Run the exact command yourself in a terminal and read the error |
| Garbled or broken connection | With stdio, **never `print()` to stdout**: it's the protocol channel. Log to **stderr** instead |
| Tool never gets called | Improve the tool's name and docstring; make it clearly match the task |
| Works in Inspector, not in the host | Different working directory or missing environment variables: pass them in the config's `env` |

## Security basics

- MCP servers can take **real actions**: give them the **least privilege** they need.
- Treat tool **results as untrusted** input (prompt injection can arrive through data).
- Require **human confirmation** for anything destructive (Module 8).
- Never put secrets in the config file you share; use environment variables.
