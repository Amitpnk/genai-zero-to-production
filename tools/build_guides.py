"""Build the GitHub Pages guide pages from guides/<name>/README.md.

    uv run --with markdown --with pymdown-extensions python tools/build_guides.py

Markdown is the source of truth: edit guides/<name>/README.md, then re-run this.
Guides with hand-made pages (HANDMADE) are only listed in the hub, never overwritten.
"""

import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
GUIDES = ROOT / "guides"
DOCS = ROOT / "docs" / "guides"
REPO = "https://github.com/Amitpnk/genai-zero-to-production"
HANDMADE = {"ollama", "uv"}

# Order and grouping for the hub page.
GROUPS = [
    ("Setup and tools", ["uv", "git-github", "aws-bedrock", "jupyter", "ollama", "docker"]),
    ("Working with LLMs", ["llm-providers", "api-errors", "prompt-patterns", "cost-estimation"]),
    ("Building and running apps", ["vector-databases", "mcp", "tracing"]),
    ("Reference", ["glossary"]),
]

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · GenAI Zero to Production</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/deck.css">
<link rel="stylesheet" href="{up}assets/guide.css">
</head>
<body>

<header class="topbar">
  <a class="brand" href="{up}">GenAI <span>Zero to Production</span></a>
  <nav aria-label="Guide">
    <a href="{hub}">All guides</a>
    <a href="{notes}">Markdown notes</a>
    <a href="{REPO}">GitHub repo</a>
  </nav>
</header>
"""

FOOT = """
  <footer>Amit · Generative AI &amp; Agentic AI Instructor · Generated from <a href="{notes}">the Markdown notes</a></footer>
</main>

<script src="{up}assets/guide.js"></script>
</body>
</html>
"""


def read_meta(slug):
    """Title (first H1), description (first paragraph) and draft flag from a guide's README."""
    text = (GUIDES / slug / "README.md").read_text(encoding="utf8")
    title = re.search(r"^# (.+)$", text, re.M).group(1).strip()
    after = text.split("\n", 1)[1].strip()
    description = after.split("\n\n", 1)[0].strip()
    return text, title, description, "**Draft**" in text


def fix_links(body):
    """Episode links point at the GitHub notes; guide-to-guide links stay relative."""
    body = re.sub(r'href="\.\./\.\./(ep\d\d[^"/]*)/?"', lambda m: f'href="{REPO}/tree/main/{m.group(1)}"', body)
    return body


def decorate(body):
    """Wrap tables and code blocks in the guide styles, with copy buttons."""
    body = body.replace("<table>", '<div class="tablecard"><table>').replace("</table>", "</table></div>")
    body = re.sub(
        r'<pre(?: class="[^"]*")?><code(?: class="[^"]*")?>(.*?)</code></pre>',
        lambda m: f'<div class="codewrap"><button class="copy" type="button">Copy</button><pre class="code">{m.group(1)}</pre></div>',
        body, flags=re.S,
    )
    body = re.sub(r"<blockquote>\s*<p>(.*?)</p>\s*</blockquote>", r'<p class="callout">\1</p>', body, flags=re.S)
    return body


def build(slug):
    text, title, description, draft = read_meta(slug)
    rest = text.split("\n", 1)[1].strip().split("\n\n", 1)[1]           # drop H1 and intro paragraph
    # Code blocks inside numbered lists need 4-space indents for python-markdown.
    rest = re.sub(r"^ {3}(?=\S)", "    ", rest, flags=re.M)
    md = markdown.Markdown(
        extensions=["tables", "pymdownx.highlight", "pymdownx.superfences", "toc", "sane_lists"],
        extension_configs={"pymdownx.highlight": {"use_pygments": False}},   # plain <pre><code>, no colour spans
    )
    body = decorate(fix_links(md.convert(rest)))
    toc = "".join(f'<a href="#{t["id"]}">{html.escape(t["name"])}</a>' for t in md.toc_tokens)

    notes = f"{REPO}/tree/main/guides/{slug}"
    page = HEAD.format(title=html.escape(title), description=html.escape(re.sub(r"[*`]", "", description)),
                       up="../../", hub="../", notes=notes, REPO=REPO)
    page += '\n<main class="guide">\n'
    page += f'  <p class="eyebrow">Guide{" · Draft" if draft else ""}</p>\n'
    page += f"  <h1>{html.escape(title)}</h1>\n"
    page += f'  <p class="intro">{markdown.markdown(description)[3:-4]}</p>\n'
    page += f'  <nav class="toc" aria-label="On this page">{toc}</nav>\n\n'
    page += body
    page += FOOT.format(notes=notes, up="../../")

    out = DOCS / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf8", newline="\n")
    return out


def build_hub():
    cards = []
    for group, slugs in GROUPS:
        items = []
        for slug in slugs:
            if not (GUIDES / slug / "README.md").exists():
                continue
            _, title, description, draft = read_meta(slug)
            plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", description)          # [text](link) -> text
            desc = html.escape(re.sub(r"[*`]", "", plain))
            badge = '<span class="tag">draft</span>' if draft else ""
            items.append(
                f'<a class="gcard hubcard" href="{slug}/"><h3>{html.escape(title)} {badge}</h3><p class="note">{desc}</p></a>'
            )
        cards.append(f"<h2>{group}</h2>\n<div class=\"grid\">{''.join(items)}</div>")

    page = HEAD.format(title="Guides", description="Practical guides and cheat sheets for the GenAI Engineering series.",
                       up="../", hub="./", notes=f"{REPO}/tree/main/guides", REPO=REPO)
    page += """
<style>
  .hubcard { display: block; text-decoration: none; color: inherit; }
  .hubcard:hover { border-color: var(--mist); }
  .hubcard h3 .tag { font: 500 11px var(--mono); color: var(--ink); background: var(--mist); border-radius: 4px; padding: 2px 6px; margin-left: 6px; vertical-align: 2px; }
  .hubcard .note { margin: 0; }
</style>
<main class="guide">
  <p class="eyebrow">GenAI Zero to Production</p>
  <h1>Guides</h1>
  <p class="intro">Practical guides and cheat sheets that sit alongside the episodes. Pages marked <b>draft</b> are still being refined.</p>
"""
    page += "\n".join(cards)
    page += FOOT.format(notes=f"{REPO}/tree/main/guides", up="../")
    (DOCS / "index.html").write_text(page, encoding="utf8", newline="\n")


if __name__ == "__main__":
    for folder in sorted(GUIDES.iterdir()):
        if folder.is_dir() and (folder / "README.md").exists() and folder.name not in HANDMADE:
            print("built", build(folder.name).relative_to(ROOT))
    build_hub()
    print("built docs/guides/index.html")
