# Tasks Index

**Feature:** [FEATURE_ID] - [FEATURE_NAME]
**Created:** [DATE]
**Last Updated:** [DATE]

## Overview

This index provides a high-level view of all tasks for this feature, organized by phase and status.

## Progress Summary

- **Total Tasks:** [TOTAL]
- **Completed:** [COMPLETED] (✅)
- **In Progress:** [IN_PROGRESS] (🔄)
- **Pending:** [PENDING] (⬜)
- **Blocked:** [BLOCKED] (🚫)
- **Overall Progress:** [PERCENTAGE]%

---

## Phase 1: [PHASE_NAME]

### Status: [Not Started / In Progress / Completed]

| Task ID | Title | Status | Assignee | Est. Hours | Dependencies |
|---------|-------|--------|----------|------------|--------------|
| T1.1 | [Task Title] | ⬜ | [Name/TBD] | [Hours] | None |
| T1.2 | [Task Title] | 🔄 | [Name/TBD] | [Hours] | T1.1 |
| T1.3 | [Task Title] | ✅ | [Name/TBD] | [Hours] | T1.1 |

**Phase Progress:** [X]/[Y] tasks complete ([PERCENTAGE]%)

---

## Phase 2: [PHASE_NAME]

### Status: [Not Started / In Progress / Completed]

| Task ID | Title | Status | Assignee | Est. Hours | Dependencies |
|---------|-------|--------|----------|------------|--------------|
| T2.1 | [Task Title] | ⬜ | [Name/TBD] | [Hours] | T1.3 |
| T2.2 | [Task Title] | ⬜ | [Name/TBD] | [Hours] | T2.1 |

**Phase Progress:** [X]/[Y] tasks complete ([PERCENTAGE]%)

---

## Critical Path

The following tasks are on the critical path for this feature:

1. **T1.1** → [Task Title] (Estimated: [Hours]h)
2. **T1.3** → [Task Title] (Estimated: [Hours]h)
3. **T2.1** → [Task Title] (Estimated: [Hours]h)

**Critical Path Duration:** [TOTAL_HOURS] hours (~[DAYS] days)

---

## Blocked Tasks

| Task ID | Title | Blocked By | Reason | Resolution Plan |
|---------|-------|------------|--------|-----------------|
| [ID] | [Title] | [Dependency] | [Reason] | [Plan] |

---

## Completed Tasks

<details>
<summary>View completed tasks ([COUNT] total)</summary>

| Task ID | Title | Completed Date | Actual Hours |
|---------|-------|----------------|--------------|
| T1.3 | [Task Title] | [DATE] | [Hours] |

</details>

---

## Risk Assessment

### High Risk Tasks

Tasks that may require special attention or have higher complexity:

- **[Task ID]**: [Task Title] - [Risk Description]

### Dependencies on External Systems

Tasks that depend on external systems or third-party integrations:

- **[Task ID]**: [Task Title] - [External Dependency]

---

## Resource Allocation

### Estimated Effort by Role

| Role | Estimated Hours | % of Total |
|------|----------------|------------|
| Backend Developer | [Hours] | [%] |
| Frontend Developer | [Hours] | [%] |
| DevOps Engineer | [Hours] | [%] |
| QA Engineer | [Hours] | [%] |

### Team Capacity

- **Available Capacity:** [Hours/week]
- **Estimated Duration:** [Weeks]
- **Target Completion:** [DATE]

---

## Quality Gates

Each phase must pass these gates before proceeding:

### Phase 1
- [ ] All tasks completed
- [ ] Unit tests pass (≥80% coverage)
- [ ] Code review completed
- [ ] Documentation updated

### Phase 2
- [ ] All tasks completed
- [ ] Integration tests pass
- [ ] Performance benchmarks met
- [ ] Security review completed

---

## Task Details

For detailed information about each task, including implementation steps and validation checklists, see:

- Phase 1 Tasks: `./tasks/phase-1.md`
- Phase 2 Tasks: `./tasks/phase-2.md`
- [Additional phases as needed]

---

## Change Log

| Date | Change | Changed By |
|------|--------|------------|
| [DATE] | Initial task breakdown | [Name] |
| [DATE] | Added Phase 2 tasks | [Name] |

---

## Notes

### Assumptions
- [List key assumptions about this feature]

### Decisions Made
- [Record important decisions that affect task planning]

### Open Questions
- [List questions that need answers before certain tasks can start]

---

## RisoTech Enhancements

When `SPECIFY_RISOTECH_MODE=true` or `SPECIFY_VALIDATION_SUBTASKS=true`:

- Each task includes **validation sub-tasks** (unit tests, code review, documentation)
- Tasks are grouped by **story** when EPIC decomposition is used
- Progress tracking includes **validation checklist completion**
- Constitution compliance checks are integrated into task workflow

---

**Last Updated:** [DATE]
**Next Review:** [DATE]
