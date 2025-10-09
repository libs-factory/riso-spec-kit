---
description: Analyze feature complexity and decompose EPIC features into user stories
scripts:
  sh: scripts/bash/epic-breakdown.sh --json
  ps: scripts/powershell/epic-breakdown.ps1 -Json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON output for FEATURE_DIR, SPEC_FILE, PLAN_FILE, TASKS_FILE. All paths must be absolute.

2. **Load context**: Read available design artifacts:
   - **Required**: spec.md (user stories, requirements)
   - **Required**: plan.md (tech stack, architecture)
   - **Optional**: data-model.md (entities and relationships)
   - **Optional**: contracts/ (API specifications)
   - **Optional**: tasks.md (task breakdown if already exists)

3. **Analyze complexity**: Use EPIC analyzer to determine feature complexity:
   - Count estimated tasks (from plan.md or user input)
   - Analyze feature description for complexity indicators:
     * Multiple user roles/personas
     * Multiple distinct workflows
     * Cross-cutting architectural changes
     * External integrations
     * Complex data models
   - Classify as: SMALL (1-5 tasks), MEDIUM (6-15 tasks), LARGE (16-30 tasks), EPIC (30+ tasks)

4. **Decision gate**:

   **If complexity is SMALL or MEDIUM:**
   - Report: "Feature is not complex enough to require EPIC decomposition"
   - Suggest: "Run `/speckit.tasks` to generate standard task breakdown"
   - **STOP** - Do not proceed with EPIC decomposition

   **If complexity is LARGE or EPIC:**
   - Report: "Feature complexity requires decomposition into user stories"
   - Continue to step 5

5. **Decompose into user stories** (EPIC/LARGE features only):

   Apply decomposition strategies in order:

   a. **Strategy 1 - By User Roles/Personas:**
      - Scan spec.md for different user types (admin, user, manager, etc.)
      - If 2+ distinct roles found → Create story per role
      - Example: "Admin Dashboard" + "User Dashboard" stories

   b. **Strategy 2 - By Functional Areas:**
      - Identify CRUD operations, reporting, export/import, search, etc.
      - Group related functionality into stories
      - Example: "Data Entry" + "Data Export" + "Reporting" stories

   c. **Strategy 3 - By Data Entities (if data-model.md exists):**
      - Map each entity to CRUD story
      - Consider entity relationships for dependencies
      - Example: "Post Management" + "Comment Management" stories

   d. **Fallback - MVP + Enhancements:**
      - Story 1 (P1): MVP - Core Functionality
      - Story 2 (P2): Enhanced Features
      - Story 3 (P3): Polish & Optimization

6. **Detect dependencies between stories**:
   - Identify foundation stories (MVP, core entities)
   - Detect mentions of other story titles in descriptions
   - Apply priority-based dependencies (P1 → P2 → P3)
   - Check for circular dependencies (ERROR if found)

7. **Assign priorities and estimates**:
   - First story = P1 (MVP foundation)
   - Core features = P1 (must have)
   - Enhancements = P2 (should have)
   - Polish/optional = P3 (nice to have)
   - Distribute total task estimate across stories
   - Ensure each story has 3+ tasks

8. **Generate EPIC breakdown document**:
   - Use template: `templates/risotech/epic-breakdown.md`
   - Fill sections:
     * Original requirement
     * Why this is an EPIC
     * Decomposed user stories (with details)
     * Story dependency graph
     * Shared components
     * Implementation strategy (iterations)
     * Cross-story considerations
     * Risk assessment
     * Success metrics
   - Save to: `FEATURE_DIR/epic-breakdown.md`

9. **Create individual story files** (optional):
   - For each user story → `FEATURE_DIR/stories/US-###.md`
   - Use template: `templates/risotech/story-template.md`
   - Fill story details, acceptance criteria, tasks, dependencies

10. **Initialize story backlog** (if RisoTech mode enabled):
    - If `SPECIFY_RISOTECH_MODE=true`:
      * Create `FEATURE_DIR/stories/backlog.json`
      * Initialize each story with metadata:
        - Story ID, title, description
        - Priority (P1/P2/P3)
        - Status (DRAFT)
        - Dependencies
        - Estimated tasks/hours
        - Metrics (progress: 0%)
      * Enable story tracking for `/speckit.implement`

11. **Report completion**:
    - Output path to epic-breakdown.md
    - Summary:
      * Total stories created
      * Breakdown by priority (P1/P2/P3 count)
      * Dependency graph overview
      * Parallel implementation opportunities
      * Suggested MVP scope (P1 stories only)
    - Next steps:
      * Option 1: Implement MVP only → `/speckit.tasks US-001` (single story)
      * Option 2: Full implementation → `/speckit.tasks` (all stories)
      * Option 3: Review/edit stories before proceeding

## EPIC Decomposition Rules

**CRITICAL**: Only decompose if complexity is LARGE or EPIC (16+ tasks).

### Decomposition Quality Criteria

1. **Independence**: Each story should be independently implementable and testable
2. **Completeness**: Each story delivers end-to-end value to users
3. **Testability**: Each story has clear, verifiable acceptance criteria
4. **Right-sized**: Each story is 3-15 tasks (not too big, not too small)
5. **Dependencies**: Minimize dependencies, make them explicit
6. **Priority-driven**: P1 stories form MVP, P2 enhance, P3 polish

### Story Naming Conventions

- **User-centric**: "User Registration", "Admin Dashboard" (not "Database Setup")
- **Value-focused**: "Data Export", "Search Functionality" (not "Add Export Button")
- **Domain language**: Use terms from spec.md
- **Action-oriented**: Start with verb when appropriate

### Dependency Rules

1. **Foundation first**: MVP/core stories must have no dependencies
2. **Layered dependencies**: P2 can depend on P1, P3 on P2
3. **No circular dependencies**: ERROR if detected
4. **Minimal coupling**: Prefer independent stories

### Priority Assignment

- **P1 (Must Have - MVP)**: Core user workflows, foundational features
- **P2 (Should Have)**: Important enhancements, additional workflows
- **P3 (Nice to Have)**: Polish, optimization, edge cases

### Task Distribution

- **MVP story**: ~30-40% of total tasks
- **Enhancement stories**: ~50-60% of total tasks
- **Polish story**: ~10-20% of total tasks

## Integration with Other Commands

**After `/speckit.epic`:**

- **Review stories**: Edit `epic-breakdown.md` or individual story files
- **Implement MVP**: `/speckit.tasks --story US-001` (single story tasks)
- **Implement all**: `/speckit.tasks` (will read epic-breakdown.md and organize by story)

**Story tracking** (RisoTech mode):

- `/speckit.story US-001 --status ready` - Mark story ready
- `/speckit.story US-001 --progress 5/10` - Update progress
- `/speckit.story --list --filter ready` - List ready stories
- `/speckit.story --next` - Get next priority story to implement

## Example Usage

```bash
# Analyze if feature needs EPIC decomposition
/speckit.epic

# Decompose with custom context
/speckit.epic "Focus on separating admin and user workflows"

# After decomposition, implement MVP only
/speckit.tasks --story US-001

# Or implement all stories
/speckit.tasks
```

## Error Handling

**If spec.md not found:**
- ERROR: "Feature specification not found. Run `/speckit.specify` first."

**If complexity is SMALL/MEDIUM:**
- INFO: "Feature not complex enough for EPIC decomposition (X tasks estimated)"
- SUGGEST: "Run `/speckit.tasks` for standard task breakdown"
- STOP

**If circular dependencies detected:**
- ERROR: "Circular dependency detected: US-001 → US-002 → US-001"
- LIST: All circular dependency chains
- SUGGEST: How to break the cycle
- STOP

**If no valid decomposition strategy works:**
- WARN: "Could not find natural decomposition boundaries"
- FALLBACK: Use MVP + Enhancement + Polish strategy
- CONTINUE

## Notes

- EPIC decomposition is **optional** - only for complex features (LARGE/EPIC)
- Each story should be **independently deployable**
- Story breakdown enables **incremental delivery** (MVP first, then enhance)
- Dependencies should be **explicit and minimal**
- All stories must have **clear acceptance criteria**
