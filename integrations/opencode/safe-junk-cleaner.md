---
description: Safely scan or clean rebuildable junk files and app caches
---

You are running the Safe Junk Cleaner workflow from the repository at `REPO_PATH`.

Use the Python script at:

`REPO_PATH/scripts/safe_junk_cleaner.py`

Rules:

- Scan first before cleaning.
- Summarize reclaimable space by category.
- Ask for confirmation before deletion unless the user explicitly requested cleanup.
- Prefer the standard profile unless the user asks for aggressive cleanup.
- Never delete documents, media, source repos, chat history, databases, or unknown folders.
- Restrict deletions to curated cache, temp, crash, updater, shader, thumbnail, and log paths.
- Mention when administrator or root privileges are required.

User request:

$ARGUMENTS
