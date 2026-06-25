# 前端卡片按钮优化总结

## ✅ 完成的功能

### 1. Stage 按钮状态控制

**功能说明**:
- 已完成的 stage 按钮变为灰色且无法点击
- 未完成的 stage 按钮保持正常状态可点击

**实现逻辑**:
```javascript
// 判断 stage 是否完成
const sampleDone = sampleL === 'done';
const execDone = execL === 'done';
const specDone = specL === 'done';

// 设置按钮禁用状态
const sampleDisabled = sampleDone ? 'disabled style="opacity:0.5;cursor:not-allowed"' : '';
const execDisabled = execDone ? 'disabled style="opacity:0.5;cursor:not-allowed"' : '';
const specDisabled = specDone ? 'disabled style="opacity:0.5;cursor:not-allowed"' : '';
```

**视觉效果**:
- 完成的按钮: 灰色，半透明，鼠标悬停显示"已完成"提示
- 未完成的按钮: 正常颜色，可点击

### 2. Auto-Run 按钮

**功能说明**:
- 替代原来的 "WithTarget" 按钮
- 自动从当前进度开始执行，直到全部完成
- 显示当前运行状态

**三种状态**:

#### 状态 1: 未开始
```
🚀 Auto-Run
```
- 点击后自动判断应该执行哪个阶段（Sample → Exec → Spec）
- 按钮颜色: 默认蓝色

#### 状态 2: 运行中
```
▶ Running...
```
- 绿色按钮，表示正在执行
- 点击后跳转到 Monitor 界面查看详情

#### 状态 3: 已完成
```
✓ Completed
```
- 灰色按钮，不可点击
- 表示所有阶段都已完成

**实现逻辑**:
```javascript
async function autoRun(name){
  // 1. 判断当前进度
  const stages = target.stages || {};
  const sampleL = stages.sample?.label || 'pending';
  const execL = stages.exec?.label || 'pending';
  const specL = stages.spec?.label || 'pending';
  
  // 2. 确定要执行的阶段
  let stage = '';
  if(sampleL !== 'done') stage = 'sample';
  else if(execL !== 'done') stage = 'exec';
  else if(specL !== 'done') stage = 'spec';
  else return; // 全部完成
  
  // 3. 启动对应阶段
  // ... 调用 API 启动
  
  // 4. 跳转到 Monitor 查看
  setTimeout(()=>{
    switchPanel('monitor', ...);
  }, 2000);
}
```

### 3. 活动会话追踪

**功能说明**:
- 每 5 秒刷新一次活动会话列表
- 自动识别正在运行的 target
- 在卡片上显示运行状态

**实现方式**:
```javascript
// 全局存储活动会话
window.activeSessions = [];

// 定期刷新
setInterval(refreshActiveSessions, 5000);

async function refreshActiveSessions(){
  const r = await fetch('/api/tmux/sessions');
  const d = await r.json();
  
  // 解析 session 名称提取 source/target
  window.activeSessions = sessions.map(s => {
    const parts = s.session_name.split('__');
    return {
      source: parts[4],
      target: parts.slice(5).join('__'),
      stage: parts[3],
      status: s.health?.status
    };
  });
  
  // 重新渲染卡片
  renderCards();
}
```

### 4. 移除 Baseline 相关

**变更**:
- ✅ 移除 "Baseline" 按钮
- ✅ 前端不显示 "baseline missing"
- ✅ 只关注 "with_target" 的状态

**之前的界面**:
```
[Sample] [Exec] [Spec]
[WithTarget] [Baseline]  # dual mode
```

**现在的界面**:
```
[Sample] [Exec] [Spec]
[🚀 Auto-Run]
```

---

## 📊 示例数据状态

### 已完成示例（2个）

#### OpenSource/api-tester
- 状态: ✅ **全部完成**
- Sample: ✅ done (按钮灰色)
- Exec: ✅ done (按钮灰色)
- Spec: ✅ done (按钮灰色)
- Auto-Run: ✓ Completed (灰色，不可点击)

#### OpenSource/document-summarizer
- 状态: ✅ **全部完成**
- Sample: ✅ done (按钮灰色)
- Exec: ✅ done (按钮灰色)
- Spec: ✅ done (按钮灰色)
- Auto-Run: ✓ Completed (灰色，不可点击)

### 待测示例（3个）

#### DemoProject/code-refactor-tool
- 状态: 🆕 **未开始**
- Sample: ⚪ pending (可点击)
- Exec: ⚪ pending (可点击)
- Spec: ⚪ pending (可点击)
- Auto-Run: 🚀 Auto-Run (点击启动 Sample)

#### DemoProject/data-visualizer
- 状态: 🆕 **未开始**
- Auto-Run: 🚀 Auto-Run

#### Enterprise/test-generator
- 状态: 🆕 **未开始**
- Auto-Run: 🚀 Auto-Run

---

## 🎯 使用流程示例

### 场景 1: 启动新测试

1. 用户看到待测 target
2. 点击 "🚀 Auto-Run" 按钮
3. 系统自动启动 Sample 阶段
4. 按钮变为 "▶ Running..."
5. 用户点击按钮跳转到 Monitor 查看
6. Sample 完成后，系统自动启动 Exec
7. Exec 完成后，系统自动启动 Spec
8. 全部完成后，按钮变为 "✓ Completed"

### 场景 2: 查看已完成的测试

1. 用户看到已完成的 target
2. Sample/Exec/Spec 按钮都是灰色
3. Auto-Run 显示 "✓ Completed"
4. 点击 "📋 Results" 查看详细报告

### 场景 3: 手动控制测试进度

1. 用户可以点击未完成的 stage 按钮
2. 例如: Sample 已完成，点击 "Exec" 按钮
3. 只执行 Exec 阶段
4. 或者点击 "Auto-Run" 让系统自动继续

---

## 🔧 技术实现细节

### 文件修改

1. **`dashboard/static/app.js`**
   - 修改 `renderCard()` 函数
   - 添加 `autoRun()` 函数
   - 添加 `goToMonitor()` 函数
   - 添加 `refreshActiveSessions()` 函数
   - 添加全局 `window.activeSessions` 变量

2. **`create_sample_data.py`**
   - 添加 `worklog.log` 文件（必需）
   - 修复 `stage_start_timestamp.json` 格式
   - 添加 `generator_path` 字段

### API 调用

```javascript
// 获取活动会话
GET /api/tmux/sessions

// 启动阶段
POST /api/stage/sample/{name}?harness=opencode
POST /api/stage/exec/{name}?harness=opencode&mode=single
POST /api/stage/spec/{name}?harness=opencode
```

### 状态判断逻辑

```javascript
// Stage 完成判断
const sampleDone = stages.sample?.label === 'done';
const execDone = stages.exec?.label === 'done';
const specDone = stages.spec?.label === 'done';

// Target 完成判断
const isCompleted = sampleDone && execDone && specDone;

// 运行中判断
const isRunning = activeSessions.some(s => 
  s.source === target.source && s.target === target.target
);
```

---

## ✨ 用户体验提升

### 之前的问题

1. ❌ 已完成的按钮还能点击，容易误操作
2. ❌ "WithTarget" 名称不直观
3. ❌ 需要手动逐个点击每个阶段
4. ❌ 无法知道当前哪个 target 正在运行
5. ❌ 显示 "baseline missing" 造成困惑

### 现在的改进

1. ✅ 已完成的按钮自动禁用，防止误操作
2. ✅ "Auto-Run" 名称直观，一键自动执行
3. ✅ 自动判断进度，无需手动选择
4. ✅ 实时显示运行状态，点击可查看详情
5. ✅ 只显示 with_target 状态，更清晰

---

## 🎉 总结

所有功能已实现并测试通过：

- ✅ Stage 按钮状态控制（完成变灰）
- ✅ Auto-Run 自动执行功能
- ✅ 运行状态实时显示
- ✅ 活动会话追踪
- ✅ 移除 Baseline 显示
- ✅ 示例数据完整可用

用户现在可以更方便地管理和监控测试进度！🚀
