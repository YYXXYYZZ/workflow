# AI-Friendly Dev-Test-Ops Workflow

## 流程总览

**Dev → PR → CI → Test → Release → Ops → Feedback**

所有阶段动作统一上报到独立的 **Efficiency Center / 效率中心**。效率中心不是主流程阶段，而是横向事件中心，单独成篇说明。

---

## 01. Issue Intake / 研发任务入口

| 干什么 | 谁 | 位置 | 命令 | 工具支持 | 说明 |
|---|---|---|---|---|---|
| 创建研发 Issue | 产品经理 / 技术负责人 / 开发 | Issue | create issue | GitHub Issues / Jira / Linear | Feature / Bug / Refactor / TechDebt |
| 补充上下文 | 开发 + AI Agent | Issue | /clarify | GitHub Actions + LLM Agent | AI 补边界、复现步骤、验收条件 |
| 任务分流 | 技术负责人 / 自动化 | 工具 | /triage | Projects / Labels / Actions | 设置负责人、优先级、里程碑 |
| 上报效率中心 | 自动化 | 工具 | auto report | Webhook / Actions | 记录 Issue 创建和分流动作 |

**阶段产物**：issue.md / issue_context.json / 负责人 / 优先级 / labels

↓ 进入 **02. Repo Rules / 仓库规则**

---

## 02. Repo Rules / 仓库规则

| 干什么 | 谁 | 位置 | 命令 | 工具支持 | 说明 |
|---|---|---|---|---|---|
| 定义 Agent 规则 | 技术负责人 / 架构师 | 仓库 | /init-agents | AGENTS.md | 安装、测试、禁止事项 |
| 定义项目原则 | 技术负责人 / 架构师 | 仓库 | /init-constitution | Spec Kit constitution | 技术原则、质量底线、约束 |
| 定义合并门禁 | 技术负责人 / 运维 | 工具 | /init-gates | Branch protection | CI green + required review |
| 上报效率中心 | 自动化 | 工具 | auto report | Webhook / Actions | 记录规则初始化和变更 |

**阶段产物**：AGENTS.md / constitution.md / PR template / CODEOWNERS / branch protection

↓ 进入 **03. Spec / 技术规格**

---

## 03. Spec / 技术规格

| 干什么 | 谁 | 位置 | 命令 | 工具支持 | 说明 |
|---|---|---|---|---|---|
| 生成技术规格 | AI Agent 起草，技术负责人审核 | 仓库 | /spec | GitHub Spec Kit | 输出 spec.md |
| 明确非目标 | AI Agent 起草，技术负责人审核 | 仓库 | /clarify-spec | Spec Kit + 模板 | 明确不做什么 |
| 校验规格覆盖 Issue | 自动化 + 技术负责人 | 工具 | /check-spec | 轻量自建 Gate | 检查是否覆盖验收标准 |
| 上报效率中心 | 自动化 | 工具 | auto report | Webhook / Actions | 记录 spec 生成和审核结果 |

**阶段产物**：spec.md / clarified scope / open questions / spec approval

↓ 进入 **04. Plan / 技术方案**

---

## 04. Plan / 技术方案

| 干什么 | 谁 | 位置 | 命令 | 工具支持 | 说明 |
|---|---|---|---|---|---|
| 生成实现计划 | AI Agent 起草，技术负责人审核 | 仓库 | /plan | GitHub Spec Kit | 输出 plan.md |
| 设计架构变更 | AI Agent 起草，架构师审核 | 仓库 | /arch | ADR / C4 / 自定义 Agent | 输出 arch.md / ADR.md |
| 定义接口/契约 | AI Agent 起草，开发审核 | 仓库 | /contract | OpenAPI / AsyncAPI / Pact | openapi.yaml / event schema |
| 风险评估 | AI Agent 起草，人确认 | 仓库 | /risk | 自定义模板 | 数据迁移、兼容性、性能、安全 |
| 上报效率中心 | 自动化 | 工具 | auto report | Webhook / Actions | 记录方案生成和风险结果 |

**阶段产物**：plan.md / arch.md / ADR.md / openapi.yaml / risk.md

↓ 进入 **05. Tasks / 任务拆解**

---

## 05. Tasks / 任务拆解

| 干什么 | 谁 | 位置 | 命令 | 工具支持 | 说明 |
|---|---|---|---|---|---|
| 拆任务清单 | AI Agent 起草，开发确认 | 仓库 | /tasks | GitHub Spec Kit | 输出 tasks.md |
| 标记依赖关系 | AI Agent + 开发 | 仓库 | /order-tasks | 轻量自建 | 标记串行 / 并行任务 |
| 标记测试任务 | AI Agent + 测试 / 开发 | 仓库 | /test-tasks | Spec Kit + 模板 | 每个功能任务对应测试任务 |
| 上报效率中心 | 自动化 | 工具 | auto report | Webhook / Actions | 记录任务拆解结果 |

**阶段产物**：tasks.md / task dependencies / test tasks / implementation-ready

↓ 进入 **06. Implement / 代码实现**

---

## 06. Implement / 代码实现

| 干什么 | 谁 | 位置 | 命令 | 工具支持 | 说明 |
|---|---|---|---|---|---|
| 分配给 Coding Agent | 技术负责人 / 开发 | Issue | assign to agent | Copilot coding agent / OpenHands | Issue 分配给 Agent |
| 创建分支 | 自动化 / AI Agent | 工具 | /start-dev | GitHub / Git / Worktree | branch: issue-123-xxx |
| 实现代码 | AI Agent 主写，开发兜底 | 仓库 | /implement | Copilot / Codex / Cline / Aider | 按 tasks.md 改代码 |
| 补测试 | AI Agent 起草，开发确认 | 仓库 | /add-tests | Cline / Aider / test runner | unit / integration tests |
| 上报效率中心 | 自动化 | 工具 | auto report | Agent logs / Webhook | 记录 Agent 操作、耗时、失败次数 |

**阶段产物**：code changes / tests / commits / implementation_summary.md / draft branch

↓ 进入 **07. Local Validate / 本地验证**

---

## 07. Local Validate / 本地验证

| 干什么 | 谁 | 位置 | 命令 | 工具支持 | 说明 |
|---|---|---|---|---|---|
| 跑 lint/typecheck | 自动化 / AI Agent | 本地 | /validate | Cline / Aider / npm scripts | pnpm lint && pnpm typecheck |
| 跑单元测试 | 自动化 / AI Agent | 本地 | /unit-test | Cline / Aider / test runner | pnpm test |
| 跑集成/契约测试 | 自动化 | 本地 | /integration-test | Testcontainers / Pact | DB / Redis / API contract |
| 解释失败 | AI Agent | 本地 | /explain-failure | Cline / Aider / logs | 根据报错继续修 |
| 上报效率中心 | 自动化 | 工具 | auto report | Test report collector | 记录测试耗时、失败类型、修复次数 |

**阶段产物**：validation.md / local test report / fixed failures

↓ 进入 **08. Open PR / 创建 PR**

---

## 08. Open PR / 创建 PR

| 干什么 | 谁 | 位置 | 命令 | 工具支持 | 说明 |
|---|---|---|---|---|---|
| 创建 PR | AI Agent / 自动化 | 工具 | /open-pr | Copilot agent / GitHub CLI | PR 关联 Issue 和 spec |
| 生成 PR 描述 | AI Agent | 工具 | /summarize-pr | Copilot / 自定义 Agent | Summary / tests / risk |
| 请求 Review | 自动化 | 工具 | request review | CODEOWNERS / GitHub reviewers | 自动找代码审查人 |
| 上报效率中心 | 自动化 | 工具 | auto report | GitHub Webhook | 记录 PR 创建、Review 分配 |

**阶段产物**：Pull Request / PR description / linked issue / linked spec

↓ 进入 **09. CI Gate / CI 卡点**

---

## 09. CI Gate / CI 卡点

| 干什么 | 谁 | 位置 | 命令 | 工具支持 | 说明 |
|---|---|---|---|---|---|
| 检查前置交付物 | 自动化 | 工具 | /ci-gate | GitHub Actions / Gate Engine | spec、plan、tasks、tests、PR 描述必须齐 |
| 自动跑 CI | 自动化 | 工具 | auto on PR | GitHub Actions / GitLab CI | push / PR 自动触发 |
| 质量检查 | 自动化 | 工具 | lint / test / build | CI pipeline | required checks |
| 安全扫描 | 自动化 | 工具 | security scan | CodeQL / Trivy / Dependabot | 高危阻断 |
| 解释 CI 失败 | AI Agent | 工具 | /explain-ci | Copilot / Cline / 自定义 Agent | 给修复建议 |
| 上报效率中心 | 自动化 | 工具 | auto report | CI Webhook / Workflow logs | 记录 CI 卡点、失败原因、耗时 |

**CI Gate 必须满足**：

- issue_context.json 存在
- spec.md 存在并 approved
- plan.md 存在
- tasks.md 存在
- implementation_summary.md 存在
- tests 已新增或说明无需新增
- PR description 完整
- lint / test / build / security 全部通过

**阶段产物**：ci-summary.json / coverage report / security report / build artifact / ci-gate-result.json

↓ 进入 **10. AI Review / AI 审查**

---

## 10. AI Review / AI 审查

| 干什么 | 谁 | 位置 | 命令 | 工具支持 | 说明 |
|---|---|---|---|---|---|
| 规则化 AI Review | AI Agent | 工具 | /ai-review | Continue | `.continue/checks/*.md` 作为 status check |
| 检查测试缺口 | AI Agent | 工具 | /check-tests | Continue / custom check | 改了逻辑但没测，标红 |
| 检查 Spec Drift | AI Agent | 工具 | /check-spec-drift | Continue + 轻量自建 | 实现是否偏离 spec.md |
| 生成修复建议 | AI Agent | 工具 | auto | Continue | red check + suggested diff |
| 上报效率中心 | 自动化 | 工具 | auto report | Review Webhook | 记录 AI review 命中问题和修复率 |

**阶段产物**：AI status checks / review.json / suggested diff / risk notes

↓ 进入 **11. Human Review / 人工审查**

---

## 11. Human Review / 人工审查

| 干什么 | 谁 | 位置 | 命令 | 工具支持 | 说明 |
|---|---|---|---|---|---|
| 审代码正确性 | 代码审查人 / 技术负责人 | 工具 | review | GitHub PR Review | 看 diff、架构、边界、异常处理 |
| 审风险和回滚 | 代码审查人 / 技术负责人 | 工具 | review risk | PR checklist | 兼容性、数据、安全、回滚 |
| 要求修改 | 代码审查人 | 工具 | request changes | GitHub Review | AI Agent 或开发继续修 |
| 批准合并 | 代码审查人 / 技术负责人 | 工具 | approve | Branch protection | 人最终负责 |
| 上报效率中心 | 自动化 | 工具 | auto report | GitHub Review Webhook | 记录 Review 耗时、返工次数 |

**阶段产物**：review comments / approval / requested changes / merge decision

↓ 进入 **12. Merge / 合并**

---

## 12. Merge / 合并

| 干什么 | 谁 | 位置 | 命令 | 工具支持 | 说明 |
|---|---|---|---|---|---|
| 检查合并条件 | 自动化 | 工具 | merge gate | Branch protection / Merge queue | CI + AI checks + human approval |
| 合并 PR | 人 / 自动化 | 工具 | merge | GitHub merge / auto-merge | squash / merge queue |
| 关闭研发 Issue | 自动化 | Issue | auto close | GitHub linked issue | Closes #123 |
| 生成研发总结 | AI Agent | 仓库 | /summary | 自定义 Agent | final-summary.md |
| 上报效率中心 | 自动化 | 工具 | auto report | GitHub Webhook | 记录合并、关闭、总结 |

**阶段产物**：merged PR / closed dev issue / final-summary.md / follow-up issues

↓ 进入 **13. Test / QA 验收**

---

## 13. Test / QA 验收

| 干什么 | 谁 | 位置 | 命令 | 工具支持 | 说明 |
|---|---|---|---|---|---|
| 生成测试计划 | AI Agent 起草，测试审核 | 仓库 | /test-plan | 自定义 Agent / Test template | test-plan.md |
| 生成测试用例 | AI Agent 起草，测试补充 | 仓库 | /test-cases | TestRail / Zephyr / Xray / 自建 | 覆盖 AC、边界、回归场景 |
| 执行测试 | 测试 + 自动化 | 工具 | /run-qa | Playwright / Cypress / Test platform | 自动化 + 手工探索测试 |
| 验收通过/打回 | 测试 / 产品经理 | 工具 | /qa-pass /qa-fail | QA board / Bug tracker | 失败创建 bug issue |
| 上报效率中心 | 自动化 | 工具 | auto report | QA Webhook / Test report | 记录用例数、失败数、缺陷分布 |

**阶段产物**：test-plan.md / test-cases.md / regression-scope.md / qa-report.md / bug issues / qa-signoff

↓ 进入 **14. Release Gate / 上线卡点**

---

## 14. Release Gate / 上线卡点

| 干什么 | 谁 | 位置 | 命令 | 工具支持 | 说明 |
|---|---|---|---|---|---|
| 检查所有前置完成 | 自动化 | 工具 | /release-gate | GitHub Environments / Gate Engine | 前面所有交付物必须完成 |
| 生成发布计划 | AI Agent 起草，运维/技术负责人审核 | 仓库 | /release-plan | Release template | release.md |
| 生成回滚计划 | AI Agent 起草，运维审核 | 仓库 | /rollback-plan | Runbook / CD history | rollback.md |
| 发布审批 | 技术负责人 / 运维 / 产品经理 | 工具 | approve release | GitHub Environment reviewers | 人批准后才能部署生产 |
| 上报效率中心 | 自动化 | 工具 | auto report | Deployment Webhook | 记录上线卡点、审批、阻断原因 |

**Release Gate 必须满足**：

- dev issue closed
- PR merged
- CI Gate passed
- AI Review passed
- Human Review approved
- QA passed
- release.md 存在
- rollback.md 存在
- observability checklist 完成
- owner approval 完成

**阶段产物**：release-gate-result.json / release.md / rollback.md / approval record

↓ 进入 **15. Deploy / 部署**

---

## 15. Deploy / 部署

| 干什么 | 谁 | 位置 | 命令 | 工具支持 | 说明 |
|---|---|---|---|---|---|
| 部署 Staging | 自动化 | 环境 | /deploy-staging | GitHub Actions / Argo CD | staging smoke |
| 部署 Production | 人批准，自动化执行 | 环境 | /deploy-prod | CD / Environments / Feature flag | 灰度发布 |
| 记录部署结果 | 自动化 | 工具 | auto | CD report | deploy-report.json |
| 上报效率中心 | 自动化 | 工具 | auto report | CD Webhook / Deploy logs | 记录部署耗时、版本、环境、结果 |

**阶段产物**：deploy-report.json / deployed version / rollout status

↓ 进入 **16. Ops / 线上验证**

---

## 16. Ops / 线上验证

| 干什么 | 谁 | 位置 | 命令 | 工具支持 | 说明 |
|---|---|---|---|---|---|
| 检查核心指标 | 自动化 + SRE | 工具 | /verify-prod | Grafana / Datadog / Sentry | error rate / latency / traffic |
| 异常诊断 | AI Agent | 工具 | /diagnose | Logs / Traces / Metrics | 关联 recent release |
| 回滚/事故处理 | SRE / 运维 / 技术负责人 | 工具 | /rollback /incident | Rollback pipeline / PagerDuty | 人判断，自动化执行 |
| 更新 Runbook | AI Agent 起草，SRE 审核 | 仓库 | /update-runbook | ops/runbooks | 固化处理流程 |
| 上报效率中心 | 自动化 | 工具 | auto report | Observability Webhook | 记录线上指标、告警、回滚、事故 |

**阶段产物**：ops-report.md / metrics-check.md / diagnosis.md / incident.md / rollback-report.md / runbook update

↓ 进入 **17. Feedback / 反馈闭环**

---

## 17. Feedback / 反馈闭环

| 干什么 | 谁 | 位置 | 命令 | 工具支持 | 说明 |
|---|---|---|---|---|---|
| 生成最终总结 | AI Agent | 仓库 | /final-summary | Issue / PR / QA / Ops reports | final-summary.md |
| 创建后续任务 | AI Agent 起草，人确认 | Issue | /followups | GitHub Issues / Jira | 技术债、测试补强、监控补强 |
| 反哺规则 | AI Agent 建议，人审核 | 仓库 | /update-rules | AGENTS.md / checks / runbook | 重复问题写进规则 |
| 上报效率中心 | 自动化 | 工具 | auto report | Efficiency Center | 汇总完整交付链路指标 |

**阶段产物**：final-summary.md / follow-up issues / updated AGENTS.md / updated checks / updated runbook / efficiency report

↓ 反哺 **01. Issue Intake / 研发任务入口**

## Efficiency Center / 效率中心

效率中心不放在主流程里。它是主流程之外的横向事件中心，接收 Issue、PR、CI、Review、QA、Deploy、Ops、Feedback 等所有工具动作上报。

| 干什么 | 谁 | 位置 | 命令 | 工具支持 | 说明 |
|---|---|---|---|---|---|
| 收集所有工具动作 | 自动化 | 工具 | auto report | GitHub Webhook / Actions | issue、PR、CI、Review、Deploy 都上报 |
| 记录人和 AI 的操作 | 自动化 | 工具 | auto audit | GitHub API / Agent logs | 谁触发、何时触发、结果如何 |
| 汇总阶段交付物 | 自动化 + AI | 工具 | /sync-status | 效率中心 / 数据库 / Dashboard | 每个 Issue 的进度、产物、卡点 |
| 生成效率指标 | AI + 自动化 | 工具 | /metrics | OTel / BI / Dashboard | Lead time、返工次数、CI失败率、Review耗时 |

上报事件格式：

```json
{
  "issue_id": "",
  "stage": "",
  "command": "",
  "actor_type": "",
  "actor": "",
  "tool": "",
  "status": "",
  "artifacts": [],
  "started_at": "",
  "finished_at": "",
  "error": ""
}
```

“效率中心”最好不要只是日志库，而是一个**研发过程事件中心**：所有工具动作都用统一事件格式上报，再做 Issue 维度、阶段维度、角色维度、Agent 维度的统计。OpenTelemetry 的思路可以借用，因为它本身就是把 logs、metrics、traces 作为可关联的信号来采集和分析。([opentelemetry.io][2])