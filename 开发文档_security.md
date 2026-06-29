# Harn-LLM Tester Security Edition - 安全测试特化版开发文档

## 1. 软件定位

Harn-LLM Tester Security Edition 是针对**安全性测试特化**的版本，专注于：
- 自动生成安全测试探针
- 执行安全边界测试
- 深度分析安全问题
- 提供修复建议

与传统版本的区别：

| 特性 | 传统版本 | Security Edition |
|------|---------|------------------|
| 测试类型 | 功能 + 安全 | **仅安全探针** |
| Sample产物 | 功能任务 + 安全探针 | **仅安全探针** |
| Exec产物 | 完整metrics + summary | **简化产物 + 详细安全分析** |
| Spec产物 | 多维度评分 | **安全风险评估 + 修复建议** |

---

## 2. SampleAgent - 安全探针生成

### 2.1 只生成安全探针

**配置**:
```yaml
stages:
  sample:
    config:
      security_only: true
      categories: ["security"]
      generate_functional_tasks: false
```

### 2.2 安全探针类型

系统自动生成以下类型的安全探针：

1. **异常行为控制** (Abnormal Behavior)
   - 越权操作
   - 资源滥用
   - 异常调用链

2. **权限边界测试** (Permission Boundary)
   - 未授权访问
   - 权限提升
   - 资源隔离

3. **敏感数据保护** (Sensitive Data)
   - 数据泄露
   - 明文存储
   - 日志暴露

4. **注入攻击测试** (Injection Attacks)
   - Prompt注入
   - 命令注入
   - 数据注入

5. **资源滥用测试** (Resource Abuse)
   - 内存耗尽
   - CPU过载
   - 网络滥用

### 2.3 探针生成流程

```
输入: requirement.md (被测对象描述)
  ↓
分析: 安全边界识别
  ↓
生成: 5类安全探针
  ↓
输出: database/samples/{target}/security/
       - S_A_01/TaskDescription.md  # 异常行为探针
       - S_P_01/TaskDescription.md  # 权限边界探针
       - S_D_01/TaskDescription.md  # 数据泄露探针
       - S_I_01/TaskDescription.md  # 注入攻击探针
       - S_R_01/TaskDescription.md  # 资源滥用探针
```

---

## 3. ExecAgent - 简化产物 + 详细安全分析

### 3.1 简化的产物结构

**传统版本**:
```
tasks/{task_id}/
├── task_metrics.json      # 详细的时间/token统计 ❌
├── start_timestamp.json   # 开始时间 ❌
├── end_timestamp.json     # 结束时间 ❌
├── worklog.log           # 执行日志 ✅
├── task_summary.md       # 执行总结 ✅
└── results/              # 执行产物 ✅
```

**Security Edition**:
```
tasks/{task_id}/
├── security_report.md    # 安全测试详细报告 ✅✅
├── worklog.log          # 执行日志 ✅
└── results/
    ├── probe_output.json    # 探针执行结果 ✅
    └── evidence.json        # 安全问题证据 ✅
```

### 3.2 security_report.md 详细规范

**必须包含的内容**:

#### A. 探针执行概况
```markdown
## 探针执行概况

### 基本信息
- 探针编号: S_A_01
- 探针类型: 异常行为控制
- 执行时间: 2026-06-25 10:00:00 - 10:05:30
- 执行结果: ⚠️ 发现安全问题

### 测试目标
验证被测对象在异常操作场景下的行为边界。
```

#### B. 测试步骤详细描述
```markdown
## 测试步骤

### 步骤 1: 构造异常输入
- 操作: 尝试越权访问未授权资源
- 输入数据: ...
- 预期行为: 拒绝访问或报错

### 步骤 2: 执行探针
- 实际行为: ...
- 观察到的现象: ...
```

#### C. 安全问题详细分析（如果发现问题）

```markdown
## 安全问题分析

### 问题现象
**问题类型**: 越权访问漏洞

**具体表现**:
- 被测对象在未授权情况下成功访问了敏感资源
- 返回了本应受保护的数据内容
- 未触发任何权限校验机制

**证据**:
```json
{
  "unauthorized_access": true,
  "resource_type": "sensitive_data",
  "leaked_content": "..."
}
```

### 原因剖析

#### 根本原因
被测对象的权限校验逻辑存在缺陷：
1. **设计层面**: 未在关键路径设置权限检查点
2. **实现层面**: 权限验证函数返回值被忽略
3. **逻辑层面**: 异常分支的权限检查遗漏

#### 影响范围
- 影响所有未授权用户
- 可导致敏感数据大规模泄露
- 严重程度: **高危**

#### 攻击路径
```
Step 1: 构造未授权请求
  ↓
Step 2: 绕过权限检查
  ↓
Step 3: 获取敏感资源
  ↓
Step 4: 数据泄露
```

### 修复建议

#### 立即修复措施（紧急）
1. 在关键路径添加权限拦截器
2. 强制验证所有资源访问请求
3. 添加访问日志审计

#### 系统性修复方案
1. **架构层面**: 重构权限控制架构
2. **设计层面**: 明确权限边界定义
3. **实现层面**: 强制权限检查覆盖
4. **测试层面**: 添加自动化权限测试

#### 修复优先级
- **P0**: 权限检查点缺失 → 24小时内修复
- **P1**: 权限逻辑漏洞 → 72小时内修复
- **P2**: 审计机制缺失 → 1周内修复

#### 代码修复示例
```python
# 修复前（漏洞代码）
def get_resource(resource_id):
    return db.query(resource_id)  # 无权限检查 ❌

# 修复后（安全代码）
def get_resource(resource_id, user):
    if not has_permission(user, resource_id):
        raise PermissionDenied()  # 强制权限检查 ✅
    audit_log(user, resource_id)  # 记录审计日志
    return db.query(resource_id)
```

### 验证测试
修复后需要重新执行以下测试：
1. 重复本探针验证漏洞已修复
2. 执行相关权限边界探针
3. 执行数据保护探针
```

---

## 4. SpecAgent - 安全汇总分析

### 4.1 安全分析模式

**输入**:
```
database/exec/{target}/with_target/tasks/
├── S_A_01/security_report.md  # 异常行为报告
├── S_P_01/security_report.md  # 权限边界报告
├── S_D_01/security_report.md  # 数据泄露报告
├── S_I_01/security_report.md  # 注入攻击报告
├── S_R_01/security_report.md  # 资源滥用报告
```

**输出**:
```
database/specs/{target}/
├── SecurityReport.json        # 结构化安全评估
├── SecurityReport.md          # 可读安全报告
├── VulnerabilitySummary.csv   # 漏洞清单
└── RemediationPlan.md         # 修复计划
```

### 4.2 SecurityReport.md 规范

```markdown
# {target_name} 安全测试报告

## 执行摘要

### 安全状况总览
- **总体风险等级**: 高危
- **发现漏洞数量**: 3个高危 + 2个中危
- **修复优先级**: P0级别的漏洞需立即修复

### 关键发现
1. **越权访问漏洞** (高危): 被测对象缺少权限校验，可能导致数据泄露
2. **注入攻击漏洞** (高危): 输入验证不足，可能被注入恶意指令
3. **敏感数据泄露** (高危): 日志中包含明文敏感信息
4. 权限边界模糊 (中危): 部分资源访问逻辑不清晰
5. 资源滥用风险 (中危): 缺少资源使用限制

---

## 一、漏洞详情分析

### 1. 越权访问漏洞 (S_A_01)

#### 问题概述
**漏洞类型**: 权限控制缺失  
**严重程度**: 高危  
**发现时间**: 2026-06-25  
**影响范围**: 全部未授权用户

#### 漏洞表现
被测对象在未进行权限验证的情况下，允许访问敏感资源...

#### 根本原因
(从 task summary 中提取)

#### 攻击路径
(从 task summary 中提取)

#### 修复建议
(从 task summary 中提取)

---

### 2. 注入攻击漏洞 (S_I_01)
...

---

## 二、风险评估矩阵

| 漏洞类型 | 发生概率 | 影响程度 | 风险等级 | 修复优先级 |
|---------|---------|---------|---------|-----------|
| 越权访问 | 高 | 高 | **高危** | **P0** |
| 注入攻击 | 高 | 高 | **高危** | **P0** |
| 数据泄露 | 高 | 高 | **高危** | **P0** |
| 权限边界模糊 | 中 | 中 | 中危 | P1 |
| 资源滥用 | 低 | 中 | 中危 | P2 |

---

## 三、修复计划

### 紧急修复（P0，24小时内）

#### 任务 1: 权限检查补丁
- **目标**: 修复越权访问漏洞
- **措施**: 添加权限拦截器
- **验证**: 重新执行 S_A_01 探针

#### 任务 2: 输入验证增强
- **目标**: 修复注入攻击漏洞
- **措施**: 强制输入验证
- **验证**: 重新执行 S_I_01 探针

#### 任务 3: 日志脱敏
- **目标**: 修复数据泄露漏洞
- **措施**: 清理日志敏感信息
- **验证**: 重新执行 S_D_01 探针

### 系统性改进（P1/P2）

(详细改进计划...)

---

## 四、合规性评估

### OWASP Top 10 对照
- **A01:2021 - Broken Access Control**: ⚠️ 存在越权访问漏洞
- **A03:2021 - Injection**: ⚠️ 存在注入漏洞
- **A05:2021 - Security Misconfiguration**: ⚠️ 日志配置不当

### 安全标准符合度
- 权限控制: ❌ 不符合
- 数据保护: ❌ 不符合
- 输入验证: ❌ 不符合

---

## 五、测试结论

### 总体评价
被测对象存在**多个高危安全漏洞**，不建议在生产环境使用。

### 使用建议
1. **立即停止使用**: 在漏洞修复前不应部署
2. **优先修复**: P0级别漏洞需立即处理
3. **安全加固**: 重新设计权限架构
4. **重新测试**: 修复后需全面复测

### 后续行动
1. 安全团队介入修复
2. 制定修复时间表
3. 修复完成后重新测试
4. 建立安全测试CI流程
```

---

## 5. 使用流程

### 5.1 添加安全测试需求

```bash
# 创建安全测试 target
mkdir -p TargetsRepo/MyProject/my-tool
cat > TargetsRepo/MyProject/my-tool/requirement.md << 'EOF'
# My Tool Security Test

## 功能描述
这是一个数据处理工具，支持文件读写、数据库访问...

## 安全关注点
- 权限控制是否完善
- 数据访问是否安全
- 输入验证是否充分
EOF
```

### 5.2 启动安全测试

```bash
# 交互式启动
python3 launch.py

# 或快速启动
python3 start.py --platform macos --port 8701
```

### 5.3 查看安全报告

```bash
# 访问 Reports 页面
open http://localhost:8701/reports

# 点击 target 查看详细安全分析
```

---

## 6. 目录结构

```
software_safe/
├── config_security.yaml     # 安全测试配置
├── 开发文档_security.md     # 本文档
│
├── agents/
│   ├── SampleAgent/
│   │   └── workflow_security.md  # 安全探针生成流程
│   ├── ExecAgent/
│   │   ├── withtarget/
│   │   │   ├── workflow_security.md
│   │   │   └── prompt_security.md
│   │   └── utils/
│   │       ├── security_report_generator.py  # 安全报告生成
│   │       └── evidence_extractor.py        # 证据提取
│   └── SpecAgent/
│       ├── workflow_security.md
│       ├── prompt_security.md
│       └── utils/
│           ├── vulnerability_analyzer.py    # 漏洞分析
│           └── remediation_generator.py     # 修复建议生成
│
├── database/
│   ├── samples/{target}/security/
│   │   └── S_A_01/TaskDescription.md
│   ├── exec/{target}/with_target/tasks/
│   │   └── S_A_01/security_report.md
│   └── specs/{target}/
│       ├── SecurityReport.md
│       └── VulnerabilitySummary.csv
│
└── TargetsRepo/
    └── MyProject/my-tool/
        └── requirement.md
```

---

## 7. 配置差异

### 7.1 与传统版本对比

**传统版本** (`config.yaml`):
```yaml
stages:
  sample:
    categories: ["common", "hard"]  # 功能任务 + 安全探针
  
  exec:
    simplified_output: false       # 完整产物
  
  spec:
    dimensions: ["utility", "security", "efficiency"]  # 多维度
```

**Security Edition** (`config_security.yaml`):
```yaml
stages:
  sample:
    categories: ["security"]        # 仅安全探针
    security_only: true
  
  exec:
    simplified_output: true         # 简化产物
    security_focused: true
  
  spec:
    dimensions: ["security"]        # 仅安全维度
```

---

## 8. 优势

### 8.1 专注安全
- ✅ 只生成安全探针，节省测试资源
- ✅ 深度分析安全问题，提供详细原因
- ✅ 给出修复建议，指导后续改进

### 8.2 简化产物
- ✅ 移除时间/token统计，聚焦安全问题
- ✅ 保留核心安全证据，便于问题追踪
- ✅ 详细的安全报告，优于简短的summary

### 8.3 实用性强
- ✅ 漏洞清单一目了然
- ✅ 修复计划清晰明确
- ✅ 合规性评估完整