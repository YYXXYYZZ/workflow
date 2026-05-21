# AI-Friendly Dev-Test-Ops 工作流设计文档

## 1. 背景与目标

本文档设计一套以 **Issue 为流程入口**、以 **研发大步骤为骨架**、以 **AI Agent + 人工审核 + 自动化门禁** 为执行方式的研发工作流。

目标不是单纯引入一个 AI 编程工具，而是把研发流程从：

```text
人手动沟通 -> 人写代码 -> 人 Review -> 人上线 -> 人复盘
```

改造为：

```text
Issue 驱动 -> AI 辅助产出 -> 自动化校验 -> 人工决策 -> 工具执行 -> 效率中心沉淀
```

这套工作流的核心思想接近 IssueOps：用 GitHub Issues、GitHub Actions、PR 作为自动化工作流入口，通过 issue comments、labels、state changes 触发任务分配、CI/CD、部署等动作。([The GitHub Blog][1])

---

## 2. 核心原则

### 2.1 Issue 是流程入口

所有研发任务都应该从 Issue 开始，包括：

```text
Feature
Bug
Refactor
TechDebt
Security
Ops
Incident
Release
```

Issue 不只是“问题描述”，而是整个工作项的主线对象。它承载：

```text
需求背景
负责人
优先级
验收标准
关联 Spec
关联 Plan
关联 Tasks
关联 PR
关联 CI
关联 QA
关联 Release
关联 Ops
最终总结
```

### 2.2 工作流保留研发大步骤

中间流程不强行变成“Issue -> Issue -> Issue”，而是保留正常研发大步骤：

```text
Issue Intake
Repo Rules
Spec
Plan
Tasks
Implement
Local Validate
Open PR
CI Gate
AI Review
Human Review
Merge
Test / QA
Release Gate
Deploy
Ops
Feedback
```

### 2.3 AI 负责生成、执行、检查；人负责判断、批准、兜底

AI Agent 可以做：

```text
生成 spec
生成 plan
拆 tasks
实现代码
补测试
解释 CI 失败
做 AI Review
生成测试计划
生成发布计划
生成总结
```

人必须负责：

```text
确认需求范围
确认技术方案
确认风险
人工 Review
QA 验收
上线审批
回滚决策
最终关闭 Issue
```

### 2.4 工具执行门禁，仓库存放规则

需要区分两类约束：

```text
仓库侧约束：随代码版本化
工具侧约束：由平台强制执行
```

例如：

```text
AGENTS.md                     -> 仓库侧
constitution.md               -> 仓库侧
PR template                   -> 仓库侧
CODEOWNERS                    -> 仓库侧
.github/workflows/ci.yml      -> 仓库侧

Branch protection             -> 工具侧
Required status checks        -> 工具侧
GitHub Environment approval   -> 工具侧
Merge queue                   -> 工具侧
Deployment protection rules   -> 工具侧
```

AGENTS.md 适合作为 AI Agent 的仓库级说明文件，它的定位就是给 coding agents 的专用 README，用来提供上下文、安装命令、测试命令和项目规则。([agents.md][2])

---

## 3. 总体架构

```text
                   ┌──────────────────────────┐
                   │      Efficiency Center    │
                   │      效率中心 / 过程事件中心 │
                   └─────────────▲────────────┘
                                 │
    所有工具动作、AI 动作、人工动作、CI 结果、部署结果、QA 结果全部上报
                                 │

Issue
  ↓
Spec
  ↓
Plan
  ↓
Tasks
  ↓
Implement
  ↓
Local Validate
  ↓
Open PR
  ↓
CI Gate
  ↓
AI Review
  ↓
Human Review
  ↓
Merge
  ↓
Test / QA
  ↓
Release Gate
  ↓
Deploy
  ↓
Ops Verify
  ↓
Feedback
```

效率中心不是一个普通日志库，而是一个研发过程事件中心。它统一接收来自 GitHub、CI、Agent、QA、CD、监控系统的事件，用于追踪每个 Issue 从创建到上线的完整过程。OpenTelemetry 的思想可以借鉴，因为它本身就是用于采集、生成、导出 traces、metrics、logs 等遥测数据的开放框架。([OpenTelemetry][3])

---

## 4. 关键工具选型

| 能力                  | 推荐工具                                                        | 说明                                                            |
| ------------------- | ----------------------------------------------------------- | ------------------------------------------------------------- |
| Issue 主线            | GitHub Issues / Jira / Linear / Meego                       | 作为任务入口和状态承载                                                   |
| Slash Command       | GitHub Actions + github/command / slash-command-dispatch    | 在 Issue / PR 评论里触发 `/spec`、`/implement`、`/deploy` 等命令         |
| Spec / Plan / Tasks | GitHub Spec Kit                                             | 负责规格驱动开发中的 specify、plan、tasks 等步骤                             |
| Agent 规则            | AGENTS.md                                                   | 给 AI Agent 固定读取的仓库规则                                          |
| Coding Agent        | Copilot coding agent / Codex / Cline / Aider / OpenHands    | 负责实现、补测试、本地验证                                                 |
| AI Review           | Continue / 自定义 Review Agent                                 | Continue 可把 `.continue/checks/*.md` 作为 PR 上的 AI status checks |
| CI                  | GitHub Actions / GitLab CI                                  | 自动跑 lint、test、build、安全扫描                                      |
| 合并门禁                | Branch Protection / Required Status Checks / Merge Queue    | 阻止未满足条件的 PR 合并                                                |
| 发布门禁                | GitHub Environments / Deployment Protection Rules / Argo CD | 阻止未审批或未满足条件的部署                                                |
| 监控与诊断               | OpenTelemetry / Grafana / Datadog / Sentry                  | 线上验证、异常诊断、回滚判断                                                |

GitHub branch protection 可以要求 PR 在合并前必须通过状态检查或获得 review approval；required status checks 通过后才允许合并。([GitHub Docs][4]) GitHub Environments 的 deployment protection rules 可以要求特定条件通过后，部署 job 才能继续，例如人工审批、等待时间、分支限制或自定义保护规则。([GitHub Docs][5])

---

## 5. 效率中心设计

### 5.1 定位

效率中心负责收集所有工具动作，并按 Issue 维度串起来。

它记录：

```text
谁做了什么
是人做的还是 AI 做的
在哪个工具里做的
触发了什么命令
产出了什么文件
是否成功
耗时多久
卡在哪个门禁
失败原因是什么
后续是否返工
```

### 5.2 事件格式

所有工具动作统一上报为事件：

```json
{
  "event_id": "evt_20260520_0001",
  "issue_id": "ISSUE-123",
  "stage": "CI Gate",
  "command": "/ci-gate",
  "actor_type": "automation",
  "actor": "github-actions",
  "tool": "GitHub Actions",
  "status": "failed",
  "artifacts": [
    "ci-summary.json",
    "security-report.json"
  ],
  "started_at": "2026-05-20T10:00:00Z",
  "finished_at": "2026-05-20T10:03:20Z",
  "error": "security scan failed"
}
```

### 5.3 需要接入的数据源

```text
GitHub Issues
GitHub Pull Requests
GitHub Actions
Branch Protection
Continue AI Checks
Coding Agent Session Logs
QA Platform
Deployment Pipeline
Observability Platform
Incident System
```

### 5.4 关键指标

效率中心至少要输出这些指标：

```text
Issue lead time
Spec 生成耗时
Plan 生成耗时
Tasks 拆解耗时
Agent 实现耗时
本地验证失败次数
CI 失败率
AI Review 命中率
人工 Review 耗时
返工次数
QA 缺陷数
上线阻断次数
回滚次数
线上事故数
Agent 贡献比例
人类介入次数
```

---

## 6. 完整工作流

### 00. Efficiency Center / 效率中心

| 干什么         | 谁              | 位置 | 命令             | 工具支持                     | 说明                              |
| ----------- | -------------- | -- | -------------- | ------------------------ | ------------------------------- |
| 收集所有工具动作    | 自动化            | 工具 | `auto report`  | GitHub Webhook / Actions | Issue、PR、CI、Review、Deploy 都上报   |
| 记录人和 AI 的操作 | 自动化            | 工具 | `auto audit`   | GitHub API / Agent logs  | 谁触发、何时触发、结果如何                   |
| 汇总阶段交付物     | 自动化 + AI Agent | 工具 | `/sync-status` | 效率中心 / 数据库 / Dashboard   | 每个 Issue 的进度、产物、卡点              |
| 生成效率指标      | AI Agent + 自动化 | 工具 | `/metrics`     | OTel / BI / Dashboard    | Lead time、返工次数、CI 失败率、Review 耗时 |

交付物：

```text
efficiency-events.jsonl
issue-timeline.json
delivery-dashboard
efficiency-report.md
```

---

### 01. Issue Intake / 研发任务入口

| 干什么              | 谁                 | 位置    | 命令             | 工具支持                          | 说明                                  |
| ---------------- | ----------------- | ----- | -------------- | ----------------------------- | ----------------------------------- |
| 创建研发 Issue       | 产品经理 / 技术负责人 / 开发 | Issue | `create issue` | GitHub Issues / Jira / Linear | Feature / Bug / Refactor / TechDebt |
| 补充上下文            | 开发 + AI Agent     | Issue | `/clarify`     | GitHub Actions + LLM Agent    | AI 补边界、复现步骤、验收条件                    |
| 任务分流             | 技术负责人 / 自动化       | 工具    | `/triage`      | Projects / Labels / Actions   | 设置负责人、优先级、里程碑                       |
| 生成 Issue Context | 自动化 + AI Agent    | 仓库    | `/context`     | 轻量自建                          | 生成 `issue_context.json`             |
| 上报效率中心           | 自动化               | 工具    | `auto report`  | Webhook / Actions             | 记录 Issue 创建和分流动作                    |

交付物：

```text
issue.md
issue_context.json
issue_comments.txt
负责人
优先级
labels
milestone
```

---

### 02. Repo Rules / 仓库规则

| 干什么         | 谁             | 位置 | 命令                   | 工具支持                  | 说明                                |
| ----------- | ------------- | -- | -------------------- | --------------------- | --------------------------------- |
| 定义 Agent 规则 | 技术负责人 / 架构师   | 仓库 | `/init-agents`       | AGENTS.md             | 安装、启动、测试、禁止事项                     |
| 定义项目原则      | 技术负责人 / 架构师   | 仓库 | `/init-constitution` | Spec Kit constitution | 技术原则、质量底线、约束                      |
| 定义 PR 模板    | 技术负责人 / 代码审查人 | 仓库 | `/init-pr-template`  | GitHub PR template    | Summary / Tests / Risk / Rollback |
| 定义合并门禁      | 技术负责人 / 运维    | 工具 | `/init-gates`        | Branch protection     | CI green + required review        |
| 上报效率中心      | 自动化           | 工具 | `auto report`        | Webhook / Actions     | 记录规则初始化和变更                        |

交付物：

```text
AGENTS.md
constitution.md
.github/PULL_REQUEST_TEMPLATE.md
CODEOWNERS
branch protection
required status checks
.continue/checks/*.md
```

AGENTS.md 应放在仓库中，作为 AI Agent 读取项目规则的入口。Codex 文档也明确说明，Codex 会在开始任务前读取 AGENTS.md，以便获得项目级上下文和约束。([OpenAI Developers][6])

---

### 03. Spec / 技术规格

| 干什么          | 谁                   | 位置 | 命令              | 工具支持               | 说明              |
| ------------ | ------------------- | -- | --------------- | ------------------ | --------------- |
| 生成技术规格       | AI Agent 起草，技术负责人审核 | 仓库 | `/spec`         | GitHub Spec Kit    | 输出 `spec.md`    |
| 明确非目标        | AI Agent 起草，技术负责人审核 | 仓库 | `/clarify-spec` | Spec Kit + 模板      | 明确不做什么          |
| 校验规格覆盖 Issue | 自动化 + 技术负责人         | 工具 | `/check-spec`   | 轻量自建 Gate          | 检查是否覆盖验收标准      |
| 审核 Spec      | 技术负责人 / 架构师 / 测试    | 工具 | `approve spec`  | GitHub PR / Review | 通过后进入 Plan      |
| 上报效率中心       | 自动化                 | 工具 | `auto report`   | Webhook / Actions  | 记录 spec 生成和审核结果 |

交付物：

```text
spec.md
clarified-scope.md
open-questions.md
spec-approval-record
```

GitHub Spec Kit 适合放在这个阶段，因为它支持围绕 spec、plan、tasks 等产物组织规格驱动开发流程。([GitHub][7])

---

### 04. Plan / 技术方案

| 干什么     | 谁                   | 位置 | 命令            | 工具支持                      | 说明                            |
| ------- | ------------------- | -- | ------------- | ------------------------- | ----------------------------- |
| 生成实现计划  | AI Agent 起草，技术负责人审核 | 仓库 | `/plan`       | GitHub Spec Kit           | 输出 `plan.md`                  |
| 设计架构变更  | AI Agent 起草，架构师审核   | 仓库 | `/arch`       | ADR / C4 / 自定义 Agent      | 输出 `arch.md` / `ADR.md`       |
| 定义接口/契约 | AI Agent 起草，开发审核    | 仓库 | `/contract`   | OpenAPI / AsyncAPI / Pact | `openapi.yaml` / event schema |
| 风险评估    | AI Agent 起草，人确认     | 仓库 | `/risk`       | 自定义模板                     | 数据迁移、兼容性、性能、安全                |
| 上报效率中心  | 自动化                 | 工具 | `auto report` | Webhook / Actions         | 记录方案生成和风险结果                   |

交付物：

```text
plan.md
arch.md
ADR.md
openapi.yaml
event-schema.yaml
risk.md
```

---

### 05. Tasks / 任务拆解

| 干什么    | 谁                  | 位置 | 命令              | 工具支持              | 说明            |
| ------ | ------------------ | -- | --------------- | ----------------- | ------------- |
| 拆任务清单  | AI Agent 起草，开发确认   | 仓库 | `/tasks`        | GitHub Spec Kit   | 输出 `tasks.md` |
| 标记依赖关系 | AI Agent + 开发      | 仓库 | `/order-tasks`  | 轻量自建              | 标记串行 / 并行任务   |
| 标记测试任务 | AI Agent + 测试 / 开发 | 仓库 | `/test-tasks`   | Spec Kit + 模板     | 每个功能任务对应测试任务  |
| 确认可执行  | 开发 / 技术负责人         | 工具 | `approve tasks` | GitHub Review     | 任务可执行后进入实现    |
| 上报效率中心 | 自动化                | 工具 | `auto report`   | Webhook / Actions | 记录任务拆解结果      |

交付物：

```text
tasks.md
task-dependencies.md
test-tasks.md
implementation-ready
```

---

### 06. Implement / 代码实现

| 干什么              | 谁                | 位置    | 命令                        | 工具支持                             | 说明                             |
| ---------------- | ---------------- | ----- | ------------------------- | -------------------------------- | ------------------------------ |
| 分配给 Coding Agent | 技术负责人 / 开发       | Issue | `assign to agent`         | Copilot coding agent / OpenHands | Issue 分配给 Agent                |
| 创建分支             | 自动化 / AI Agent   | 工具    | `/start-dev`              | GitHub / Git / Worktree          | `branch: issue-123-xxx`        |
| 实现代码             | AI Agent 主写，开发兜底 | 仓库    | `/implement`              | Copilot / Codex / Cline / Aider  | 按 `tasks.md` 改代码               |
| 补测试              | AI Agent 起草，开发确认 | 仓库    | `/add-tests`              | Cline / Aider / test runner      | unit / integration tests       |
| 生成实现总结           | AI Agent         | 仓库    | `/implementation-summary` | Copilot PR / 自定义 Agent           | summary / changed files / risk |
| 上报效率中心           | 自动化              | 工具    | `auto report`             | Agent logs / Webhook             | 记录 Agent 操作、耗时、失败次数            |

交付物：

```text
code changes
tests
commits
implementation_summary.md
draft branch
agent-session-log.json
```

---

### 07. Local Validate / 本地验证

| 干什么              | 谁              | 位置 | 命令                  | 工具支持                        | 说明                            |
| ---------------- | -------------- | -- | ------------------- | --------------------------- | ----------------------------- |
| 跑 lint/typecheck | 自动化 / AI Agent | 本地 | `/validate`         | Cline / Aider / npm scripts | `pnpm lint && pnpm typecheck` |
| 跑单元测试            | 自动化 / AI Agent | 本地 | `/unit-test`        | Cline / Aider / test runner | `pnpm test`                   |
| 跑集成/契约测试         | 自动化            | 本地 | `/integration-test` | Testcontainers / Pact       | DB / Redis / API contract     |
| 解释失败             | AI Agent       | 本地 | `/explain-failure`  | Cline / Aider / logs        | 根据报错继续修                       |
| 上报效率中心           | 自动化            | 工具 | `auto report`       | Test report collector       | 记录测试耗时、失败类型、修复次数              |

交付物：

```text
validation.md
local-test-report.json
fixed-failures.md
known-issues.md
```

---

### 08. Open PR / 创建 PR

| 干什么       | 谁              | 位置 | 命令               | 工具支持                          | 说明                     |
| --------- | -------------- | -- | ---------------- | ----------------------------- | ---------------------- |
| 创建 PR     | AI Agent / 自动化 | 工具 | `/open-pr`       | Copilot agent / GitHub CLI    | PR 关联 Issue 和 spec     |
| 生成 PR 描述  | AI Agent       | 工具 | `/summarize-pr`  | Copilot / 自定义 Agent           | Summary / tests / risk |
| 填 PR 模板   | AI Agent + 自动化 | 仓库 | `auto`           | PR template                   | 不完整则阻断 review          |
| 请求 Review | 自动化            | 工具 | `request review` | CODEOWNERS / GitHub reviewers | 自动找代码审查人               |
| 上报效率中心    | 自动化            | 工具 | `auto report`    | GitHub Webhook                | 记录 PR 创建、Review 分配     |

交付物：

```text
Pull Request
PR description
linked issue
linked spec
requested reviewers
```

---

### 09. CI Gate / CI 卡点

| 干什么      | 谁        | 位置 | 命令                    | 工具支持                         | 说明                             |
| -------- | -------- | -- | --------------------- | ---------------------------- | ------------------------------ |
| 检查前置交付物  | 自动化      | 工具 | `/ci-gate`            | GitHub Actions / Gate Engine | spec、plan、tasks、tests、PR 描述必须齐 |
| 自动跑 CI   | 自动化      | 工具 | `auto on PR`          | GitHub Actions / GitLab CI   | push / PR 自动触发                 |
| 质量检查     | 自动化      | 工具 | `lint / test / build` | CI pipeline                  | required checks                |
| 安全扫描     | 自动化      | 工具 | `security scan`       | CodeQL / Trivy / Dependabot  | 高危阻断                           |
| 解释 CI 失败 | AI Agent | 工具 | `/explain-ci`         | Copilot / Cline / 自定义 Agent  | 给修复建议                          |
| 上报效率中心   | 自动化      | 工具 | `auto report`         | CI Webhook / Workflow logs   | 记录 CI 卡点、失败原因、耗时               |

CI Gate 必须满足：

```text
issue_context.json 存在
spec.md 存在并 approved
plan.md 存在
tasks.md 存在
implementation_summary.md 存在
tests 已新增或说明无需新增
PR description 完整
lint / test / build / security 全部通过
```

交付物：

```text
ci-summary.json
coverage-report
security-report.json
build-artifact
ci-gate-result.json
```

GitHub required status checks 适合承担 CI Gate 的基础能力，因为它可以要求所有必需状态检查通过后才允许合并。([GitHub Docs][8])

---

### 10. AI Review / AI 审查

| 干什么           | 谁        | 位置 | 命令                  | 工具支持                    | 说明                                      |
| ------------- | -------- | -- | ------------------- | ----------------------- | --------------------------------------- |
| 规则化 AI Review | AI Agent | 工具 | `/ai-review`        | Continue                | `.continue/checks/*.md` 作为 status check |
| 检查测试缺口        | AI Agent | 工具 | `/check-tests`      | Continue / custom check | 改了逻辑但没测，标红                              |
| 检查 Spec Drift | AI Agent | 工具 | `/check-spec-drift` | Continue + 轻量自建         | 实现是否偏离 `spec.md`                        |
| 生成修复建议        | AI Agent | 工具 | `auto`              | Continue                | red check + suggested diff              |
| 上报效率中心        | 自动化      | 工具 | `auto report`       | Review Webhook          | 记录 AI Review 命中问题和修复率                   |

交付物：

```text
AI status checks
review.json
suggested-diff.md
risk-notes.md
```

Continue 的优势是把 AI checks 作为仓库内的 markdown 文件管理，并在 PR 上显示为 GitHub status check。([docs.continue.dev][9])

---

### 11. Human Review / 人工审查

| 干什么    | 谁             | 位置 | 命令                | 工具支持                  | 说明                |
| ------ | ------------- | -- | ----------------- | --------------------- | ----------------- |
| 审代码正确性 | 代码审查人 / 技术负责人 | 工具 | `review`          | GitHub PR Review      | 看 diff、架构、边界、异常处理 |
| 审风险和回滚 | 代码审查人 / 技术负责人 | 工具 | `review risk`     | PR checklist          | 兼容性、数据、安全、回滚      |
| 要求修改   | 代码审查人         | 工具 | `request changes` | GitHub Review         | AI Agent 或开发继续修   |
| 批准合并   | 代码审查人 / 技术负责人 | 工具 | `approve`         | Branch protection     | 人最终负责             |
| 上报效率中心 | 自动化           | 工具 | `auto report`     | GitHub Review Webhook | 记录 Review 耗时、返工次数 |

交付物：

```text
review comments
approval
requested changes
merge decision
```

---

### 12. Merge / 合并

| 干什么        | 谁        | 位置    | 命令            | 工具支持                            | 说明                              |
| ---------- | -------- | ----- | ------------- | ------------------------------- | ------------------------------- |
| 检查合并条件     | 自动化      | 工具    | `merge gate`  | Branch protection / Merge queue | CI + AI checks + human approval |
| 合并 PR      | 人 / 自动化  | 工具    | `merge`       | GitHub merge / auto-merge       | squash / merge queue            |
| 关闭研发 Issue | 自动化      | Issue | `auto close`  | GitHub linked issue             | `Closes #123`                   |
| 生成研发总结     | AI Agent | 仓库    | `/summary`    | 自定义 Agent                       | `final-summary.md`              |
| 上报效率中心     | 自动化      | 工具    | `auto report` | GitHub Webhook                  | 记录合并、关闭、总结                      |

交付物：

```text
merged PR
closed dev issue
final-summary.md
follow-up issues
```

---

### 13. Test / QA 验收

| 干什么     | 谁                | 位置 | 命令                      | 工具支持                                 | 说明             |
| ------- | ---------------- | -- | ----------------------- | ------------------------------------ | -------------- |
| 生成测试计划  | AI Agent 起草，测试审核 | 仓库 | `/test-plan`            | 自定义 Agent / Test template            | `test-plan.md` |
| 生成测试用例  | AI Agent 起草，测试补充 | 仓库 | `/test-cases`           | TestRail / Zephyr / Xray / 自建        | 覆盖 AC、边界、回归场景  |
| 执行测试    | 测试 + 自动化         | 工具 | `/run-qa`               | Playwright / Cypress / Test platform | 自动化 + 手工探索测试   |
| 验收通过/打回 | 测试 / 产品经理        | 工具 | `/qa-pass` / `/qa-fail` | QA board / Bug tracker               | 失败创建 bug issue |
| 上报效率中心  | 自动化              | 工具 | `auto report`           | QA Webhook / Test report             | 记录用例数、失败数、缺陷分布 |

交付物：

```text
test-plan.md
test-cases.md
regression-scope.md
qa-report.md
bug issues
qa-signoff
```

---

### 14. Release Gate / 上线卡点

| 干什么      | 谁                      | 位置 | 命令                | 工具支持                              | 说明             |
| -------- | ---------------------- | -- | ----------------- | --------------------------------- | -------------- |
| 检查所有前置完成 | 自动化                    | 工具 | `/release-gate`   | GitHub Environments / Gate Engine | 前面所有交付物必须完成    |
| 生成发布计划   | AI Agent 起草，运维/技术负责人审核 | 仓库 | `/release-plan`   | Release template                  | `release.md`   |
| 生成回滚计划   | AI Agent 起草，运维审核       | 仓库 | `/rollback-plan`  | Runbook / CD history              | `rollback.md`  |
| 发布审批     | 技术负责人 / 运维 / 产品经理      | 工具 | `approve release` | GitHub Environment reviewers      | 人批准后才能部署生产     |
| 上报效率中心   | 自动化                    | 工具 | `auto report`     | Deployment Webhook                | 记录上线卡点、审批、阻断原因 |

Release Gate 必须满足：

```text
dev issue closed
PR merged
CI Gate passed
AI Review passed
Human Review approved
QA passed
release.md 存在
rollback.md 存在
observability checklist 完成
owner approval 完成
```

交付物：

```text
release-gate-result.json
release.md
rollback.md
approval-record.json
```

GitHub Environments 的 deployment protection rules 可以作为上线卡点的一部分，要求特定审批或保护规则通过后部署才能继续。([GitHub Docs][5])

---

### 15. Deploy / 部署

| 干什么           | 谁         | 位置 | 命令                | 工具支持                             | 说明                   |
| ------------- | --------- | -- | ----------------- | -------------------------------- | -------------------- |
| 部署 Staging    | 自动化       | 环境 | `/deploy-staging` | GitHub Actions / Argo CD         | staging smoke        |
| 部署 Production | 人批准，自动化执行 | 环境 | `/deploy-prod`    | CD / Environments / Feature flag | 灰度发布                 |
| 记录部署结果        | 自动化       | 工具 | `auto`            | CD report                        | `deploy-report.json` |
| 上报效率中心        | 自动化       | 工具 | `auto report`     | CD Webhook / Deploy logs         | 记录部署耗时、版本、环境、结果      |

交付物：

```text
deploy-report.json
deployed-version.txt
rollout-status.json
```

---

### 16. Ops / 线上验证

| 干什么        | 谁                  | 位置 | 命令                        | 工具支持                          | 说明                             |
| ---------- | ------------------ | -- | ------------------------- | ----------------------------- | ------------------------------ |
| 检查核心指标     | 自动化 + SRE          | 工具 | `/verify-prod`            | Grafana / Datadog / Sentry    | error rate / latency / traffic |
| 异常诊断       | AI Agent           | 工具 | `/diagnose`               | Logs / Traces / Metrics       | 关联 recent release              |
| 回滚/事故处理    | SRE / 运维 / 技术负责人   | 工具 | `/rollback` / `/incident` | Rollback pipeline / PagerDuty | 人判断，自动化执行                      |
| 更新 Runbook | AI Agent 起草，SRE 审核 | 仓库 | `/update-runbook`         | ops/runbooks                  | 固化处理流程                         |
| 上报效率中心     | 自动化                | 工具 | `auto report`             | Observability Webhook         | 记录线上指标、告警、回滚、事故                |

交付物：

```text
ops-report.md
metrics-check.md
diagnosis.md
incident.md
rollback-report.md
runbook update
```

---

### 17. Feedback / 反馈闭环

| 干什么    | 谁               | 位置    | 命令               | 工具支持                          | 说明                 |
| ------ | --------------- | ----- | ---------------- | ----------------------------- | ------------------ |
| 生成最终总结 | AI Agent        | 仓库    | `/final-summary` | Issue / PR / QA / Ops reports | `final-summary.md` |
| 创建后续任务 | AI Agent 起草，人确认 | Issue | `/followups`     | GitHub Issues / Jira          | 技术债、测试补强、监控补强      |
| 反哺规则   | AI Agent 建议，人审核 | 仓库    | `/update-rules`  | AGENTS.md / checks / runbook  | 重复问题写进规则           |
| 上报效率中心 | 自动化             | 工具    | `auto report`    | Efficiency Center             | 汇总完整交付链路指标         |

交付物：

```text
final-summary.md
follow-up issues
updated AGENTS.md
updated checks
updated runbook
efficiency report
```

---

## 7. CI Gate 设计

CI Gate 不只是跑测试，而是检查前面的研发交付是否完整。

### 7.1 CI Gate 输入

```text
issue_context.json
spec.md
plan.md
tasks.md
implementation_summary.md
PR description
test reports
security report
AI Review result
```

### 7.2 CI Gate 必须检查

```text
Issue 已绑定 PR
Spec 已批准
Plan 已存在
Tasks 已存在
代码变更与 tasks 对应
测试已新增或说明无需新增
PR 描述完整
lint 通过
typecheck 通过
unit tests 通过
integration tests 通过
security scan 通过
AI checks 通过
```

### 7.3 CI Gate 输出

```json
{
  "issue_id": "ISSUE-123",
  "gate": "ci-gate",
  "status": "passed",
  "checks": {
    "spec_approved": true,
    "plan_exists": true,
    "tasks_exists": true,
    "tests_added_or_explained": true,
    "pr_description_complete": true,
    "lint_passed": true,
    "tests_passed": true,
    "security_passed": true,
    "ai_review_passed": true
  }
}
```

### 7.4 CI Gate 阻断规则

```text
任何 required check 失败 -> 禁止合并
Spec 缺失 -> 禁止合并
Tasks 缺失 -> 禁止合并
AI Review 未完成 -> 禁止合并
Human Review 未批准 -> 禁止合并
```

---

## 8. Release Gate 设计

Release Gate 不只是部署审批，而是检查研发、测试、上线准备是否全部完成。

### 8.1 Release Gate 输入

```text
merged PR
closed dev issue
ci-gate-result.json
AI Review result
Human Review approval
qa-report.md
release.md
rollback.md
observability-checklist.md
approval record
```

### 8.2 Release Gate 必须检查

```text
PR 已合并
Dev Issue 已关闭
CI Gate 已通过
AI Review 已通过
人工 Review 已批准
QA 已通过
无 P0/P1 阻断 bug
release.md 存在
rollback.md 存在
灰度方案存在
监控指标已配置
告警已配置
Runbook 已存在
上线审批已完成
```

### 8.3 Release Gate 输出

```json
{
  "issue_id": "ISSUE-123",
  "gate": "release-gate",
  "status": "passed",
  "checks": {
    "pr_merged": true,
    "ci_gate_passed": true,
    "qa_passed": true,
    "release_plan_exists": true,
    "rollback_plan_exists": true,
    "observability_ready": true,
    "approval_done": true
  }
}
```

### 8.4 Release Gate 阻断规则

```text
QA 未通过 -> 禁止上线
rollback.md 缺失 -> 禁止上线
release.md 缺失 -> 禁止上线
监控和告警未确认 -> 禁止上线
上线审批未完成 -> 禁止上线
```

---

## 9. 命令体系

### 9.1 需求与上下文命令

```text
/clarify
/context
/triage
```

### 9.2 规格与计划命令

```text
/spec
/clarify-spec
/check-spec
/plan
/arch
/contract
/risk
/tasks
/order-tasks
/test-tasks
```

### 9.3 实现命令

```text
/start-dev
/implement
/add-tests
/implementation-summary
```

### 9.4 验证与 CI 命令

```text
/validate
/unit-test
/integration-test
/explain-failure
/ci-gate
/explain-ci
```

### 9.5 Review 命令

```text
/open-pr
/summarize-pr
/ai-review
/check-tests
/check-spec-drift
review
request changes
approve
```

### 9.6 测试与发布命令

```text
/test-plan
/test-cases
/run-qa
/qa-pass
/qa-fail
/release-gate
/release-plan
/rollback-plan
/deploy-staging
/deploy-prod
```

### 9.7 运维与反馈命令

```text
/verify-prod
/diagnose
/rollback
/incident
/update-runbook
/final-summary
/followups
/update-rules
```

---

## 10. 仓库目录建议

```text
repo/
  AGENTS.md
  constitution.md
  CODEOWNERS
  CONTRIBUTING.md
  SECURITY.md

  .github/
    ISSUE_TEMPLATE/
      feature.yml
      bug.yml
      refactor.yml
      ops.yml
    PULL_REQUEST_TEMPLATE.md
    workflows/
      issue-command.yml
      spec.yml
      implement.yml
      ci.yml
      ai-review.yml
      release-gate.yml
      deploy.yml
    instructions/
      backend.instructions.md
      frontend.instructions.md
      testing.instructions.md
      security.instructions.md

  .continue/
    checks/
      security.md
      testing.md
      spec-drift.md
      migration.md
      observability.md

  .skills/
    clarify/
    spec/
    plan/
    tasks/
    implement/
    ai-review/
    test-plan/
    release-plan/
    diagnose/

  issues/
    ISSUE-123/
      issue.md
      issue_context.json
      issue_comments.txt
      spec.md
      plan.md
      tasks.md
      implementation_summary.md
      validation.md
      final-summary.md

  specs/
    ISSUE-123/
      spec.md
      arch.md
      plan.md
      tasks.md
      risk.md

  adr/
    ADR-001-example.md

  contracts/
    openapi/
    events/

  tests/
    test-plans/
    test-cases/
    regression/

  release/
    ISSUE-123/
      release.md
      rollout.md
      rollback.md
      release-gate-result.json

  ops/
    runbooks/
    alerts/
    dashboards/
    postmortems/
```

---

## 11. 角色口径

本文档统一使用中文角色名：

```text
产品经理
技术负责人
架构师
开发
测试
代码审查人
运维
SRE
安全负责人
事项负责人
AI Agent
自动化
```

工具名保留英文：

```text
GitHub
Spec Kit
AGENTS.md
Continue
Codex
Cline
Aider
OpenHands
OpenAPI
Pact
Testcontainers
GitHub Actions
Argo CD
OpenTelemetry
Grafana
Datadog
Sentry
```

---

## 12. 最小可行落地版本

第一阶段不要全做，先落地研发主链路：

```text
Issue
  -> /context
  -> /spec
  -> /plan
  -> /tasks
  -> /implement
  -> /open-pr
  -> /ci-gate
  -> /ai-review
  -> human review
  -> merge
```

第一阶段必须做：

```text
AGENTS.md
constitution.md
PR template
CODEOWNERS
GitHub Actions CI
Branch protection
Continue AI checks
Issue command workflow
Efficiency Center event collector
```

第二阶段补测试与发布：

```text
/test-plan
/test-cases
/qa-pass
/release-gate
/release-plan
/rollback-plan
/deploy-staging
/deploy-prod
```

第三阶段补运维与反馈：

```text
/verify-prod
/diagnose
/incident
/update-runbook
/final-summary
/followups
/update-rules
```

---

## 13. 结论

这套方案的本质是：

```text
用 Issue 作为研发任务入口；
用 Spec / Plan / Tasks 作为 AI 可执行上下文；
用 Agent 执行实现和检查；
用 CI Gate 保证研发交付物完整；
用 Release Gate 保证上线前所有卡点完成；
用效率中心沉淀所有工具动作和研发效率指标。
```

现成工具已经可以支撑大部分单点能力：

```text
IssueOps 命令入口       -> GitHub Actions / command action
规格驱动开发           -> GitHub Spec Kit
Agent 仓库规则          -> AGENTS.md
代码实现               -> Copilot / Codex / Cline / Aider / OpenHands
AI Review              -> Continue
CI 门禁                -> GitHub Actions + Required status checks
上线门禁               -> GitHub Environments / Deployment protection rules
观测与诊断             -> OpenTelemetry / Grafana / Datadog / Sentry
```

真正需要自建的是中间编排层：

```text
Issue Router
Command Dispatcher
Context Pack Builder
Gate Engine
Artifact Checker
Efficiency Center
Status Sync
```

这部分就是产品机会。现成工具负责“单点能力”，你要做的是把它们串成一条可治理、可度量、可复盘的 AI-Friendly Dev-Test-Ops 工作流。

[1]: https://github.blog/engineering/issueops-automate-ci-cd-and-more-with-github-issues-and-actions/?utm_source=chatgpt.com "IssueOps: Automate CI/CD (and more!) with GitHub Issues ..."
[2]: https://agents.md/?utm_source=chatgpt.com "AGENTS.md"
[3]: https://opentelemetry.io/docs/?utm_source=chatgpt.com "Documentation"
[4]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule?utm_source=chatgpt.com "Managing a branch protection rule"
[5]: https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments?utm_source=chatgpt.com "Deployments and environments"
[6]: https://developers.openai.com/codex/guides/agents-md?utm_source=chatgpt.com "Custom instructions with AGENTS.md – Codex"
[7]: https://github.com/?utm_source=chatgpt.com "GitHub · Change is constant. GitHub keeps you ahead. · GitHub"
[8]: https://docs.github.com/articles/about-status-checks?utm_source=chatgpt.com "About status checks"
[9]: https://docs.continue.dev/?utm_source=chatgpt.com "What is Continue? | Continue Docs"
