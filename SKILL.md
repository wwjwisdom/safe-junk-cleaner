---
name: safe-junk-cleaner
description: Interactive cleanup of local computer junk files across Windows, macOS, and Linux. Use when a user wants to free disk space by safely cleaning temporary files, browser caches, desktop-app caches, updater leftovers, logs, crash dumps, thumbnails, recycle bins or trash, and optional package-manager caches across one drive or all mounted local drives without deleting documents, media, projects, chat history, or other useful files.
---

# Safe Junk Cleaner

Use this skill to run a strong but conservative disk cleanup. Prefer high-yield junk categories that the OS or apps can rebuild. Keep the user in control: scan first, show the estimated savings, then clean only after confirmation.

## Interaction Contract

Match the user's language.

If the user has not already specified the cleanup shape, ask a short question set before deleting anything:
1. `scope`: current account or whole machine
2. `profile`: standard or aggressive
3. recycle bin or trash: include or skip

Recommend `standard`. Use `aggressive` only after warning that it also clears package-manager and developer caches, so the next install or first launch may be slower.

After you have the answers:
1. Run a dry scan
2. Summarize the biggest categories and estimated savings
3. Ask for confirmation
4. Run the cleanup
5. Report reclaimed space, skipped locked files, and any categories that needed elevated rights

## Safety Rules

- Clean only curated junk locations and known cache directories.
- Prefer explicit cache, temp, crash, shader, thumbnail, and log directories for each supported app family.
- Never delete from `Documents`, `Desktop`, `Downloads`, `Pictures`, `Videos`, `Music`, source repos, cloud-sync roots, VM images, databases, or unknown folders just because they are large.
- Never uninstall apps, delete restore points, touch browser cookies or password stores, or remove files outside the curated target set.
- Never delete chat attachments, message databases, offline media libraries, user profiles as a whole, or application content folders that are not clearly marked as cache, temp, crash, updater, or log storage.
- Never follow symlinks, junctions, or reparse points into unrelated paths.
- If the user asks to be tougher, widen only within the bundled script's `aggressive` profile or with explicit per-path review.

## Command Workflow

Prefer chat-driven interaction. Use the bundled script for both scan and cleanup.

Find a Python 3 interpreter first. Try `python3`, then `py -3`, then `python` only if it reports Python 3.

Dry scan:

```bash
python3 scripts/safe_junk_cleaner.py scan --scope machine --profile standard --include-trash --json
```

Cleanup:

```bash
python3 scripts/safe_junk_cleaner.py clean --scope machine --profile standard --include-trash --execute --json
```

Terminal-guided mode:

```bash
python3 scripts/safe_junk_cleaner.py --interactive
```

## Choosing Scope and Strength

- `scope user`: clean the current user's junk only. Use this when the user wants a lower-risk cleanup or does not have admin rights.
- `scope machine`: clean the current user plus system temp or crash areas and every accessible local user profile on every mounted local drive. Use this when the user wants the whole computer cleaned.
- `profile conservative`: older temp files and the safest cache targets.
- `profile standard`: recommended. Clear temp, browser or app caches, crash dumps, thumbnails, logs, and optional recycle-bin or trash contents.
- In `standard`, also clear curated desktop-app cache directories such as Electron caches, selected Chromium-derived app caches, updater leftovers, Adobe media caches, JetBrains caches, and app log folders that are safe to rebuild.
- `profile aggressive`: everything in `standard` plus package-manager and developer caches that are safe to rebuild but may slow the next install or first app launch.

## Reading Results

The script reports:
- mounted local volumes it inspected
- total reclaimable bytes
- bytes by category
- largest individual targets
- skipped files due to locks, permissions, or safety rules

If system-only categories are skipped, tell the user exactly which ones need elevation. Do not pretend the whole-machine cleanup was complete if it was not.

## Platform Notes

Read [references/coverage.md](C:\Users\cmp\.codex\skills\safe-junk-cleaner\references\coverage.md) when you need the full target map or need to explain what the script does not touch.

Highlights:
- Windows: temp folders, WER, crash dumps, browser caches, shader caches, thumbnail caches, recycle bins on each drive, and curated app caches for Electron apps, Chromium-derived apps, Adobe media caches, JetBrains caches, DingTalk logs, and QQ cache partitions.
- macOS: `~/Library/Caches`, `~/Library/Logs`, crash reports, `.Trash`, system temp, mounted-volume trash folders, and common Electron app caches under `~/Library/Application Support`.
- Linux: `~/.cache`, selected Chromium and Electron app caches under `~/.config`, `/tmp`, `/var/tmp`, `/var/crash`, trash folders, and optional package caches in aggressive mode.

## Final Response

Tell the user:
- what scope and profile you used
- estimated space found and space actually removed
- the three to five biggest categories
- what you intentionally did not touch
- what to rerun with admin rights if they want deeper whole-machine cleanup
