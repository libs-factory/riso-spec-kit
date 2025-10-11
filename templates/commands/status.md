---
description: Generate comprehensive progress report for feature implementation
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
  ps: scripts/powershell/check-prerequisites.ps1 -Json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

## MANDATORY COMPLIANCE REQUIREMENTS

**ABSOLUTE PROCESS ADHERENCE**: Do NOT assume or independently decide to change the process. All steps in "Outline" below must be executed completely and in the exact order specified.

**MANDATORY TODO LIST**: Before starting execution, AI MUST create a TODO list based on the items in "Outline" to ensure no step is missed.

1. **Setup**: Run `{SCRIPT}` from repo root and parse FEATURE_DIR. All paths must be absolute.

2. **Parse arguments** from user input:
   - `--format <type>` - Output format: markdown (default), json, summary
   - `--save` - Save report to FEATURE_DIR/progress-report.md
   - `--story <story-id>` - Show status for specific story only

3. **Collect workflow status**:
   - Detect current workflow stage (specify/plan/tasks/implement)
   - Check which stages are complete
   - Calculate overall workflow progress percentage

4. **Collect story progress** (if EPIC mode enabled):
   - Load backlog.json if exists
   - Count stories by status (draft/ready/in_progress/complete/blocked)
   - Calculate story completion rate
   - Get next story to implement
   - Calculate story velocity (stories per day/week)

5. **Collect task progress**:
   - Parse tasks.md for task list
   - Count total tasks vs completed tasks (marked with [X])
   - Calculate task completion percentage
   - Identify current phase
   - Get current task being worked on

6. **Calculate metrics**:
   - **Time metrics**:
     * Estimated hours vs actual hours (from backlog if available)
     * Efficiency ratio
     * Average hours per task/story
   - **Velocity metrics**:
     * Stories/tasks completed per day
     * Projected completion date
   - **Quality metrics**:
     * Test coverage (if available from test reports)
     * Constitution compliance status

7. **Generate status report** based on format:

   ### Format: summary (quick overview)

   ```
   Feature: [FEATURE_NAME] ([FEATURE_ID])
   Status: [On Track / At Risk / Blocked]
   Progress: [X]% ([Y]/[Z] tasks complete)

   Current Stage: [STAGE]
   Current Task: [TASK_ID] - [TASK_DESCRIPTION]

   Stories: [COMPLETED]/[TOTAL] complete ([X]%)
   Next Story: [STORY_ID] - [STORY_TITLE]

   Estimated Completion: [DATE]
   ```

   ### Format: markdown (detailed report)

   Use template: `templates/risotech/progress-report.md`

   Fill all sections:
   - Executive Summary
   - Workflow Progress (stage completion table)
   - Story Progress (if EPIC mode):
     * Completed stories table
     * In-progress stories table
     * Blocked stories table
     * Upcoming stories table
   - Task Progress (phase-by-phase breakdown)
   - Metrics & Analytics:
     * Velocity metrics
     * Estimation accuracy
     * Task completion rate graph
   - Risks & Issues (if any found)
   - Quality Metrics:
     * Test coverage
     * Constitution compliance
   - Timeline & Milestones
   - Next Steps

   ### Format: json (machine-readable)

   ```json
   {
     "feature_id": "...",
     "feature_name": "...",
     "report_date": "...",
     "overall_progress": 0.0-100.0,
     "status": "on_track|at_risk|blocked",
     "workflow": {
       "current_stage": "...",
       "completed_stages": [...],
       "progress_percentage": 0.0-100.0
     },
     "stories": {
       "total": 0,
       "completed": 0,
       "in_progress": 0,
       "ready": 0,
       "blocked": 0,
       "completion_rate": 0.0-100.0,
       "next_story": {...}
     },
     "tasks": {
       "total": 0,
       "completed": 0,
       "completion_rate": 0.0-100.0,
       "current_phase": "...",
       "current_task": {...}
     },
     "metrics": {
       "estimated_hours": 0.0,
       "actual_hours": 0.0,
       "efficiency": 0.0-1.0,
       "velocity": {
         "stories_per_week": 0.0,
         "tasks_per_day": 0.0
       },
       "projected_completion": "YYYY-MM-DD"
     }
   }
   ```

8. **Output report**:
   - Display to console (formatted according to --format)
   - If `--save` flag: Write to FEATURE_DIR/progress-report.md
   - Report saved path if applicable

9. **Provide recommendations**:
   - If behind schedule: Suggest optimizations or scope reduction
   - If blocked: List blockers and suggested actions
   - If on track: Show next priorities

## Status Calculation Rules

### Overall Status

- **On Track**: Progress >= 90% of expected based on timeline
- **At Risk**: Progress 70-90% of expected
- **Blocked**: Has active blockers OR progress < 70% of expected

### Risk Detection

**Automatic risk identification:**
- Velocity trend decreasing over time
- Estimation accuracy < 80% (under/over-estimating)
- Blocked stories > 20% of total
- Critical tasks failing or stuck

### Recommendations

**If velocity low:**
- "Consider breaking down remaining tasks into smaller units"
- "Review if any tasks can be parallelized"

**If estimation poor:**
- "Actual hours significantly different from estimates"
- "Review estimation process for future stories"

**If stories blocked:**
- "Unblock US-### by completing dependencies"
- "Consider re-ordering story priorities"

## Integration with Other Commands

**Related commands:**
- `/speckit.story --list` - Detailed story status
- `/speckit.story --next` - Next story to implement
- `/speckit.implement` - Continue implementation

**Typical workflow:**
```bash
# Check current status
/speckit.status --format summary

# Generate full report
/speckit.status --save

# Check specific story
/speckit.status --story US-003

# Get machine-readable status
/speckit.status --format json
```

## Example Usage

```bash
# Quick status check
/speckit.status

# Detailed report saved to file
/speckit.status --format markdown --save

# JSON output for CI/CD
/speckit.status --format json

# Story-specific status
/speckit.status --story US-003
```

## Error Handling

**If no tasks.md found:**
- WARN: "No task breakdown found"
- Show workflow status only
- Suggest: "Run `/speckit.tasks` to generate tasks"

**If no backlog.json found:**
- INFO: "Not in EPIC mode, showing task-level progress only"
- Skip story metrics section

**If feature directory not found:**
- ERROR: "Feature directory not found"
- Suggest: "Are you in the correct git branch?"

## Notes

- Status command is read-only (no modifications)
- Can be run at any time during workflow
- Useful for daily standups and progress tracking
- JSON format useful for CI/CD integration
- Report can be committed to track historical progress
