---
description: Manage individual user stories - view, update status, track progress
scripts:
  sh: scripts/bash/story-management.sh --json
  ps: scripts/powershell/story-management.ps1 -Json
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON output for FEATURE_DIR, BACKLOG_FILE, STORY_ID (if provided). All paths must be absolute.

2. **Parse command arguments** from user input:
   - **Story ID**: US-### (optional for list/next operations)
   - **Action flags**:
     * `--list` - List stories (optionally filtered)
     * `--next` - Get next priority story to work on
     * `--status <status>` - Update story status
     * `--progress <completed>/<total>` - Update progress
     * `--start` - Mark story as in-progress
     * `--complete` - Mark story as complete
     * `--block <blocker-ids>` - Mark story as blocked
     * `--unblock` - Remove blocked status
     * `--show` - Show detailed story info (default if story ID provided)
   - **Filters** (for --list):
     * `--filter <status>` - Filter by status (draft/ready/in_progress/complete/blocked)
     * `--priority <priority>` - Filter by priority (p1/p2/p3)
     * `--epic <epic-id>` - Filter by EPIC ID

3. **Execute requested action**:

   ### Action: List Stories (`--list`)

   ```bash
   /speckit.story --list
   /speckit.story --list --filter ready
   /speckit.story --list --priority p1
   /speckit.story --list --epic EPIC-001
   ```

   a. Load backlog from BACKLOG_FILE
   b. Apply filters (status, priority, epic) if provided
   c. Sort by priority (P1 > P2 > P3), then by ID
   d. Display table:
      ```
      | Story ID | Title              | Priority | Status      | Progress | Dependencies |
      |----------|-------------------|----------|-------------|----------|--------------|
      | US-001   | User Login        | P1       | Complete    | 5/5      | -            |
      | US-002   | User Dashboard    | P1       | In Progress | 3/8      | US-001       |
      | US-003   | Admin Panel       | P2       | Ready       | 0/6      | US-001       |
      | US-004   | Data Export       | P2       | Blocked     | 0/4      | US-002,US-003|
      ```
   e. Summary:
      - Total stories: X
      - By status: Y ready, Z in progress, W complete
      - By priority: X P1, Y P2, Z P3

   ### Action: Get Next Story (`--next`)

   ```bash
   /speckit.story --next
   ```

   a. Load backlog
   b. Find all ready stories (status=ready, no blockers)
   c. Sort by priority
   d. Return highest priority ready story
   e. Display:
      ```
      ╔══════════════════════════════════════════════╗
      ║  NEXT STORY TO IMPLEMENT                     ║
      ╚══════════════════════════════════════════════╝

      Story ID: US-003
      Title: Admin Panel
      Priority: P2 (Should Have)
      Estimated Tasks: 6
      Estimated Hours: 12.0

      Dependencies: US-001 ✓ (Complete)

      Acceptance Criteria:
      - Admins can access admin panel
      - Admin can view user list
      - Admin can modify user permissions

      Ready to implement!

      Run: /speckit.tasks --story US-003
      ```
   f. If no ready stories:
      - Check for blocked stories
      - Show what's blocking progress
      - Suggest unblocking actions

   ### Action: Show Story Details (`--show` or default)

   ```bash
   /speckit.story US-002
   /speckit.story US-002 --show
   ```

   a. Load story from backlog
   b. Display full story details:
      ```
      ╔══════════════════════════════════════════════╗
      ║  STORY: US-002 - User Dashboard              ║
      ╚══════════════════════════════════════════════╝

      EPIC: EPIC-001 (User Management)
      Priority: P1 (Must Have - MVP)
      Status: In Progress

      Description:
      Implement user dashboard where users can view their profile,
      recent activity, and account settings.

      Progress: 3/8 tasks (37.5%)
      Estimated: 16.0 hours
      Actual: 8.5 hours

      Acceptance Criteria:
      ✓ Users can view profile information
      ✓ Users can see recent activity
      ✗ Users can access account settings
      ✗ Dashboard loads in <2 seconds

      Dependencies:
      - US-001: User Login ✓ (Complete)

      Blocked By: None

      Created: 2025-01-15T10:30:00
      Updated: 2025-01-16T14:20:00
      ```

   ### Action: Update Status (`--status`)

   ```bash
   /speckit.story US-002 --status ready
   /speckit.story US-002 --status in_progress
   /speckit.story US-002 --status complete
   ```

   a. Load story from backlog
   b. Validate status value (draft/ready/in_progress/complete/blocked)
   c. Update story status
   d. Update timestamps
   e. If status=complete: Set completed_at timestamp
   f. Save backlog
   g. Report: "Story US-002 status updated to: ready"

   ### Action: Update Progress (`--progress`)

   ```bash
   /speckit.story US-002 --progress 5/8
   /speckit.story US-002 --progress 5/8 --hours 12.5
   ```

   a. Load story
   b. Parse completed/total tasks
   c. Update metrics:
      - completed_tasks = X
      - actual_hours = Y (if --hours provided)
   d. Calculate progress percentage
   e. If completed_tasks >= estimated_tasks: Auto-complete story
   f. Save backlog
   g. Report:
      ```
      Story US-002 progress updated:
      - Tasks: 5/8 (62.5%)
      - Hours: 12.5 actual vs 16.0 estimated
      - Status: In Progress
      ```

   ### Action: Start Work (`--start`)

   ```bash
   /speckit.story US-003 --start
   ```

   a. Load story
   b. Check dependencies:
      - If dependencies incomplete → ERROR "Cannot start: dependencies incomplete"
      - List incomplete dependencies
   c. If dependencies OK:
      - Set status = in_progress
      - Update timestamp
      - Save backlog
   d. Report: "Started work on US-003: Admin Panel"
   e. Show story details

   ### Action: Mark Complete (`--complete`)

   ```bash
   /speckit.story US-002 --complete
   ```

   a. Load story
   b. Set status = complete
   c. Set completed_tasks = estimated_tasks
   d. Set completed_at timestamp
   e. Check for stories blocked by this one:
      - Find stories with this ID in dependencies
      - Update their blocked status
   f. Save backlog
   g. Report:
      ```
      ✓ Story US-002 marked complete!

      Unblocked stories:
      - US-004: Data Export (now ready)
      - US-005: Reporting (now ready)
      ```

   ### Action: Block Story (`--block`)

   ```bash
   /speckit.story US-004 --block US-002,US-003
   ```

   a. Load story
   b. Parse blocker IDs
   c. Validate blockers exist
   d. Set status = blocked
   e. Set blocked_by = [blocker IDs]
   f. Save backlog
   g. Report:
      ```
      Story US-004 marked as blocked by:
      - US-002: User Dashboard (in progress)
      - US-003: Admin Panel (ready)
      ```

   ### Action: Unblock Story (`--unblock`)

   ```bash
   /speckit.story US-004 --unblock
   ```

   a. Load story
   b. Clear blocked_by list
   c. Set status = ready
   d. Save backlog
   e. Report: "Story US-004 unblocked and marked ready"

4. **Update dependency status** (automatic):
   - After any status change, run dependency check:
     * For each story, check if dependencies are complete
     * Auto-block stories with incomplete dependencies
     * Auto-unblock stories when dependencies complete
   - Report any automatic status changes

5. **Report summary** (for list/status operations):
   - Stories modified
   - Current backlog state
   - Suggestions for next actions

## Story Management Rules

### Status Transitions

```
DRAFT → READY → IN_PROGRESS → COMPLETE
   ↓       ↓          ↓
   └───────┴──────→ BLOCKED ──→ READY
```

**Valid transitions:**
- DRAFT → READY (when story is fully defined)
- READY → IN_PROGRESS (start work)
- READY → BLOCKED (dependency issue)
- IN_PROGRESS → COMPLETE (all tasks done)
- IN_PROGRESS → BLOCKED (blocker discovered)
- BLOCKED → READY (blocker resolved)

**Invalid transitions** (ERROR):
- DRAFT → IN_PROGRESS (must go through READY)
- COMPLETE → * (completed stories cannot change)

### Dependency Rules

1. **Cannot start story** with incomplete dependencies
2. **Auto-block** if dependency becomes incomplete
3. **Auto-unblock** when all dependencies complete
4. **Cannot complete** if story has blockers

### Progress Tracking

- **Auto-complete**: If completed_tasks ≥ estimated_tasks → status=complete
- **Actual hours** tracked separately from estimates
- **Test coverage** optional metric (0-100%)

## Integration with Other Commands

**After `/speckit.epic`:**
- Stories initialized in `backlog.json`
- All stories start in DRAFT status

**Before `/speckit.tasks --story US-###`:**
- Check story is READY or IN_PROGRESS
- If DRAFT → ERROR "Story not ready for implementation"

**During `/speckit.implement`:**
- Auto-update progress as tasks complete
- Auto-mark complete when all tasks done

**Story workflow:**
1. `/speckit.epic` - Decompose EPIC into stories
2. `/speckit.story US-001 --status ready` - Mark MVP story ready
3. `/speckit.story --next` - Confirm next story
4. `/speckit.tasks --story US-001` - Generate tasks for story
5. `/speckit.implement` - Execute implementation
6. `/speckit.story US-001` - Check progress
7. Repeat for next story

## Example Usage

```bash
# List all stories
/speckit.story --list

# List ready stories
/speckit.story --list --filter ready

# Get next story to work on
/speckit.story --next

# Show story details
/speckit.story US-002

# Mark story ready
/speckit.story US-001 --status ready

# Start work on story
/speckit.story US-001 --start

# Update progress
/speckit.story US-001 --progress 5/10 --hours 12.5

# Mark complete
/speckit.story US-001 --complete

# Block story
/speckit.story US-004 --block US-002,US-003

# Unblock story
/speckit.story US-004 --unblock
```

## Error Handling

**If backlog.json not found:**
- ERROR: "Story backlog not initialized"
- SUGGEST: "Run `/speckit.epic` first to decompose feature into stories"

**If story ID not found:**
- ERROR: "Story US-### not found in backlog"
- LIST: Available story IDs

**If invalid status transition:**
- ERROR: "Cannot transition from COMPLETE to IN_PROGRESS"
- SHOW: Valid status transitions diagram

**If dependencies incomplete:**
- ERROR: "Cannot start US-004: dependencies incomplete"
- LIST: Incomplete dependencies with their status
- SUGGEST: Complete dependencies first

**If circular dependencies detected:**
- ERROR: "Circular dependency detected"
- SHOW: Dependency chain causing cycle

## Notes

- Story management requires RisoTech mode or EPIC decomposition
- Backlog stored in `FEATURE_DIR/stories/backlog.json`
- Story files optional: `FEATURE_DIR/stories/US-###.md`
- Progress auto-tracked during `/speckit.implement`
- Dependencies auto-checked on every status change
