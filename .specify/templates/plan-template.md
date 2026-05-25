# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]

**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Language**: 正文描述使用中文；SDD、PoC、Spec Kit、API、contract、test、CI、PR
等特定名词保留惯用 English 用法。

**Note**: This template is filled in by the `/speckit-plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]

**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]

**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]

**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]

**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]

**Project Type**: [e.g., library/cli/web-service/mobile-app/compiler/desktop-app or NEEDS CLARIFICATION]

**PoC Location**: `demo/` (all runnable PoC implementation files, tests,
fixtures, contract examples, and local scripts MUST stay under this directory)

**API Contracts**: [contract files or boundary description, e.g., OpenAPI,
CLI schema, event schema, module interface, or N/A with rationale]

**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]

**Constraints**: [domain-specific constraints plus repository constraints:
implementation remains small/reviewable, runnable PoC files stay in `demo/`,
requirements have completed clarification, or NEEDS CLARIFICATION]

**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [ ] Clarification complete: no critical `NEEDS CLARIFICATION` item blocks planning
      or implementation; non-goals and scope boundaries are explicit.
- [ ] PoC boundary respected: every runnable implementation file, test, fixture,
      contract example, mock, and local script is planned under `demo/`.
- [ ] Simplicity justified: architecture is the smallest clear design that satisfies
      the spec; any extra dependency, abstraction, or layer has a stated reason.
- [ ] API contract explicit: every HTTP/CLI/event/file/module boundary has input,
      output, error semantics, and compatibility expectations documented.
- [ ] Automated test evidence planned: tests or justified alternative validation map
      to the user stories and include repeatable commands.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. All runnable PoC implementation files MUST stay under demo/.
  Documentation under specs/ and governance files under .specify/ are allowed
  outside demo/ because they are not PoC implementation files.
-->

```text
demo/
├── src/
├── tests/
│   ├── contract/
│   ├── integration/
│   └── unit/
├── contracts/
├── fixtures/
└── scripts/
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above. Explain any omitted demo/ subdirectory.]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., file outside demo/] | [current need] | [why demo/ placement is insufficient] |
| [e.g., additional framework/layer] | [specific problem] | [why direct/simple implementation is insufficient] |
