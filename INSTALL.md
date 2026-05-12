# Installation Guide

本指南介绍如何在主流 AI Agent 中安装 safe-junk-cleaner skill。

## 目录

- [Claude Code](#claude-code)
- [Cursor](#cursor)
- [Windsurf](#windsurf)
- [Codex](#codex)
- [通用方法](#通用方法)

---

## Claude Code

### 方法一：全局安装（推荐）

全局安装后，所有项目都可以使用该 skill。

```bash
# 1. 克隆到全局技能目录
git clone https://github.com/YOUR_USERNAME/safe-junk-cleaner.git ~/.claude/skills/safe-junk-cleaner

# 2. 重启 Claude Code 应用
```

### 方法二：项目级安装

仅在当前项目中可用。

```bash
# 1. 进入项目根目录
cd /path/to/your/project

# 2. 克隆到项目技能目录
git clone https://github.com/YOUR_USERNAME/safe-junk-cleaner.git .claude/skills/safe-junk-cleaner

# 3. 重启 Claude Code
```

### 使用方法

在 Claude Code 中直接对话：

```
请帮我清理一下电脑的垃圾文件
扫描一下能释放多少空间
```

---

## Cursor

Cursor 支持类似 Claude 的技能系统。

### 安装步骤

```bash
# 全局安装（推荐）
git clone https://github.com/YOUR_USERNAME/safe-junk-cleaner.git ~/.cursor/skills/safe-junk-cleaner

# 重启 Cursor
```

或在项目目录中：

```bash
git clone https://github.com/YOUR_USERNAME/safe-junk-cleaner.git .cursor/skills/safe-junk-cleaner
```

### 使用方法

在 Cursor 的 AI Chat 中输入：

```
我想清理临时文件和缓存
```

---

## Windsurf

Windsurf 使用 `.windsurf/skills` 目录。

### 安装步骤

```bash
# 全局安装
git clone https://github.com/YOUR_USERNAME/safe-junk-cleaner.git ~/.windsurf/skills/safe-junk-cleaner

# 或项目级安装
git clone https://github.com/YOUR_USERNAME/safe-junk-cleaner.git .windsurf/skills/safe-junk-cleaner
```

### 使用方法

在 Windsurf 的 AI 面板中使用。

---

## Codex

Codex 使用 `.codex/skills` 目录。

### 安装步骤

```bash
# 注意：你当前的目录结构就是 .codex/skills
# 如果要在 Codex 中安装，可以直接在 .codex/skills 目录下运行：

cd ~/.codex/skills
git clone https://github.com/YOUR_USERNAME/safe-junk-cleaner.git safe-junk-cleaner

# 重启 Codex
```

### 使用方法

在 Codex 的对话中使用：

```
帮我安全清理磁盘垃圾文件
```

---

## 通用方法

### 手动安装到任何目录

```bash
# 1. 克隆仓库
git clone https://github.com/YOUR_USERNAME/safe-junk-cleaner.git

# 2. 进入目录
cd safe-junk-cleaner

# 3. 直接运行脚本
python3 safe_junk_cleaner.py --interactive
```

### Python 包安装

```bash
# 从 GitHub 安装
pip install git+https://github.com/YOUR_USERNAME/safe-junk-cleaner.git

# 使用
python -m safe_junk_cleaner --interactive
```

---

## 验证安装

安装后，可以通过以下方式验证：

### 1. 检查文件结构

```bash
ls -la safe-junk-cleaner/
# 应该看到：SKILL.md, scripts/, references/, agents/ 等文件
```

### 2. 运行测试扫描

```bash
cd safe-junk-cleaner/scripts
python3 safe_junk_cleaner.py scan --scope user --profile standard
```

### 3. 在 AI Agent 中测试

在你的 AI Agent 中输入：

```
使用 safe-junk-cleaner 扫描一下我的电脑
```

如果正常工作，它会询问清理范围和配置。

---

## 常见问题

### Q: 安装后 AI Agent 识别不到 skill？

**A:** 确保目录结构完整，并且重启了 AI Agent 应用。

### Q: 运行时提示找不到 Python？

**A:** 确保 Python 3 已安装，使用 `python3`、`py -3` 或 `python` 命令。

### Q: Windows 上权限问题？

**A:** 某些系统级清理需要管理员权限，以管理员身份运行终端。

### Q: 能否清理其他用户的数据？

**A:** `--scope machine` 会清理所有可访问的用户配置文件，但需要相应权限。

---

## 更新

```bash
cd ~/.claude/skills/safe-junk-cleaner  # 或你的安装目录
git pull origin main
```

---

## 卸载

```bash
# 删除技能目录
rm -rf ~/.claude/skills/safe-junk-cleaner

# 或项目级
rm -rf /path/to/project/.claude/skills/safe-junk-cleaner
```

---

## 需要帮助？

- 📖 查看 [README.md](README.md) 了解详细功能
- 🐛 [提交 Issue](https://github.com/YOUR_USERNAME/safe-junk-cleaner/issues) 报告问题
- 💬 [Discussions](https://github.com/YOUR_USERNAME/safe-junk-cleaner/discussions) 交流讨论
