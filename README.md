# Safe Junk Cleaner

Safe Junk Cleaner is a cross-platform, whitelist-based cleanup skill and CLI for Windows, macOS, and Linux.

It is built for AI agents and power users who want a cleanup workflow that is:

- strong enough to reclaim meaningful space
- safe enough to avoid deleting useful files
- transparent enough to show what will be removed before deletion
- broad enough to cover 100+ common professional apps or app families

## What It Does

Safe Junk Cleaner scans and removes rebuildable junk such as:

- temporary files
- browser caches
- desktop app caches
- updater leftovers
- shader caches
- crash dumps and crashpad reports
- thumbnails and icon caches
- app logs
- recycle-bin or trash contents
- optional package-manager and developer caches

The workflow is intentionally interactive:

1. scan first
2. summarize reclaimable space
3. ask for confirmation
4. clean
5. report what was removed and what was skipped

## Safety Model

This project uses a curated whitelist of safe cache, temp, crash, shader, updater, and log paths.

It does not delete:

- `Documents`, `Desktop`, `Downloads`, `Pictures`, `Videos`, `Music`
- source repos and workspaces
- cloud-sync roots
- chat history databases
- offline attachments and media libraries
- browser cookies or password stores
- databases, VM images, or disk images
- installed applications, drivers, restore points, or unknown large folders

The goal is not "delete anything large". The goal is "delete what is clearly rebuildable junk".

## 100+ Professional Software Catalog

The bundled catalog currently covers **101** common software entries across several work profiles.

### Developers and DevOps

Examples:

- Visual Studio Code
- VS Code Insiders
- Cursor
- Windsurf
- Trae
- VSCodium
- Docker Desktop
- Podman Desktop
- Rancher Desktop
- GitHub Desktop
- GitKraken
- Postman
- Insomnia
- Bruno
- Hoppscotch
- JetBrains IDE family

### Product, PM, and Knowledge Work

Examples:

- Notion
- Notion Calendar
- Obsidian
- Joplin
- ClickUp
- Trello
- Todoist
- Miro
- Xmind
- Linear
- Loom

### Communication and Collaboration

Examples:

- Slack
- Microsoft Teams
- Discord
- QQ
- QQEX
- DingTalk
- Lark
- Feishu
- Tencent Meeting
- Mattermost
- Rocket.Chat

### Creative, Design, and Media

Examples:

- Adobe Creative Cloud Desktop
- Adobe Premiere Pro cache families
- Adobe After Effects cache families
- Adobe Audition cache families
- Adobe Media Encoder cache families
- Figma
- OBS Studio
- Unity Hub
- Unity Editor cache families
- Unreal Engine cache families

### Browsers and Browser-Based Workflows

Examples:

- Google Chrome
- Microsoft Edge
- Mozilla Firefox
- Brave
- Vivaldi
- Opera
- Opera GX
- Quark
- RoxyBrowser
- Chromium

To inspect the current catalog from the script itself:

```bash
python3 scripts/safe_junk_cleaner.py --list-supported-software
```

Or JSON output:

```bash
python3 scripts/safe_junk_cleaner.py --list-supported-software --json
```

## Platforms

- Windows
- macOS
- Linux

Windows currently has the deepest app-specific coverage.

## Cleanup Profiles

- `conservative`: safest temp cleanup, older temporary files only
- `standard`: recommended default, covers system junk plus curated app caches and logs
- `aggressive`: adds rebuildable package-manager and developer caches

## Usage

Dry scan:

```bash
python3 scripts/safe_junk_cleaner.py scan --scope machine --profile standard --include-trash --json
```

Cleanup:

```bash
python3 scripts/safe_junk_cleaner.py clean --scope machine --profile standard --include-trash --execute --json
```

Interactive mode:

```bash
python3 scripts/safe_junk_cleaner.py --interactive
```

## Agent Support

This repository is designed to work with multiple mainstream coding agents:

- Codex: native skill installation
- Claude Code: native skill installation or slash command wrapper
- Gemini CLI: custom command wrapper
- OpenCode: custom command wrapper

See [INSTALL.md](INSTALL.md) for step-by-step installation instructions.

## Repository Layout

```text
safe-junk-cleaner/
|- SKILL.md
|- README.md
|- INSTALL.md
|- LICENSE
|- agents/
|  `- openai.yaml
|- references/
|  `- coverage.md
|- scripts/
|  `- safe_junk_cleaner.py
`- integrations/
   |- claude-code/
   |  `- safe-junk-cleaner.md
   |- gemini-cli/
   |  `- safe-junk-cleaner.toml
   `- opencode/
      `- safe-junk-cleaner.md
```

## Notes for Maintainers

- Keep deletions whitelist-based.
- Expand coverage by adding app-specific cache rules, not by broadening into entire app data trees.
- Prefer explicit cache, temp, crash, updater, shader, and log paths.
- Run a dry scan after every meaningful rule expansion.

## License

MIT. See [LICENSE](LICENSE).
