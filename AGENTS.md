<!-- SPECKIT START -->
Current Spec Kit plan: specs/001-local-task-api/plan.md
Current feature spec: specs/001-local-task-api/spec.md
PoC implementation root: demo/
Tech stack for this plan: Python 3.12 via uv, FastAPI, SQLite, pytest
<!-- SPECKIT END -->

## 仓库治理规则

- 本仓库是 SDD PoC 工作区；所有 PoC source code、test、fixture、mock、contract 示例和本地运行脚本必须放在 `demo/`。
- 需求必须先澄清再进入 implementation；关键 `NEEDS CLARIFICATION` 未解决时，不要继续写 plan、tasks 或代码。
- implementation 必须保持小而清晰、可测试、易审查，优先选择满足当前 spec 的最简单架构。
- 涉及边界交互时，先写清 API / contract，再让实现和测试对齐 contract。
- 后续文档描述使用中文；SDD、PoC、Spec Kit、API、contract、test、workflow、agent、CI、PR 等特定名词保留惯用 English 用法。
