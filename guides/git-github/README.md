# Git and GitHub for this course

Everything you need to follow along: get the code, stay up to date, keep your own experiments, and never leak a key.

> **Draft** · Supports Episode 2 onwards · Commands work the same on Windows (Git Bash or PowerShell), macOS and Linux.

## 1. Install and set up once

```bash
git --version                                   # check it's installed (git-scm.com if not)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

Optional but handy: the [GitHub CLI](https://cli.github.com/) (`gh auth login`) makes cloning, forking and opening pull requests easier.

## 2. Get the course code

```bash
git clone https://github.com/Amitpnk/genai-zero-to-production.git
cd genai-zero-to-production
uv sync
cp .env.example .env        # then paste your keys
```

## 3. Stay up to date

```bash
git pull                    # get new episodes
uv sync                     # install any new packages
```

**`git pull` complains about local changes?** You edited a course file. Either keep your change on a branch (below), or put it aside:

```bash
git stash                   # put your changes aside
git pull
git stash pop               # bring them back (fix any conflicts)
```

## 4. Experiment without breaking anything

Work on your own **branch** so `main` always matches the course:

```bash
git switch -c my-experiments        # create and move to a new branch
# ... edit, run, break things ...
git add -A
git commit -m "Try a higher temperature"
git switch main                     # back to the clean course code
```

**Want your own copy on GitHub?** Fork the repo on GitHub (or `gh repo fork --clone`), then push your branch to your fork.

## 5. Everyday commands

| Command | What it does |
| --- | --- |
| `git status` | What's changed? (`.env` must **never** appear here) |
| `git diff` | Exactly what changed in each file |
| `git log --oneline -10` | The last 10 commits |
| `git restore <file>` | Throw away your changes to one file |
| `git switch <branch>` | Move to another branch |
| `git branch` | List branches |

## 6. Never leak a key

1. **`.env` is in `.gitignore`**: check with `git check-ignore .env` (it should print `.env`).
2. **Look before you commit**: `git status` and `git diff --staged`.
3. **Turn on GitHub's protection** for your own repos: *Settings → Code security → Secret scanning* and **Push protection**, which blocks pushes that contain known key formats.
4. **Optional pre-commit scanner**, such as `gitleaks` or `detect-secrets`, to catch keys before they're committed.

**If a key does get pushed:**

1. **Revoke and rotate it first**, in the provider's console. This stops the damage.
2. Check usage and billing for anything unexpected.
3. Then clean history (e.g. `git filter-repo`), knowing forks and clones may still have it.

> Rotation comes **before** cleanup: [Episode 2](../../ep02-setup/)'s interview question.

## 7. Found a bug in the course?

Open an issue: [github.com/Amitpnk/genai-zero-to-production/issues](https://github.com/Amitpnk/genai-zero-to-production/issues). Include the episode, the command you ran, and the full error (with keys removed).
