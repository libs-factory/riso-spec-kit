# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to the Specify CLI and templates are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-08

### Added - RisoTech Integration

This is a **MINOR** version bump introducing significant new features while maintaining backward compatibility.

#### Core Modules

- **config.py**: Feature flag system for progressive rollout
  - `SPECIFY_RISOTECH_MODE` - Master switch for all RisoTech enhancements
  - `SPECIFY_TIERED_CONSTITUTION` - Tiered constitution framework
  - `SPECIFY_EPIC_DECOMPOSITION` - EPIC decomposition for large features
  - `SPECIFY_CLARIFICATION_GATE` - Enhanced clarification workflows
  - `SPECIFY_VALIDATION_SUBTASKS` - Validation sub-tasks for quality gates
  - `SPECIFY_MULTISTORY_BACKLOG` - Multi-story backlog management

- **constitution.py**: Tiered constitution management
  - Three-tier structure: CORE, HIGH-PRIORITY, FLEXIBLE rules
  - Load/save constitution from markdown
  - Validate plans against constitution rules
  - Merge constitutions with conflict resolution
  - Generate constitution summaries
  - **NEW**: Constitution preset system with stack-specific templates
  - **NEW**: `load_preset()` method for quick constitution setup
  - **NEW**: `list_available_presets()` and `get_preset_description()` helpers

- **epic_analyzer.py**: Large feature decomposition
  - Analyze feature complexity (SMALL, MEDIUM, LARGE, EPIC)
  - Decompose EPICs into manageable stories
  - **NEW**: `decompose_feature_to_stories()` with 4 strategies (roles, functional areas, entities, MVP)
  - **NEW**: `detect_story_dependencies()` for automatic dependency detection
  - **NEW**: `apply_dependencies()` for dependency management
  - Generate story sequences respecting dependencies
  - Estimate EPIC duration
  - Load/save EPICs from markdown

- **story_manager.py**: User story tracking and backlog management
  - **NEW**: `UserStory` dataclass with status tracking (DRAFT/READY/IN_PROGRESS/COMPLETE/BLOCKED)
  - **NEW**: `StoryBacklog` for story persistence (JSON-based)
  - **NEW**: `StoryManager` for multi-feature story management
  - Track story progress with metrics (tasks, hours, test coverage)
  - Automatic dependency checking and blocking/unblocking
  - Story velocity calculation
  - Circular dependency detection
  - Story status transitions with validation

- **workflow_runner.py**: Workflow orchestration
  - **NEW**: `WorkflowRunner` for end-to-end workflow management
  - Detect current workflow stage (SPECIFY/PLAN/TASKS/IMPLEMENT)
  - Validate prerequisites before stage transitions
  - Story readiness validation for implementation
  - Automatic progress tracking and backlog updates
  - Story completion with auto-unblocking of dependents
  - Workflow summary generation

- **progress_tracker.py**: Implementation progress tracking
  - **NEW**: `ProgressTracker` for task-level progress monitoring
  - Track task status (pending/in_progress/complete/failed)
  - Phase-by-phase progress calculation
  - Duration tracking for tasks
  - Overall progress metrics

- **validation.py**: Validation sub-task generation
  - Auto-generate validation checks for tasks
  - Support multiple validation types (unit test, integration test, manual check, code review, documentation, performance)
  - Track task completion via validation checklists
  - Generate progress reports
  - Validate task dependencies

#### Templates

- **RisoTech Constitution Templates**:
  - `templates/risotech/core.md` - Non-negotiable core rules
  - `templates/risotech/high-priority.md` - Strong recommendations
  - `templates/risotech/flexible.md` - Adaptable guidelines
  - **NEW**: `templates/risotech/constitution-presets/react-typescript.md` - React + TS preset
  - **NEW**: `templates/risotech/constitution-presets/nextjs-tailwind.md` - Next.js + Tailwind preset
  - **NEW**: `templates/risotech/constitution-presets/django-postgresql.md` - Django + PostgreSQL preset

- **EPIC & Story Templates**:
  - **NEW**: `templates/risotech/epic-breakdown.md` - EPIC decomposition template
  - **NEW**: `templates/risotech/story-template.md` - User story template
  - **NEW**: `templates/risotech/progress-report.md` - Progress report template

- **New Commands**:
  - `templates/commands/constitution-validation.md` - Validate artifacts against constitution
  - `templates/commands/constitution-upgrade.md` - Upgrade to tiered constitution
  - **NEW**: `templates/commands/epic.md` - EPIC decomposition workflow
  - **NEW**: `templates/commands/story.md` - Story management (list, status, progress)
  - **NEW**: `templates/commands/status.md` - Generate progress reports

- **Enhanced Commands**:
  - **UPDATED**: `templates/commands/specify.md` - Added constitution validation step
  - **UPDATED**: `templates/commands/plan.md` - Added EPIC complexity analysis
  - **UPDATED**: `templates/commands/tasks.md` - Added EPIC integration, single-story mode
  - **UPDATED**: `templates/commands/implement.md` - Added story-scoped implementation, progress tracking
  - **UPDATED**: `memory/constitution.md` - Enhanced with tier structure

- **Scripts**:
  - **NEW**: `scripts/bash/epic-breakdown.sh` - EPIC workflow helper
  - **NEW**: `scripts/bash/story-management.sh` - Story management helper

- **Tasks Index Template**:
  - `templates/tasks-index-template.md` - Comprehensive task tracking

#### Tests

- Comprehensive test suite with 80%+ coverage goal
  - `tests/test_config.py` - Config and feature flag tests (8 tests)
  - `tests/test_constitution.py` - Constitution management tests (12 tests)
  - `tests/test_epic_analyzer.py` - EPIC decomposition tests (11 tests)
  - `tests/test_validation.py` - Validation sub-task tests (14 tests)
  - **NEW**: `tests/test_constitution_presets.py` - Constitution preset tests (13 tests)
  - **NEW**: `tests/test_story_manager.py` - Story management tests (15 tests)
  - **NEW**: `tests/test_workflow_runner.py` - Workflow orchestration tests (12 tests)

### Changed

- Bumped version from `0.0.18` to `0.1.0` (MINOR version bump)
- Updated `pyproject.toml` description to mention RisoTech enhancements
- Added `dev` optional dependencies for testing (pytest, pytest-cov, pytest-mock)
- Enhanced `config.py` with workflow settings:
  - `ENABLE_STORY_TRACKING` - Story-level progress tracking
  - `ENABLE_PROGRESS_REPORTING` - Automatic progress reports
  - `AUTO_UPDATE_BACKLOG` - Auto-update backlog on task completion
  - `TRACK_ACTUAL_HOURS` - Track actual vs estimated hours
  - `CALCULATE_VELOCITY` - Calculate story/task velocity
  - `REQUIRE_READY_STATUS` - Require READY status before implementation
  - `AUTO_UNBLOCK_STORIES` - Auto-unblock stories when dependencies complete
  - `BLOCK_ON_INCOMPLETE_DEPS` - Auto-block stories with incomplete dependencies

### Features Overview

#### EPIC Decomposition Workflow

For large/complex features (30+ tasks):

```bash
/speckit.specify "Build user management system"
/speckit.plan                    # Detects EPIC complexity
/speckit.epic                    # Decomposes into stories
/speckit.story --list            # View all stories
/speckit.tasks --story US-001    # Generate tasks for MVP story
/speckit.implement --story US-001 # Implement MVP
/speckit.story US-001 --complete # Mark complete, unblock dependents
/speckit.story --next            # Get next story
```

#### Story-by-Story Implementation

Incremental delivery with dependency tracking:

- Implement one story at a time
- Automatic dependency validation
- Progress tracking per story
- Auto-unblocking of dependent stories
- Velocity calculation for planning

#### Progress Reporting

Comprehensive status monitoring:

```bash
/speckit.status                  # Quick summary
/speckit.status --format markdown --save # Detailed report
/speckit.status --story US-003   # Story-specific status
/speckit.status --format json    # Machine-readable (CI/CD)
```

### Migration Guide

Existing users can continue using specify-cli without changes. All RisoTech features are disabled by default.

To enable RisoTech enhancements:

```bash
# Enable all RisoTech features
export SPECIFY_RISOTECH_MODE=true

# Or enable specific features
export SPECIFY_TIERED_CONSTITUTION=true
export SPECIFY_VALIDATION_SUBTASKS=true
```

New commands available:
- `/speckit.constitution-validation` - Validate artifacts
- `/speckit.constitution-upgrade` - Upgrade to tiered constitution

## [0.0.18] - 2025-10-06

### Added

- Support for using `.` as a shorthand for current directory in `specify init .` command, equivalent to `--here` flag but more intuitive for users.
- Use the `/speckit.` command prefix to easily discover Spec Kit-related commands.
- Refactor the prompts and templates to simplify their capabilities and how they are tracked. No more polluting things with tests when they are not needed.
- Ensure that tasks are created per user story (simplifies testing and validation).
- Add support for Visual Studio Code prompt shortcuts and automatic script execution.

### Changed

- All command files now prefixed with `speckit.` (e.g., `speckit.specify.md`, `speckit.plan.md`) for better discoverability and differentiation in IDE/CLI command palettes and file explorers

## [0.0.17] - 2025-09-22

### Added

- New `/clarify` command template to surface up to 5 targeted clarification questions for an existing spec and persist answers into a Clarifications section in the spec.
- New `/analyze` command template providing a non-destructive cross-artifact discrepancy and alignment report (spec, clarifications, plan, tasks, constitution) inserted after `/tasks` and before `/implement`.
	- Note: Constitution rules are explicitly treated as non-negotiable; any conflict is a CRITICAL finding requiring artifact remediation, not weakening of principles.

## [0.0.16] - 2025-09-22

### Added

- `--force` flag for `init` command to bypass confirmation when using `--here` in a non-empty directory and proceed with merging/overwriting files.

## [0.0.15] - 2025-09-21

### Added

- Support for Roo Code.

## [0.0.14] - 2025-09-21

### Changed

- Error messages are now shown consistently.

## [0.0.13] - 2025-09-21

### Added

- Support for Kilo Code. Thank you [@shahrukhkhan489](https://github.com/shahrukhkhan489) with [#394](https://github.com/github/spec-kit/pull/394).
- Support for Auggie CLI. Thank you [@hungthai1401](https://github.com/hungthai1401) with [#137](https://github.com/github/spec-kit/pull/137).
- Agent folder security notice displayed after project provisioning completion, warning users that some agents may store credentials or auth tokens in their agent folders and recommending adding relevant folders to `.gitignore` to prevent accidental credential leakage.

### Changed

- Warning displayed to ensure that folks are aware that they might need to add their agent folder to `.gitignore`.
- Cleaned up the `check` command output.

## [0.0.12] - 2025-09-21

### Changed

- Added additional context for OpenAI Codex users - they need to set an additional environment variable, as described in [#417](https://github.com/github/spec-kit/issues/417).

## [0.0.11] - 2025-09-20

### Added

- Codex CLI support (thank you [@honjo-hiroaki-gtt](https://github.com/honjo-hiroaki-gtt) for the contribution in [#14](https://github.com/github/spec-kit/pull/14))
- Codex-aware context update tooling (Bash and PowerShell) so feature plans refresh `AGENTS.md` alongside existing assistants without manual edits.

## [0.0.10] - 2025-09-20

### Fixed

- Addressed [#378](https://github.com/github/spec-kit/issues/378) where a GitHub token may be attached to the request when it was empty.

## [0.0.9] - 2025-09-19

### Changed

- Improved agent selector UI with cyan highlighting for agent keys and gray parentheses for full names

## [0.0.8] - 2025-09-19

### Added

- Windsurf IDE support as additional AI assistant option (thank you [@raedkit](https://github.com/raedkit) for the work in [#151](https://github.com/github/spec-kit/pull/151))
- GitHub token support for API requests to handle corporate environments and rate limiting (contributed by [@zryfish](https://github.com/@zryfish) in [#243](https://github.com/github/spec-kit/pull/243))

### Changed

- Updated README with Windsurf examples and GitHub token usage
- Enhanced release workflow to include Windsurf templates

## [0.0.7] - 2025-09-18

### Changed

- Updated command instructions in the CLI.
- Cleaned up the code to not render agent-specific information when it's generic.


## [0.0.6] - 2025-09-17

### Added

- opencode support as additional AI assistant option

## [0.0.5] - 2025-09-17

### Added

- Qwen Code support as additional AI assistant option

## [0.0.4] - 2025-09-14

### Added

- SOCKS proxy support for corporate environments via `httpx[socks]` dependency

### Fixed

N/A

### Changed

N/A
