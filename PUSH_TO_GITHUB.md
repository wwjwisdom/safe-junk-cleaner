# Push to GitHub

This repository is ready to publish as a normal GitHub repository.

## Option A: Use an Existing Empty Repository

If you already created an empty GitHub repository, add it as `origin` and push:

```bash
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/safe-junk-cleaner.git
git branch -M main
git push -u origin main
```

## Option B: Create the Repository with GitHub CLI

If `gh` is installed and authenticated:

```bash
gh repo create safe-junk-cleaner --public --source=. --remote=origin --push
```

## Option C: Create the Repository in the Browser

1. Open `https://github.com/new`
2. Repository name: `safe-junk-cleaner`
3. Choose `Public` or `Private`
4. Do not pre-initialize with README
5. After creation, run:

```bash
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/safe-junk-cleaner.git
git branch -M main
git push -u origin main
```

## Suggested Repository Description

```text
Cross-platform, whitelist-based junk cleaner skill for Codex, Claude Code, Gemini CLI, and OpenCode.
```

## Suggested Topics

```text
ai-agent, skill, codex, claude-code, gemini-cli, opencode, cleanup, cache-cleaner, windows, macos, linux
```

## Before You Push

- replace `YOUR_GITHUB_USERNAME` in docs if needed
- confirm README and INSTALL match your preferred repo URL
- run a dry scan once on your machine after major rule updates
