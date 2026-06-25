# AutoTester

**通用 Agent Harness 自动化评测工具**

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动服务

#### 方式 1: 交互式启动（推荐）

```bash
python3 launch.py
```

按照提示选择测试拉起平台（macOS/Linux/Windows）。

#### 方式 2: 快速启动

```bash
# 自动检测平台
python3 start.py

# 指定平台
python3 start.py --platform macos

# 自定义端口
python3 start.py --port 8080
```

#### 方式 3: 直接启动

```bash
python3 -m api.app
```

### 访问界面

启动成功后访问：
- **Dashboard**: http://localhost:8700/
- **报告浏览**: http://localhost:8700/reports
- **API 文档**: http://localhost:8700/api/

## 平台支持

| 平台 | 终端管理 | 状态 |
|------|---------|------|
| macOS | tmux | ✅ 完全支持 |
| Linux | tmux | ✅ 完全支持 |
| Windows | Windows Terminal / PowerShell | ✅ 支持 |

## 主要功能

### 1. 通用评测框架
- 🔄 Harness 无关设计（支持 OpenCode、Claude、Kimi、Codex）
- 📊 对照执行模式（baseline vs with_target）
- 📝 证据优先（基于文件系统产物）

### 2. 三阶段流水线
- **Sample** - 生成测试任务包
- **Exec** - 执行测试任务
- **Spec** - 生成评测报告

### 3. 报告浏览
- 📊 Web 界面浏览报告
- 📋 任务预览和详情
- 🔍 搜索和过滤

### 4. 跨平台支持
- 🖥️ macOS / Linux (tmux)
- 🪟 Windows (Windows Terminal)

## 文档

- [启动指南](docs/LAUNCH_GUIDE.md) - 详细的启动说明
- [平台支持](docs/PLATFORM_SUPPORT.md) - 跨平台技术文档
- [开发文档](开发文档.md) - 架构和实现细节

## 目录结构

```
software/
├── launch.py              # 交互式启动脚本
├── start.py               # 快速启动脚本
├── config.yaml            # 配置文件
├── 开发文档.md            # 开发文档
│
├── core/                  # 核心逻辑
│   ├── platform_manager.py        # 平台管理
│   ├── tmux_manager.py           # tmux 管理
│   ├── windows_terminal_manager.py # Windows 终端管理
│   └── scanner.py                # 扫描器
│
├── api/                   # REST API
│   ├── app.py            # Flask 应用
│   ├── routes_target.py  # Target 管理
│   ├── routes_stage.py   # Stage 操作
│   └── routes_query.py   # 查询接口
│
├── dashboard/             # Web 前端
│   ├── index.html        # 主页面
│   ├── reports.html      # 报告页面
│   └── static/           # 静态资源
│
├── harnesses/             # Harness 适配器
│   ├── opencode.py
│   ├── claude.py
│   ├── kimi.py
│   └── codex.py
│
├── agents/                # Agent 定义
│   ├── SampleAgent/
│   ├── ExecAgent/
│   └── SpecAgent/
│
├── autotest/              # 自动测试控制器
│   └── controller.py
│
└── docs/                  # 文档
    ├── LAUNCH_GUIDE.md
    └── PLATFORM_SUPPORT.md
```

## 配置

编辑 `config.yaml` 配置文件：

```yaml
# 服务器配置
server:
  host: 127.0.0.1
  port: 8700
  max_upload_size_mb: 50

# 默认 Harness
default_harness: opencode

# Harness 列表
harnesses:
  opencode:
    display_name: OpenCode
    enabled: true
  claude:
    display_name: Claude Code
    enabled: true
  kimi:
    display_name: KimiCode
    enabled: false
  codex:
    display_name: Codex CLI
    enabled: false
```

## API 端点

### Target 管理
- `GET /api/targets` - 获取所有 targets
- `POST /api/targets` - 创建新 target
- `GET /api/targets/{name}` - 获取 target 详情
- `DELETE /api/targets/{name}` - 删除 target

### Stage 操作
- `POST /api/stage/sample/{name}` - 启动 Sample 阶段
- `POST /api/stage/exec/{name}` - 启动 Exec 阶段
- `POST /api/stage/spec/{name}` - 启动 Spec 阶段

### 查询接口
- `GET /api/tmux/sessions` - 获取活动会话
- `GET /api/targets/{name}/tasks` - 获取任务列表
- `GET /api/targets/{name}/tasks/{id}/report` - 获取任务报告
- `GET /api/results/{name}` - 获取完整结果

## 开发

### 运行测试

```bash
pytest tests/
```

### 代码风格

```bash
# 格式化代码
black .

# 类型检查
mypy .
```

## 故障排查

### tmux 未找到（macOS/Linux）

```bash
# macOS
brew install tmux

# Linux
sudo apt-get install tmux
```

### 端口被占用

```bash
# 使用其他端口
python3 start.py --port 8080
```

### Windows 权限错误

以管理员身份运行 PowerShell。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 致谢

设计参考：
- [Web_dashboard](../Web_dashboard) - UI 设计
- [迁移repo](../迁移repo) - 平台支持逻辑
