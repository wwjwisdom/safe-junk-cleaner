#!/usr/bin/env python3

from __future__ import annotations

import argparse
import ctypes
import hashlib
import heapq
import json
import os
import platform
import shutil
import string
import sys
import time
from dataclasses import dataclass
from pathlib import Path
WINDOWS_USER_EXCLUDES = {
    "all users",
    "default",
    "default user",
    "defaultuser0",
    "public",
}

LINUX_SKIP_FS = {
    "autofs",
    "bpf",
    "cgroup",
    "cgroup2",
    "configfs",
    "debugfs",
    "devpts",
    "devtmpfs",
    "fusectl",
    "hugetlbfs",
    "mqueue",
    "nsfs",
    "overlay",
    "proc",
    "pstore",
    "securityfs",
    "selinuxfs",
    "squashfs",
    "sysfs",
    "tmpfs",
    "tracefs",
}

PROTECTED_TEMP_EXTENSIONS = {
    ".7z",
    ".avi",
    ".cer",
    ".cfg",
    ".conf",
    ".csv",
    ".db",
    ".doc",
    ".docx",
    ".eml",
    ".epub",
    ".flac",
    ".gif",
    ".gz",
    ".heic",
    ".ini",
    ".iso",
    ".jpeg",
    ".jpg",
    ".json",
    ".key",
    ".kdbx",
    ".m4a",
    ".mkv",
    ".md",
    ".mov",
    ".mp3",
    ".mp4",
    ".odp",
    ".ods",
    ".odt",
    ".opus",
    ".pages",
    ".pdf",
    ".pem",
    ".png",
    ".ppt",
    ".pptx",
    ".psd",
    ".rar",
    ".rtf",
    ".sqlite",
    ".sqlite3",
    ".tar",
    ".txt",
    ".wav",
    ".webm",
    ".xls",
    ".xlsx",
    ".xml",
    ".yaml",
    ".yml",
    ".zip",
}

PROFILE_TEMP_AGES = {
    "conservative": 72,
    "standard": 24,
    "aggressive": 6,
}

CLEANUP_LEVEL_CHOICES = (1, 2)
LEVEL_TWO_STALE_HOURS = 24 * 365 * 2

CATEGORY_TITLES = {
    "temp": "Temporary Files",
    "browser-cache": "Browser Caches",
    "app-cache": "App Caches",
    "shader-cache": "Shader Caches",
    "crash": "Crash Dumps and Reports",
    "thumbnails": "Thumbnails and Icons",
    "logs": "Logs",
    "trash": "Recycle Bin or Trash",
    "package-cache": "Package and Developer Caches",
}

SPECIALTY_CHOICES = (
    "common",
    "system-drive",
    "wechat",
    "qq",
    "residual",
    "developer",
)

SPECIALTY_TITLES = {
    "common": "Common Junk Cleanup",
    "system-drive": "System Drive Cleanup",
    "wechat": "WeChat Cleanup",
    "qq": "QQ Cleanup",
    "residual": "Software Leftovers Cleanup",
    "developer": "Developer Cache Cleanup",
}

COMMON_SPECIALTY_CATEGORIES = {
    "temp",
    "browser-cache",
    "app-cache",
    "shader-cache",
    "crash",
    "thumbnails",
    "logs",
    "trash",
}

QQ_PATH_KEYWORDS = (
    "\\qq\\",
    "\\qqex\\",
    "\\qqbrowser\\",
    "\\qqguild\\",
    "\\qqminiapp\\",
    "\\qq-play\\",
    "\\qqmusic\\",
    "\\qq-chat-updater",
    "\\qqminiapp-updater",
    "\\qqplay-updater",
    "\\qq_guild-updater",
    "\\tencent files\\",
)

WECHAT_PATH_KEYWORDS = (
    "\\wechat\\",
    "\\weixin\\",
    "\\xwechat\\",
    "\\wxwork\\",
)

RESIDUAL_PATH_KEYWORDS = (
    "squirreltemp",
    "-updater",
    "_updater",
    "\\upgrade",
    "updatepackages",
    "\\updates\\",
)

WINDOWS_CONTENT_SCAN_SKIP_DIRS = {
    "$recycle.bin",
    "appdata",
    "msocache",
    "onedrivetemp",
    "perflogs",
    "program files",
    "program files (x86)",
    "programdata",
    "recovery",
    "system volume information",
    "windows",
}

DUPLICATE_SCAN_EXTENSIONS = {
    ".7z",
    ".avi",
    ".doc",
    ".docx",
    ".epub",
    ".flac",
    ".gz",
    ".heic",
    ".iso",
    ".jpeg",
    ".jpg",
    ".m4a",
    ".mkv",
    ".mov",
    ".mp3",
    ".mp4",
    ".pdf",
    ".png",
    ".ppt",
    ".pptx",
    ".psd",
    ".rar",
    ".svg",
    ".tar",
    ".tif",
    ".tiff",
    ".txt",
    ".wav",
    ".webm",
    ".xls",
    ".xlsx",
    ".zip",
}

CHROMIUM_PROFILE_CACHE_SUBDIRS = (
    "Cache",
    "Code Cache",
    "CodeCache",
    "GPUCache",
    "GrShaderCache",
    "ShaderCache",
    "DawnGraphiteCache",
    "DawnWebGPUCache",
    "GraphiteDawnCache",
    "Media Cache",
)

CHROMIUM_PROFILE_WEB_CACHE_SUBDIRS = (
    Path("Service Worker") / "CacheStorage",
    Path("Service Worker") / "ScriptCache",
)

CHROMIUM_ROOT_CACHE_SUBDIRS = (
    "Code Cache",
    "CodeCache",
    "component_crx_cache",
    "GraphiteDawnCache",
    "GrShaderCache",
    "ShaderCache",
    "DawnGraphiteCache",
    "DawnWebGPUCache",
)

ELECTRON_CACHE_SUBDIRS = (
    "Cache",
    "Code Cache",
    "GPUCache",
    "CachedData",
    "DawnGraphiteCache",
    "DawnWebGPUCache",
    "GraphiteDawnCache",
    "Media Cache",
)

ELECTRON_WEB_CACHE_SUBDIRS = (
    Path("Service Worker") / "CacheStorage",
    Path("Service Worker") / "ScriptCache",
)

UWP_LOCAL_CACHE_SUBDIRS = (
    "Cache",
    "Caches",
    "Code Cache",
    "GPUCache",
    "INetCache",
    "Temp",
    "DawnGraphiteCache",
    "DawnWebGPUCache",
    "GraphiteDawnCache",
    "GrShaderCache",
    "ShaderCache",
    Path("Service Worker") / "CacheStorage",
    Path("Service Worker") / "ScriptCache",
)

WINDOWS_ELECTRON_APP_NAMES = (
    "Basecamp 3",
    "Beekeeper Studio",
    "Bruno",
    "Chatbox",
    "Claude",
    "ClickUp",
    "Code",
    "Code - Insiders",
    "Cursor",
    "Discord",
    "DiscordCanary",
    "DiscordPTB",
    "Docker Desktop",
    "draw.io",
    "Figma",
    "Flock",
    "GitHub Desktop",
    "GitKraken",
    "Hoppscotch",
    "Insomnia",
    "Joplin",
    "KeeWeb",
    "Lark",
    "Linear",
    "Loom",
    "Mattermost",
    "Microsoft Teams",
    "Miro",
    "MQTTFX",
    "MQTTX",
    "Notion",
    "Notion Calendar",
    "Obsidian",
    "OpenAI",
    "PicGo",
    "Podman Desktop",
    "Postman",
    "QQ",
    "QQEX",
    "Rocket.Chat",
    "Rancher Desktop",
    "Signal",
    "Slack",
    "Stoplight Studio",
    "Teams",
    "Todoist",
    "Trae",
    "Trello",
    "VSCodium",
    "wemeetapp",
    "Windsurf",
    "Wire",
    "Xmind",
)

MACOS_ELECTRON_APP_NAMES = (
    "Basecamp 3",
    "Beekeeper Studio",
    "Bruno",
    "Chatbox",
    "Claude",
    "ClickUp",
    "Code",
    "Code - Insiders",
    "Cursor",
    "Discord",
    "Docker Desktop",
    "draw.io",
    "Figma",
    "GitHub Desktop",
    "GitKraken",
    "Hoppscotch",
    "Insomnia",
    "Joplin",
    "KeeWeb",
    "Linear",
    "Loom",
    "Mattermost",
    "Miro",
    "MQTTX",
    "Notion",
    "Notion Calendar",
    "Obsidian",
    "OpenAI",
    "PicGo",
    "Podman Desktop",
    "Postman",
    "Rocket.Chat",
    "Rancher Desktop",
    "Signal",
    "Slack",
    "Stoplight Studio",
    "Teams",
    "Todoist",
    "Trae",
    "Trello",
    "VSCodium",
    "Windsurf",
    "Wire",
    "Xmind",
)

LINUX_ELECTRON_APP_NAMES = (
    "Beekeeper Studio",
    "Bruno",
    "Chatbox",
    "Claude",
    "Code",
    "Code - Insiders",
    "Cursor",
    "discord",
    "Docker Desktop",
    "draw.io",
    "Figma",
    "GitHub Desktop",
    "GitKraken",
    "Hoppscotch",
    "Insomnia",
    "Joplin",
    "KeeWeb",
    "Linear",
    "Mattermost",
    "Miro",
    "MQTTX",
    "Notion",
    "Obsidian",
    "OpenAI",
    "PicGo",
    "Podman Desktop",
    "Postman",
    "Rocket.Chat",
    "Rancher Desktop",
    "Signal",
    "Slack",
    "Stoplight Studio",
    "Teams",
    "Trae",
    "VSCodium",
    "Windsurf",
    "Wire",
    "Xmind",
)

SOFTWARE_CATALOG = {
    "Browsers": (
        "Google Chrome",
        "Google Chrome Beta",
        "Google Chrome Canary",
        "Microsoft Edge",
        "Microsoft Edge Beta",
        "Microsoft Edge Dev",
        "Brave Browser",
        "Mozilla Firefox",
        "Chromium",
        "Vivaldi",
        "Opera",
        "Opera GX",
        "Quark Browser",
        "RoxyBrowser",
        "Sidekick",
        "Wavebox",
        "Yandex Browser",
    ),
    "Communication": (
        "Slack",
        "Microsoft Teams",
        "Discord",
        "Discord Canary",
        "Discord PTB",
        "QQ",
        "QQEX",
        "DingTalk",
        "Lark",
        "Feishu",
        "Tencent Meeting",
        "Mattermost",
        "Rocket.Chat",
        "Signal Desktop",
        "Flock",
        "Wire",
        "WebCatalog",
    ),
    "Developer and Productivity": (
        "Visual Studio Code",
        "VS Code Insiders",
        "VSCodium",
        "Cursor",
        "Trae",
        "Windsurf",
        "GitHub Desktop",
        "GitKraken",
        "Postman",
        "Insomnia",
        "Bruno",
        "Hoppscotch",
        "Docker Desktop",
        "Podman Desktop",
        "Rancher Desktop",
        "MQTTX",
        "MQTTFX",
        "Beekeeper Studio",
        "Stoplight Studio",
        "KeeWeb",
        "Figma",
        "Notion",
        "Notion Calendar",
        "Obsidian",
        "Joplin",
        "Xmind",
        "draw.io Desktop",
        "Miro",
        "Linear",
        "Loom",
        "Trello",
        "Todoist",
        "ClickUp",
        "Basecamp 3",
        "Chatbox",
        "OpenAI Desktop",
        "Claude Desktop",
        "PicGo",
        "Sublime Text",
        "Visual Studio",
    ),
    "JetBrains and IDE Families": (
        "JetBrains Toolbox",
        "IntelliJ IDEA",
        "PyCharm",
        "WebStorm",
        "CLion",
        "GoLand",
        "Rider",
        "PhpStorm",
        "RubyMine",
        "DataGrip",
        "DataSpell",
        "Fleet",
        "Aqua",
        "Android Studio",
        "RustRover",
    ),
    "Creative and Media": (
        "Adobe Creative Cloud Desktop",
        "Adobe Premiere Pro",
        "Adobe After Effects",
        "Adobe Audition",
        "Adobe Media Encoder",
        "Adobe Character Animator",
        "Adobe Prelude",
        "OBS Studio",
        "Unity Hub",
        "Unity Editor",
        "Unreal Engine",
        "Quark Cloud Drive Components",
    ),
}


@dataclass(frozen=True)
class Target:
    label: str
    path: Path
    kind: str
    category: str
    min_age_hours: int = 0
    patterns: tuple[str, ...] = ()
    age_mode: str = "mtime"
    min_level: int = 1


def detect_os():
    system = platform.system().lower()
    if system.startswith("win"):
        return "windows"
    if system == "darwin":
        return "darwin"
    return "linux"


def format_bytes(size):
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    value = float(size)
    for unit in units:
        if value < 1024.0 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024.0
    return f"{int(size)} B"


def now_ts():
    return time.time()


def append_error(errors, message, limit=20):
    if len(errors) < limit:
        errors.append(message)


def is_symlink_like(path):
    try:
        return path.is_symlink()
    except OSError:
        return True


def is_old_enough(path, min_age_hours, age_mode="mtime"):
    if min_age_hours <= 0:
        return True
    try:
        stat_result = os.lstat(path)
        if age_mode == "activity":
            marker = max(stat_result.st_atime, stat_result.st_mtime)
        else:
            marker = stat_result.st_mtime
        age_seconds = now_ts() - marker
        return age_seconds >= min_age_hours * 3600
    except OSError:
        return False


def is_protected_temp_file(path):
    name = path.name.lower()
    if name in {"desktop.ini", "ntuser.dat"}:
        return True
    return path.suffix.lower() in PROTECTED_TEMP_EXTENSIONS


def clear_readonly(path):
    try:
        mode = os.lstat(path).st_mode
        os.chmod(path, mode | 0o200)
    except Exception:
        return


def rmtree_onerror(func, target, exc_info):
    del exc_info
    try:
        clear_readonly(Path(target))
        func(target)
    except Exception:
        return


def measure_path(path, errors):
    try:
        if is_symlink_like(path):
            return 0, 0
        if path.is_file():
            return os.lstat(path).st_size, 1
        if not path.is_dir():
            return 0, 0
    except OSError as exc:
        append_error(errors, f"measure failed for {path}: {exc}")
        return 0, 0

    total_size = 0
    total_items = 0
    stack = [path]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as it:
                for entry in it:
                    try:
                        if entry.is_symlink():
                            continue
                        if entry.is_dir(follow_symlinks=False):
                            stack.append(Path(entry.path))
                            continue
                        if entry.is_file(follow_symlinks=False):
                            stat_result = entry.stat(follow_symlinks=False)
                            total_size += stat_result.st_size
                            total_items += 1
                    except OSError as exc:
                        append_error(errors, f"measure failed for {entry.path}: {exc}")
        except OSError as exc:
            append_error(errors, f"measure failed for {current}: {exc}")
    return total_size, total_items


def remove_file(path, errors):
    clear_readonly(path)
    try:
        size = os.lstat(path).st_size
    except OSError:
        size = 0
    try:
        path.unlink()
        return size, 1, 0
    except OSError as exc:
        append_error(errors, f"delete failed for {path}: {exc}")
        return 0, 0, 1


def remove_tree(path, errors):
    size, items = measure_path(path, errors)
    try:
        shutil.rmtree(path, onerror=rmtree_onerror)
        return size, items, 0
    except OSError as exc:
        append_error(errors, f"delete failed for {path}: {exc}")
        return 0, 0, 1


def remove_entry(path, errors):
    try:
        if is_symlink_like(path):
            clear_readonly(path)
            path.unlink()
            return 0, 1, 0
        if path.is_file():
            return remove_file(path, errors)
        if path.is_dir():
            return remove_tree(path, errors)
    except OSError as exc:
        append_error(errors, f"delete failed for {path}: {exc}")
        return 0, 0, 1
    return 0, 0, 0


def summarize_purge_dir(root, errors):
    if not root.exists() or not root.is_dir():
        return 0, 0
    total_size = 0
    total_items = 0
    try:
        children = list(root.iterdir())
    except OSError as exc:
        append_error(errors, f"scan failed for {root}: {exc}")
        return 0, 0
    for child in children:
        size, items = measure_path(child, errors)
        total_size += size
        total_items += items
    return total_size, total_items


def clean_purge_dir(root, errors):
    if not root.exists() or not root.is_dir():
        return 0, 0, 0
    total_size = 0
    total_items = 0
    skipped = 0
    try:
        children = list(root.iterdir())
    except OSError as exc:
        append_error(errors, f"scan failed for {root}: {exc}")
        return 0, 0, 1
    for child in children:
        size, items, failures = remove_entry(child, errors)
        total_size += size
        total_items += items
        skipped += failures
    return total_size, total_items, skipped


def summarize_temp_dir(root, min_age_hours, errors):
    if not root.exists() or not root.is_dir():
        return 0, 0
    total_size = 0
    total_items = 0
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as it:
                for entry in it:
                    entry_path = Path(entry.path)
                    try:
                        if entry.is_symlink():
                            continue
                        if entry.is_dir(follow_symlinks=False):
                            stack.append(entry_path)
                            continue
                        if not entry.is_file(follow_symlinks=False):
                            continue
                        if not is_old_enough(entry_path, min_age_hours):
                            continue
                        if is_protected_temp_file(entry_path):
                            continue
                        total_size += entry.stat(follow_symlinks=False).st_size
                        total_items += 1
                    except OSError as exc:
                        append_error(errors, f"scan failed for {entry.path}: {exc}")
        except OSError as exc:
            append_error(errors, f"scan failed for {current}: {exc}")
    return total_size, total_items


def clean_temp_dir(root, min_age_hours, errors):
    if not root.exists() or not root.is_dir():
        return 0, 0, 0
    total_size = 0
    total_items = 0
    skipped = 0
    stack = [root]
    seen_dirs = []
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as it:
                for entry in it:
                    entry_path = Path(entry.path)
                    try:
                        if entry.is_symlink():
                            continue
                        if entry.is_dir(follow_symlinks=False):
                            stack.append(entry_path)
                            seen_dirs.append(entry_path)
                            continue
                        if not entry.is_file(follow_symlinks=False):
                            continue
                        if not is_old_enough(entry_path, min_age_hours):
                            continue
                        if is_protected_temp_file(entry_path):
                            continue
                        size, items, failures = remove_file(entry_path, errors)
                        total_size += size
                        total_items += items
                        skipped += failures
                    except OSError as exc:
                        append_error(errors, f"delete failed for {entry.path}: {exc}")
                        skipped += 1
        except OSError as exc:
            append_error(errors, f"scan failed for {current}: {exc}")
            skipped += 1

    for directory in sorted(seen_dirs, key=lambda item: len(item.parts), reverse=True):
        if not is_old_enough(directory, min_age_hours):
            continue
        try:
            directory.rmdir()
        except OSError:
            continue
    return total_size, total_items, skipped


def summarize_stale_dir(root, min_age_hours, errors, age_mode):
    if not root.exists() or not root.is_dir():
        return 0, 0
    total_size = 0
    total_items = 0
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as it:
                for entry in it:
                    entry_path = Path(entry.path)
                    try:
                        if entry.is_symlink():
                            continue
                        if entry.is_dir(follow_symlinks=False):
                            stack.append(entry_path)
                            continue
                        if not entry.is_file(follow_symlinks=False):
                            continue
                        if not is_old_enough(entry_path, min_age_hours, age_mode):
                            continue
                        total_size += entry.stat(follow_symlinks=False).st_size
                        total_items += 1
                    except OSError as exc:
                        append_error(errors, f"scan failed for {entry.path}: {exc}")
        except OSError as exc:
            append_error(errors, f"scan failed for {current}: {exc}")
    return total_size, total_items


def clean_stale_dir(root, min_age_hours, errors, age_mode):
    if not root.exists() or not root.is_dir():
        return 0, 0, 0
    total_size = 0
    total_items = 0
    skipped = 0
    stack = [root]
    seen_dirs = []
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as it:
                for entry in it:
                    entry_path = Path(entry.path)
                    try:
                        if entry.is_symlink():
                            continue
                        if entry.is_dir(follow_symlinks=False):
                            stack.append(entry_path)
                            seen_dirs.append(entry_path)
                            continue
                        if not entry.is_file(follow_symlinks=False):
                            continue
                        if not is_old_enough(entry_path, min_age_hours, age_mode):
                            continue
                        size, items, failures = remove_file(entry_path, errors)
                        total_size += size
                        total_items += items
                        skipped += failures
                    except OSError as exc:
                        append_error(errors, f"delete failed for {entry.path}: {exc}")
                        skipped += 1
        except OSError as exc:
            append_error(errors, f"scan failed for {current}: {exc}")
            skipped += 1

    for directory in sorted(seen_dirs, key=lambda item: len(item.parts), reverse=True):
        if not directory.exists():
            continue
        if not is_old_enough(directory, min_age_hours, age_mode):
            continue
        try:
            directory.rmdir()
        except OSError:
            continue
    return total_size, total_items, skipped


def summarize_match_files(root, patterns, min_age_hours, errors):
    if not root.exists() or not root.is_dir():
        return 0, 0
    total_size = 0
    total_items = 0
    for pattern in patterns:
        try:
            for item in root.glob(pattern):
                if not item.is_file():
                    continue
                if not is_old_enough(item, min_age_hours):
                    continue
                total_size += item.stat(follow_symlinks=False).st_size
                total_items += 1
        except OSError as exc:
            append_error(errors, f"scan failed for {root}: {exc}")
    return total_size, total_items


def clean_match_files(root, patterns, min_age_hours, errors):
    if not root.exists() or not root.is_dir():
        return 0, 0, 0
    total_size = 0
    total_items = 0
    skipped = 0
    for pattern in patterns:
        try:
            for item in root.glob(pattern):
                if not item.is_file():
                    continue
                if not is_old_enough(item, min_age_hours):
                    continue
                size, items, failures = remove_file(item, errors)
                total_size += size
                total_items += items
                skipped += failures
        except OSError as exc:
            append_error(errors, f"delete failed for {root}: {exc}")
            skipped += 1
    return total_size, total_items, skipped


def summarize_single_file(path, errors):
    if not path.exists() or not path.is_file():
        return 0, 0
    try:
        return os.lstat(path).st_size, 1
    except OSError as exc:
        append_error(errors, f"scan failed for {path}: {exc}")
        return 0, 0


def clean_single_file(path, errors):
    if not path.exists() or not path.is_file():
        return 0, 0, 0
    return remove_file(path, errors)


def normalize_key(target):
    path_text = str(target.path)
    if detect_os() == "windows":
        path_text = path_text.lower()
    return (target.kind, target.category, path_text, target.min_age_hours, target.patterns, target.age_mode, target.min_level)


def add_target(targets, seen, label, path, kind, category, min_age_hours=0, patterns=(), age_mode="mtime", min_level=1):
    target = Target(
        label=label,
        path=Path(path),
        kind=kind,
        category=category,
        min_age_hours=min_age_hours,
        patterns=tuple(patterns),
        age_mode=age_mode,
        min_level=min_level,
    )
    key = normalize_key(target)
    if key in seen:
        return
    seen.add(key)
    targets.append(target)


def normalize_path_text(path):
    return str(path).replace("/", "\\").lower()


def specialty_matches(category, label, path_text, specialty, system_drive):
    if specialty == "common":
        return category in COMMON_SPECIALTY_CATEGORIES
    if specialty == "developer":
        return category == "package-cache"
    if specialty == "system-drive":
        return path_text.startswith(system_drive)
    if specialty == "wechat":
        return any(keyword in path_text for keyword in WECHAT_PATH_KEYWORDS)
    if specialty == "qq":
        return any(keyword in path_text for keyword in QQ_PATH_KEYWORDS)
    if specialty == "residual":
        label_text = label.lower()
        return any(keyword in path_text or keyword in label_text for keyword in RESIDUAL_PATH_KEYWORDS)
    return False


def target_matches_specialties(target, specialties, system_drive):
    if not specialties:
        return True
    path_text = normalize_path_text(target.path)
    return any(specialty_matches(target.category, target.label, path_text, specialty, system_drive) for specialty in specialties)


def entry_matches_specialty(entry, specialty, system_drive):
    path_text = normalize_path_text(entry["path"])
    return specialty_matches(entry["category"], entry["label"], path_text, specialty, system_drive)


def filter_targets_by_specialties(targets, specialties):
    if not specialties:
        return targets
    system_drive = normalize_path_text(os.environ.get("SystemDrive", "C:\\")) + "\\"
    return [target for target in targets if target_matches_specialties(target, specialties, system_drive)]


def filter_targets_by_level(targets, level):
    return [target for target in targets if target.min_level <= level]


def iter_windows_volumes():
    volumes = []
    try:
        mask = ctypes.windll.kernel32.GetLogicalDrives()
        drive_type = ctypes.windll.kernel32.GetDriveTypeW
    except Exception:
        return [Path(os.environ.get("SystemDrive", "C:\\"))]
    for letter in string.ascii_uppercase:
        if mask & 1:
            drive = f"{letter}:\\"
            dtype = drive_type(ctypes.c_wchar_p(drive))
            if dtype in (2, 3, 6):
                volumes.append(Path(drive))
        mask >>= 1
    return volumes or [Path(os.environ.get("SystemDrive", "C:\\"))]


def iter_linux_volumes():
    volumes = []
    mounts_file = Path("/proc/self/mounts")
    if mounts_file.exists():
        try:
            for line in mounts_file.read_text(encoding="utf-8", errors="ignore").splitlines():
                parts = line.split()
                if len(parts) < 3:
                    continue
                device, mount_point, fs_type = parts[:3]
                mount_point = mount_point.replace("\\040", " ")
                if fs_type in LINUX_SKIP_FS:
                    continue
                if device.startswith("/dev/") or mount_point == "/" or mount_point.startswith(("/mnt/", "/media/", "/run/media/")):
                    volumes.append(Path(mount_point))
        except OSError:
            pass
    if not volumes:
        volumes = [Path("/")]
        for root in (Path("/mnt"), Path("/media"), Path("/run/media")):
            if not root.exists():
                continue
            for child in root.iterdir():
                if child.is_dir():
                    volumes.append(child)
    return dedupe_paths(volumes)


def iter_macos_volumes():
    volumes = [Path("/")]
    vol_root = Path("/Volumes")
    if vol_root.exists():
        for child in vol_root.iterdir():
            if child.is_dir():
                volumes.append(child)
    return dedupe_paths(volumes)


def dedupe_paths(paths):
    seen = set()
    result = []
    for path in paths:
        text = str(path)
        key = text.lower() if detect_os() == "windows" else text
        if key in seen:
            continue
        seen.add(key)
        result.append(path)
    return result


def iter_user_homes(os_name, scope):
    homes = [Path.home()]
    if scope != "machine":
        return dedupe_paths(homes)

    if os_name == "windows":
        users_root = Path(os.environ.get("SystemDrive", "C:\\")) / "Users"
        if users_root.exists():
            for child in users_root.iterdir():
                if not child.is_dir():
                    continue
                if child.name.lower() in WINDOWS_USER_EXCLUDES:
                    continue
                homes.append(child)
    else:
        for base in (Path("/Users"), Path("/home")):
            if not base.exists():
                continue
            for child in base.iterdir():
                if child.is_dir():
                    homes.append(child)
        root_home = Path("/root")
        if root_home.exists():
            homes.append(root_home)
    return dedupe_paths(homes)


def expand_existing_dirs(pattern):
    parent = pattern.parent
    name = pattern.name
    if not parent.exists():
        return []
    try:
        return [item for item in parent.glob(name) if item.exists() and item.is_dir()]
    except OSError:
        return []


def add_subdir_targets(targets, seen, label_prefix, root, subdirs, category, kind="purge_dir", min_age_hours=0, age_mode="mtime", min_level=1):
    for subdir in subdirs:
        add_target(
            targets,
            seen,
            f"{label_prefix} {str(subdir).replace('/', ' ')}",
            root / Path(subdir),
            kind,
            category,
            min_age_hours=min_age_hours,
            age_mode=age_mode,
            min_level=min_level,
        )


def add_chromium_user_data_targets(targets, seen, label_prefix, user_data_root):
    add_subdir_targets(targets, seen, label_prefix, user_data_root, CHROMIUM_ROOT_CACHE_SUBDIRS, "browser-cache")
    add_target(
        targets,
        seen,
        f"{label_prefix} Crashpad reports",
        user_data_root / "Crashpad" / "reports",
        "purge_dir",
        "crash",
    )
    for profile_dir in expand_existing_dirs(user_data_root / "*"):
        add_subdir_targets(
            targets,
            seen,
            f"{label_prefix} {profile_dir.name}",
            profile_dir,
            CHROMIUM_PROFILE_CACHE_SUBDIRS,
            "browser-cache",
        )
        add_subdir_targets(
            targets,
            seen,
            f"{label_prefix} {profile_dir.name}",
            profile_dir,
            CHROMIUM_PROFILE_WEB_CACHE_SUBDIRS,
            "browser-cache",
        )

    partitions_root = user_data_root / "Partitions"
    if partitions_root.exists():
        for partition_dir in expand_existing_dirs(partitions_root / "*"):
            add_subdir_targets(
                targets,
                seen,
                f"{label_prefix} {partition_dir.name}",
                partition_dir,
                CHROMIUM_PROFILE_CACHE_SUBDIRS,
                "browser-cache",
            )
            add_subdir_targets(
                targets,
                seen,
                f"{label_prefix} {partition_dir.name}",
                partition_dir,
                CHROMIUM_PROFILE_WEB_CACHE_SUBDIRS,
                "browser-cache",
            )


def add_electron_app_targets(targets, seen, label_prefix, app_root):
    add_subdir_targets(targets, seen, label_prefix, app_root, ELECTRON_CACHE_SUBDIRS, "app-cache")
    add_subdir_targets(targets, seen, label_prefix, app_root, ELECTRON_WEB_CACHE_SUBDIRS, "app-cache")
    add_target(
        targets,
        seen,
        f"{label_prefix} Crashpad reports",
        app_root / "Crashpad" / "reports",
        "purge_dir",
        "crash",
    )

    partitions_root = app_root / "Partitions"
    if partitions_root.exists():
        for partition_dir in expand_existing_dirs(partitions_root / "*"):
            add_subdir_targets(
                targets,
                seen,
                f"{label_prefix} {partition_dir.name}",
                partition_dir,
                CHROMIUM_PROFILE_CACHE_SUBDIRS,
                            "app-cache",
            )


def add_windows_electron_catalog_targets(targets, seen, home_name, roaming):
    for app_name in WINDOWS_ELECTRON_APP_NAMES:
        add_electron_app_targets(targets, seen, f"{home_name} {app_name}", roaming / app_name)


def add_windows_tencent_targets(targets, seen, home):
    local = home / "AppData" / "Local"
    roaming = home / "AppData" / "Roaming"
    home_name = home.name
    tencent_roaming = roaming / "Tencent"
    tencent_files = home / "Documents" / "Tencent Files"

    xwechat_root = tencent_roaming / "xwechat"
    add_target(targets, seen, f"{home_name} xwechat crashinfo", xwechat_root / "crashinfo", "purge_dir", "crash")
    add_target(targets, seen, f"{home_name} xwechat logs", xwechat_root / "log", "purge_dir", "logs")
    add_target(targets, seen, f"{home_name} xwechat update", xwechat_root / "update", "purge_dir", "app-cache")
    add_target(targets, seen, f"{home_name} xwechat cdn cache", xwechat_root / "ilink" / "netbridge" / "cdn", "purge_dir", "app-cache")
    add_target(targets, seen, f"{home_name} xwechat net cache", xwechat_root / "net" / "cdncomm" / "cdn", "purge_dir", "app-cache")
    add_target(targets, seen, f"{home_name} xwechat radium cache", xwechat_root / "radium" / "cache", "purge_dir", "app-cache", min_level=2)
    add_target(targets, seen, f"{home_name} xwechat web filter cache", xwechat_root / "radium" / "web" / "Subresource Filter", "purge_dir", "app-cache", min_level=2)

    for web_profile in expand_existing_dirs(xwechat_root / "radium" / "web" / "profiles" / "*"):
        add_subdir_targets(
            targets,
            seen,
            f"{home_name} xwechat {web_profile.name}",
            web_profile,
            CHROMIUM_PROFILE_CACHE_SUBDIRS,
            "app-cache",
            min_level=2,
        )
        add_subdir_targets(
            targets,
            seen,
            f"{home_name} xwechat {web_profile.name}",
            web_profile,
            CHROMIUM_PROFILE_WEB_CACHE_SUBDIRS,
            "app-cache",
            min_level=2,
        )

    wechat_cdn_roots = [xwechat_root / "ilink" / "netbridge" / "cdn" / "cdn", xwechat_root / "net" / "cdncomm" / "cdn"]
    wechat_cdn_roots.extend(net_root / "cdncomm" / "cdn" for net_root in expand_existing_dirs(xwechat_root / "net_*"))
    for cdn_root in wechat_cdn_roots:
        add_subdir_targets(
            targets,
            seen,
            f"{home_name} xwechat stale media",
            cdn_root,
            ("download", "upload", Path("download") / "4hours"),
            "app-cache",
            kind="stale_dir",
            min_age_hours=LEVEL_TWO_STALE_HOURS,
            age_mode="activity",
            min_level=2,
        )

    wemeet_global = tencent_roaming / "WeMeet" / "Global"
    add_target(targets, seen, f"{home_name} WeMeet logs", wemeet_global / "Logs", "purge_dir", "logs")
    add_target(targets, seen, f"{home_name} WeMeet update packages", wemeet_global / "UpdatePackages", "purge_dir", "app-cache")
    add_target(targets, seen, f"{home_name} WeMeet upgrade", wemeet_global / "Upgrade", "purge_dir", "app-cache")
    for data_subdir in (
        "CustomLayoutPreview",
        "DynamicResource",
        "DynamicResourcePackage",
        "StartUp",
        "Timeline",
        "Upgrade",
        "VirtualBkg",
        "WebkitCacheData",
        "XCast",
    ):
        add_target(
            targets,
            seen,
            f"{home_name} WeMeet {data_subdir}",
            wemeet_global / "Data" / data_subdir,
            "purge_dir",
            "app-cache",
        )

    add_target(targets, seen, f"{home_name} Wemeet local logs", local / "Tencent" / "Wemeet" / "Logs", "purge_dir", "logs")

    for log_cache in expand_existing_dirs(tencent_files / "*" / "nt_qq" / "nt_data" / "log-cache"):
        add_target(targets, seen, f"{home_name} QQ nt log-cache", log_cache, "purge_dir", "logs")
    for avatar_temp in expand_existing_dirs(tencent_files / "*" / "nt_qq" / "nt_data" / "avatar" / "user" / "temp"):
        add_target(targets, seen, f"{home_name} QQ avatar temp", avatar_temp, "purge_dir", "app-cache")
    for avatar_root in expand_existing_dirs(tencent_files / "*" / "nt_qq" / "nt_data" / "avatar" / "user"):
        add_target(
            targets,
            seen,
            f"{home_name} QQ stale avatar cache",
            avatar_root,
            "stale_dir",
            "app-cache",
            min_age_hours=LEVEL_TWO_STALE_HOURS,
            age_mode="activity",
            min_level=2,
        )
    for thumb_root in expand_existing_dirs(tencent_files / "*" / "nt_qq" / "nt_data" / "dataline" / ".thumb"):
        add_target(
            targets,
            seen,
            f"{home_name} QQ stale thumbnails",
            thumb_root,
            "stale_dir",
            "app-cache",
            min_age_hours=LEVEL_TWO_STALE_HOURS,
            age_mode="activity",
            min_level=2,
        )

    for updater_dir in expand_existing_dirs(local / "*updater"):
        add_target(targets, seen, f"{home_name} {updater_dir.name}", updater_dir, "purge_dir", "app-cache")


def add_macos_electron_catalog_targets(targets, seen, home_name, app_support):
    for app_name in MACOS_ELECTRON_APP_NAMES:
        add_electron_app_targets(targets, seen, f"{home_name} {app_name}", app_support / app_name)


def add_linux_electron_catalog_targets(targets, seen, home_name, config):
    for app_name in LINUX_ELECTRON_APP_NAMES:
        add_electron_app_targets(targets, seen, f"{home_name} {app_name}", config / app_name)


def build_windows_targets(scope, profile, include_trash, include_package_caches):
    targets = []
    seen = set()
    homes = iter_user_homes("windows", scope)
    volumes = iter_windows_volumes()
    temp_age = PROFILE_TEMP_AGES[profile]

    for home in homes:
        local = home / "AppData" / "Local"
        roaming = home / "AppData" / "Roaming"

        add_target(targets, seen, f"{home.name} temp", local / "Temp", "temp_dir", "temp", temp_age)
        add_target(targets, seen, f"{home.name} local low temp", home / "AppData" / "LocalLow" / "Temp", "temp_dir", "temp", temp_age)
        add_target(targets, seen, f"{home.name} SquirrelTemp", local / "SquirrelTemp", "purge_dir", "temp")
        add_target(targets, seen, f"{home.name} inet cache", local / "Microsoft" / "Windows" / "INetCache", "purge_dir", "browser-cache")
        add_target(targets, seen, f"{home.name} crash dumps", local / "CrashDumps", "purge_dir", "crash")
        add_target(targets, seen, f"{home.name} CrashRpt", local / "CrashRpt", "purge_dir", "crash")
        add_target(targets, seen, f"{home.name} Direct3D cache", local / "D3DSCache", "purge_dir", "shader-cache")
        add_target(targets, seen, f"{home.name} explorer caches", local / "Microsoft" / "Windows" / "Explorer", "match_files", "thumbnails", 0, ("thumbcache_*.db", "iconcache_*.db"))

        for adobe_root in (
            local / "Adobe" / "Common",
            roaming / "Adobe" / "Common",
        ):
            add_subdir_targets(
                targets,
                seen,
                f"{home.name} Adobe",
                adobe_root,
                ("Media Cache", "Media Cache Files", "Peak Files"),
                "app-cache",
            )

        for shader_dir in (
            local / "NVIDIA" / "DXCache",
            local / "NVIDIA" / "GLCache",
            local / "NVIDIA" / "NvCache",
            local / "AMD" / "DxCache",
            local / "AMD" / "DxcCache",
        ):
            add_target(targets, seen, f"{home.name} {shader_dir.name}", shader_dir, "purge_dir", "shader-cache")

        chromium_roots = {
            "Chrome": local / "Google" / "Chrome" / "User Data",
            "Chrome Beta": local / "Google" / "Chrome Beta" / "User Data",
            "Edge": local / "Microsoft" / "Edge" / "User Data",
            "Brave": local / "BraveSoftware" / "Brave-Browser" / "User Data",
            "Vivaldi": local / "Vivaldi" / "User Data",
            "Opera": roaming / "Opera Software" / "Opera Stable",
            "Opera GX": roaming / "Opera Software" / "Opera GX Stable",
            "Quark": local / "Quark" / "User Data",
            "QQBrowser": local / "Tencent" / "QQBrowser" / "User Data",
            "MiniBrowser": local / "Tencent" / "MiniBrowser" / "User Data",
            "RoxyBrowser": roaming / "RoxyBrowser" / "User Data",
        }
        for browser_name, user_data_root in chromium_roots.items():
            if user_data_root.exists():
                add_chromium_user_data_targets(targets, seen, f"{home.name} {browser_name}", user_data_root)

        firefox_profiles = local / "Mozilla" / "Firefox" / "Profiles"
        if firefox_profiles.exists():
            for profile_dir in expand_existing_dirs(firefox_profiles / "*"):
                add_target(targets, seen, f"{home.name} Firefox cache", profile_dir / "cache2", "purge_dir", "browser-cache")
                add_target(targets, seen, f"{home.name} Firefox thumbnails", profile_dir / "thumbnails", "purge_dir", "thumbnails")

        electron_roots = (
            roaming / "wemeetapp",
        )
        for app_root in electron_roots:
            add_electron_app_targets(targets, seen, f"{home.name} {app_root.name}", app_root)
        add_windows_electron_catalog_targets(targets, seen, home.name, roaming)
        add_windows_tencent_targets(targets, seen, home)

        for idea_root in expand_existing_dirs(local / "JetBrains" / "*"):
            add_target(targets, seen, f"{home.name} {idea_root.name} caches", idea_root / "caches", "purge_dir", "app-cache")
            add_target(targets, seen, f"{home.name} {idea_root.name} tmp", idea_root / "tmp", "purge_dir", "temp")
            add_target(targets, seen, f"{home.name} {idea_root.name} log", idea_root / "log", "purge_dir", "logs")

        add_subdir_targets(
            targets,
            seen,
            f"{home.name} DingTalk",
            roaming / "DingTalk",
            ("log", "holmeslogs", "updaterlogs"),
            "logs",
        )
        add_subdir_targets(
            targets,
            seen,
            f"{home.name} QQ",
            roaming / "QQ",
            ("log",),
            "logs",
        )

        packages_root = local / "Packages"
        if packages_root.exists():
            for temp_state in expand_existing_dirs(packages_root / "*" / "TempState"):
                add_target(targets, seen, f"{home.name} {temp_state.parent.name} TempState", temp_state, "purge_dir", "app-cache")
            for ac_temp in expand_existing_dirs(packages_root / "*" / "AC" / "Temp"):
                add_target(targets, seen, f"{home.name} {ac_temp.parent.parent.name} AC Temp", ac_temp, "purge_dir", "app-cache")
            for ac_inet_cache in expand_existing_dirs(packages_root / "*" / "AC" / "INetCache"):
                add_target(targets, seen, f"{home.name} {ac_inet_cache.parent.parent.name} AC INetCache", ac_inet_cache, "purge_dir", "app-cache")
            for local_cache in expand_existing_dirs(packages_root / "*" / "LocalCache"):
                add_subdir_targets(
                    targets,
                    seen,
                    f"{home.name} {local_cache.parent.name} LocalCache",
                    local_cache,
                    UWP_LOCAL_CACHE_SUBDIRS,
                    "app-cache",
                )

        if include_package_caches:
            for package_cache in (
                local / "pip" / "Cache",
                local / "uv" / "cache",
                local / "npm-cache" / "_cacache",
                local / "npm-cache" / "_npx",
                local / "Yarn" / "Cache",
                local / "go-build",
                home / ".cargo" / "registry" / "cache",
                home / ".cargo" / "git" / "db",
                home / ".gradle" / "caches",
                home / ".nuget" / "packages-cache",
                home / ".nuget" / "v3-cache",
                home / ".nuget" / "plugins-cache",
                local / "pnpm-store",
                home / ".pnpm-store",
            ):
                add_target(targets, seen, f"{home.name} {package_cache.name}", package_cache, "purge_dir", "package-cache")

    if scope == "machine":
        windir = Path(os.environ.get("SystemRoot", r"C:\Windows"))
        program_data = Path(os.environ.get("ProgramData", r"C:\ProgramData"))
        add_target(targets, seen, "Windows temp", windir / "Temp", "temp_dir", "temp", temp_age)
        add_target(targets, seen, "WER archive", program_data / "Microsoft" / "Windows" / "WER" / "ReportArchive", "purge_dir", "crash")
        add_target(targets, seen, "WER queue", program_data / "Microsoft" / "Windows" / "WER" / "ReportQueue", "purge_dir", "crash")
        add_target(targets, seen, "WER temp", program_data / "Microsoft" / "Windows" / "WER" / "Temp", "purge_dir", "crash")
        add_target(targets, seen, "Windows minidumps", windir / "Minidump", "purge_dir", "crash")
        add_target(targets, seen, "Windows memory dump", windir / "MEMORY.DMP", "single_file", "crash")
        if profile == "aggressive":
            add_target(targets, seen, "CBS logs", windir / "Logs" / "CBS", "match_files", "logs", 168, ("*.log",))
            add_target(targets, seen, "DISM logs", windir / "Logs" / "DISM", "match_files", "logs", 168, ("*.log",))

    if include_trash:
        for volume in volumes:
            add_target(targets, seen, f"{volume} recycle bin", volume / "$Recycle.Bin", "purge_dir", "trash")

    return targets, volumes


def build_macos_targets(scope, profile, include_trash, include_package_caches):
    targets = []
    seen = set()
    homes = iter_user_homes("darwin", scope)
    volumes = iter_macos_volumes()
    temp_age = PROFILE_TEMP_AGES[profile]

    for home in homes:
        library = home / "Library"
        app_support = library / "Application Support"
        add_target(targets, seen, f"{home.name} caches", library / "Caches", "purge_dir", "app-cache")
        add_target(targets, seen, f"{home.name} logs", library / "Logs", "purge_dir", "logs")
        add_target(targets, seen, f"{home.name} crash reporter", library / "Application Support" / "CrashReporter", "purge_dir", "crash")
        add_macos_electron_catalog_targets(targets, seen, home.name, app_support)
        if include_trash:
            add_target(targets, seen, f"{home.name} trash", home / ".Trash", "purge_dir", "trash")
        if profile == "aggressive":
            add_target(targets, seen, f"{home.name} Xcode DerivedData", library / "Developer" / "Xcode" / "DerivedData", "purge_dir", "package-cache")
        if include_package_caches:
            for package_cache in (
                home / ".npm" / "_cacache",
                home / ".pnpm-store",
                home / ".cargo" / "registry" / "cache",
                home / ".cargo" / "git" / "db",
                home / ".cache" / "uv",
            ):
                add_target(targets, seen, f"{home.name} {package_cache.name}", package_cache, "purge_dir", "package-cache")

    if scope == "machine":
        add_target(targets, seen, "system tmp", Path("/tmp"), "temp_dir", "temp", temp_age)
        add_target(targets, seen, "system var tmp", Path("/private/var/tmp"), "temp_dir", "temp", temp_age)
        add_target(targets, seen, "Library caches", Path("/Library/Caches"), "purge_dir", "app-cache")
        add_target(targets, seen, "diagnostic reports", Path("/Library/Logs/DiagnosticReports"), "purge_dir", "crash")

    if include_trash:
        for volume in volumes:
            if str(volume) == "/":
                continue
            add_target(targets, seen, f"{volume.name} trashes", volume / ".Trashes", "purge_dir", "trash")

    return targets, volumes


def build_linux_targets(scope, profile, include_trash, include_package_caches):
    targets = []
    seen = set()
    homes = iter_user_homes("linux", scope)
    volumes = iter_linux_volumes()
    temp_age = PROFILE_TEMP_AGES[profile]

    for home in homes:
        config = home / ".config"
        add_target(targets, seen, f"{home.name} caches", home / ".cache", "purge_dir", "app-cache")
        add_target(targets, seen, f"{home.name} thumbnails", home / ".thumbnails", "purge_dir", "thumbnails")
        for browser_name, user_data_root in {
            "Chrome": config / "google-chrome",
            "Chrome Beta": config / "google-chrome-beta",
            "Chromium": config / "chromium",
            "Edge": config / "microsoft-edge",
            "Brave": config / "BraveSoftware" / "Brave-Browser",
            "Vivaldi": config / "vivaldi",
            "Opera": config / "opera",
        }.items():
            if user_data_root.exists():
                add_chromium_user_data_targets(targets, seen, f"{home.name} {browser_name}", user_data_root)
        add_linux_electron_catalog_targets(targets, seen, home.name, config)
        if include_trash:
            add_target(targets, seen, f"{home.name} trash", home / ".local" / "share" / "Trash" / "files", "purge_dir", "trash")
        if include_package_caches:
            for package_cache in (
                home / ".pnpm-store",
                home / ".cargo" / "registry" / "cache",
                home / ".cargo" / "git" / "db",
            ):
                add_target(targets, seen, f"{home.name} {package_cache.name}", package_cache, "purge_dir", "package-cache")

    if scope == "machine":
        add_target(targets, seen, "tmp", Path("/tmp"), "temp_dir", "temp", temp_age)
        add_target(targets, seen, "var tmp", Path("/var/tmp"), "temp_dir", "temp", temp_age)
        add_target(targets, seen, "var crash", Path("/var/crash"), "purge_dir", "crash")
        if include_package_caches:
            for package_cache in (
                Path("/var/cache/apt/archives"),
                Path("/var/cache/dnf"),
                Path("/var/cache/yum"),
                Path("/var/cache/pacman/pkg"),
                Path("/var/cache/apk"),
                Path("/var/lib/systemd/coredump"),
            ):
                add_target(targets, seen, package_cache.name, package_cache, "purge_dir", "package-cache")

    if include_trash:
        for volume in volumes:
            for candidate in (volume / ".Trash",):
                add_target(targets, seen, f"{volume} trash", candidate, "purge_dir", "trash")
            if volume.exists():
                try:
                    for child in volume.iterdir():
                        if child.name.startswith(".Trash-") and child.is_dir():
                            add_target(targets, seen, f"{volume} {child.name}", child, "purge_dir", "trash")
                except OSError:
                    continue

    return targets, volumes


def build_targets(os_name, scope, profile, include_trash, include_package_caches):
    if os_name == "windows":
        return build_windows_targets(scope, profile, include_trash, include_package_caches)
    if os_name == "darwin":
        return build_macos_targets(scope, profile, include_trash, include_package_caches)
    return build_linux_targets(scope, profile, include_trash, include_package_caches)


def summarize_target(target):
    errors = []
    if target.kind == "purge_dir":
        total_size, total_items = summarize_purge_dir(target.path, errors)
    elif target.kind == "temp_dir":
        total_size, total_items = summarize_temp_dir(target.path, target.min_age_hours, errors)
    elif target.kind == "stale_dir":
        total_size, total_items = summarize_stale_dir(target.path, target.min_age_hours, errors, target.age_mode)
    elif target.kind == "match_files":
        total_size, total_items = summarize_match_files(target.path, target.patterns, target.min_age_hours, errors)
    elif target.kind == "single_file":
        total_size, total_items = summarize_single_file(target.path, errors)
    else:
        total_size, total_items = 0, 0
    return {
        "label": target.label,
        "path": str(target.path),
        "category": target.category,
        "bytes": total_size,
        "items": total_items,
        "skipped": 0,
        "errors": errors,
    }


def clean_target(target):
    errors = []
    if target.kind == "purge_dir":
        total_size, total_items, skipped = clean_purge_dir(target.path, errors)
    elif target.kind == "temp_dir":
        total_size, total_items, skipped = clean_temp_dir(target.path, target.min_age_hours, errors)
    elif target.kind == "stale_dir":
        total_size, total_items, skipped = clean_stale_dir(target.path, target.min_age_hours, errors, target.age_mode)
    elif target.kind == "match_files":
        total_size, total_items, skipped = clean_match_files(target.path, target.patterns, target.min_age_hours, errors)
    elif target.kind == "single_file":
        total_size, total_items, skipped = clean_single_file(target.path, errors)
    else:
        total_size, total_items, skipped = 0, 0, 0
    return {
        "label": target.label,
        "path": str(target.path),
        "category": target.category,
        "bytes": total_size,
        "items": total_items,
        "skipped": skipped,
        "errors": errors,
    }


def compile_report(entries, volumes, os_name, scope, profile, level, include_trash, include_package_caches):
    category_totals = {}
    total_bytes = 0
    total_items = 0
    skipped = 0
    errors = []
    for entry in entries:
        total_bytes += entry["bytes"]
        total_items += entry["items"]
        skipped += entry["skipped"]
        if entry["bytes"] > 0:
            category_totals.setdefault(entry["category"], 0)
            category_totals[entry["category"]] += entry["bytes"]
        for message in entry["errors"]:
            append_error(errors, message, limit=40)

    sorted_targets = sorted(
        [entry for entry in entries if entry["bytes"] > 0],
        key=lambda item: item["bytes"],
        reverse=True,
    )
    sorted_categories = sorted(category_totals.items(), key=lambda item: item[1], reverse=True)

    return {
        "os": os_name,
        "scope": scope,
        "profile": profile,
        "level": level,
        "include_trash": include_trash,
        "include_package_caches": include_package_caches,
        "volumes": [str(volume) for volume in volumes],
        "total_bytes": total_bytes,
        "total_items": total_items,
        "skipped": skipped,
        "category_totals": [
            {
                "category": category,
                "title": CATEGORY_TITLES.get(category, category),
                "bytes": size,
            }
            for category, size in sorted_categories
        ],
        "largest_targets": sorted_targets[:10],
        "error_count": len(errors),
        "errors": errors,
    }


def build_panel_report(entries):
    system_drive = normalize_path_text(os.environ.get("SystemDrive", "C:\\")) + "\\"
    panels = []
    for specialty in SPECIALTY_CHOICES:
        matched_entries = [
            entry
            for entry in entries
            if entry["bytes"] > 0 and entry_matches_specialty(entry, specialty, system_drive)
        ]
        matched_entries.sort(key=lambda item: item["bytes"], reverse=True)
        panels.append(
            {
                "id": specialty,
                "title": SPECIALTY_TITLES[specialty],
                "bytes": sum(entry["bytes"] for entry in matched_entries),
                "targets": len(matched_entries),
                "largest_targets": matched_entries[:5],
            }
        )
    return {"panels": panels}


def should_skip_content_dir(path, os_name):
    if is_symlink_like(path):
        return True
    name = path.name.lower()
    if os_name == "windows" and name in WINDOWS_CONTENT_SCAN_SKIP_DIRS:
        return True
    return False


def iter_content_files(volumes, os_name, min_size_bytes=0, extensions=None):
    stack = [volume for volume in reversed(volumes) if volume.exists()]
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as it:
                for entry in it:
                    entry_path = Path(entry.path)
                    try:
                        if entry.is_symlink():
                            continue
                        if entry.is_dir(follow_symlinks=False):
                            if should_skip_content_dir(entry_path, os_name):
                                continue
                            stack.append(entry_path)
                            continue
                        if not entry.is_file(follow_symlinks=False):
                            continue
                        if extensions and entry_path.suffix.lower() not in extensions:
                            continue
                        stat_result = entry.stat(follow_symlinks=False)
                        if stat_result.st_size < min_size_bytes:
                            continue
                        yield entry_path, stat_result.st_size
                    except OSError:
                        continue
        except OSError:
            continue


def build_large_file_report(volumes, os_name, min_size_mb, limit):
    min_size_bytes = max(1, int(min_size_mb)) * 1024 * 1024
    heap = []
    scanned_files = 0
    for path, size in iter_content_files(volumes, os_name, min_size_bytes=min_size_bytes):
        scanned_files += 1
        item = (size, str(path))
        if len(heap) < limit:
            heapq.heappush(heap, item)
        elif size > heap[0][0]:
            heapq.heapreplace(heap, item)
    candidates = [
        {"bytes": size, "path": path}
        for size, path in sorted(heap, key=lambda item: item[0], reverse=True)
    ]
    return {
        "mode": "large-files",
        "advisory_only": True,
        "min_size_mb": min_size_mb,
        "scanned_files": scanned_files,
        "candidates": candidates,
    }


def file_quick_hash(path, size):
    hasher = hashlib.sha256()
    chunk_size = 1024 * 1024
    with path.open("rb") as handle:
        if size <= chunk_size * 2:
            hasher.update(handle.read())
        else:
            hasher.update(handle.read(chunk_size))
            handle.seek(-chunk_size, os.SEEK_END)
            hasher.update(handle.read(chunk_size))
    return hasher.hexdigest()


def file_full_hash(path):
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def build_duplicate_report(volumes, os_name, min_size_mb, limit):
    min_size_bytes = max(1, int(min_size_mb)) * 1024 * 1024
    by_size = {}
    scanned_files = 0
    for path, size in iter_content_files(
        volumes,
        os_name,
        min_size_bytes=min_size_bytes,
        extensions=DUPLICATE_SCAN_EXTENSIONS,
    ):
        scanned_files += 1
        by_size.setdefault(size, []).append(path)

    duplicate_groups = []
    for size, paths in sorted(by_size.items(), key=lambda item: item[0], reverse=True):
        if len(paths) < 2:
            continue
        quick_groups = {}
        for path in paths:
            try:
                quick_groups.setdefault(file_quick_hash(path, size), []).append(path)
            except OSError:
                continue
        for quick_hash, quick_paths in quick_groups.items():
            del quick_hash
            if len(quick_paths) < 2:
                continue
            full_groups = {}
            for path in quick_paths:
                try:
                    full_groups.setdefault(file_full_hash(path), []).append(path)
                except OSError:
                    continue
            for full_hash, full_paths in full_groups.items():
                del full_hash
                if len(full_paths) < 2:
                    continue
                duplicate_groups.append(
                    {
                        "bytes": size,
                        "count": len(full_paths),
                        "wasted_bytes": size * (len(full_paths) - 1),
                        "files": [str(path) for path in sorted(full_paths)],
                    }
                )

    duplicate_groups.sort(
        key=lambda item: (item["wasted_bytes"], item["bytes"], item["count"]),
        reverse=True,
    )
    return {
        "mode": "duplicates",
        "advisory_only": True,
        "min_size_mb": min_size_mb,
        "scanned_files": scanned_files,
        "groups": duplicate_groups[:limit],
    }


def build_global_stale_report(volumes, os_name, min_age_hours, limit):
    stale_threshold = now_ts() - (min_age_hours * 3600)
    stack = [volume for volume in reversed(volumes) if volume.exists()]
    matched_files = 0
    scanned_files = 0
    file_heap = []
    folder_totals = {}
    folder_counts = {}

    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as it:
                for entry in it:
                    entry_path = Path(entry.path)
                    try:
                        if entry.is_symlink():
                            continue
                        if entry.is_dir(follow_symlinks=False):
                            if should_skip_content_dir(entry_path, os_name):
                                continue
                            stack.append(entry_path)
                            continue
                        if not entry.is_file(follow_symlinks=False):
                            continue
                        scanned_files += 1
                        stat_result = entry.stat(follow_symlinks=False)
                        activity_ts = max(stat_result.st_atime, stat_result.st_mtime)
                        if activity_ts > stale_threshold:
                            continue
                        matched_files += 1
                        size = stat_result.st_size
                        item = (size, str(entry_path), activity_ts)
                        if len(file_heap) < limit:
                            heapq.heappush(file_heap, item)
                        elif size > file_heap[0][0]:
                            heapq.heapreplace(file_heap, item)
                        parent_text = str(entry_path.parent)
                        folder_totals[parent_text] = folder_totals.get(parent_text, 0) + size
                        folder_counts[parent_text] = folder_counts.get(parent_text, 0) + 1
                    except OSError:
                        continue
        except OSError:
            continue

    top_files = [
        {
            "bytes": size,
            "path": path,
            "activity_ts": activity_ts,
        }
        for size, path, activity_ts in sorted(file_heap, key=lambda item: item[0], reverse=True)
    ]
    top_folders = [
        {
            "bytes": total_bytes,
            "items": folder_counts[path],
            "path": path,
        }
        for path, total_bytes in sorted(folder_totals.items(), key=lambda item: item[1], reverse=True)[:limit]
    ]
    return {
        "mode": "global-stale-review",
        "advisory_only": True,
        "age_mode": "activity",
        "min_age_hours": min_age_hours,
        "scanned_files": scanned_files,
        "matched_files": matched_files,
        "largest_files": top_files,
        "largest_folders": top_folders,
    }


def print_human_report(title, report):
    print(title)
    print(f"Platform: {report['os']}")
    print(f"Scope: {report['scope']}")
    print(f"Profile: {report['profile']}")
    print(f"Level: {report['level']}")
    print(f"Mounted local volumes: {', '.join(report['volumes']) or 'none detected'}")
    print(f"Reclaimable space: {format_bytes(report['total_bytes'])}")
    print(f"Eligible files: {report['total_items']}")
    if report["skipped"]:
        print(f"Skipped due to locks or permissions: {report['skipped']}")
    print("")
    if report["category_totals"]:
        print("By category:")
        for item in report["category_totals"]:
            print(f"  - {item['title']}: {format_bytes(item['bytes'])}")
    else:
        print("By category:")
        print("  - nothing matched the current rules")
    print("")
    if report["largest_targets"]:
        print("Largest targets:")
        for item in report["largest_targets"][:5]:
            print(f"  - {item['label']}: {format_bytes(item['bytes'])} ({item['path']})")
    if report["errors"]:
        print("")
        print("Sample errors:")
        for message in report["errors"][:5]:
            print(f"  - {message}")


def print_panel_report(report):
    print("Special Cleanup Panels")
    print("")
    for panel in report["panels"]:
        print(f"{panel['title']}: {format_bytes(panel['bytes'])}")
        if panel["largest_targets"]:
            for item in panel["largest_targets"][:3]:
                print(f"  - {item['label']}: {format_bytes(item['bytes'])}")
        else:
            print("  - nothing matched")
        print("")


def print_large_file_report(report):
    print("Large Files Review")
    print("Advisory only: review before deleting anything.")
    print(f"Minimum file size: {report['min_size_mb']} MiB")
    print(f"Matched files: {report['scanned_files']}")
    print("")
    if not report["candidates"]:
        print("No large files matched the current threshold.")
        return
    for item in report["candidates"]:
        print(f"  - {format_bytes(item['bytes'])}: {item['path']}")


def print_duplicate_report(report):
    print("Duplicate Files Review")
    print("Advisory only: duplicates may still be useful.")
    print(f"Minimum file size: {report['min_size_mb']} MiB")
    print(f"Scanned candidate files: {report['scanned_files']}")
    print("")
    if not report["groups"]:
        print("No duplicate groups matched the current threshold.")
        return
    for group in report["groups"]:
        print(f"  - {format_bytes(group['wasted_bytes'])} recoverable across {group['count']} files of {format_bytes(group['bytes'])} each")
        for file_path in group["files"][:5]:
            print(f"      {file_path}")


def print_global_stale_report(report):
    print("Global Stale Review")
    print("Advisory only: ordinary user files are not auto-deleted.")
    print(f"Minimum age: about {int(report['min_age_hours'] / 24 / 365)} years")
    print(f"Scanned files: {report['scanned_files']}")
    print(f"Matched stale files: {report['matched_files']}")
    print("")
    if report["largest_folders"]:
        print("Folders with the most stale content:")
        for item in report["largest_folders"][:5]:
            print(f"  - {format_bytes(item['bytes'])} across {item['items']} files: {item['path']}")
        print("")
    if report["largest_files"]:
        print("Largest stale files:")
        for item in report["largest_files"][:10]:
            print(f"  - {format_bytes(item['bytes'])}: {item['path']}")
    else:
        print("No stale files matched the current rules.")


def build_supported_software_summary():
    groups = []
    total = 0
    for group_name, software_names in SOFTWARE_CATALOG.items():
        deduped = sorted(dict.fromkeys(software_names))
        total += len(deduped)
        groups.append(
            {
                "group": group_name,
                "count": len(deduped),
                "software": deduped,
            }
        )
    return {"total_supported_software": total, "groups": groups}


def print_supported_software(summary):
    print(f"Supported software catalog: {summary['total_supported_software']} entries")
    for group in summary["groups"]:
        print(f"")
        print(f"{group['group']} ({group['count']}):")
        for name in group["software"]:
            print(f"  - {name}")


def add_bool_flag(parser, name, help_text):
    parser.add_argument(
        f"--{name}",
        dest=name.replace("-", "_"),
        action="store_true",
        default=None,
        help=help_text,
    )
    parser.add_argument(
        f"--no-{name}",
        dest=name.replace("-", "_"),
        action="store_false",
    )


def prompt_choice(label, choices, default):
    prompt = f"{label} [{'/'.join(choices)}] (default: {default}): "
    while True:
        answer = input(prompt).strip().lower()
        if not answer:
            return default
        if answer in choices:
            return answer
        print(f"Please choose one of: {', '.join(choices)}")


def prompt_yes_no(label, default):
    suffix = "Y/n" if default else "y/N"
    answer = input(f"{label} [{suffix}]: ").strip().lower()
    if not answer:
        return default
    return answer in {"y", "yes"}


def resolve_interactive_args(args):
    if args.level is None:
        args.level = int(prompt_choice("Cleanup level", ("1", "2"), "1"))
    if args.scope is None:
        args.scope = prompt_choice("Cleanup scope", ("user", "machine"), "machine")
    if args.profile is None:
        args.profile = prompt_choice("Cleanup profile", ("conservative", "standard", "aggressive"), "standard")
    if args.include_trash is None:
        args.include_trash = prompt_yes_no("Empty recycle bin or trash too", True)
    if args.include_package_caches is None:
        default_packages = args.profile == "aggressive"
        args.include_package_caches = prompt_yes_no(
            "Include package-manager and developer caches",
            default_packages,
        )
    return args


def resolve_defaults(args):
    if args.level is None:
        args.level = 1
    if args.scope is None:
        args.scope = "machine"
    if args.profile is None:
        args.profile = "standard"
    if args.include_trash is None:
        args.include_trash = True
    if args.include_package_caches is None:
        args.include_package_caches = args.profile == "aggressive"
    return args


def build_parser():
    parser = argparse.ArgumentParser(
        description="Safely scan and clean rebuildable junk files across local drives.",
    )
    parser.add_argument(
        "action",
        nargs="?",
        choices=("scan", "clean"),
        default="scan",
        help="scan only or clean after scanning",
    )
    parser.add_argument("--level", type=int, choices=CLEANUP_LEVEL_CHOICES, help="cleanup level: 1 keeps current safe behavior, 2 adds deeper WeChat or QQ resource cleanup plus a global 2-year stale-file review across local drives")
    parser.add_argument("--scope", choices=("user", "machine"))
    parser.add_argument("--profile", choices=("conservative", "standard", "aggressive"))
    add_bool_flag(parser, "include-trash", "include recycle bin or trash contents")
    add_bool_flag(parser, "include-package-caches", "include rebuildable package-manager and developer caches")
    parser.add_argument("--execute", action="store_true", help="required for non-interactive cleanup")
    parser.add_argument("--interactive", action="store_true", help="ask for scope, profile, and confirmation")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of human-readable text")
    parser.add_argument("--list-supported-software", action="store_true", help="show the curated software catalog and exit")
    parser.add_argument(
        "--specialty",
        action="append",
        choices=SPECIALTY_CHOICES,
        help="limit cleanup to a specialty panel such as qq, wechat, common, developer, residual, or system-drive",
    )
    parser.add_argument("--panel-summary", action="store_true", help="show specialty panel totals for the current scan")
    parser.add_argument("--large-files", action="store_true", help="scan for large user files and report only")
    parser.add_argument("--duplicate-files", action="store_true", help="scan for duplicate user files and report only")
    parser.add_argument("--min-file-size-mb", type=int, default=512, help="minimum file size in MiB for large-file or duplicate-file review")
    parser.add_argument("--top", type=int, default=20, help="maximum number of large-file items or duplicate groups to report")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    os_name = detect_os()

    if args.list_supported_software:
        summary = build_supported_software_summary()
        if args.json:
            print(json.dumps(summary, indent=2))
        else:
            print_supported_software(summary)
        return 0

    if args.large_files and args.duplicate_files:
        parser.error("--large-files and --duplicate-files are mutually exclusive")

    if args.interactive:
        args = resolve_interactive_args(args)
    else:
        args = resolve_defaults(args)

    if args.large_files:
        _, volumes = build_targets(
            os_name,
            args.scope,
            args.profile,
            args.include_trash,
            args.include_package_caches,
        )
        report = build_large_file_report(volumes, os_name, args.min_file_size_mb, args.top)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print_large_file_report(report)
        return 0

    if args.duplicate_files:
        _, volumes = build_targets(
            os_name,
            args.scope,
            args.profile,
            args.include_trash,
            args.include_package_caches,
        )
        report = build_duplicate_report(volumes, os_name, args.min_file_size_mb, args.top)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print_duplicate_report(report)
        return 0

    if args.action == "clean" and not args.execute and not args.interactive:
        parser.error("clean requires --execute unless --interactive is used")

    targets, volumes = build_targets(
        os_name,
        args.scope,
        args.profile,
        args.include_trash,
        args.include_package_caches,
    )
    targets = filter_targets_by_level(targets, args.level)
    targets = filter_targets_by_specialties(targets, args.specialty)
    global_stale_report = None
    if args.level >= 2:
        global_stale_report = build_global_stale_report(volumes, os_name, LEVEL_TWO_STALE_HOURS, args.top)

    scan_entries = [summarize_target(target) for target in targets]
    scan_report = compile_report(
        scan_entries,
        volumes,
        os_name,
        args.scope,
        args.profile,
        args.level,
        args.include_trash,
        args.include_package_caches,
    )
    panel_report = build_panel_report(scan_entries)

    if args.json and args.action != "clean":
        payload = {"scan": scan_report}
        if args.panel_summary or args.specialty:
            payload["panels"] = panel_report
        if global_stale_report is not None:
            payload["global_stale_review"] = global_stale_report
        print(json.dumps(payload, indent=2))
    elif not args.json:
        print_human_report("Scan Report", scan_report)
        if args.panel_summary or args.specialty:
            print("")
            print_panel_report(panel_report)
        if global_stale_report is not None:
            print("")
            print_global_stale_report(global_stale_report)

    should_clean = args.action == "clean"
    if args.interactive and not should_clean:
        should_clean = prompt_yes_no("Run cleanup now", scan_report["total_bytes"] > 0)
    elif args.interactive and should_clean:
        should_clean = prompt_yes_no("Proceed with cleanup now", True)

    if not should_clean:
        return 0

    clean_entries = [clean_target(target) for target in targets]
    clean_report = compile_report(
        clean_entries,
        volumes,
        os_name,
        args.scope,
        args.profile,
        args.level,
        args.include_trash,
        args.include_package_caches,
    )
    clean_panel_report = build_panel_report(clean_entries)

    if args.json:
        payload = {"scan": scan_report, "clean": clean_report}
        if args.panel_summary or args.specialty:
            payload["panels"] = {
                "scan": panel_report,
                "clean": clean_panel_report,
            }
        if global_stale_report is not None:
            payload["global_stale_review"] = global_stale_report
        print(json.dumps(payload, indent=2))
    else:
        print("")
        print_human_report("Cleanup Report", clean_report)
        if args.panel_summary or args.specialty:
            print("")
            print_panel_report(clean_panel_report)
        if global_stale_report is not None:
            print("")
            print_global_stale_report(global_stale_report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
