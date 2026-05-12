# Coverage Map

Read this file only when you need to explain or adjust the cleaner's coverage.

## Design Goal

Beat shallow junk cleaners by covering more high-yield junk classes while staying inside a hard safety boundary:
- temporary files
- browser and app caches
- shader caches
- crash dumps and reports
- thumbnails and icon caches
- logs
- recycle-bin or trash contents
- optional package-manager and developer caches

Do not use this skill to chase space by deleting user content or installed software.

The cleaner now includes a curated software catalog covering 100+ common professional apps or app families. Coverage is still path-specific and cache-specific.

## Global Exclusions

Never target these on speculation:
- `Documents`, `Desktop`, `Downloads`, `Pictures`, `Videos`, `Music`
- project folders, repos, and workspaces
- cloud-sync roots such as OneDrive, iCloud Drive, Dropbox, or Google Drive
- browser cookies, history databases, password stores, or profiles as a whole
- chat history databases, offline attachments, avatar or media libraries, or app data folders that are not explicit cache, temp, updater, or log storage
- database files, virtual machines, disk images, or archives
- restore points, drivers, installed programs, or package registries

## Windows Coverage

User-scope targets:
- `%LOCALAPPDATA%\Temp`
- `%LOCALAPPDATA%\Microsoft\Windows\INetCache`
- `%LOCALAPPDATA%\Microsoft\Windows\Explorer\thumbcache_*.db`
- `%LOCALAPPDATA%\Microsoft\Windows\Explorer\iconcache_*.db`
- `%LOCALAPPDATA%\CrashDumps`
- `%LOCALAPPDATA%\D3DSCache`
- common GPU shader caches under NVIDIA and AMD local-cache paths
- Chromium-family caches for Chrome, Edge, Brave, Vivaldi, Opera, Quark, and similar user-data layouts
- Firefox `cache2` and thumbnails
- Electron-style caches for common apps such as VS Code, Cursor, Docker Desktop, Discord, GitHub Desktop, Slack, Teams, Notion, Obsidian, Postman, QQ, and Xmind
- app-specific logs and updater leftovers for curated targets such as DingTalk, QQ, and Squirrel-based updaters
- Adobe media caches and JetBrains `caches`, `tmp`, and `log`
- UWP `TempState`, `AC\Temp`, and `AC\INetCache` folders
- broad Electron-family coverage for collaboration, developer, and productivity apps through explicit app-name whitelists

Machine-scope additions:
- `%SystemRoot%\Temp`
- `%SystemRoot%\Minidump`
- `%SystemRoot%\MEMORY.DMP`
- `%ProgramData%\Microsoft\Windows\WER\ReportArchive`
- `%ProgramData%\Microsoft\Windows\WER\ReportQueue`
- `%ProgramData%\Microsoft\Windows\WER\Temp`
- recycle bins on every accessible local drive
- old CBS and DISM logs in aggressive mode

Aggressive additions:
- pip, uv, npm, pnpm, yarn, and Cargo caches

## macOS Coverage

User-scope targets:
- `~/Library/Caches`
- `~/Library/Logs`
- `~/Library/Application Support/CrashReporter`
- `~/.Trash`
- selected Electron app caches under `~/Library/Application Support`

Machine-scope additions:
- `/tmp`
- `/private/var/tmp`
- `/Library/Caches`
- `/Library/Logs/DiagnosticReports`
- `.Trashes` on mounted local volumes

Aggressive additions:
- `~/Library/Developer/Xcode/DerivedData`
- package-manager caches outside `~/Library/Caches`

## Linux Coverage

User-scope targets:
- `~/.cache`
- `~/.local/share/Trash/files`
- legacy `~/.thumbnails`
- selected Chromium and Electron app caches under `~/.config`

Machine-scope additions:
- `/tmp`
- `/var/tmp`
- `/var/crash`
- trash folders on mounted local volumes

Aggressive additions:
- `/var/cache/apt/archives`
- `/var/cache/dnf`
- `/var/cache/yum`
- `/var/cache/pacman/pkg`
- `/var/cache/apk`
- `/var/lib/systemd/coredump`
- user package caches such as Cargo or pnpm stores outside `~/.cache`

## Interaction Rules

When the user is vague, ask three short questions:
1. current account or whole machine
2. standard or aggressive
3. include recycle bin or trash or not

Then run a dry scan first. Summarize the estimated reclaimable space before you delete anything.

If the user asks what software is covered, run:

```bash
python3 scripts/safe_junk_cleaner.py --list-supported-software
```

## Risk Notes

- `aggressive` is still meant to be safe, but it trades convenience for space by removing rebuildable developer caches.
- Some files will be skipped if they are locked by running apps. Report those skips instead of forcing deletion.
- If whole-machine cleanup hits protected system paths, report that elevation is required for those categories.
