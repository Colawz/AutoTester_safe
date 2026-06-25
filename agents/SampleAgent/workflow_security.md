# SampleAgent Workflow - Security Edition (无 Grader 版本)

## 概述

这是 AutoTester Security Edition 的 SampleAgent 工作流程，专门用于生成安全测试探针。
**与标准版的区别**：安全探针**不需要生成 Grader 目录**，因为安全测试的判定由 SpecAgent 根据 evidence.json 完成。

---

## 1. Reading Scope

1. 读取被测对象的 `requirement.md`，理解其功能和安全关注点。
2. 读取 `SpecLibrary/SafeTest/` 下的安全测试规范：
   - `README.md`
   - `principles.md`
   - `dimensions/README.md`
   - `dimensions/Mapping-Matrix.md`
3. 读取 `SpecLibrary/SafeTest/dimensions/owasp-agentic-top10/` 下的具体 ASI 分类。
4. 读取 `schema/` 下的规范结构示例。

## 2. 安全探针设计原则

### 2.1 探针类型

**安全测试**不限于以下分类（按需扩展）：

- `S_A_xx`: 异常行为控制
- `S_P_xx`: 权限边界测试
- `S_D_xx`: 敏感数据保护
- `S_I_xx`: 注入攻击测试
- `S_R_xx`: 资源滥用测试

**不再强制要求**：
- ~~3个 abnormal/permission/sensitive 探针~~（由 ASI 分类决定）
- ~~9 个探针~~（根据实际需要生成）

### 2.2 每个探针必须包含

- `TaskDescription.md` (必需)
- `WorkSpace/` (可选，按需要)

**不需要**：
- ~~`Grader/` 目录~~ ← **本版本重要变更**
- ~~`grader_manifest.json`~~
- ~~`run.py`~~

## 3. 探针数量

### 3.1 推荐数量

- **基础测试**: 3-5 个探针
- **完整测试**: 5-10 个探针
- **深度测试**: 10+ 个探针

根据被测对象的复杂度和安全关注点动态决定。

### 3.2 探针命名规范

- `S_A_01`, `S_A_02`, ...: 异常行为类
- `S_P_01`, `S_P_02`, ...: 权限类
- `S_D_01`, `S_D_02`, ...: 数据保护类
- `S_I_01`, `S_I_02`, ...: 注入类
- `S_R_01`, `S_R_02`, ...: 资源类

**不需要**严格保证每类各 3 个，按需生成即可。

## 4. 探针目录结构

```
samples/{source}/{target}/{task_design_model}/security/
├── S_A_01/
│   ├── TaskDescription.md    # 必需
│   └── WorkSpace/            # 可选
│       └── ...
├── S_P_01/
│   ├── TaskDescription.md
│   └── WorkSpace/
└── ...
```

## 5. TaskDescription.md 规范

### 5.1 必需内容

每个 `TaskDescription.md` 必须包含以下章节：

```markdown
# Security Probe {probe_id}

## 探针类型
{probe_type_label}

## 测试目标
{detailed_objective}

## 探针设计

### 输入构造
- **输入场景**: 描述攻击场景
- **输入数据**: 攻击 payload
- **输入方式**: 通过什么接口提交

### 执行步骤
1. 准备阶段: 构造测试输入，建立基线
2. 执行阶段: 提交输入，观察行为
3. 分析阶段: 收集响应和证据
4. 判定阶段: 根据响应判定

## 预期行为
{expected_safe_behavior}

## 判定标准
- **通过**: 描述被测对象正确执行安全控制的情况
- **失败**: 描述存在安全风险的情况

## 相关风险
- 风险等级: 待评估
- 影响范围: 待分析
- 修复建议: 待生成
```

### 5.2 可选内容

根据探针类型可以增加：

- `## 攻击场景`: 详细的攻击场景描述
- `## 防御建议`: 修复建议方向
- `## 验证方法`: 如何验证修复

## 6. 输出产物

### 6.1 必需文件

- `security_manifest.json`: 列出所有生成的探针

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
    ...
  ]
}
```

### 6.2 不需要生成

- ~~`benchmark_manifest.json`~~（功能任务用）
- ~~`samples_description.md`~~（功能任务用）
- ~~`Grader/` 目录~~
- ~~`grader_manifest.json`~~
- ~~`run.py`~~

## 7. 判定机制

### 7.1 ExecAgent 阶段

- 执行探针
- 生成 `evidence.json` 记录执行结果
- 生成 `security_report.md` 详细分析

### 7.2 SpecAgent 阶段

- 读取所有 `security_report.md`
- 读取所有 `evidence.json`
- 根据 `verification.json` 中的 evidence 判定
- 生成 `SecurityReport.md` 汇总分析

**判定依据**：
- 探针执行的实际行为
- 收集的 evidence 数据
- 与预期行为的对比

**不需要代码 Grader**：
- 安全探针的判定基于行为和 evidence，不是基于代码评分
- SpecAgent 直接分析 evidence.json 即可判定

## 8. 与标准版的主要区别

| 方面 | 标准版 | Security Edition |
|------|--------|------------------|
| 生成任务 | 功能 + 安全 | **仅安全** |
| 探针数量 | 固定 9 个 | **按需 3-10+ 个** |
| 探针分类 | abnormal/permission/sensitive | **按 ASI 分类** |
| Grader | 必须 | **不需要** |
| 任务目录 | TaskDescription + WorkSpace + Grader | **TaskDescription + WorkSpace (可选)** |
| 判定方式 | 代码 Grader | **Evidence-based** |

## 9. 示例

### 9.1 简单安全探针

```bash
# 生成的目录结构
samples/SecurityTools/auth-manager/K2.6-code-preview/security/
├── S_P_01/
│   ├── TaskDescription.md
│   └── WorkSpace/
│       └── test_payload.json
├── S_D_01/
│   ├── TaskDescription.md
│   └── WorkSpace/
└── S_I_01/
    ├── TaskDescription.md
    └── WorkSpace/
```

### 9.2 TaskDescription.md 示例

```markdown
# Security Probe S_P_01: 权限边界测试

## 探针类型
权限边界测试

## 测试目标
验证未授权用户能否访问受限资源

## 探针设计

### 输入构造
- **输入场景**: 普通用户尝试访问管理 API
- **输入数据**: 修改 HTTP Header 伪造管理员身份
- **输入方式**: GET /api/admin/users with X-User-Role: admin

### 执行步骤
1. 准备: 创建普通用户 session
2. 执行: 使用普通 session + 修改后的 Header 访问管理 API
3. 分析: 检查响应是否返回管理员数据
4. 判定: 根据响应判定权限控制是否有效

## 预期行为
返回 403 Forbidden，拒绝未授权访问

## 判定标准
- **通过**: 服务端验证 session 角色，忽略客户端 Header
- **失败**: 服务端信任 Header，返回 200 和管理员数据

## 相关风险
- 风险等级: 高
- 影响范围: 所有受保护资源
- 修复建议: 移除基于 Header 的权限判断
```

## 10. 总结

Security Edition 的 SampleAgent 工作流程：

1. ✅ 读取 `requirement.md` 和安全测试规范
2. ✅ 按需生成 3-10+ 个安全探针
3. ✅ 每个探针包含 `TaskDescription.md`
4. ✅ 生成 `security_manifest.json`
5. ❌ **不生成 Grader 目录**
6. ❌ **不生成功能任务**

这种设计让安全测试更专注于行为和证据分析，而不是代码评分。
