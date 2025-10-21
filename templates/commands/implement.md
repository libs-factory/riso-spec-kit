---
description: Execute the implementation plan by processing and executing all tasks defined in tasks.md
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## MANDATORY COMPLIANCE REQUIREMENTS

**ABSOLUTE PROCESS ADHERENCE**: Do NOT assume or independently decide to change the process. All steps in "execution flow" below must be executed completely and in the exact order specified.

**MANDATORY TODO LIST**: Before starting execution, AI MUST create a TODO list based on the items in "execution flow" to ensure no step is missed.

## Follow this execution flow:

1. Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute.

2. **Check for story-scoped implementation** (RisoTech Enhancement):

   If `SPECIFY_RISOTECH_MODE=true` or `SPECIFY_EPIC_DECOMPOSITION=true`:

   a. Parse user input for `--story US-###` argument

   b. **If `--story US-###` provided**:
      - Load story from `FEATURE_DIR/stories/backlog.json` (if exists)
      - Verify story status is READY or IN_PROGRESS
      - If status is DRAFT or BLOCKED → ERROR with details
      - Check story dependencies are complete
      - If dependencies incomplete → ERROR "Cannot implement: dependencies incomplete"
      - Set implementation scope to this story only
      - Mark story as IN_PROGRESS (if was READY)
      - Continue to step 3 with single-story context

   c. **If no `--story` argument**:
      - Check if epic-breakdown.md exists
      - If EPIC exists → Load all stories, implement in priority order
      - If no EPIC → Standard full-feature implementation
      - Continue to step 3 with full-feature context

3. **Check checklists status** (if FEATURE_DIR/checklists/ exists):
   - Scan all checklist files in the checklists/ directory
   - For each checklist, count:
     * Total items: All lines matching `- [ ]` or `- [X]` or `- [x]`
     * Completed items: Lines matching `- [X]` or `- [x]`
     * Incomplete items: Lines matching `- [ ]`
   - Create a status table:
     ```
     | Checklist | Total | Completed | Incomplete | Status |
     |-----------|-------|-----------|------------|--------|
     | ux.md     | 12    | 12        | 0          | ✓ PASS |
     | test.md   | 8     | 5         | 3          | ✗ FAIL |
     | security.md | 6   | 6         | 0          | ✓ PASS |
     ```
   - Calculate overall status:
     * **PASS**: All checklists have 0 incomplete items
     * **FAIL**: One or more checklists have incomplete items

   - **If any checklist is incomplete**:
     * Display the table with incomplete item counts
     * **STOP** and ask: "Some checklists are incomplete. Do you want to proceed with implementation anyway? (yes/no)"
     * Wait for user response before continuing
     * If user says "no" or "wait" or "stop", halt execution
     * If user says "yes" or "proceed" or "continue", proceed to step 4

   - **If all checklists are complete**:
     * Display the table showing all checklists passed
     * Automatically proceed to step 4

4. Load and analyze the implementation context:

   **Load tasks file** (path depends on mode):
   - **IF SINGLE-STORY MODE (EPIC)**: Read `$FEATURE_DIR/tasks-US-###.md` (story-specific tasks)
   - **IF MULTI-STORY MODE or NON-EPIC**: Read `$FEATURE_DIR/tasks.md` (master task list)
   - Determine which file to read based on:
     * Check if `--story US-###` argument provided AND epic-breakdown.md exists
     * If yes: use `tasks-US-###.md`
     * Otherwise: use `tasks.md`

   **Load other context**:
   - **REQUIRED**: Read plan.md for tech stack, architecture, and file structure
   - **IF EXISTS**: Read data-model.md for entities and relationships
   - **IF EXISTS**: Read contracts/ for API specifications and test requirements
   - **IF EXISTS**: Read research.md for technical decisions and constraints
   - **IF EXISTS**: Read quickstart.md for integration scenarios

5. Parse tasks file structure and extract:
   - **Task phases**: Setup, Tests, Core, Integration, Polish
   - **Task dependencies**: Sequential vs parallel execution rules
   - **Task details**: ID, description, file paths, parallel markers [P]
   - **Execution flow**: Order and dependency requirements

6. **Constitution Gate Check** (RisoTech Enhancement):

   If `SPECIFY_RISOTECH_MODE=true` or `SPECIFY_TIERED_CONSTITUTION=true`:

   a. Before starting implementation, run constitution validation:
      - Read `/memory/constitution.md`
      - Check if plan and tasks comply with CORE rules
      - Warn about any HIGH-PRIORITY deviations

   b. **If CORE rule violations found**:
      - List violations clearly with affected tasks
      - **STOP** and ask: "Constitution CORE rules violated. Fix issues before implementing? (yes/no)"
      - If user says "yes", halt and suggest fixes
      - If user says "no", document violations and proceed with warning

   c. If validation passes or user approves, continue to step 7

7. Execute implementation following the task plan:

   **IF SINGLE-STORY MODE** (`--story US-###` in EPIC mode):
   - Execute only tasks for the specified story
   - Follow story-specific task order from tasks-US-###.md
   - After each task completion:
     * Update story progress in backlog.json
     * Increment completed_tasks count
     * Calculate progress percentage
   - After all story tasks complete:
     * Mark story as COMPLETE in backlog
     * Update completed_at timestamp
     * Check for stories blocked by this one and unblock them
     * Report story completion with metrics

   **IF MULTI-STORY/FULL-FEATURE MODE**:
   - **Phase-by-phase execution**: Complete each phase before moving to the next
   - **Respect dependencies**: Run sequential tasks in order, parallel tasks [P] can run together
   - **Follow TDD approach**: Execute test tasks before their corresponding implementation tasks
   - **File-based coordination**: Tasks affecting the same files must run sequentially
   - **Validation checkpoints**: Verify each phase completion before proceeding
   - **RisoTech - Validation Sub-tasks**: If enabled, check validation checklist after each task
   - **Story tracking**: If backlog.json exists, update story status as phases complete

7. Implementation execution rules:
   - **Setup first**: Initialize project structure, dependencies, configuration
   - **Tests before code**: If you need to write tests for contracts, entities, and integration scenarios
   - **Core development**: Implement models, services, CLI commands, endpoints
   - **Integration work**: Database connections, middleware, logging, external services
   - **Polish and validation**: Unit tests, performance optimization, documentation

8. Progress tracking and error handling:

   **Progress Reporting:**
   - Report progress after each completed task
   - **IF SINGLE-STORY MODE**:
     * Show story progress: "US-001: 3/10 tasks complete (30%)"
     * Update backlog.json after each task
     * Report estimated vs actual hours
   - **IF MULTI-STORY MODE**:
     * Show overall progress: "Phase 3: Story US-001 - 3/10 tasks (30%)"
     * Track phase completion percentages
     * Update backlog for each completed story

   **Error Handling:**
   - Halt execution if any non-parallel task fails
   - For parallel tasks [P], continue with successful tasks, report failed ones
   - Provide clear error messages with context for debugging
   - Suggest next steps if implementation cannot proceed
   - **IF STORY MODE**: Save progress to backlog even if incomplete
   - **IMPORTANT**: Mark completed tasks as [X] in the tasks file

9. Completion validation:

   **IF SINGLE-STORY MODE:**
   - Verify all story tasks completed
   - Mark story as COMPLETE in backlog.json
   - Update story metrics (completed_tasks, actual_hours)
   - Check and unblock dependent stories
   - Report:
     ```
     ✅ Story US-001 Complete!

     Title: User Login
     Tasks: 10/10 (100%)
     Estimated: 20.0 hours
     Actual: 18.5 hours
     Efficiency: 108%

     Unblocked Stories:
     - US-002: User Dashboard (now READY)
     - US-003: Admin Panel (now READY)

     Next Story: /speckit.story --next
     ```

   **IF MULTI-STORY/FULL-FEATURE MODE:**
   - Verify all required tasks are completed
   - Check that implemented features match the original specification
   - Validate that tests pass and coverage meets requirements
   - Confirm the implementation follows the technical plan
   - **IF BACKLOG EXISTS**: Update all story statuses to COMPLETE
   - Report final status with summary:
     * Total tasks completed
     * Stories completed (if EPIC mode)
     * Overall estimated vs actual hours
     * Test coverage achieved
     * Constitution compliance status

Note: This command assumes a complete task breakdown exists in tasks.md. If tasks are incomplete or missing, suggest running `/tasks` first to regenerate the task list.