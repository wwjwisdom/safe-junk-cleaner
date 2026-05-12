# Safe Junk Cleaner

> This repository has moved. Active development now lives in [`wwjwisdom/safe-junk-cleaner-skill`](https://github.com/wwjwisdom/safe-junk-cleaner-skill).
>
> Please update your clone URL or Git remote:
>
> ```bash
> git remote set-url origin https://github.com/wwjwisdom/safe-junk-cleaner-skill.git
> ```
>
> For the latest README, installation steps, and ongoing updates, use the new repository.

Safe Junk Cleaner is a cross-platform, whitelist-based cleanup skill and CLI for Windows, macOS, and Linux.

It helps AI agents and power users reclaim disk space from rebuildable junk without touching documents, projects, chat history, media libraries, browser credentials, or unknown large folders.

It is built for AI agents and power users who want a cleanup workflow that is:

- strong enough to reclaim meaningful space
- safe enough to avoid deleting useful files
- transparent enough to show what will be removed before deletion
- broad enough to cover 100+ common professional apps or app families

The default workflow is:

1. scan first
2. show reclaimable space
3. confirm before deletion
4. clean only known-safe targets
5. report what was removed and what was skipped

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

It also supports:

- `level 1` cleanup for the normal safe path
- `level 2` cleanup for deeper WeChat or QQ cache cleanup plus a global two-year stale-file review
- specialty cleanup panels for `common`, `system-drive`, `wechat`, `qq`, `residual`, and `developer`
- advisory-only large-file review
- advisory-only duplicate-file review
- interactive terminal mode and JSON output for agent workflows

`level 2` is stronger than the default path, but it still keeps automatic deletion constrained to curated junk locations and explicit cache-resource paths. The global stale-file review is report-only and meant for manual review.

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

## Cleanup Modes

- `scope user`: clean the current user's junk only
- `scope machine`: also include system temp, crash areas, and every accessible local user profile on mounted local drives
- `profile conservative`: older temp files and the safest cache targets
- `profile standard`: recommended default, covering temp, caches, logs, thumbnails, crashes, and optional trash
- `profile aggressive`: adds rebuildable package-manager and developer caches
- `level 1`: current default behavior
- `level 2`: adds deeper WeChat or QQ image-resource cache cleanup plus a global two-year stale-file review

## Specialty Panels

The script can summarize or limit work to focused cleanup panels:

- `common`: broad day-to-day junk cleanup
- `system-drive`: targets rooted on the system drive
- `wechat`: Tencent and WeChat-family cache cleanup
- `qq`: QQ, QQ NT, QQ Browser, and related cache cleanup
- `residual`: updater leftovers and software residue
- `developer`: package-manager and developer caches

These panels are useful when the user wants a narrow cleanup instead of a whole-machine pass.

## Advisory Reviews

Some storage problems are better reviewed than auto-deleted. Safe Junk Cleaner includes two report-only review modes:

- large-file review for oversized user files
- duplicate-file review using size plus content hashing

Both modes are advisory only. They surface candidates for manual cleanup and do not delete anything.

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

## Common Workflows

Use a Python 3 interpreter. On some Windows systems, `python` may still point to Python 2, so prefer `python3`, `py -3`, or a bundled Python 3 runtime.

Dry scan:

```bash
python3 scripts/safe_junk_cleaner.py scan --scope machine --profile standard --level 1 --include-trash --json
```

Cleanup after confirmation:

```bash
python3 scripts/safe_junk_cleaner.py clean --scope machine --profile standard --level 1 --include-trash --execute --json
```

Show specialty panel totals:

```bash
python3 scripts/safe_junk_cleaner.py scan --scope machine --profile aggressive --level 2 --panel-summary
```

Focus on one cleanup panel:

```bash
python3 scripts/safe_junk_cleaner.py scan --scope machine --profile aggressive --level 2 --specialty wechat --panel-summary
python3 scripts/safe_junk_cleaner.py clean --scope machine --profile aggressive --level 2 --specialty qq --execute --json
```

Review large files:

```bash
python3 scripts/safe_junk_cleaner.py --large-files --min-file-size-mb 512 --top 20
```

Review duplicate files:

```bash
python3 scripts/safe_junk_cleaner.py --duplicate-files --min-file-size-mb 128 --top 20
```

Interactive mode:

```bash
python3 scripts/safe_junk_cleaner.py --interactive
```

## Platform Highlights

- Windows: the deepest coverage, including temp folders, WER, crash dumps, shader caches, recycle bins, Electron and Chromium caches, JetBrains caches, Adobe caches, and Tencent-family safe cache paths
- macOS: `~/Library/Caches`, `~/Library/Logs`, crash reports, trash folders, system temp, and common Electron app caches
- Linux: `~/.cache`, selected Chromium and Electron cache paths, `/tmp`, `/var/tmp`, `/var/crash`, trash folders, and optional package caches

## Agent Support

This repository is designed to work with multiple mainstream coding agents:

- Codex: native skill installation
- Claude Code: native skill installation or slash command wrapper
- Gemini CLI: custom command wrapper
- OpenCode: custom command wrapper

See [INSTALL.md](INSTALL.md) for step-by-step installation instructions.

## Repository Layout

```text
safe-junk-cleaner-skill/
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
- Keep report-only review modes clearly separate from automatic cleanup behavior.
- Run a dry scan after every meaningful rule expansion.

## License

MIT. See [LICENSE](LICENSE).
