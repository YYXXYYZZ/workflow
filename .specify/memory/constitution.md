<!--
Sync Impact Report
Version change: template -> 1.0.0
Modified principles:
- Template principle 1 -> I. SDD PoC Workspace Scope
- Template principle 2 -> II. Clarification Before Implementation
- Template principle 3 -> III. Small, Clear, Reviewable Implementation
- Template principle 4 -> IV. Explicit API Contracts
- Template principle 5 -> V. Automated Test Evidence
Added sections:
- PoC Boundaries
- Development Workflow
Removed sections:
- None
Templates requiring updates:
- ✅ .specify/templates/plan-template.md
- ✅ .specify/templates/spec-template.md
- ✅ .specify/templates/tasks-template.md
- ✅ .specify/templates/checklist-template.md
- ✅ AGENTS.md
- ✅ README.md
- ✅ .specify/extensions/git/commands/*.md reviewed, no update needed
Follow-up TODOs:
- None
-->
# AiFlow SDD PoC Constitution

## Core Principles

### I. SDD PoC Workspace Scope
本仓库 MUST 作为 SDD PoC 工作区使用。所有 PoC 实现文件，包括 source code、
test、fixture、mock、contract 示例和运行脚本，MUST 保留在 `demo/` 目录内。
`specs/`、`.specify/`、`AGENTS.md`、`README.md` 等治理和文档文件可以保留在
仓库约定位置，但不得承载可运行 PoC 实现。这样可以把实验实现与 Spec Kit
治理资产清晰隔离，降低审查和清理成本。

### II. Clarification Before Implementation
任何需求进入 implementation 之前 MUST 先完成澄清。`spec.md` MUST 记录已澄清
的问题、范围边界、非目标、验收场景和仍未解决的 `NEEDS CLARIFICATION` 项。
存在未解决关键澄清项时，MUST 停止进入 `plan.md`、`tasks.md` 或代码实现。
该规则保证 PoC 验证的是明确需求，而不是实现阶段的猜测。

### III. Small, Clear, Reviewable Implementation
每个 PoC implementation MUST 保持小而清晰、可测试、易审查。默认选择能满足
当前 spec 的最简单架构，避免提前抽象、隐藏控制流和跨目录散落实现。新增模块、
依赖或架构层级 MUST 在 `plan.md` 的 Constitution Check 中说明必要性，并列出
被拒绝的更简单替代方案。该规则让 PoC 保持适合学习、复盘和快速迭代的形态。

### IV. Explicit API Contracts
涉及边界交互的 PoC MUST 优先定义明确 API 契约。HTTP、CLI、event、file 或
module boundary 都 MUST 在 `spec.md` 或 `contracts/` 中描述输入、输出、错误
语义和兼容性要求。实现和测试 MUST 以这些 contract 为准，而不是依赖隐式行为。
该规则让需求、实现和验证之间保持同一事实来源。

### V. Automated Test Evidence
PoC implementation MUST 配套自动化测试证据。至少要覆盖核心 user journey、
API contract 或关键边界条件；如果某项测试暂不适用，MUST 在 `tasks.md` 和
最终验证说明中记录原因与人工验证替代方式。测试任务 MUST 优先于对应实现任务
定义，并在实现完成后提供可复跑命令。该规则保证 PoC 的结论可以被复核。

## PoC Boundaries

所有后续文档描述 MUST 使用中文，特定名词保留惯用 English 用法，例如 SDD、
PoC、Spec Kit、API、contract、test、workflow、agent、CI、PR。文档 MUST 明确
区分 `specs/` 中的需求和计划、`.specify/` 中的治理模板、`demo/` 中的 PoC 实现。

允许的仓库边界：

- `demo/`: PoC source code、tests、fixtures、contracts、scripts 和本地运行资产。
- `specs/`: feature spec、plan、tasks、research、quickstart 和 feature 文档。
- `.specify/`: Spec Kit 模板、脚本、constitution 和扩展配置。
- 根目录: `README.md`、`AGENTS.md` 等仓库级说明。

新增可运行文件或测试文件放在 `demo/` 之外时，MUST 视为 constitution 违规，除非
该文件属于 Spec Kit 自身治理资产并在审查中说明。

## Development Workflow

标准流程 MUST 按 clarify -> specify -> plan -> tasks -> implement -> validate 推进。
每次进入下一阶段前，产物 MUST 通过上一阶段的 constitution gate：

- Clarify gate: 无关键未解决需求问题，非目标和边界清楚。
- Spec gate: user stories、acceptance scenarios、requirements 和 success criteria 可测。
- Plan gate: implementation path 限定在 `demo/`，架构选择简单且 contract 清楚。
- Tasks gate: 测试、contract、实现、验证任务可追踪到 user story。
- Validate gate: 自动化测试或明确记录的替代验证已经执行并保留命令/结果。

任何 gate 失败时，MUST 回到相应文档修正，而不是直接补代码绕过。

## Governance

本 constitution 优先于仓库内其他流程描述。任何冲突的 template、plan、tasks 或
agent 指令 MUST 以本文件为准并同步修订。

Amendment procedure:

- 修改 constitution MUST 同时更新受影响的 `.specify/templates/`、`AGENTS.md` 和
  README 级说明。
- 每次修改 MUST 在文件顶部 Sync Impact Report 中记录版本变化、原则变化、模板
  同步状态和遗留 TODO。
- 版本号遵循 Semantic Versioning：MAJOR 用于删除或重定义核心原则；MINOR 用于
  新增原则、章节或实质扩展治理要求；PATCH 用于措辞澄清、错别字和非语义修订。
- 每个 feature 的 `plan.md` MUST 执行 Constitution Check；每次 code review
  MUST 检查 PoC 边界、澄清记录、contract 和 test evidence。

**Version**: 1.0.0 | **Ratified**: 2026-05-25 | **Last Amended**: 2026-05-25
