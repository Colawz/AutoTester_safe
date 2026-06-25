# AutoTester 启动指南

## 启动方式

AutoTester 提供两种启动方式：

### 1. 交互式启动（推荐）

```bash
python3 launch.py
```

交互式启动会引导你选择测试拉起平台：
- ✅ 平台选择（macOS / Linux / Windows / 自动检测）

**示例输出**：
```
╔═══════════════════════════════════════════════════════════════╗
║   █████╗ ███████╗ ██████╗ ██████╗ ███████╗████████╗██████╗  ║
║  ██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔════╝╚══██╔══╝██╔══██╗ ║
║  ███████║███████╗██║     ██║   ██║███████╗   ██║   ██████╔╝ ║
║  ██╔══██║╚════██║██║     ██║   ██║╚════██║   ██║   ██╔══██╗ ║
║  ██║  ██║███████║╚██████╗╚██████╔╝███████║   ██║   ██║  ██║ ║
║  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ║
║         Automated Agent Harness Testing Framework             ║
╚═══════════════════════════════════════════════════════════════╝

🖥️  Platform Selection
============================================================
  Auto-detected: MACOS

  Available platforms:
    [1] macOS     (tmux)
    [2] Linux     (tmux)
    [3] Windows   (Windows Terminal / PowerShell)
    [A] Auto      (use detected platform)

  Select platform [1-3/A] (default: A): A

  ✓ Using auto-detected platform: MACOS
  ✓ Platform environment set: AUTOTEST_PLATFORM=macos

============================================================
  🚀 Starting AutoTester Server...
============================================================
  Platform:     MACOS
  Server URL:   http://127.0.0.1:8700
  Reports URL:  http://127.0.0.1:8700/reports
============================================================
```

### 2. 快速启动（命令行参数）

```bash
# 自动检测平台
python3 start.py

# 指定平台
python3 start.py --platform macos
python3 start.py --platform linux
python3 start.py --platform windows

# 自定义端口
python3 start.py --port 8080

# 自定义 host 和 port
python3 start.py --host 0.0.0.0 --port 8080

# 查看帮助
python3 start.py --help
```

**命令行参数**：
```
usage: start.py [-h] [--platform {macos,linux,windows,auto}] [--host HOST]
                [--port PORT]

AutoTester - Automated Agent Harness Testing Framework

options:
  -h, --help            show this help message and exit
  --platform {macos,linux,windows,auto}, -p {macos,linux,windows,auto}
                        Platform to use (default: auto-detect)
  --host HOST           Server host (default: from config)
  --port PORT           Server port (default: from config)
```

### 3. 直接启动（开发模式）

```bash
# 直接启动 Flask 应用
python3 -m api.app
```

## 平台说明

### macOS

**终端管理**: tmux

**要求**:
```bash
# 安装 tmux
brew install tmux
```

**特性**:
- ✅ 原生支持
- ✅ 会话持久化
- ✅ 窗口管理
- ✅ 日志捕获

### Linux

**终端管理**: tmux

**要求**:
```bash
# Ubuntu/Debian
sudo apt-get install tmux

# CentOS/RHEL
sudo yum install tmux
```

**特性**:
- ✅ 原生支持
- ✅ 会话持久化
- ✅ 窗口管理
- ✅ 日志捕获

### Windows

**终端管理**: Windows Terminal / PowerShell

**要求**:
- Windows 10/11
- Windows Terminal（推荐）或 PowerShell

**特性**:
- ✅ Windows Terminal 支持
- ✅ PowerShell 降级支持
- ✅ 防休眠功能
- ⚠️  会话管理有限（相比 tmux）

## 环境变量

可以通过环境变量覆盖配置：

```bash
# 强制指定平台
export AUTOTEST_PLATFORM=macos  # 或 linux, windows

# 启动
python3 start.py
```

## 配置文件

服务器配置在 `config.yaml`:

```yaml
server:
  host: 127.0.0.1
  port: 8700
  max_upload_size_mb: 50
```

## 常见问题

### Q: 如何选择平台？

**A**:
- 大多数情况选择 "Auto" 即可
- 如果在 WSL 中运行，选择 "Linux"
- 如果在远程服务器运行，选择对应平台

### Q: macOS/Linux 提示 tmux 未找到？

**A**: 安装 tmux:
```bash
# macOS
brew install tmux

# Linux
sudo apt-get install tmux
```

### Q: Windows 上无法启动？

**A**:
1. 确保使用 Python 3.8+
2. 安装依赖: `pip install -r requirements.txt`
3. 尝试使用 PowerShell 管理员模式

### Q: 端口被占用怎么办？

**A**:
```bash
# 使用其他端口
python3 start.py --port 8080

# 或修改 config.yaml
```

### Q: 如何在后台运行？

**A**:
```bash
# 使用 nohup
nohup python3 start.py &

# 或使用 systemd / supervisor（生产环境推荐）
```

## 示例场景

### 场景 1: 本地开发

```bash
# 交互式启动，选择 macOS
python3 launch.py
# 选择: [A] Auto -> Enter
```

### 场景 2: 远程服务器

```bash
# 快速启动，监听所有接口
python3 start.py --host 0.0.0.0 --port 8080
```

### 场景 3: Windows 开发

```bash
# 交互式启动
python3 launch.py
# 选择: [3] Windows -> Enter
```

## 性能建议

- **macOS/Linux**: tmux 性能优秀，无特殊要求
- **Windows**: 建议使用 Windows Terminal（比 PowerShell 更快）
- **远程服务器**: 建议使用 `--host 0.0.0.0` 以允许外部访问

## 下一步

启动成功后：
1. 访问 Dashboard: http://localhost:8700/
2. 访问报告页面: http://localhost:8700/reports
3. 查看 API 文档: http://localhost:8700/api/

祝测试愉快！🎉

## 平台说明

### macOS

**终端管理**: tmux

**要求**:
```bash
# 安装 tmux
brew install tmux
```

**特性**:
- ✅ 原生支持
- ✅ 会话持久化
- ✅ 窗口管理
- ✅ 日志捕获

### Linux

**终端管理**: tmux

**要求**:
```bash
# Ubuntu/Debian
sudo apt-get install tmux

# CentOS/RHEL
sudo yum install tmux
```

**特性**:
- ✅ 原生支持
- ✅ 会话持久化
- ✅ 窗口管理
- ✅ 日志捕获

### Windows

**终端管理**: Windows Terminal / PowerShell

**要求**:
- Windows 10/11
- Windows Terminal（推荐）或 PowerShell

**特性**:
- ✅ Windows Terminal 支持
- ✅ PowerShell 降级支持
- ✅ 防休眠功能
- ⚠️  会话管理有限（相比 tmux）

## 环境变量

可以通过环境变量覆盖配置：

```bash
# 强制指定平台
export AUTOTEST_PLATFORM=macos  # 或 linux, windows

# 启动
python3 start.py
```

## 配置文件

服务器配置在 `config.yaml`:

```yaml
server:
  host: 127.0.0.1
  port: 8700
  max_upload_size_mb: 50
```

## 常见问题

### Q: 如何选择平台？

**A**:
- 大多数情况选择 "Auto" 即可
- 如果在 WSL 中运行，选择 "Linux"
- 如果在远程服务器运行，选择对应平台

### Q: macOS/Linux 提示 tmux 未找到？

**A**: 安装 tmux:
```bash
# macOS
brew install tmux

# Linux
sudo apt-get install tmux
```

### Q: Windows 上无法启动？

**A**:
1. 确保使用 Python 3.8+
2. 安装依赖: `pip install -r requirements.txt`
3. 尝试使用 PowerShell 管理员模式

### Q: 端口被占用怎么办？

**A**:
```bash
# 使用其他端口
python3 start.py --port 8080

# 或修改 config.yaml
```

### Q: 如何在后台运行？

**A**:
```bash
# 使用 nohup
nohup python3 start.py &

# 或使用 systemd / supervisor（生产环境推荐）
```

## 示例场景

### 场景 1: 本地开发

```bash
# 交互式启动，选择 macOS
python3 launch.py
# 选择: [A] Auto -> [1] Server -> Enter -> Enter
```

### 场景 2: 远程服务器

```bash
# 快速启动，监听所有接口
python3 start.py --host 0.0.0.0 --port 8080
```

### 场景 3: CI/CD 集成

```bash
# 启动 AutoTest 控制器
python3 start.py --mode autotest --platform linux
```

### 场景 4: Windows 开发

```bash
# 交互式启动
python3 launch.py
# 选择: [3] Windows -> [1] Server -> Enter -> Enter
```

### 场景 5: 调试模式

```bash
# 交互模式，可以实时查看状态
python3 start.py --mode interactive

autotester> status    # 查看状态
autotester> targets   # 查看 targets
autotester> sessions  # 查看活动会话
autotester> quit      # 退出
```

## 性能建议

- **macOS/Linux**: tmux 性能优秀，无特殊要求
- **Windows**: 建议使用 Windows Terminal（比 PowerShell 更快）
- **远程服务器**: 建议使用 `--host 0.0.0.0` 以允许外部访问

## 下一步

启动成功后：
1. 访问 Dashboard: http://localhost:8700/
2. 访问报告页面: http://localhost:8700/reports
3. 查看 API 文档: http://localhost:8700/api/

祝测试愉快！🎉
