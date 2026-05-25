# Feature Specification: Local Task Management API

**Feature Branch**: `001-local-task-api`

**Created**: 2026-05-25

**Status**: Draft

**Input**: User description: "在 demo/ 目录内构建一个本地任务管理 API。用户可以创建任务、查看任务列表、更新任务状态、删除任务。一个任务包含 title、description、status、created_at、updated_at。status 只能是 todo、doing、done。本 PoC 不包含登录、多用户支持、前端页面、通知和部署。"

**Language**: 正文描述使用中文；SDD、PoC、Spec Kit、API、contract、test、CI、PR
等特定名词保留惯用 English 用法。

## Clarifications *(mandatory before planning/implementation)*

### Completed Clarifications

- 2026-05-25: PoC 范围 -> 仅构建本地任务管理 API，不包含登录、多用户支持、前端页面、通知和部署。
- 2026-05-25: 任务状态范围 -> `status` 只能是 `todo`、`doing`、`done`。
- 2026-05-25: PoC 文件边界 -> 后续 source code、test、fixture、mock、contract 示例和本地运行脚本必须放在 `demo/`。

### Open Questions

- None.

### Session 2026-05-25

- Q: 数据持久化预期是什么？ → A: Local file persistence：任务持久化到本地文件，重启后仍可读取。
- Q: API contract surface 采用什么形式？ → A: REST-style HTTP JSON，包含 `POST /tasks`、`GET /tasks`、`PATCH /tasks/{id}/status`、`DELETE /tasks/{id}`。
- Q: 错误响应格式是什么？ → A: Unified error object：错误响应统一为 `{ "error": { "code": "...", "message": "..." } }`。
- Q: 参数校验策略是什么？ → A: Strict profile：trim `title`/`description`；`title` 长度 1-100；`description` 最长 1000；reject unknown fields 和系统维护字段。
- Q: 测试覆盖范围是什么？ → A: Core happy-path only：自动化测试只覆盖创建、列表、更新、删除的成功路径。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 创建任务 (Priority: P1)

用户可以通过本地任务管理 API 创建一个任务，用于记录待处理事项和描述信息。

**Why this priority**: 创建任务是任务管理的入口；没有任务创建，列表、状态更新和删除都没有可操作对象。

**Independent Test**: 可以独立验证用户提交任务信息后，系统返回一个包含完整任务字段的新任务，并且该任务可以被后续列表查询发现。

**Acceptance Scenarios**:

1. **Given** 当前没有任务，**When** 用户创建一个包含 `title` 和 `description` 的任务且未指定 `status`，**Then** 系统创建新任务，返回稳定任务标识，并将 `status` 设为 `todo`。
2. **Given** 用户准备创建任务，**When** 用户提交空白 `title`，**Then** 系统拒绝创建并返回可理解的校验错误，任务列表不新增记录。
3. **Given** 用户准备创建任务，**When** 用户提交 `status` 为 `todo`、`doing` 或 `done`，**Then** 系统创建任务并保留用户选择的合法状态。
4. **Given** 用户创建任务后重启本地 API，**When** 用户再次查看任务列表，**Then** 已创建且未删除的任务仍然可见。

---

### User Story 2 - 查看任务列表 (Priority: P1)

用户可以查看当前本地 PoC 中已经创建且未删除的任务列表，以了解待办事项的整体状态。

**Why this priority**: 查看任务列表是确认创建结果和管理任务状态的基础能力，必须与创建任务一起形成最小可用闭环。

**Independent Test**: 可以独立验证空列表、单个任务列表和多个任务列表都返回一致、完整的任务字段。

**Acceptance Scenarios**:

1. **Given** 当前没有任务，**When** 用户查看任务列表，**Then** 系统返回空列表而不是错误。
2. **Given** 当前存在多个未删除任务，**When** 用户查看任务列表，**Then** 系统返回所有未删除任务，每个任务都包含 `title`、`description`、`status`、`created_at` 和 `updated_at`。
3. **Given** 一个任务已经被删除，**When** 用户查看任务列表，**Then** 该任务不再出现在列表中。

---

### User Story 3 - 更新任务状态 (Priority: P2)

用户可以将一个已有任务的状态更新为 `todo`、`doing` 或 `done`，用于表达任务推进情况。

**Why this priority**: 状态更新让任务从静态记录变成可管理工作项，是任务管理 API 的核心行为之一。

**Independent Test**: 可以独立验证指定任务从一个合法状态变为另一个合法状态，并且非法状态不会改变任务。

**Acceptance Scenarios**:

1. **Given** 一个任务当前状态为 `todo`，**When** 用户将状态更新为 `doing`，**Then** 系统保存新状态并更新 `updated_at`。
2. **Given** 一个任务已经存在，**When** 用户将状态更新为 `blocked`，**Then** 系统拒绝更新并保持原状态不变。
3. **Given** 用户指定的任务不存在或已删除，**When** 用户请求更新状态，**Then** 系统返回未找到结果且不创建新任务。

---

### User Story 4 - 删除任务 (Priority: P3)

用户可以删除不再需要的任务，使其不再出现在任务列表中，也不能继续被更新。

**Why this priority**: 删除任务用于清理本地 PoC 数据，但它依赖已有任务对象，优先级低于创建、查看和状态更新。

**Independent Test**: 可以独立验证删除已有任务后，列表不再返回该任务，后续更新同一任务会得到未找到结果。

**Acceptance Scenarios**:

1. **Given** 一个任务已经存在，**When** 用户删除该任务，**Then** 系统确认删除，任务列表不再包含该任务。
2. **Given** 一个任务已经被删除，**When** 用户再次删除或更新该任务，**Then** 系统返回未找到结果且不影响其他任务。

### Edge Cases

- 用户提交空白或仅包含空格的 `title`。
- 用户提交不属于 `todo`、`doing`、`done` 的 `status`。
- 用户更新或删除不存在的任务。
- 用户删除任务后再次查看列表或尝试更新该任务。
- 用户未提供 `description` 或提供空 `description`。
- 用户尝试提供或覆盖系统维护的 `created_at`、`updated_at`。
- 用户提交超过长度限制的 `title` 或 `description`。
- 用户提交 contract 未定义的未知字段。
- 当前没有任何任务时查看任务列表。
- 本地持久化文件不存在时启动 API。
- 本地持久化文件包含无法识别的数据时启动 API。
- API 返回参数校验错误、未找到错误或本地持久化错误时，错误响应结构不一致。

### Non-Goals

- 不包含登录、鉴权或用户身份管理。
- 不包含多用户隔离、团队协作或权限模型。
- 不包含前端页面、移动端页面或可视化管理界面。
- 不包含通知、提醒、订阅或消息推送。
- 不包含部署、托管环境、生产运维或线上发布流程。
- 不包含任务搜索、筛选、排序自定义、分页、标签、优先级、截止日期或评论。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 系统 MUST 允许用户创建任务。
- **FR-002**: 系统 MUST 为每个任务提供稳定任务标识，以便后续更新状态和删除。
- **FR-003**: 创建任务时，`title` MUST 为必填且不能是空白文本。
- **FR-004**: 创建任务时，`description` MAY 为空；为空时任务仍然可以创建。
- **FR-005**: 创建任务时，`status` MUST 只能是 `todo`、`doing`、`done`；未提供时 MUST 默认为 `todo`。
- **FR-006**: 系统 MUST 为任务维护 `created_at` 和 `updated_at`，创建时两者均有值且表示任务创建时间。
- **FR-007**: 系统 MUST 允许用户查看所有未删除任务的列表。
- **FR-008**: 任务列表中的每个任务 MUST 包含稳定任务标识、`title`、`description`、`status`、`created_at` 和 `updated_at`。
- **FR-009**: 系统 MUST 允许用户仅更新已有任务的 `status`，并在成功更新后改变 `updated_at`，保持 `created_at` 不变。
- **FR-010**: 系统 MUST 拒绝非法 `status`，并保证失败的状态更新不会改变原任务。
- **FR-011**: 系统 MUST 允许用户删除已有任务；删除后该任务 MUST 不再出现在任务列表中。
- **FR-012**: 系统 MUST 对不存在或已删除任务的更新、删除请求返回明确的未找到结果，且不影响其他任务。
- **FR-013**: 系统 MUST 在校验失败时返回可理解的错误信息，并保证失败操作不创建、不更新、不删除任务。
- **FR-014**: 系统 MUST 在本 PoC 范围内不要求登录、多用户配置、前端页面、通知配置或部署环境。
- **FR-015**: 系统 MUST 将任务持久化到本地文件，并在本地 API 重启后保留已创建且未删除的任务。
- **FR-016**: 系统 MUST 通过 REST-style HTTP JSON contract 暴露创建任务、查看任务列表、更新任务状态和删除任务操作。
- **FR-017**: 系统 MUST 对所有失败响应使用统一错误对象，格式为 `{ "error": { "code": "...", "message": "..." } }`。
- **FR-018**: 系统 MUST 在写入前 trim `title` 和 `description`，并要求 trim 后的 `title` 长度为 1-100 个字符、`description` 长度不超过 1000 个字符。
- **FR-019**: 系统 MUST 拒绝 contract 未定义的未知输入字段，以及用户提交的系统维护字段，包括稳定任务标识、`created_at` 和 `updated_at`。

### API / Contract Requirements *(include when feature crosses a boundary)*

- **AC-001**: 本地任务管理 API contract MUST 使用 REST-style HTTP JSON，并覆盖 `POST /tasks`、`GET /tasks`、`PATCH /tasks/{id}/status`、`DELETE /tasks/{id}` 四类操作。
- **AC-002**: Contract MUST 定义每类操作的 HTTP method、path、JSON 输入字段、JSON 输出字段、成功结果、校验错误、未找到结果和无副作用失败语义。
- **AC-003**: Contract MUST 明确 `status` 允许值、默认值、非法值处理方式，以及 `created_at`、`updated_at` 的维护规则。
- **AC-004**: Contract examples、fixtures 或 executable checks 如果属于 PoC 可运行资产，MUST 放在 `demo/`；`specs/` 只保存 feature 文档和设计说明。
- **AC-005**: Contract MUST 明确本地文件持久化的重启后读取预期，以及持久化文件缺失或数据无法识别时的失败语义。
- **AC-006**: Contract MUST 为参数校验错误、未找到错误和本地持久化错误定义稳定的 `error.code` 与用户可理解的 `error.message`。
- **AC-007**: Contract MUST 包含 strict validation examples，覆盖 trim、长度限制、非法 `status`、未知字段和系统维护字段输入。
- **AC-008**: 本轮自动化 test scope MUST 覆盖同一本地 API 会话内 `POST /tasks`、`GET /tasks`、`PATCH /tasks/{id}/status`、`DELETE /tasks/{id}` 的成功路径；重启后持久化读取、失败路径和 strict validation examples MUST 在 contract 中定义，但不要求本轮自动化测试全部覆盖。

### Key Entities *(include if feature involves data)*

- **Task**: 用户创建和管理的本地工作项。关键属性包括稳定任务标识、`title`、`description`、`status`、`created_at`、`updated_at`。`title` trim 后长度为 1-100 个字符，`description` trim 后长度不超过 1000 个字符，`status` 只能是 `todo`、`doing`、`done`。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 用户按照 contract 完成创建任务、查看列表、更新状态、删除任务的完整核心流程用时不超过 2 分钟。
- **SC-002**: 在 PoC 验收中，新创建任务在本地 API 重启后 100% 仍可以从任务列表中看到。
- **SC-003**: 对 `todo`、`doing`、`done` 之外状态值的尝试，100% 被拒绝且不会改变已有任务。
- **SC-004**: 删除成功的任务在 100% 的删除场景中不再出现在任务列表中，且不能再被更新。
- **SC-005**: PoC 验收可以完全在本地完成，且不需要登录、多用户设置、前端页面、通知配置或部署步骤。
- **SC-006**: 本轮自动化测试 100% 覆盖创建、查看列表、更新状态、删除任务四个成功路径。
- **SC-007**: 参数校验、错误响应和持久化异常的 contract examples 100% 明确预期行为，但不要求本轮自动化测试全部覆盖。

## Assumptions

- 本 PoC 的目标用户是本地运行和验证 API contract 的开发者或技术评审者。
- 本轮 PoC 使用本地文件持久化任务数据，并要求验证本地 API 重启后的任务保留行为。
- `title` 是用户可读任务名称，因此作为必填字段；`description` 可以为空文本；两者写入前都会进行 trim。
- 用户不需要直接设置 `created_at`、`updated_at`；这两个字段由系统根据任务创建和更新行为维护。
- 列表只需要覆盖当前未删除任务；搜索、筛选、分页和排序自定义不在本轮范围内。
- 本轮测试覆盖采用 core happy-path only；失败路径和 strict validation 仍需写清 contract examples，后续可按风险追加自动化测试。
