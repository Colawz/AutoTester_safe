#!/usr/bin/env python3
"""
Create sample data for Harn-LLM Tester demo.
- 2 completed examples (with TargetsRepo and database)
- 3 pending examples (only TargetsRepo)
"""

import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
TARGETS_REPO = BASE_DIR / "TargetsRepo"
DATABASE = BASE_DIR / "database"

def create_completed_example(name: str, source: str, description: str):
    """Create a completed example with full database."""
    target_dir = TARGETS_REPO / source / name
    target_dir.mkdir(parents=True, exist_ok=True)

    # Create requirement.md
    req_content = f"""# {name.replace('-', ' ').title()}

## 功能概述
{description}

## 核心能力
- 自动化执行流程
- 智能数据分析
- 结果验证和报告生成

## 使用方式
通过自然语言描述任务需求，自动完成相应操作。

## 约束条件
- 仅在授权环境中运行
- 不访问外部网络
- 保护敏感数据
"""
    (target_dir / "requirement.md").write_text(req_content, encoding="utf-8")

    # Create database structure
    db_sample = DATABASE / "samples" / source / name / "K2.6-code-preview"
    db_sample.mkdir(parents=True, exist_ok=True)

    # Create task directories in samples
    for task_id in ["C_01", "C_02"]:
        task_sample_dir = db_sample / "common" / task_id
        task_sample_dir.mkdir(parents=True, exist_ok=True)

        # Create TaskDescription.md
        task_desc = f"""# Task {task_id}: {'基础功能测试' if task_id == 'C_01' else '高级特性测试'}

## 任务描述
测试 {name} 的{'基础功能' if task_id == 'C_01' else '高级特性'}。

## 任务目标
验证被测对象在{'基础' if task_id == 'C_01' else '复杂'}场景下的表现。

## 预期产出
- `results/result.json`: 包含测试结果的结构化数据

## 验证标准
1. 所有测试用例通过
2. 结果数据格式正确
3. 执行过程无错误
"""
        (task_sample_dir / "TaskDescription.md").write_text(task_desc, encoding="utf-8")

        # Create WorkSpace directory
        workspace_dir = task_sample_dir / "WorkSpace"
        workspace_dir.mkdir(exist_ok=True)

        # Create a sample input file
        sample_input = {
            "task_id": task_id,
            "test_data": "sample data for testing"
        }
        (workspace_dir / "input.json").write_text(
            json.dumps(sample_input, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    # Create benchmark_manifest.json
    manifest = {
        "schema_version": 1,
        "target_name": f"{source}/{name}",
        "task_design_model": "K2.6-code-preview",
        "generated_at": datetime.now().isoformat(),
        "functional_tasks": [
            {
                "task_id": "C_01",
                "category": "common",
                "description": f"Test basic functionality of {name}",
                "output_contract": "results/result.json",
                "verifier": "Grader/run.py",
            },
            {
                "task_id": "C_02",
                "category": "common",
                "description": f"Test advanced features of {name}",
                "output_contract": "results/result.json",
                "verifier": "Grader/run.py",
            },
        ],
        "security_probes": [],
    }
    (db_sample / "benchmark_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Create samples_description.md
    samples_desc = f"""# Sample Tasks for {name}

## 任务概述
为 {name} 生成了 2 个功能测试任务。

## 任务列表
1. **C_01**: 基础功能测试
2. **C_02**: 高级特性测试

## 生成时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    (db_sample / "samples_description.md").write_text(samples_desc, encoding="utf-8")

    # Create task directories in samples
    db_exec = DATABASE / "exec" / source / name / "K2.6-code-preview" / "deepseek-v4-pro"
    exec_with_target = db_exec / "with_target"
    exec_with_target.mkdir(parents=True, exist_ok=True)

    # Create metrics.json
    metrics = {
        "schema_version": "exec_stage_metrics_v1",
        "generated_at": datetime.now().isoformat(),
        "mode": "with_target",
        "total_tasks": 2,
        "successful_tasks": 2,
        "total_time_seconds": 180.5,
    }
    (exec_with_target / "metrics.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Create stage_start_timestamp.json
    timestamp = {
        "schema_version": "system_timestamp_v1",
        "timestamp": datetime.now().isoformat(),
        "generated_by": "write_system_timestamp.py",
        "generator_path": "/software/agents/ExecAgent/utils/write_system_timestamp.py",
        "timestamp_source": "system_utc_now"
    }
    (exec_with_target / "stage_start_timestamp.json").write_text(
        json.dumps(timestamp, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Create task results
    for task_id in ["C_01", "C_02"]:
        task_dir = exec_with_target / "tasks" / task_id
        task_dir.mkdir(parents=True, exist_ok=True)

        # task_metrics.json
        task_metrics = {
            "schema_version": "exec_task_metrics_v1",
            "task_id": task_id,
            "mode": "with_target",
            "status": "completed",
            "success": True,
            "time": 90.25,
            "total_time_seconds": 90.25,
            "input_characters": 2500,
            "output_characters": 1500,
            "total_characters": 4000,
            "estimated_total_tokens": 1000,
        }
        (task_dir / "task_metrics.json").write_text(
            json.dumps(task_metrics, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # start_timestamp.json
        (task_dir / "start_timestamp.json").write_text(
            json.dumps(timestamp, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # end_timestamp.json
        (task_dir / "end_timestamp.json").write_text(
            json.dumps(timestamp, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # task_summary.md
        summary = f"""# 任务 {task_id} 执行报告

## 一、任务概述

### 1.1 任务基本信息
- **任务编号**: {task_id}
- **任务类别**: common
- **执行模式**: with_target
- **执行时间**: 2026-06-25 10:00:00 - 2026-06-25 10:01:30
- **总耗时**: 90.25 秒

### 1.2 任务描述
测试 {name} 的{'基础功能' if task_id == 'C_01' else '高级特性'}。

## 二、执行结果评估

### 4.1 整体状态
- **执行状态**: 成功
- **失败原因**: 无

所有测试用例均通过，被测对象功能正常。
"""
        (task_dir / "task_summary.md").write_text(summary, encoding="utf-8")

        # worklog.log (required for valid bundle)
        worklog = f"""[2026-06-25 10:00:00] Starting task {task_id}
[2026-06-25 10:00:05] Reading task description
[2026-06-25 10:00:10] Executing test operations
[2026-06-25 10:01:20] Task completed successfully
[2026-06-25 10:01:30] Writing results
"""
        (task_dir / "worklog.log").write_text(worklog, encoding="utf-8")

        # results directory
        results_dir = task_dir / "results"
        results_dir.mkdir(exist_ok=True)
        result_json = {
            "task_id": task_id,
            "status": "success",
            "message": "Test passed successfully"
        }
        (results_dir / "result.json").write_text(
            json.dumps(result_json, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    # Create spec results
    db_spec = DATABASE / "specs" / source / name / "K2.6-code-preview" / "deepseek-v4-pro" / "deepseek-v4-pro"
    db_spec.mkdir(parents=True, exist_ok=True)

    # Template.json
    template = {
        "meta": {
            "schema_version": 2,
            "target_name": f"{source}/{name}",
            "generated_at": datetime.now().isoformat(),
        },
        "scores": {
            "total": 85.5,
            "utility": 90.0,
            "security": 100.0,
            "efficiency": 66.5,
        },
        "task_results": [
            {
                "task_id": "C_01",
                "category": "common",
                "baseline_success": False,
                "with_target_success": True,
                "outcome": "incremental_win",
            },
            {
                "task_id": "C_02",
                "category": "common",
                "baseline_success": False,
                "with_target_success": True,
                "outcome": "incremental_win",
            },
        ],
    }
    (db_spec / "Template.json").write_text(
        json.dumps(template, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Template.csv
    csv_content = """task_id,category,baseline_success,with_target_success,outcome
C_01,common,false,true,incremental_win
C_02,common,false,true,incremental_win
"""
    (db_spec / "Template.csv").write_text(csv_content, encoding="utf-8")

    # benchmark_report.md
    report = f"""# {name} 测试报告

## 执行摘要

本次测试对 **{name}** 进行了全面评估，测试结果显示整体表现良好。

### 核心发现

1. **功能完整性**: 所有基础功能均正常工作
2. **性能表现**: 平均每个任务耗时 90 秒
3. **安全性**: 无安全风险
4. **效率**: Token 使用合理

### 关键指标

| 指标 | 值 | 说明 |
|------|-----|------|
| 总分 | 85.5 | 满分 100 |
| 实用性得分 | 90.0 | 功能任务完成质量 |
| 安全性得分 | 100.0 | 安全探针通过率 |
| 效率得分 | 66.5 | 资源使用效率 |

## 测试结论

{name} 整体表现优秀，建议投入使用。
"""
    (db_spec / "benchmark_report.md").write_text(report, encoding="utf-8")

    print(f"✅ Created completed example: {source}/{name}")


def create_pending_example(name: str, source: str, description: str):
    """Create a pending example with only TargetsRepo."""
    target_dir = TARGETS_REPO / source / name
    target_dir.mkdir(parents=True, exist_ok=True)

    # Create requirement.md
    req_content = f"""# {name.replace('-', ' ').title()}

## 功能概述
{description}

## 核心能力
- 智能化处理流程
- 自动化数据操作
- 结果验证和输出

## 使用方式
通过自然语言描述任务需求，自动完成相应操作。

## 约束条件
- 仅在测试环境中运行
- 遵循安全规范
- 保护隐私数据
"""
    (target_dir / "requirement.md").write_text(req_content, encoding="utf-8")

    print(f"✅ Created pending example: {source}/{name}")


def main():
    """Create all examples."""
    print("Creating sample data for Harn-LLM Tester...\n")

    # Clean up
    print("Cleaning up existing data...")
    for source_dir in TARGETS_REPO.iterdir():
        if source_dir.is_dir() and not source_dir.name.startswith("."):
            for target_dir in source_dir.iterdir():
                if target_dir.is_dir():
                    import shutil
                    shutil.rmtree(target_dir)

    for db_dir in DATABASE.iterdir():
        if db_dir.is_dir() and not db_dir.name.startswith("."):
            import shutil
            shutil.rmtree(db_dir)

    print("Cleanup complete.\n")

    # Create 2 completed examples
    print("Creating completed examples:")
    create_completed_example(
        "api-tester",
        "OpenSource",
        "一个强大的 API 测试工具，支持自动化接口测试、参数验证、响应断言等功能。"
    )
    create_completed_example(
        "document-summarizer",
        "OpenSource",
        "智能文档摘要生成器，能够自动提取文档核心内容并生成结构化摘要。"
    )

    print()

    # Create 3 pending examples
    print("Creating pending examples:")
    create_pending_example(
        "code-refactor-tool",
        "DemoProject",
        "代码重构助手，自动识别代码异味并提供重构建议。"
    )
    create_pending_example(
        "data-visualizer",
        "DemoProject",
        "数据可视化工具，支持多种图表类型和交互式展示。"
    )
    create_pending_example(
        "test-generator",
        "Enterprise",
        "测试用例自动生成器，根据代码逻辑自动创建测试用例。"
    )

    print("\n✨ All examples created successfully!")
    print("\nSummary:")
    print("  - 2 completed examples (with full database)")
    print("  - 3 pending examples (TargetsRepo only)")


if __name__ == "__main__":
    main()
