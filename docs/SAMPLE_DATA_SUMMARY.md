# 示例数据创建总结

## ✅ 已完成

### 1. 清理旧数据
- ✅ 清空 `TargetsRepo/DemoProject/*`
- ✅ 清空 `database/*`

### 2. 创建示例数据

#### 已完成示例（2个）
包含完整的 TargetsRepo 和 database 数据：

1. **OpenSource/api-tester**
   - 状态: `completed` (全部完成)
   - 分数: 总分 85.5
   - 功能: API 测试工具
   - 数据包含:
     - ✅ TargetsRepo/requirement.md
     - ✅ database/samples/ (任务包)
     - ✅ database/exec/ (执行结果)
     - ✅ database/specs/ (评测报告)

2. **OpenSource/document-summarizer**
   - 状态: `completed` (全部完成)
   - 分数: 总分 85.5
   - 功能: 文档摘要生成器
   - 数据包含:
     - ✅ TargetsRepo/requirement.md
     - ✅ database/samples/ (任务包)
     - ✅ database/exec/ (执行结果)
     - ✅ database/specs/ (评测报告)

#### 待测示例（3个）
只包含 TargetsRepo 数据：

3. **DemoProject/code-refactor-tool**
   - 状态: `new` (未开始)
   - 功能: 代码重构助手
   - 数据包含:
     - ✅ TargetsRepo/requirement.md
     - ❌ 无 database 数据

4. **DemoProject/data-visualizer**
   - 状态: `new` (未开始)
   - 功能: 数据可视化工具
   - 数据包含:
     - ✅ TargetsRepo/requirement.md
     - ❌ 无 database 数据

5. **Enterprise/test-generator**
   - 状态: `new` (未开始)
   - 功能: 测试用例生成器
   - 数据包含:
     - ✅ TargetsRepo/requirement.md
     - ❌ 无 database 数据

## 📊 统计信息

```
Total Targets:     5
Completed:         2 (40%)
Exec Completed:    0 (0%)
Sample Completed:  0 (0%)
New:               3 (60%)
```

## 📁 目录结构

### TargetsRepo
```
TargetsRepo/
├── DemoProject/
│   ├── code-refactor-tool/
│   │   └── requirement.md
│   └── data-visualizer/
│   │       └── requirement.md
├── Enterprise/
│   └── test-generator/
│       └── requirement.md
└── OpenSource/
    ├── api-tester/
    │   └── requirement.md
    └── document-summarizer/
        └── requirement.md
```

### Database
```
database/
├── samples/
│   └── OpenSource/
│       ├── api-tester/
│       │   └── K2.6-code-preview/
│       │       ├── benchmark_manifest.json
│       │       └── samples_description.md
│       └── document-summarizer/
│           └── K2.6-code-preview/
│               ├── benchmark_manifest.json
│               └── samples_description.md
├── exec/
│   └── OpenSource/
│       ├── api-tester/
│       │   └── K2.6-code-preview/
│       │       └── deepseek-v4-pro/
│       │           └── with_target/
│       │               ├── metrics.json
│       │               ├── stage_start_timestamp.json
│       │               └── tasks/
│       │                   ├── C_01/
│       │                   │   ├── task_metrics.json
│       │                   │   ├── start_timestamp.json
│       │                   │   ├── end_timestamp.json
│       │                   │   ├── task_summary.md
│       │                   │   └── results/
│       │                   └── C_02/
│       │                       ├── (同 C_01)
│       └── document-summarizer/
│           └── (同 api-tester)
└── specs/
    └── OpenSource/
        ├── api-tester/
        │   └── K2.6-code-preview/
        │       └── deepseek-v4-pro/
        │           └── deepseek-v4-pro/
        │               ├── Template.json
        │               ├── Template.csv
        │               └── benchmark_report.md
        └── document-summarizer/
            └── (同 api-tester)
```

## 🎯 用途说明

### 已完成示例
用于演示和测试：
- ✅ Dashboard 显示完成状态
- ✅ 报告浏览功能（查看 benchmark_report.md）
- ✅ 任务详情查看（查看 task_summary.md）
- ✅ 评分展示（Template.json 分数）
- ✅ 结果对比（baseline vs with_target）

### 待测示例
用于测试流程：
- ✅ 新 target 识别
- ✅ Sample 阶段触发
- ✅ Exec 阶段执行
- ✅ Spec 阶段评测
- ✅ 状态流转演示

## 🔧 创建脚本

脚本位置: `/software/create_sample_data.py`

可以随时重新运行：
```bash
python3 create_sample_data.py
```

会清理并重新创建所有示例数据。

## ✨ 特性

1. **真实的目录结构**: 符合 AutoTester 的证据协议
2. **完整的数据文件**: 包含所有必需的 JSON 和 Markdown 文件
3. **合理的分数**: 模拟真实的测试结果（85.5分）
4. **中文描述**: 符合报告规范要求
5. **多来源分类**: OpenSource、DemoProject、Enterprise 三个来源

所有示例数据已创建完成，可以用于演示和测试！🎉