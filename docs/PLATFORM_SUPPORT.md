# Harn-LLM Tester 平台支持与终端管理

## 概述

Harn-LLM Tester 现已支持跨平台运行，提供统一的终端管理接口，支持：
- **macOS**: tmux（原生支持）
- **Linux**: tmux（原生支持）
- **Windows**: Windows Terminal / PowerShell（新增支持）

## 平台检测

### 使用方法

```python
from core.platform_manager import is_windows, is_macos, is_linux, ACTIVE

if is_windows():
    # Windows 特定逻辑
    pass
elif is_macos():
    # macOS 特定逻辑
    pass
else:
    # Linux 逻辑
    pass
```

### 环境变量覆盖

可以通过环境变量强制指定平台：
```bash
export AUTOTEST_PLATFORM=windows  # 或 macos, linux
```

## 终端管理

### Unix 系统（macOS/Linux）

使用 `tmux` 进行会话管理：

```python
from core.tmux_manager import (
    open_tmux_window,
    kill_tmux_session,
    capture_tmux_pane,
    list_autotester_tmux_sessions,
)

# 创建新会话
result = open_tmux_window(
    session_name="autotester__test",
    window_name="exec",
    script_path=Path("/path/to/script.sh"),
    log_path=Path("/path/to/log.txt"),
    title="Test Execution",
    create_session=True,
)

# 列出所有会话
sessions = list_autotester_tmux_sessions()

# 捕获输出
content = capture_tmux_pane("autotester__test:0", line_count=200)

# 杀掉会话
kill_tmux_session("autotester__test")
```

### Windows 系统

使用 Windows Terminal 或 PowerShell：

```python
from core.windows_terminal_manager import (
    open_windows_terminal,
    write_powershell_job_script,
    list_windows_terminal_tabs,
    kill_windows_terminal_tab,
)

# 创建 PowerShell 脚本
write_powershell_job_script(
    script_path=Path("C:/path/to/script.ps1"),
    launch_cwd=Path("C:/workspace"),
    mkdir_paths=[Path("C:/output")],
    env_exports={"AUTOTEST_VAR": "value"},
    runner_command="python run.py",
    title="Test Execution",
)

# 打开 Windows Terminal
result = open_windows_terminal(
    profile_name="autotester__test",
    script_path=Path("C:/path/to/script.ps1"),
    log_path=Path("C:/path/to/log.txt"),
    title="Test Execution",
)

# 列出运行中的标签页
tabs = list_windows_terminal_tabs()

# 杀掉特定进程
kill_windows_terminal_tab(process_id=12345)
```

### 统一接口

使用 `TerminalSession` 类实现跨平台统一接口：

```python
from core.windows_terminal_manager import TerminalSession

# 创建会话
session = TerminalSession("autotester__test")

# 启动会话
result = session.launch(
    script_path=Path("/path/to/script"),
    log_path=Path("/path/to/log"),
    title="Test Execution",
)

# 检查会话是否存在
exists = session.exists()

# 捕获输出
content = session.capture(line_count=200)

# 杀掉会话
session.kill()
```

## Windows 特性

### 防止系统休眠

在长时间运行测试时，可以防止 Windows 进入休眠状态：

```python
from core.windows_terminal_manager import _windows_keep_awake_start, _windows_keep_awake_stop

# 开始测试前
_windows_keep_awake_start()

# 测试完成后
_windows_keep_awake_stop()
```

## 会话命名规范

### Unix（tmux）

格式：`autotester__{timestamp}__{harness}__{stage}__{source}__{target}`

示例：
- `autotester__20260625-143022__opencode__exec__DemoProject__browser-form-automation`
- `autotester__20260625-143022__claude__sample__ClawhubTop1000__agent-browser-2`

### Windows（Terminal Tab Title）

格式：与 Unix 相同，用作窗口标题

示例：
- `autotester__20260625-143022__opencode__exec__DemoProject__browser-form-automation`

## 脚本生成

### Bash 脚本（Unix）

```bash
#!/usr/bin/env bash
set -u
set -o pipefail
echo '========================================'
echo '  Harn-LLM Tester - {title}'
echo '========================================'
echo 'Started at: '$(date '+%Y-%m-%d %H:%M:%S %Z')

mkdir -p {output_dirs}
cd {launch_cwd}
export AUTOTEST_VAR=value

{runner_command} 2>&1 | tee /tmp/autotester-output.log
status=${PIPESTATUS[0]}

echo 'Finished at: '$(date '+%Y-%m-%d %H:%M:%S %Z')
echo 'Exit status: '$status
exec "${SHELL:-/bin/bash}" -l
```

### PowerShell 脚本（Windows）

```powershell
# Harn-LLM Tester Job Script
Write-Host "========================================"
Write-Host "  Harn-LLM Tester - {title}"
Write-Host "========================================"
Write-Host "Started at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"

New-Item -ItemType Directory -Force -Path "{output_path}"
Set-Location "{launch_cwd}"
$env:AUTOTEST_VAR = "value"

{runner_command} 2>&1 | Tee-Object -FilePath $autotester_output_log

Write-Host "Finished at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
Write-Host "Exit status: $LASTEXITCODE"
```

## 健康检查

### Unix（tmux）

通过检查 tmux pane 状态判断：
- `running`: pane 活跃
- `done`: 所有 pane 退出码为 0
- `failed`: 有 pane 退出码非 0
- `dead`: pane 异常退出
- `attention`: 检测到错误模式

### Windows

通过检查 PowerShell 进程状态：
- 检查窗口标题匹配
- 读取进程状态（Running / Not Responding）

## 迁移指南

### 从 SkillTester 迁移

Harn-LLM Tester 的平台管理模块完全兼容 SkillTester 的设计：

| SkillTester | Harn-LLM Tester |
|------------|-----------|
| `dashboard.platinfo` | `core.platform_manager` |
| `SKILLTEST_PLATFORM` | `AUTOTEST_PLATFORM` |
| `auto_loop_unix.py` | `core.tmux_manager` |
| `auto_loop_windows.py` | `core.windows_terminal_manager` |

### API 兼容性

所有 SkillTester 的平台检测 API 在 Harn-LLM Tester 中保持相同签名：

```python
# SkillTester
from dashboard.platinfo import is_windows, is_macos, is_linux

# Harn-LLM Tester
from core.platform_manager import is_windows, is_macos, is_linux
```

## 最佳实践

1. **优先使用统一接口**：使用 `TerminalSession` 类而不是直接调用平台特定 API
2. **环境变量导出**：使用提供的脚本生成函数，确保跨平台兼容
3. **错误处理**：始终检查返回的 `success` 字段
4. **资源清理**：在测试完成后调用 `kill()` 清理会话

## 故障排查

### Windows

**问题**: Windows Terminal 未找到
**解决**: 自动降级到 PowerShell 窗口

**问题**: 权限错误
**解决**: 确保脚本有执行权限，检查 PowerShell 执行策略

### Unix

**问题**: tmux 未安装
**解决**: `brew install tmux` (macOS) 或 `apt-get install tmux` (Linux)

**问题**: 会话已存在
**解决**: 使用不同的时间戳或先调用 `kill_tmux_session()`

## 性能考虑

- **Windows**: PowerShell 启动比 tmux 稍慢，但差距在可接受范围
- **Unix**: tmux 会话管理开销极低
- **日志**: 所有平台都使用相同的日志格式和结构
