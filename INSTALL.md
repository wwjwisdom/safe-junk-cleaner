# Installation Guide

This repository can be used from several mainstream AI agents.

## Support Matrix

| Agent | Integration style | Recommended path |
| --- | --- | --- |
| Codex | Native skill | `~/.codex/skills/safe-junk-cleaner` |
| Claude Code | Native skill or custom slash command | `~/.claude/skills/safe-junk-cleaner` |
| Gemini CLI | Custom command | `~/.gemini/commands/safe-junk-cleaner.toml` |
| OpenCode | Custom command | `.opencode/commands/safe-junk-cleaner.md` |

## 1. Codex

Codex uses filesystem skills discovered under `$CODEX_HOME/skills` or `~/.codex/skills`.

Global install:

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/safe-junk-cleaner.git ~/.codex/skills/safe-junk-cleaner
```

Then use it naturally in chat, or name the skill explicitly:

```text
$safe-junk-cleaner
```

Examples:

```text
Use $safe-junk-cleaner to scan my whole machine and ask before deleting anything.
Use $safe-junk-cleaner to clean browser and app caches in standard mode.
```

## 2. Claude Code

Claude Code supports both:

- native skills in `~/.claude/skills/` or `.claude/skills/`
- custom slash commands in `~/.claude/commands/` or `.claude/commands/`

### Option A: Install as a native skill

Global install:

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/safe-junk-cleaner.git ~/.claude/skills/safe-junk-cleaner
```

Project-level install:

```bash
mkdir -p .claude/skills
git clone https://github.com/YOUR_GITHUB_USERNAME/safe-junk-cleaner.git .claude/skills/safe-junk-cleaner
```

Then use it naturally in chat, or mention the skill explicitly:

```text
$safe-junk-cleaner
```

Examples:

```text
Use $safe-junk-cleaner to scan the whole machine in standard mode.
Use $safe-junk-cleaner to clean browser caches and app caches after a dry run.
```

### Option B: Install as a slash command

This repository also ships a command template at:

```text
integrations/claude-code/safe-junk-cleaner.md
```

1. Clone this repository somewhere stable:

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/safe-junk-cleaner.git ~/ai-skills/safe-junk-cleaner
```

2. Copy the command template:

macOS or Linux:

```bash
mkdir -p ~/.claude/commands
cp ~/ai-skills/safe-junk-cleaner/integrations/claude-code/safe-junk-cleaner.md ~/.claude/commands/
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\commands" | Out-Null
Copy-Item "$env:USERPROFILE\ai-skills\safe-junk-cleaner\integrations\claude-code\safe-junk-cleaner.md" "$env:USERPROFILE\.claude\commands\"
```

3. Edit the copied file and replace `REPO_PATH` with the real repository path.

4. Use the command:

```text
/safe-junk-cleaner scan the whole machine in standard mode
```

## 3. Gemini CLI

Gemini CLI supports custom commands in:

- global: `~/.gemini/commands/`
- project: `.gemini/commands/`

This repository ships a command template at:

```text
integrations/gemini-cli/safe-junk-cleaner.toml
```

### Recommended install

1. Clone this repository somewhere stable:

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/safe-junk-cleaner.git ~/ai-skills/safe-junk-cleaner
```

2. Copy the template into Gemini's global commands directory:

macOS or Linux:

```bash
mkdir -p ~/.gemini/commands
cp ~/ai-skills/safe-junk-cleaner/integrations/gemini-cli/safe-junk-cleaner.toml ~/.gemini/commands/
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.gemini\commands" | Out-Null
Copy-Item "$env:USERPROFILE\ai-skills\safe-junk-cleaner\integrations\gemini-cli\safe-junk-cleaner.toml" "$env:USERPROFILE\.gemini\commands\"
```

3. Edit the copied file and replace `REPO_PATH` with the real repository path.

4. Use the command:

```text
/safe-junk-cleaner scan whole machine in standard mode
```

## 4. OpenCode

OpenCode supports project command files in `.opencode/commands/`.

This repository ships a command template at:

```text
integrations/opencode/safe-junk-cleaner.md
```

### Recommended install

1. Clone this repository somewhere stable:

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/safe-junk-cleaner.git ~/ai-skills/safe-junk-cleaner
```

2. Copy the template into a project command directory:

macOS or Linux:

```bash
mkdir -p .opencode/commands
cp ~/ai-skills/safe-junk-cleaner/integrations/opencode/safe-junk-cleaner.md .opencode/commands/
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path ".opencode\commands" | Out-Null
Copy-Item "$env:USERPROFILE\ai-skills\safe-junk-cleaner\integrations\opencode\safe-junk-cleaner.md" ".opencode\commands\"
```

3. Edit the copied file and replace `REPO_PATH` with the real repository path.

4. Use the command:

```text
/safe-junk-cleaner scan user scope in standard mode
```

## 5. Generic CLI Usage

You can always run the script directly:

```bash
python3 scripts/safe_junk_cleaner.py --interactive
```

Dry scan:

```bash
python3 scripts/safe_junk_cleaner.py scan --scope machine --profile standard --include-trash --json
```

Cleanup:

```bash
python3 scripts/safe_junk_cleaner.py clean --scope machine --profile standard --include-trash --execute --json
```

## Verification

List the supported catalog:

```bash
python3 scripts/safe_junk_cleaner.py --list-supported-software
```

Run a safe dry scan:

```bash
python3 scripts/safe_junk_cleaner.py scan --scope user --profile standard --include-trash
```

## Notes

- `standard` is the recommended default.
- `aggressive` also removes rebuildable package-manager and developer caches.
- Some system directories require administrator or root rights.
- Some files may be skipped if they are locked by running applications.
