---
description: Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
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

1. **Setup**: Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute.

2. **Check for EPIC decomposition** (RisoTech Enhancement):

   If `SPECIFY_RISOTECH_MODE=true` or `SPECIFY_EPIC_DECOMPOSITION=true`:

   a. Check if `FEATURE_DIR/epic-breakdown.md` exists

   b. **If epic-breakdown.md EXISTS**:
      - Load epic-breakdown.md
      - Extract user stories (US-001, US-002, etc.)
      - Parse story priorities, dependencies, task estimates
      - Check for `--story US-###` argument in user input

      **If `--story US-###` provided:**
      - Generate tasks for ONLY that specific user story
      - Load story details from epic-breakdown.md or stories/US-###.md
      - Skip to step 3 with single-story context

      **If no `--story` argument:**
      - Generate tasks for ALL stories in epic-breakdown.md
      - Organize by story phases (as described below)
      - Continue to step 3 with multi-story context

   c. **If epic-breakdown.md DOES NOT EXIST**:
      - Proceed with standard task generation (no EPIC decomposition)
      - Continue to step 3

3. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
   - **If EPIC mode**: epic-breakdown.md (story decomposition)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

4. **Execute task generation workflow** (follow the template structure):

   **IF EPIC MODE (epic-breakdown.md exists):**

   a. **Single-story mode** (`--story US-###` provided):
      - Load story from epic-breakdown.md or stories/US-###.md
      - Extract story details: title, description, acceptance criteria, dependencies
      - Check dependencies are complete (from backlog.json if exists)
      - Generate tasks for ONLY this story:
        * Story-specific setup (if needed)
        * Tests for this story (if requested)
        * Implementation tasks for this story
        * Story-specific integration
        * Story validation checklist
      - Number tasks: T001, T002... (scoped to this story)
      - Skip other stories entirely

   b. **Multi-story mode** (no `--story` argument):
      - Load all stories from epic-breakdown.md
      - Sort by priority (P1, P2, P3) and dependencies
      - Generate tasks organized by story phases:
        * Phase 1: Setup (shared infrastructure)
        * Phase 2: Foundational (blocking prerequisites)
        * Phase 3+: One phase per user story (P1 stories first)
        * Final Phase: Polish & integration
      - Each story phase includes:
        * Story goal and acceptance criteria
        * Independent test scenario
        * Tests (if requested)
        * Implementation tasks
        * Story validation (if RisoTech validation enabled)
        * Checkpoint after story complete
      - Number tasks sequentially across all stories

   **IF STANDARD MODE (no EPIC decomposition):**

   - Load plan.md and extract tech stack, libraries, project structure
   - **Load spec.md and extract user stories with their priorities (P1, P2, P3, etc.)**
   - If data-model.md exists: Extract entities → map to user stories
   - If contracts/ exists: Each file → map endpoints to user stories
   - If research.md exists: Extract decisions → generate setup tasks
   - **Generate tasks ORGANIZED BY USER STORY**:
     - Setup tasks (shared infrastructure needed by all stories)
     - **Foundational tasks (prerequisites that must complete before ANY user story can start)**
     - For each user story (in priority order P1, P2, P3...):
       - Group all tasks needed to complete JUST that story
       - Include models, services, endpoints, UI components specific to that story
       - Mark which tasks are [P] parallelizable
       - If tests requested: Include tests specific to that story
     - Polish/Integration tasks (cross-cutting concerns)
   - **Tests are OPTIONAL**: Only generate test tasks if explicitly requested in the feature spec or user asks for TDD approach
   - **RisoTech Enhancement - Validation Sub-tasks**: If `SPECIFY_VALIDATION_SUBTASKS=true`:
     * Auto-generate validation checklist for EACH implementation task:
       - Unit tests (if code changes)
       - Integration tests (if API/database)
       - Manual checks (if UI/UX)
       - Code review (always)
       - Documentation (if new feature)
     * Add validation sub-task section to each task
     * Validate tasks don't proceed until sub-tasks complete
   - Apply task rules:
     - Different files = mark [P] for parallel
     - Same file = sequential (no [P])
     - If tests requested: Tests before implementation (TDD order)
   - Number tasks sequentially (T001, T002...)
   - Generate dependency graph showing user story completion order
   - Create parallel execution examples per user story
   - Validate task completeness (each user story has all needed tasks, independently testable)
   - **EPIC Integration**: If epic-breakdown.md exists, reference story IDs and follow story-based organization

5. **Generate tasks.md**: Use `.specify.specify/templates/tasks-template.md` as structure, fill with:

   **CRITICAL - OUTPUT PATH LOGIC**:

   **IF NOT EPIC MODE** (no epic-breakdown.md exists):
   - **Output to**: `$FEATURE_DIR/tasks.md`
   - Single file contains all tasks organized by user story phases

   **IF EPIC MODE** (epic-breakdown.md exists):
   - **Single-story mode** (`--story US-###` provided):
     * **Output to**: `$FEATURE_DIR/tasks-US-###.md` (e.g., tasks-US-001.md)
     * One file per story for independent tracking and implementation
   - **Multi-story mode** (no `--story` argument):
     * **Output to**: `$FEATURE_DIR/tasks.md`
     * Master file with all stories, organized by phases

   **IF SINGLE-STORY MODE** (`--story US-###` provided in EPIC mode):
   - Feature name + story title header
   - Story context (ID, goal, acceptance criteria, dependencies)
   - Story-specific tasks only (setup, tests, implementation, validation)
   - Numbered tasks scoped to this story (T001, T002...)
   - Story completion checklist
   - **Output to**: `$FEATURE_DIR/tasks-US-###.md`

   **IF MULTI-STORY MODE** (standard or EPIC with all stories):
   - Correct feature name from plan.md
   - Phase 1: Setup tasks (project initialization)
   - Phase 2: Foundational tasks (blocking prerequisites for all user stories)
   - Phase 3+: One phase per user story (in priority order from spec.md or epic-breakdown.md)
     - Each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks
     - Clear [Story] labels (US1, US2, US3...) for each task
     - [P] markers for parallelizable tasks within each story
     - Checkpoint markers after each story phase
   - Final Phase: Polish & cross-cutting concerns
   - Numbered tasks (T001, T002...) in execution order
   - Clear file paths for each task
   - Dependencies section showing story completion order
   - Parallel execution examples per story
   - Implementation strategy section (MVP first, incremental delivery)
   - **Output to**: `$FEATURE_DIR/tasks.md`

6. **Update story backlog** (if EPIC mode with backlog.json):
   - If `FEATURE_DIR/stories/backlog.json` exists:
     * Load backlog
     * Update story with tasks file path reference (tasks-US-###.md for single-story)
     * Update estimated_tasks count for the story
     * Set status to READY (if was DRAFT)
     * Save backlog

7. **Report**: Output path to generated tasks file and summary:

   **IF SINGLE-STORY MODE (EPIC):**
   - **Output file**: `$FEATURE_DIR/tasks-US-###.md`
   - Story ID and title
   - Total task count for this story
   - Estimated hours for this story
   - Dependencies status (complete/incomplete)
   - Ready to implement: Yes/No
   - Next step: `/speckit.implement --story US-###`

   **IF MULTI-STORY MODE:**
   - **Output file**: `$FEATURE_DIR/tasks.md` (master file for all stories)
   - Total task count
   - Task count per user story
   - Parallel opportunities identified
   - Independent test criteria for each story
   - Suggested MVP scope (typically just User Story 1 or all P1 stories)
   - Next step: `/speckit.implement` (all stories) or `/speckit.implement --story US-001` (MVP only)

Context for task generation: {ARGS}

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**IMPORTANT**: Tests are optional. Only generate test tasks if the user explicitly requested testing or TDD approach in the feature specification.

**CRITICAL**: Tasks MUST be organized by user story to enable independent implementation and testing.

1. **From User Stories (spec.md)** - PRIMARY ORGANIZATION:
   - Each user story (P1, P2, P3...) gets its own phase
   - Map all related components to their story:
     - Models needed for that story
     - Services needed for that story
     - Endpoints/UI needed for that story
     - If tests requested: Tests specific to that story
   - Mark story dependencies (most stories should be independent)

2. **From Contracts**:
   - Map each contract/endpoint → to the user story it serves
   - If tests requested: Each contract → contract test task [P] before implementation in that story's phase

3. **From Data Model**:
   - Map each entity → to the user story(ies) that need it
   - If entity serves multiple stories: Put in earliest story or Setup phase
   - Relationships → service layer tasks in appropriate story phase

4. **From Setup/Infrastructure**:
   - Shared infrastructure → Setup phase (Phase 1)
   - Foundational/blocking tasks → Foundational phase (Phase 2)
     - Examples: Database schema setup, authentication framework, core libraries, base configurations
     - These MUST complete before any user story can be implemented
   - Story-specific setup → within that story's phase

5. **Ordering**:
   - Phase 1: Setup (project initialization)
   - Phase 2: Foundational (blocking prerequisites - must complete before user stories)
   - Phase 3+: User Stories in priority order (P1, P2, P3...)
     - Within each story: Tests (if requested) → Models → Services → Endpoints → Integration
   - Final Phase: Polish & Cross-Cutting Concerns
   - Each user story phase should be a complete, independently testable increment

