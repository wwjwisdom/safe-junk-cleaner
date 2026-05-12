# Safe Junk Cleaner

**一个跨平台的安全垃圾文件清理工具**

Safe Junk Cleaner 是一个保守而强大的磁盘清理工具，用于安全地清理临时文件、浏览器缓存、应用缓存、着色器缓存、崩溃转储、缩略图、日志、回收站/垃圾桶以及可选的包管理器缓存。

## ✨ 特性

- **🛡️ 安全第一** - 只清理已知的垃圾位置和缓存目录，从不触碰文档、媒体、项目或用户数据
- **🌍 跨平台支持** - 完整支持 Windows、macOS 和 Linux
- **🎯 三种清理模式** - conservative（保守）、standard（标准）、aggressive（激进）
- **📊 详细报告** - 清理前预览，显示可回收空间和分类统计
- **🔍 智能扫描** - 自动检测所有本地驱动器上的用户配置文件
- **⚙️ 高度可配置** - 支持用户/机器范围、回收站清理、包管理器缓存等选项

## 🚀 快速开始

### 基本用法

```bash
# 扫描模式（推荐先运行）
python3 safe_junk_cleaner.py scan --scope machine --profile standard --include-trash

# 清理模式（需要 --execute 确认）
python3 safe_junk_cleaner.py clean --scope machine --profile standard --include-trash --execute

# 交互式模式
python3 safe_junk_cleaner.py --interactive
```

### 命令行选项

- `scan` / `clean` - 扫描或清理操作
- `--scope {user|machine}` - 清理范围（当前用户 / 整机）
- `--profile {conservative|standard|aggressive}` - 清理强度
- `--include-trash` / `--no-include-trash` - 是否清空回收站
- `--include-package-caches` / `--no-include-package-caches` - 是否清理包管理器缓存
- `--execute` - 确认执行清理（clean 模式必需）
- `--interactive` - 交互式询问所有选项
- `--json` - 输出 JSON 格式报告

## 📦 清理内容

### Windows
- 临时文件（`%TEMP%`、`%SystemRoot%\Temp`）
- 浏览器缓存（Chrome、Edge、Firefox、Brave、Vivaldi）
- 应用缓存（VS Code、Discord、Slack、Teams 等）
- GPU 着色器缓存（NVIDIA、AMD）
- 缩略图和图标缓存
- 崩溃转储和内存转储
- Windows 错误报告（WER）
- 每个驱动器的回收站

### macOS
- `~/Library/Caches`、`~/Library/Logs`
- 崩溃报告
- `.Trash`（垃圾桶）
- 系统临时目录（`/tmp`、`/private/var/tmp`）
- 挂载卷的 `.Trashes` 文件夹

### Linux
- `~/.cache`、`~/.thumbnails`
- 系统临时目录（`/tmp`、`/var/tmp`、`/var/crash`）
- 挂载卷的 trash 文件夹
- 可选：发行版包管理器缓存（apt、dnf、yum、pacman、apk）

## 🛡️ 安全承诺

**永不触碰以下内容：**
- ❌ 文档、桌面、下载、图片、视频、音乐等用户文件夹
- ❌ 项目文件夹、代码仓库、工作空间
- ❌ 云同步根目录（OneDrive、iCloud Drive、Dropbox、Google Drive）
- ❌ 浏览器 cookies、历史记录、密码库
- ❌ 数据库文件、虚拟机、磁盘镜像
- ❌ 已安装程序、驱动、还原点

## 📋 安装方法

### 方法一：直接下载（推荐）

1. 下载本仓库
2. 运行脚本：
   ```bash
   python3 safe_junk_cleaner.py --interactive
   ```

### 方法二：作为 Skill 使用

**适用于支持技能的系统（如 Codex / Cursor / Windsurf / Claude Code）**

1. 将仓库克隆到技能目录：
   ```bash
   # 全局安装（推荐）
   git clone https://github.com/YOUR_USERNAME/safe-junk-cleaner.git ~/.claude/skills/safe-junk-cleaner

   # 或项目级安装
   git clone https://github.com/YOUR_USERNAME/safe-junk-cleaner.git .claude/skills/safe-junk-cleaner
   ```

2. 重启你的 AI Agent 应用
3. 在对话中直接使用，例如：
   ```
   帮我清理一下电脑的垃圾文件
   扫描一下能释放多少空间
   ```

### 方法三：Python 包安装

```bash
# 从 GitHub 安装
pip install git+https://github.com/YOUR_USERNAME/safe-junk-cleaner.git

# 使用
python -m safe_junk_cleaner --interactive
```

## 🎯 使用示例

### 示例 1：标准清理
```bash
# 扫描
python3 safe_junk_cleaner.py scan --scope machine --profile standard --include-trash

# 查看报告后清理
python3 safe_junk_cleaner.py clean --scope machine --profile standard --include-trash --execute
```

### 示例 2：保守清理（仅当前用户）
```bash
python3 safe_junk_cleaner.py clean --scope user --profile conservative --no-include-trash --execute
```

### 示例 3：激进清理（开发者推荐）
```bash
python3 safe_junk_cleaner.py clean --scope machine --profile aggressive --include-trash --include-package-caches --execute
```

### 示例 4：仅清理包管理器缓存
```bash
python3 safe_junk_cleaner.py clean --scope machine --profile standard --include-package-caches --execute
```

## 📊 报告示例

```
Scan Report
Platform: windows
Scope: machine
Profile: standard
Mounted local volumes: C:\, D:\
Reclaimable space: 3.2 GiB
Eligible files: 48,392

By category:
  - Temporary Files: 1.2 GiB
  - Browser Caches: 856.3 MiB
  - App Caches: 512.4 MiB
  - Shader Caches: 256.1 MiB
  - Thumbnails and Icons: 128.7 MiB
  - Logs: 64.2 MiB
  - Crash Dumps and Reports: 48.3 MiB
  - Recycle Bin or Trash: 128.9 MiB

Largest targets:
  - C:\Users\YourName\AppData\Local\Temp: 612.4 MiB
  - Chrome Cache: 234.1 MiB
  - NVIDIA DXCache: 156.8 MiB
```

## 🔧 高级配置

### 临时文件年龄限制
不同 profile 对临时文件的最小年龄有不同要求：
- `conservative`: 72 小时（3天）
- `standard`: 24 小时（1天）
- `aggressive`: 6 小时

受保护的文件扩展名（不会被清理）：
```
.doc, .docx, .pdf, .txt, .jpg, .png, .mp3, .mp4, .zip, .xlsx, .pptx, .sqlite, .kdbx, .pem, .key 等
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 开源许可

本项目采用 MIT 许可证开源 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 设计灵感来自系统自带清理工具的常见功能
- 跨平台兼容性参考了多个开源清理项目的实现
- 感谢所有贡献者和使用者的反馈

## 📮 联系方式

- 作者：wwj
- GitHub：[@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- 问题反馈：[Issues](https://github.com/YOUR_USERNAME/safe-junk-cleaner/issues)

---

⚡ **使用前建议先运行 `scan` 模式，确认清理内容后再执行 `clean`！**
