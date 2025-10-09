# RisoTech Integration - Architecture Documentation

**Version:** 0.1.0
**Last Updated:** 2025-10-08

---

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Core Modules](#core-modules)
4. [Workflow Orchestration](#workflow-orchestration)
5. [Data Models](#data-models)
6. [Templates & Commands](#templates--commands)
7. [Configuration System](#configuration-system)
8. [Analysis & Reporting](#analysis--reporting)
9. [Design Decisions](#design-decisions)
10. [Future Architecture](#future-architecture)

---

## Overview

### Purpose

RisoTech Integration enhances the Specify CLI with:
- **Tiered Constitution Framework** for governance
- **EPIC Decomposition** for large feature breakdown
- **Story Management** with progress tracking
- **Workflow Orchestration** for end-to-end delivery

### Architecture Principles

1. **Modularity**: Each component has a single, well-defined responsibility
2. **Backward Compatibility**: All features are opt-in via feature flags
3. **Progressive Enhancement**: Features can be enabled individually or all at once
4. **Template-Driven**: Workflows driven by markdown templates for AI agent consumption
5. **Data Persistence**: JSON-based storage for simplicity and portability

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Specify CLI (User)                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Command Templates                         │
│   /speckit.specify  /speckit.plan  /speckit.epic           │
│   /speckit.tasks    /speckit.implement  /speckit.story     │
│   /speckit.status   /speckit.constitution-applying         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Workflow Orchestration                     │
│                  (workflow_runner.py)                       │
│  - Stage Detection  - Prerequisite Validation              │
│  - Story Readiness  - Progress Tracking                    │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
┌─────────────────┐ ┌─────────────┐ ┌──────────────┐
│  Epic Analyzer  │ │Story Manager│ │Constitution  │
│  - Decompose    │ │- Backlog    │ │- Validation  │
│  - Dependencies │ │- Status     │ │- Presets     │
└─────────────────┘ └─────────────┘ └──────────────┘
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
┌─────────────────┐ ┌─────────────┐ ┌──────────────┐
│Story Analyzer   │ │Risk Analyzer│ │Bottleneck    │
│- Complexity     │ │- Assessment │ │Detector      │
│- Quality        │ │- Mitigation │ │- Critical    │
└─────────────────┘ └─────────────┘ └──────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Persistence                          │
│  - backlog.json (Story state)                               │
│  - epic-breakdown.md (Story decomposition)                  │
│  - .progress.json (Task progress)                           │
│  - constitution.md (Governance rules)                       │
└─────────────────────────────────────────────────────────────┘
```

### Component Layers

1. **Interface Layer**: Command templates consumed by AI agents
2. **Orchestration Layer**: Workflow coordination and validation
3. **Business Logic Layer**: Core domain logic (epic, story, constitution)
4. **Analysis Layer**: Advanced analytics and optimization
5. **Persistence Layer**: JSON/Markdown file storage

---

## Core Modules

### 1. Configuration (`config.py`)

**Purpose**: Centralized feature flag management

**Key Components**:
```python
class SpecifyConfig:
    # Feature flags
    RISOTECH_MODE: bool
    ENABLE_TIERED_CONSTITUTION: bool
    ENABLE_EPIC_DECOMPOSITION: bool
    ENABLE_STORY_TRACKING: bool

    # Workflow settings
    AUTO_UPDATE_BACKLOG: bool
    REQUIRE_READY_STATUS: bool
    AUTO_UNBLOCK_STORIES: bool
```

**Design Pattern**: Singleton with class methods for global access

---

### 2. Constitution (`constitution.py`)

**Purpose**: Tiered governance framework

**Architecture**:
```
Constitution
├── Tier: CORE (non-negotiable)
├── Tier: HIGH-PRIORITY (strong recommendations)
└── Tier: FLEXIBLE (guidelines)

ConstitutionPreset
├── react-typescript.md
├── nextjs-tailwind.md
└── django-postgresql.md
```

**Key Classes**:
- `ConstitutionTier(Enum)`: Defines tier levels
- `ConstitutionPreset(Enum)`: Available presets
- `Constitution`: Load, validate, merge constitutions
- `ConstitutionRule`: Individual rule representation

---

### 3. EPIC Analyzer (`epic_analyzer.py`)

**Purpose**: Feature decomposition and dependency management

**Decomposition Strategies**:
1. **By User Roles**: Admin, User, Manager workflows
2. **By Functional Areas**: CRUD, Reporting, Export/Import
3. **By Data Entities**: One story per entity
4. **MVP Fallback**: Core → Enhancement → Polish

**Dependency Detection**:
- MVP foundation dependencies
- Entity relationship dependencies
- Priority-based dependencies
- Circular dependency prevention

**Key Classes**:
- `EpicComplexity(Enum)`: SMALL/MEDIUM/LARGE/EPIC
- `Story`: User story representation
- `Epic`: EPIC container with stories
- `EpicAnalyzer`: Decomposition and analysis engine

---

### 4. Story Manager (`story_manager.py`)

**Purpose**: Story lifecycle and backlog management

**State Machine**:
```
DRAFT → READY → IN_PROGRESS → COMPLETE
   ↓       ↓          ↓
   └───────┴──────→ BLOCKED ──→ READY
```

**Key Components**:
- `UserStory`: Story entity with metrics
- `StoryMetrics`: Progress tracking (tasks, hours, coverage)
- `StoryBacklog`: Story persistence and operations
- `StoryManager`: Multi-feature management

**Storage**: JSON (`stories/backlog.json`)

---

### 5. Workflow Runner (`workflow_runner.py`)

**Purpose**: End-to-end workflow orchestration

**Workflow Stages**:
1. **SPECIFY**: Create specification
2. **PLAN**: Generate implementation plan
3. **TASKS**: Break down into tasks
4. **IMPLEMENT**: Execute implementation

**Responsibilities**:
- Stage detection and validation
- Prerequisite checking
- Story readiness validation
- Progress tracking integration
- Workflow summaries

---

### 6. Progress Tracker (`progress_tracker.py`)

**Purpose**: Task-level progress monitoring

**Tracking Levels**:
- **Task**: Individual task status
- **Phase**: Phase completion percentage
- **Overall**: Full feature progress

**Storage**: JSON (`.progress.json`)

---

## Workflow Orchestration

### Standard Workflow

```
/speckit.specify
       ↓
/speckit.plan (detects complexity)
       ↓
  [SMALL/MEDIUM] → /speckit.tasks → /speckit.implement
       ↓
  [LARGE/EPIC] → /speckit.epic → story-by-story workflow
```

### EPIC Workflow

```
/speckit.epic
   ↓
   ├─ Create epic-breakdown.md
   ├─ Generate stories (US-001, US-002, ...)
   └─ Initialize backlog.json

/speckit.story --list
   ↓
   View all stories with status

/speckit.story --next
   ↓
   Get next ready story (US-001)

/speckit.tasks --story US-001
   ↓
   Generate tasks for single story

/speckit.implement --story US-001
   ↓
   ├─ Execute story tasks
   ├─ Update progress
   └─ Mark complete

/speckit.story US-001 --complete
   ↓
   ├─ Mark COMPLETE
   └─ Unblock dependent stories

[Repeat for each story]

/speckit.status --save
   ↓
   Generate progress report
```

---

## Data Models

### UserStory

```python
@dataclass
class UserStory:
    id: str                          # US-001
    epic_id: Optional[str]           # EPIC-001
    title: str                       # "User Login"
    description: str                 # Full description
    acceptance_criteria: List[str]   # AC1, AC2, ...
    priority: StoryPriority          # P1/P2/P3
    status: StoryStatus              # DRAFT/READY/IN_PROGRESS/COMPLETE/BLOCKED
    dependencies: List[str]          # [US-002, US-003]
    blocked_by: List[str]            # [US-004]
    metrics: StoryMetrics            # Progress tracking
    created_at: str                  # ISO timestamp
    updated_at: str                  # ISO timestamp
    completed_at: Optional[str]      # ISO timestamp
```

### StoryMetrics

```python
@dataclass
class StoryMetrics:
    estimated_tasks: int      # 10
    completed_tasks: int      # 7
    estimated_hours: float    # 20.0
    actual_hours: float       # 18.5
    test_coverage: float      # 85.0 (percentage)
```

### Constitution Structure

```markdown
## CORE Principles
### [PRINCIPLE_NAME]
**Tier:** `core`
[Description]
**Rationale:** [Why this is CORE]
**Examples:** [...]

## HIGH-PRIORITY Rules
### [RULE_NAME]
**Tier:** `high-priority`
[Description]
**Exceptions:** [When deviation is acceptable]

## FLEXIBLE Guidelines
### [GUIDELINE_NAME]
**Tier:** `flexible`
[Description]
**Considerations:** [...]
```

---

## Templates & Commands

### Template Architecture

**Location**: `templates/commands/*.md`

**Structure**:
```markdown
---
description: Command description
scripts:
  sh: scripts/bash/helper.sh --json
---

## Outline
1. Setup
2. Load context
3. Execute workflow
4. Report results
```

### Command Categories

1. **Workflow Commands**:
   - `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`

2. **EPIC Commands**:
   - `/speckit.epic`, `/speckit.story`, `/speckit.status`

3. **Constitution Commands**:
   - `/speckit.constitution-applying`, `/speckit.constitution-upgrade`

---

## Configuration System

### Feature Flag Hierarchy

```
SPECIFY_RISOTECH_MODE=true
  └─ Enables ALL features

OR individual flags:
├─ SPECIFY_TIERED_CONSTITUTION=true
├─ SPECIFY_EPIC_DECOMPOSITION=true
├─ SPECIFY_STORY_TRACKING=true
├─ SPECIFY_PROGRESS_REPORTING=true
└─ SPECIFY_VALIDATION_SUBTASKS=true
```

### Workflow Settings

```
AUTO_UPDATE_BACKLOG=true         # Auto-update on task completion
TRACK_ACTUAL_HOURS=true          # Track actual vs estimated
CALCULATE_VELOCITY=true          # Calculate story velocity
REQUIRE_READY_STATUS=true        # Must be READY before implement
AUTO_UNBLOCK_STORIES=true        # Auto-unblock on dependency complete
BLOCK_ON_INCOMPLETE_DEPS=true   # Auto-block on incomplete deps
```

---

## Analysis & Reporting

### Analysis Modules

1. **Story Analyzer** (`story_analyzer.py`):
   - Complexity analysis (entities, integrations, UI, business logic)
   - Quality metrics (acceptance criteria, test scenarios)
   - Improvement suggestions

2. **Risk Analyzer** (`risk_analyzer.py`):
   - Schedule risks (velocity, blocked stories)
   - Technical risks (complexity)
   - Dependency risks (circular, long chains)
   - Quality risks (test coverage)
   - Estimation risks (accuracy)

3. **Bottleneck Detector** (`bottleneck_detector.py`):
   - Dependency bottlenecks (story blocking many others)
   - Complexity bottlenecks (slow progress on complex stories)
   - Status bottlenecks (too many in-progress/blocked)
   - Duration bottlenecks (stories taking too long)
   - Critical path analysis

4. **Estimation Analyzer** (`estimation_analyzer.py`):
   - Accuracy metrics (actual/estimated ratio)
   - Pattern detection (systematic under/over-estimation)
   - Complexity-based analysis
   - Prediction for future stories

---

## Design Decisions

### 1. Why JSON for Story Persistence?

**Decision**: Use JSON instead of database

**Rationale**:
- Simplicity: No DB setup required
- Portability: Easy to move between projects
- Version Control: Can be committed to git
- Human-Readable: Easy to inspect and debug

**Tradeoffs**:
- Limited query capability
- Manual consistency management
- File locking concerns (mitigated by single-user assumption)

### 2. Why Template-Driven Architecture?

**Decision**: Use markdown templates instead of CLI commands

**Rationale**:
- AI Agent Consumption: Claude can read and follow markdown
- Flexibility: Easy to modify workflows without code changes
- Documentation: Templates serve as documentation
- Progressive Enhancement: Can add features without breaking existing

**Tradeoffs**:
- Requires AI agent to execute
- Less direct user control
- Consistency depends on agent interpretation

### 3. Why Feature Flags?

**Decision**: All features behind flags, disabled by default

**Rationale**:
- Backward Compatibility: Existing users not affected
- Progressive Rollout: Enable features incrementally
- Testing: Can test individual features
- Opt-In: Users choose what they want

### 4. Why Tiered Constitution?

**Decision**: Three-tier structure (CORE/HIGH-PRIORITY/FLEXIBLE)

**Rationale**:
- Clarity: Clear distinction between must-have and nice-to-have
- Flexibility: Teams can adapt without breaking core principles
- Pragmatism: Acknowledges real-world constraints
- Documentation: Forces justification for deviations

---

## Future Architecture

### Planned Enhancements

1. **CLI Implementation**: Actual Python CLI commands (not just templates)
2. **Database Backend**: Optional PostgreSQL/SQLite for larger projects
3. **Real-Time Dashboard**: Web UI for progress visualization
4. **Integration APIs**: Jira, Trello, GitHub Projects sync
5. **ML-Based Estimation**: Use historical data for prediction
6. **Distributed Workflows**: Multi-team coordination

### Scalability Considerations

- **Current**: Single project, single user, file-based
- **Future**: Multi-project, multi-user, database-backed
- **Migration Path**: Maintain JSON compatibility, add database layer

---

## Security Considerations

### Current Security Model

- No authentication (local CLI tool)
- No authorization (single user)
- No encryption (plain text files)

### Future Security

- User authentication for multi-user setups
- Role-based access control (RBAC)
- Encryption for sensitive constitution data
- Audit logging for compliance

---

## Performance Characteristics

### Current Performance

- **Story Analysis**: O(n) where n = number of stories
- **Dependency Resolution**: O(n²) for circular detection
- **Backlog Operations**: O(1) for single story, O(n) for queries
- **File I/O**: Minimal (only on state changes)

### Optimization Opportunities

- Caching of analysis results
- Incremental dependency graph updates
- Batch operations for multiple stories
- Lazy loading of large backlogs

---

## Testing Architecture

### Test Structure

```
tests/
├── test_config.py              # Configuration tests
├── test_constitution.py        # Constitution management
├── test_epic_analyzer.py       # EPIC decomposition
├── test_story_manager.py       # Story lifecycle
├── test_workflow_runner.py     # Workflow orchestration
├── test_story_analyzer.py      # Analysis modules
├── test_risk_analyzer.py       # Risk assessment
├── test_bottleneck_detector.py # Bottleneck detection
└── test_epic_workflow_integration.py  # End-to-end
```

### Test Coverage

- **Target**: ≥85%
- **Current**: ~80%
- **Strategy**: Unit tests + integration tests

---

## Appendix: Module Dependency Graph

```
config.py (base)
    ↓
constitution.py, validation.py
    ↓
epic_analyzer.py
    ↓
story_manager.py
    ↓
workflow_runner.py, progress_tracker.py
    ↓
story_analyzer.py, risk_analyzer.py, bottleneck_detector.py, estimation_analyzer.py
```

**Dependency Rules**:
- No circular dependencies
- Core modules depend only on stdlib
- Analysis modules depend on core but not each other
- Workflow layer depends on business logic layer

---

**Document Version**: 1.0
**Maintained By**: RisoTech Team
**Last Review**: 2025-10-08
