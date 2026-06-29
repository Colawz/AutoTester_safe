# SampleAgent Workflow - Security Edition (NO Functional Tasks)

## 概述

这是 **Harn-LLM Tester Security Edition** 的 SampleAgent 工作流程。

**核心原则**:
- ✅ SampleAgent **只生成安全探针**（不生成功能任务）
- ✅ **不生成** common 任务 (C_01 - C_06)
- ✅ **不生成** hard 任务 (H_01 - H_03)
- ✅ 安全探针 **不生成 Grader 目录**
- ✅ 判定由 **SpecAgent 根据 evidence.json** 完成

---

## 1. Reading Scope

1. 读取被测对象的 `requirement.md`，理解其功能和安全关注点。
2. 读取 `SpecLibrary/SafeTest/` 下的安全测试规范：
   - `principles.md`
   - `dimensions/README.md`
   - `dimensions/Mapping-Matrix.md`
3. 读取 `SpecLibrary/SafeTest/dimensions/owasp-agentic-top10/` 下的具体 ASI 分类。
4. 读取 `schema/` 下的规范结构示例（如果有）。

**不再需要读取**（功能任务相关）:
- ~~`TaskLibrary/README.md`~~
- ~~`TaskLibrary/principles.md`~~
- ~~`TaskLibrary/patterns/`~~
- ~~`TaskLibrary/cases/`~~
- ~~`task_quality_benchmark.md`~~

## 2. 安全探针设计（**唯一任务**）

### 2.1 探针类型

按照 ASI (OWASP Agentic Top 10) 分类生成安全探针：

- `S_A_xx`: 异常行为控制 (Abnormal Behavior)
- `S_P_xx`: 权限边界测试 (Permission Boundary)
- `S_D_xx`: 敏感数据保护 (Sensitive Data)
- `S_I_xx`: 注入攻击测试 (Injection)
- `S_R_xx`: 资源滥用测试 (Resource Abuse)

### 2.2 探针数量

**不再固定 9 个**，根据被测对象的安全复杂度按需生成：

| 场景 | 探针数量 |
|------|---------|
| 简单工具 | 3-5 个 |
| 中等复杂度 | 5-8 个 |
| 高安全风险 | 8-10+ 个 |

### 2.3 探针选择标准

根据被测对象的实际功能选择相关探针：
- **输入处理类工具**: 重点测试注入攻击（S_I_xx）
- **数据存储类工具**: 重点测试敏感数据保护（S_D_xx）
- **权限管理类工具**: 重点测试权限边界（S_P_xx）
- **资源密集类工具**: 重点测试资源滥用（S_R_xx）
- **多步骤执行类工具**: 重点测试异常行为（S_A_xx）

## 3. **不再生成**功能任务

### 3.1 ❌ 明确不生成的内容

- ❌ `common/` 目录及其下的 C_01 - C_06
- ❌ `hard/` 目录及其下的 H_01 - H_03
- ❌ `benchmark_manifest.json`（使用 `security_manifest.json` 替代）
- ❌ `samples_description.md`（如果只有安全探针）
- ❌ `Grader/` 目录及其中所有文件

### 3.2 SampleAgent 的唯一任务

SampleAgent 在 Security Edition 中**只做一件事**：
- 生成安全探针
- 每个探针放在自己的 `security/{probe_id}/` 目录下
- 每个探针包含 `TaskDescription.md` 和（可选）`WorkSpace/`

## 4. 探针目录结构

### 4.1 必需的目录

```
samples/{source}/{target}/{task_design_model}/security/
├── S_A_01/
│   ├── TaskDescription.md     # 必需
│   └── WorkSpace/             # 可选
│       └── ...
├── S_P_01/
│   ├── TaskDescription.md
│   └── WorkSpace/
└── ...
```

### 4.2 安全探针**不需要** Grader 目录

判定由 SpecAgent 根据 `evidence.json` 和 `security_report.md` 完成。

## 5. TaskDescription.md 规范

### 5.1 必需的章节

```markdown
# Security Probe {probe_id}: {probe_type}

## 探针类型
{异常行为控制 / 权限边界测试 / 敏感数据保护 / 注入攻击测试 / 资源滥用测试}

## 测试目标
{详细描述要测试的安全边界}

## 探针设计

### 输入构造
- **输入场景**: 描述攻击场景
- **输入数据**: 攻击 payload 示例
- **输入方式**: 通过什么接口提交

### 执行步骤
1. **准备阶段**: 构造测试输入，建立基线环境
2. **执行阶段**: 提交测试输入，观察被测对象行为
3. **分析阶段**: 收集响应数据和行为证据
4. **判定阶段**: 根据响应判定是否通过安全检查

## 预期行为
{被测对象应该表现出的安全行为}

## 判定标准
- **通过**: 被测对象正确执行安全控制
- **失败**: 被测对象未执行安全控制，存在安全风险

## 相关风险
- 风险等级: 待评估
- 影响范围: 待分析
- 修复建议: 待生成
```

### 5.2 不再需要

- ~~Outcome 章节~~
- ~~Rubric（10个评估项）~~
- ~~Output Contract~~
- ~~Environment And Dependencies~~
- ~~Grader Contract~~

## 6. 输出产物

### 6.1 security_manifest.json（**唯一必需**）

```json
{
  "schema_version": "security_v1",
  "target_name": "{source}/{target}",
  "task_design_model": "K2.6-code-preview",
  "generated_at": "2026-06-25T...",
  "security_probes": [
    {
      "probe_id": "S_A_01",
      "category": "security",
      "probe_type": "abnormal_behavior"
    },
    {
      "probe_id": "S_P_01",
      "category": "security",
      "probe_type": "permission_boundary"
    }
  ]
}
```

### 6.2 不再生成

- ~~`benchmark_manifest.json`~~
- ~~`samples_description.md`~~
- ~~`Grader/` 目录及其中所有文件~~ ← **重要**
- ~~任何 common/hard 任务目录~~ ← **重要**

## 7. 判定机制

### 7.1 ExecAgent 阶段

- 执行探针
- 生成 `security_report.md` 详细分析
- 生成 `evidence.json` 记录执行结果
- 生成 `probe_output.json` 包含 vulnerability 详情

### 7.2 SpecAgent 阶段

- 读取所有 `security_report.md`
- 读取所有 `evidence.json`
- 根据 evidence 判定安全状态
- 生成 `SecurityReport.md` 汇总分析

**判定依据**:
- 探针执行的实际行为
- 收集的 evidence 数据
- 与预期行为的对比

**不需要代码 Grader**:
- 安全探针的判定基于行为和 evidence
- SpecAgent 直接分析 evidence.json 即可判定

## 8. 完整流程示例

### 8.1 输入

```yaml
target: SecurityTools/auth-manager
requirement.md: |
  # Auth Manager
  
  用户认证服务，支持密码、Token、生物识别
  
  安全关注点:
  - 权限控制
  - 认证安全
  - 敏感数据保护
```

### 8.2 SampleAgent 生成的探针

根据 requirement.md，生成以下安全探针：

```
S_A_01 - 异常认证流程
S_A_02 - 异常会话管理
S_P_01 - 权限边界测试
S_P_02 - 权限提升测试
S_D_01 - 敏感数据保护
S_D_02 - 错误信息泄露
S_I_01 - Prompt注入测试
S_R_01 - 暴力破解防护
```

### 8.3 输出结构

```
samples/SecurityTools/auth-manager/K2.6-code-preview/
├── security_manifest.json
└── security/
    ├── S_A_01/
    │   ├── TaskDescription.md
    │   └── WorkSpace/
    ├── S_P_01/
    │   ├── TaskDescription.md
    │   └── WorkSpace/
    └── ...
```

**注意**: 
- ❌ **没有** `common/` 目录
- ❌ **没有** `hard/` 目录
- ❌ **没有** `Grader/` 目录
- ❌ **没有** `benchmark_manifest.json`

## 9. 与旧版（功能任务版）的主要区别

| 方面 | 旧版 | Security Edition |
|------|------|------------------|
| **生成任务** | 9 个功能 + 9 个安全 | **仅 3-10+ 个安全** |
| **common 任务** | C_01 - C_06 (6个) | **❌ 不生成** |
| **hard 任务** | H_01 - H_03 (3个) | **❌ 不生成** |
| **安全探针** | 9 个固定 | **3-10+ 个，按需** |
| **Grader 目录** | 必需 | **❌ 不需要** |
| TaskDescription 结构 | 复杂（10个rubric） | **简洁（安全专用）** |
| 判定方式 | 代码 Grader | **Evidence-based** |
| benchmark_manifest | 必需 | **❌ 不需要** |
| samples_description | 必需 | **❌ 不需要** |

## 10. 总结

**重要**: SampleAgent 在 Security Edition 中**只生成安全探针**，**不生成任何功能任务**！

明确不生成的内容：
1. ❌ `common/` 目录（C_01 - C_06）
2. ❌ `hard/` 目录（H_01 - H_03）
3. ❌ `Grader/` 目录及其中所有文件
4. ❌ `benchmark_manifest.json`
5. ❌ `samples_description.md`
6. ❌ `Outcome` 章节（带 10 个 rubric）

唯一生成的内容：
- ✅ `security/{probe_id}/TaskDescription.md`
- ✅ `security/{probe_id}/WorkSpace/`（可选）
- ✅ `security_manifest.json`

这种设计让安全测试更专注于行为和证据分析，而不是代码评分。
