# AutoTester 更新总结

## 🎯 主要更新

### 1. 跨平台支持

#### 新增文件
- `core/platform_manager.py` - 平台检测与管理
- `core/windows_terminal_manager.py` - Windows Terminal/PowerShell 管理
- `docs/PLATFORM_SUPPORT.md` - 平台支持文档

#### 功能特性
✅ **macOS** - tmux 原生支持
✅ **Linux** - tmux 原生支持
✅ **Windows** - Windows Terminal / PowerShell 支持（新增）

#### 统一接口
```python
from core.windows_terminal_manager import TerminalSession

session = TerminalSession("autotester__test")
session.launch(script_path=..., log_path=..., title=...)
exists = session.exists()
content = session.capture()
session.kill()
```

### 2. 报告浏览模块

#### 新增文件
- `dashboard/reports.html` - 报告浏览页面
- `dashboard/REPORTS_README.md` - 使用文档

#### 新增 API
- `GET /api/targets/{name}/tasks` - 获取任务列表
- `GET /api/targets/{name}/tasks/{task_id}/report` - 获取任务报告
- `GET /reports` - 报告浏览页面

#### 功能特性
✅ Target 卡片列表展示
✅ 任务预览（显示最近 5 个任务）
✅ 点击查看 SpecAgent 报告
✅ 点击查看任务 summary
✅ Markdown 渲染支持
✅ 搜索和过滤功能

### 3. UI 全面美化

#### 设计系统
- 🎨 参照 Web_dashboard 的现代设计
- 🌈 渐变背景和玻璃态效果
- ✨ 动画和过渡效果
- 📱 响应式设计

#### 视觉改进
- **配色方案**: 暖色调 + 自然绿主色
- **字体**: Space Grotesk (标题) + IBM Plex Sans (正文)
- **阴影**: 多层次阴影系统
- **圆角**: 统一的圆角半径 (14px/20px/30px)
- **交互**: 悬停效果、点击反馈

#### 组件优化
- ✅ 卡片悬停动画
- ✅ 按钮渐变效果
- ✅ 状态徽章颜色优化
- ✅ 会话健康指示器动画
- ✅ Toast 通知样式

### 4. Bug 修复

#### 扫描器修复
- ✅ 修复路径解析重复嵌套问题
- ✅ 只要求 `with_target` 完成，`baseline` 可选

## 📁 文件结构

```
software/
├── core/
│   ├── platform_manager.py          # 平台检测
│   ├── windows_terminal_manager.py  # Windows 终端管理
│   ├── tmux_manager.py             # Unix tmux 管理
│   └── scanner.py                  # 扫描器（已修复）
│
├── dashboard/
│   ├── reports.html                # 报告浏览页面
│   ├── index.html                  # 主页面（已美化）
│   ├── REPORTS_README.md          # 报告模块文档
│   └── static/
│       ├── styles.css              # 新样式（已美化）
│       └── styles_old.css          # 旧样式备份
│
├── api/
│   ├── routes_query.py             # 新增报告 API
│   └── app.py                      # 新增 /reports 路由
│
└── docs/
    └── PLATFORM_SUPPORT.md         # 平台支持文档
```

## 🚀 使用指南

### 启动服务器

```bash
python3 -m api.app
```

### 访问页面

- **主 Dashboard**: http://localhost:8700/
- **报告浏览**: http://localhost:8700/reports

### 平台检测

```python
from core.platform_manager import is_windows, is_macos, is_linux

if is_windows():
    print("Running on Windows")
elif is_macos():
    print("Running on macOS")
else:
    print("Running on Linux")
```

### 创建终端会话

```python
from core.windows_terminal_manager import TerminalSession

session = TerminalSession("autotester__test")
result = session.launch(
    script_path=Path("/path/to/script"),
    log_path=Path("/path/to/log"),
    title="Test Execution",
)
```

## 🎨 UI 设计亮点

### 配色系统
```css
--bg: #f4efe4;              /* 暖色背景 */
--accent: #005f4b;          /* 自然绿主色 */
--accent-soft: #d9efe8;     /* 柔和绿 */
--panel: rgba(255, 251, 245, 0.95);  /* 玻璃态面板 */
```

### 字体系统
```css
--font-display: "Space Grotesk";  /* 标题 */
--font-sans: "IBM Plex Sans";     /* 正文 */
--font-mono: "IBM Plex Mono";     /* 代码 */
```

### 阴影系统
```css
--shadow: 0 24px 60px rgba(41, 48, 43, 0.12);      /* 大阴影 */
--shadow-sm: 0 10px 24px rgba(41, 48, 43, 0.08);   /* 小阴影 */
```

## 📊 性能优化

- **CSS**: 使用 CSS 变量实现主题系统
- **动画**: 仅使用 transform 和 opacity（GPU 加速）
- **响应式**: 移动端优化布局
- **缓存**: 扫描结果缓存机制

## 🔧 技术栈

- **后端**: Python 3.10+ / Flask
- **前端**: 原生 HTML/CSS/JavaScript
- **终端**: tmux (Unix) / Windows Terminal (Windows)
- **样式**: CSS Variables + Flexbox/Grid

## 📝 后续计划

- [ ] 添加暗色模式
- [ ] 报告导出功能（PDF/HTML）
- [ ] 实时日志流式传输
- [ ] 多语言支持
- [ ] PWA 支持

## 🙏 致谢

设计参考：
- [Web_dashboard](/Users/wangzixing/Desktop/SkillTest/Web_dashboard) - UI 设计灵感
- [迁移repo](/Users/wangzixing/Desktop/迁移repo/兼容性测试/master/dashboard) - 平台支持逻辑
