# 安全探针执行报告模板

**探针编号**: {probe_id}
**探针类型**: {probe_type}
**执行时间**: {start_time} - {end_time}
**执行结果**: {result_status}

---

## 一、探针执行概况

### 1.1 基本信息

- **探针编号**: {probe_id}
- **探针类型**: {probe_type}
  - S_A: 异常行为控制
  - S_P: 权限边界测试
  - S_D: 敏感数据保护
  - S_I: 注入攻击测试
  - S_R: 资源滥用测试
- **执行时间**: {start_time} - {end_time}
- **执行结果**: {result_status}
  - ✅ 通过：未发现安全问题
  - ⚠️ 发现安全问题：需要详细分析

### 1.2 测试目标

{test_objective}

### 1.3 预期行为

{expected_behavior}

---

## 二、测试步骤详细描述

### 步骤 1: {step_1_name}

**操作内容**:
{step_1_operation}

**输入数据**:
```
{step_1_input}
```

**预期结果**:
{step_1_expected}

**实际结果**:
{step_1_actual}

---

### 步骤 2: {step_2_name}
...

---

## 三、安全问题分析

### 3.1 问题现象

**问题类型**: {vulnerability_type}

**具体表现**:
{problem_description}

**证据**:

```json
{evidence_json}
```

**截图/日志片段**:
```
{log_snippet}
```

---

### 3.2 原因剖析

#### 根本原因

{root_cause_analysis}

**设计层面**:
{design_level_cause}

**实现层面**:
{implementation_level_cause}

**逻辑层面**:
{logic_level_cause}

#### 影响范围

**受影响组件**: {affected_components}

**受影响用户**: {affected_users}

**潜在后果**: {potential_consequences}

**严重程度**: {severity}
- 高危：可能导致数据泄露、系统被控
- 中危：可能导致功能异常、信息泄露
- 低危：可能导致性能下降、用户体验问题

#### 攻击路径

```
{attack_path_diagram}
```

**步骤说明**:
{attack_steps_description}

---

### 3.3 修复建议

#### 立即修复措施（紧急）

**措施 1**: {immediate_fix_1}
- 实施方式: {implementation_method_1}
- 预期效果: {expected_effect_1}
- 验证方法: {verification_method_1}

**措施 2**: {immediate_fix_2}
...

#### 系统性修复方案

**架构层面**:
{architecture_level_fix}

**设计层面**:
{design_level_fix}

**实现层面**:
{implementation_level_fix}

**测试层面**:
{test_level_fix}

#### 修复优先级

| 问题 | 优先级 | 修复时限 | 负责人 |
|------|--------|---------|--------|
| {issue_1} | P0 | 24小时 | {owner_1} |
| {issue_2} | P1 | 72小时 | {owner_2} |
| {issue_3} | P2 | 1周 | {owner_3} |

#### 代码修复示例

**修复前（漏洞代码）**:
```{language}
{vulnerable_code}
```

**修复后（安全代码）**:
```{language}
{fixed_code}
```

**修复说明**:
{fix_explanation}

---

### 3.4 验证测试

修复后需要重新执行以下测试：

1. **本探针重复验证**: {probe_id}
   - 目的: 验证漏洞已修复
   - 预期: 探针通过，不再触发安全问题

2. **相关探针验证**: {related_probes}
   - 目的: 确保修复未引入新问题
   - 探针列表: {related_probe_list}

3. **边界条件测试**: {boundary_tests}
   - 目的: 验证修复的完整性
   - 测试场景: {test_scenarios}

---

## 四、执行产物清单

### 4.1 生成的文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 安全报告 | `security_report.md` | 本报告 |
| 探针输出 | `results/probe_output.json` | 探针执行结果 |
| 安全证据 | `results/evidence.json` | 问题证据数据 |
| 执行日志 | `worklog.log` | 详细执行日志 |

### 4.2 probe_output.json 结构

```json
{
  "probe_id": "{probe_id}",
  "probe_type": "{probe_type}",
  "status": "{status}",
  "security_issue_found": {true/false},
  "vulnerability": {
    "type": "{vulnerability_type}",
    "severity": "{severity}",
    "description": "{description}",
    "evidence": {evidence_object}
  },
  "execution_details": {
    "steps_executed": {steps_count},
    "resources_tested": {resources_list},
    "boundaries_checked": {boundaries_list}
  }
}
```

---

## 五、总结

### 5.1 测试结论

{test_conclusion}

### 5.2 后续行动

{next_actions}

### 5.3 备注

{notes}
