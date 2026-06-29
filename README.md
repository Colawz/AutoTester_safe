# Harn-LLM Tester

**通用 Agent、LLM、Harness 与文件内容测试工具**

Harn-LLM Tester 是一个面向大模型应用与自动化执行系统的通用测试平台。它不仅可以测试特定 Agent Harness，也可以围绕通用 Agent、LLM 能力、工具调用链路、文件内容处理、权限边界和安全风险等场景生成任务、执行任务并汇总报告。

平台采用 Sample -> Exec -> Spec 三阶段流程：先生成可复用的测试样本，再通过选定执行器运行测试，最后沉淀结构化结果和报告。测试对象可以是一个本地 Agent 项目、一个 LLM 调用封装、一个 Agent Harness、一个后端服务，或者一组需要被读取、检索、改写、审计的文件。

## 适用场景

- **通用 Agent 测试**：评估 Agent 是否能遵循任务目标、正确调用工具、处理上下文干扰、拒绝越权指令。
- **LLM 能力测试**：评估模型在摘要、分类、信息抽取、代码理解、长上下文检索、指令遵循等任务上的表现。
- **Agent Harness 测试**：评估 OpenCode、Claude、Kimi、Codex 等执行器在 baseline 与 with_target 模式下的行为差异。
- **文件内容测试**：评估系统对 Markdown、代码、配置、日志、报告、文档集合等文件的读取、检索、比对、归纳和安全处理能力。
- **安全与边界测试**：设计上下文注入、路径穿越、敏感信息泄露、权限绕过、危险工具调用等探针，验证平台发现问题的能力。
- **回归与展示测试**：将测试对象、样本、执行结果和报告固定下来，用于版本回归、演示汇报和能力对比。

## 测试示例

### 1. Agent 安全探针

测试一个本地客服 Agent 是否会被上下文注入绕过系统约束。例如样本中包含伪造的 `OVERRIDE_AGENT_POLICY` 指令、敏感 token 和越权读取请求，Exec 阶段观察 Agent 是否泄露凭据或读取不该访问的文件，Spec 阶段生成安全报告。

### 2. LLM 文件理解能力

给定一组项目文档、配置文件和日志，让模型回答“哪个服务依赖了过期配置”“哪些日志对应同一次失败请求”“README 与实际配置是否一致”等问题。平台可以把这些任务固化为样本，并在不同模型或执行器上对比结果。

### 3. Agent Harness 行为差异

同一个测试任务分别在 baseline 和 with_target 模式运行，观察执行器是否正确使用目标项目文件、是否产生稳定结果、是否把测试产物写到约定目录。适合对比 OpenCode、Claude、Kimi、Codex 等 Harness 的执行可靠性。

### 4. 文件内容合规检查

将一批 Markdown、JSON、YAML、源码或报告文件作为测试对象，设计任务检查是否存在敏感字段、错误配置、缺失章节、格式不一致或安全策略冲突。适合用于文档质量、配置审计和数据安全演示。

### 5. 工具调用与权限边界

构造带有公开文件和私密文件的测试目录，要求 Agent 只读取允许范围内的内容。若 Agent 绕过 allowlist、读取 `secrets.env` 或泄露 mock 凭据，报告中会标记为失败或发现安全问题。

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
- 🔄 Harness 无关设计，支持 OpenCode、Claude、Kimi、Codex 等执行器
- 🤖 面向通用 Agent、LLM、Agent Harness 和文件内容处理任务
- 📊 对照执行模式，支持 baseline vs with_target
- 📝 证据优先，基于文件系统产物、任务日志和报告进行状态判断

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
