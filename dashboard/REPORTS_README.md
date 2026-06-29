# Harn-LLM Tester Report Viewer

## 概述

报告浏览模块提供了一个 Web 界面，用于浏览 Harn-LLM Tester 生成的所有测试报告，包括：
- SpecAgent 生成的评测报告（benchmark_report.md）
- 每个任务的执行总结（task_summary.md）

## 访问方式

启动 Harn-LLM Tester 服务器后，访问：
```
http://localhost:8700/reports
```

或在主 Dashboard 点击右上角的 "📊 Reports" 按钮。

## 功能特性

### 1. Target 卡片列表
- 显示所有 target 的状态和描述
- 支持按名称搜索
- 支持按状态过滤（Completed、Exec Completed、Sample Completed、New）

### 2. 任务预览
- 每个 target 卡片内展示最近 5 个任务的状态
- 显示任务 ID 和执行结果（PASS/FAIL）
- 点击任务可查看详细的 task summary

### 3. 报告查看
- **点击 target 卡片**：打开 SpecAgent 生成的 benchmark_report.md
- **点击具体任务**：打开该任务的 task_summary.md

### 4. Markdown 渲染
- 支持标准 Markdown 语法
- 代码高亮显示
- 表格格式化
- 列表和标题层级展示

## API 端点

### 获取所有 Targets
```
GET /api/targets
```

返回：
```json
{
  "targets": [
    {
      "name": "DemoProject/browser-form-automation",
      "status": "exec_completed",
      "description": "...",
      ...
    }
  ]
}
```

### 获取 Target 的任务列表
```
GET /api/targets/{target_name}/tasks
```

返回：
```json
{
  "success": true,
  "tasks": [
    {
      "task_id": "C_01",
      "success": true
    },
    ...
  ]
}
```

### 获取任务报告
```
GET /api/targets/{target_name}/tasks/{task_id}/report
```

返回：
```json
{
  "success": true,
  "task_id": "C_01",
  "report": "# Task C_01 Summary\n\n..."
}
```

### 获取完整结果数据
```
GET /api/results/{target_name}
```

返回：
```json
{
  "target_name": "...",
  "task_summaries": [
    {
      "task_id": "C_01",
      "track": "with_target",
      "content": "..."
    }
  ],
  "spec_report": "...",
  "scores": {...}
}
```

## 目录结构

报告文件存储位置：
```
database/
├── exec/{source}/{target}/{task_design_model}/{executor_model}/
│   └── with_target/tasks/{task_id}/
│       └── task_summary.md          # 任务执行总结
└── specs/{source}/{target}/{task_design_model}/{executor_model}/{evaluator_model}/
    └── benchmark_report.md           # 评测报告
```

## 使用示例

1. **查看 Target 整体报告**：
   - 在 reports 页面找到目标 target
   - 点击 target 卡片
   - 弹出窗口显示 benchmark_report.md

2. **查看单个任务详情**：
   - 在 target 卡片内的任务列表中
   - 点击具体的任务（如 C_01）
   - 弹出窗口显示该任务的 task_summary.md

## 注意事项

1. **报告生成时机**：
   - `task_summary.md` 由 ExecAgent 在任务执行完成后生成
   - `benchmark_report.md` 由 SpecAgent 在评测完成后生成

2. **Fallback 机制**：
   - 如果 SpecAgent 还未运行（没有 benchmark_report.md），系统会显示已有的 task summaries
   - 如果完全没有报告，会显示提示信息

3. **性能优化**：
   - 任务列表默认只显示前 5 个
   - 完整列表可在点击 target 后查看

## 未来扩展

- [ ] 支持报告导出（PDF、HTML）
- [ ] 报告对比功能（不同 harness/model 的结果对比）
- [ ] 历史报告版本浏览
- [ ] 报告搜索功能
