
## ⚡ Get started

### 1. Install Specify

Choose your preferred installation method:

#### Option 1: Persistent Installation (Recommended)

Install once and use everywhere:

```bash
uv tool install specify-cli --from git+https://github.com/libs-factory/riso-spec-kit.git
```

Then use the tool directly:

```bash
specify init <PROJECT_NAME>
specify check
```

#### Option 2: One-time Usage

Run directly without installing:

```bash
uvx --from git+https://github.com/libs-factory/riso-spec-kit.git specify init <PROJECT_NAME>
```

**Benefits of persistent installation:**

- Tool stays installed and available in PATH
- No need to create shell aliases
- Better tool management with `uv tool list`, `uv tool upgrade`, `uv tool uninstall`
- Cleaner shell configuration

---

## 📋 Core Workflows

### 1. Initialize Spec Kit for New Project

Complete setup guide with all RisoTech enhancement options.

#### Step 1: Install Specify CLI

Choose your installation method:

**Option A: Persistent Installation (Recommended)**
```bash
# Install once, use everywhere
uv tool install specify-cli --from git+https://github.com/libs-factory/riso-spec-kit.git

# Verify installation
uv tool list | grep specify-cli
# Expected output: specify-cli v0.1.0
```

**Option B: One-time Usage**
```bash
# Run without installing (for testing)
uvx --from git+https://github.com/libs-factory/riso-spec-kit.git specify init <PROJECT_NAME>
```

---

#### Step 2: Enable RisoTech Features (Optional but Recommended)

Choose your feature adoption path:

**Option A: Full RisoTech Mode (All Features - Recommended for New Projects)**
```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
export SPECIFY_RISOTECH_MODE=true

# This enables ALL RisoTech enhancements:
# ✅ Tiered Constitution Framework
# ✅ EPIC Decomposition (for 30+ task features)
# ✅ Story Management with dependency tracking
# ✅ Workflow Orchestration with stage detection
# ✅ Progress Tracking & Reporting
# ✅ Risk & Bottleneck Analysis

# Reload shell
source ~/.bashrc  # or ~/.zshrc
```

**Option B: Selective Features (Gradual Adoption)**
```bash
# Enable only specific features

# Constitution Framework (recommended)
export SPECIFY_TIERED_CONSTITUTION=true

# EPIC Decomposition (for large features)
export SPECIFY_EPIC_DECOMPOSITION=true

# Story Tracking (for story-by-story development)
export SPECIFY_STORY_TRACKING=true

# Progress Reporting (for status reports)
export SPECIFY_PROGRESS_REPORTING=true

# Workflow Settings (fine-tuning)
export SPECIFY_AUTO_UPDATE_BACKLOG=true        # Auto-save story progress
export SPECIFY_TRACK_ACTUAL_HOURS=true         # Track actual hours vs estimated
export SPECIFY_CALCULATE_VELOCITY=true         # Calculate story velocity
export SPECIFY_REQUIRE_READY_STATUS=true       # Require story to be READY before implementation
export SPECIFY_AUTO_UNBLOCK_STORIES=true       # Auto-unblock stories when dependencies complete
export SPECIFY_BLOCK_ON_INCOMPLETE_DEPS=true   # Auto-block stories with incomplete dependencies
```

**Option C: Standard Mode (No RisoTech Features)**
```bash
# Don't set any environment variables
# Use traditional Specify CLI workflow
# All new features are opt-in, so default behavior is unchanged
```

---

#### Step 3: Initialize Project Structure

```bash
# Navigate to your project directory
cd /path/to/your/project

# Initialize Spec Kit with your preferred AI agent
specify init my-project --ai claude    # For Claude
# or
specify init my-project --ai copilot   # For GitHub Copilot
# or
specify init my-project --ai cursor    # For Cursor

# This creates:
# .specify/
# ├── memory/
# │   ├── project-context.md      # Project overview
# │   └── technical-context.md    # Tech stack details
# ├── specs/                      # Feature specifications (empty initially)
# └── templates/                  # Workflow command templates
```

---

#### Step 4: Set Up Project Constitution (RisoTech Feature)

Create your project's governing principles with three-tier priority system.

**Option A: Use a Technology Preset (Quick Start - Recommended)**

```bash
# React + TypeScript
/speckit.constitution-upgrade --preset react-typescript

# Creates tiered constitution:
# CORE (Non-negotiable):
#   - TypeScript strict mode required
#   - 80%+ test coverage
#   - No 'any' types except migrations
#   - Security: Input validation, XSS prevention
#
# HIGH-PRIORITY (Strong recommendations):
#   - React Hooks over class components
#   - Functional programming patterns
#   - CSS-in-JS or Tailwind
#   - Component composition over inheritance
#
# FLEXIBLE (Guidelines):
#   - Prefer named exports
#   - File naming: kebab-case
#   - Max file length: 300 lines
```

**Other Presets:**
```bash
# Next.js + Tailwind
/speckit.constitution-upgrade --preset nextjs-tailwind

# Django + PostgreSQL
/speckit.constitution-upgrade --preset django-postgresql

# List all available presets
/speckit.constitution-upgrade --list
```

**Option B: Create Custom Constitution**

```bash
/speckit.constitution-upgrade --custom

# Follow interactive prompts to define:
# 1. CORE rules (must-follow, enforced in code review)
#    Example: "All API endpoints must have authentication"
#
# 2. HIGH-PRIORITY rules (strong recommendations)
#    Example: "Use repository pattern for data access"
#
# 3. FLEXIBLE rules (guidelines, team preferences)
#    Example: "Prefer async/await over .then() chains"
```

**Constitution File Created:**
```
.specify/constitution.md

# Structure:
## CORE Rules (Non-Negotiable)
- Rule 1: [Title]
  - Description: [Details]
  - Rationale: [Why it's CORE]
  - Examples: [Code examples]

## HIGH-PRIORITY Rules (Strong Recommendations)
- Rule 2: [Title]
  ...

## FLEXIBLE Rules (Guidelines)
- Rule 3: [Title]
  ...
```

---

#### Step 5: Configure Project Context

Fill in project-specific information to provide AI context:

**A. Project Context** (`.specify/memory/project-context.md`)

```bash
# Edit with your favorite editor
code .specify/memory/project-context.md

# Fill in:
# 1. Project Overview
#    - Name: "Acme E-commerce Platform"
#    - Description: "B2C e-commerce with inventory management"
#    - Business Goals: "Increase online sales by 30%"
#
# 2. Target Users
#    - Primary: "Online shoppers (18-45 years old)"
#    - Secondary: "Store managers, inventory staff"
#
# 3. Key Features
#    - Product catalog with search
#    - Shopping cart & checkout
#    - Inventory management dashboard
#    - Analytics & reporting
#
# 4. Success Metrics
#    - User engagement: "Average session duration > 5 minutes"
#    - Performance: "Page load time < 2 seconds"
#    - Quality: "Bug rate < 1 per 1000 users/month"
```

**B. Technical Context** (`.specify/memory/technical-context.md`)

```bash
code .specify/memory/technical-context.md

# Fill in:
# 1. Tech Stack
#    Frontend: React 18 + TypeScript + Vite
#    Backend: Node.js + Express + PostgreSQL
#    Deployment: Docker + AWS ECS
#    CI/CD: GitHub Actions
#
# 2. Architecture Decisions
#    - Microservices architecture (auth, catalog, orders)
#    - Event-driven communication (RabbitMQ)
#    - REST API + GraphQL for complex queries
#
# 3. Development Environment
#    - Node.js 20+
#    - PostgreSQL 15
#    - Redis for caching
#    - Docker Compose for local development
#
# 4. Coding Standards
#    - ESLint + Prettier
#    - Husky pre-commit hooks
#    - Conventional commits
#    - PR requires 2 approvals
```

---

#### Step 6: Verify Setup

**Run Spec Kit Check**

```bash
# Comprehensive validation
specify check

# Expected output:
# ✅ .specify/ directory exists
# ✅ constitution.md configured (15 rules: 4 CORE, 6 HIGH-PRIORITY, 5 FLEXIBLE)
# ✅ project-context.md configured
# ✅ technical-context.md configured
# ✅ templates/ directory ready
# ✅ RisoTech mode: ENABLED
#
# Feature Status:
# ✅ Tiered Constitution: ENABLED
# ✅ EPIC Decomposition: ENABLED
# ✅ Story Tracking: ENABLED
# ✅ Progress Reporting: ENABLED
#
# 🎉 Spec Kit initialized successfully!
# 📚 Next: Create your first feature with /speckit.specify
```

---

**🎉 Setup Complete!**

Your project is now configured with:

✅ **Spec Kit Core**
- Project structure initialized
- Templates ready for workflows

✅ **RisoTech Enhancements** (if enabled)
- 📜 Tiered Constitution (CORE/HIGH-PRIORITY/FLEXIBLE)
- 📊 EPIC Decomposition (automatic for 30+ task features)
- 📈 Story Management (lifecycle tracking with dependencies)
- 🎯 Workflow Orchestration (stage detection & validation)
- 📊 Progress Tracking (task/story/feature levels)

✅ **Project Context**
- Business goals documented
- Technical stack defined
- Team standards established

**Next:** Create your first feature (see Section 2: Feature Development Workflow)

---

### 2. Feature Development Workflow (Specify to Implement)

Complete workflow from feature idea to implementation:

#### Standard Workflow (Small/Medium Features)

**Step 1: Create Feature Specification**

```bash
# Create a new feature branch
git checkout -b feature/user-authentication

# Generate feature specification
/speckit.specify "Implement user authentication with email/password and social login (Google, GitHub)"

# This creates:
# .specify/specs/001-user-authentication/
# ├── spec.md          # Feature specification with user stories
# └── README.md        # Feature overview

# Review and refine spec.md:
# - User stories with priorities (P1, P2, P3)
# - Acceptance criteria
# - Success metrics
# - Out of scope items
```

**Step 2: Generate Implementation Plan**

```bash
# Generate technical plan
/speckit.plan

# This creates:
# .specify/specs/001-user-authentication/
# ├── spec.md
# ├── plan.md          # Technical implementation plan
# ├── data-model.md    # Database schema (if needed)
# ├── contracts/       # API contracts (if needed)
# └── research.md      # Technical research notes

# Detects feature complexity:
# - SMALL (1-5 tasks): Simple feature
# - MEDIUM (6-15 tasks): Standard feature
# - LARGE (16-30 tasks): Complex feature - consider EPIC
# - EPIC (30+ tasks): Very complex - requires decomposition
```

**Step 3: Generate Task Breakdown**

```bash
# Generate actionable tasks
/speckit.tasks

# This creates:
# .specify/specs/001-user-authentication/tasks.md
# - Phase 1: Setup
# - Phase 2: Implementation by user story
# - Phase 3: Integration & testing
# - Task numbering (T001, T002, ...)
# - [P] markers for parallel tasks
# - Dependencies clearly marked
```

**Step 4: Implement**

```bash
# Execute implementation
/speckit.implement

# Process:
# 1. Validates constitution compliance (if enabled)
# 2. Checks checklist prerequisites
# 3. Executes tasks phase-by-phase
# 4. Marks tasks complete in tasks.md
# 5. Updates progress tracking
```

**Step 5: Verify & Commit**

```bash
# Verify all tasks complete
grep "- \[ \]" .specify/specs/001-user-authentication/tasks.md
# Should return empty (all tasks marked [X])

# Commit changes
git add .
git commit -m "feat: Implement user authentication

- Add email/password authentication
- Add Google OAuth integration
- Add GitHub OAuth integration
- Add JWT token management
- Add password reset flow

🤖 Generated with Spec Kit"

# Create pull request
git push origin feature/user-authentication
gh pr create --fill
```

#### EPIC Workflow (Large/Complex Features 30+ tasks)

> 💡 **When to use EPIC workflow:**
> - Feature estimates 30+ tasks
> - Multiple independent user journeys
> - Implementation will span weeks/months
> - Need incremental delivery (MVP → enhancements)

**Key difference from Standard Workflow:**
EPIC workflow breaks features into **user stories**, then generates **tasks per story**.

```
Standard:  specify → plan → tasks (all 45) → implement (all at once)
EPIC:      specify → plan → epic → story → tasks (8-12) → implement (per story) ↻
```

**Step 1-2: Same as Standard Workflow**

```bash
git checkout -b feature/user-management-system

/speckit.specify "Build comprehensive user management system with authentication, authorization, profile management, activity tracking, and admin dashboard"

/speckit.plan
# Output: "Feature complexity: EPIC (~45 tasks estimated)"
# Recommendation: "Consider running /speckit.epic to decompose into user stories"
```

**Step 3: Decompose into Stories**

```bash
# Enable RisoTech EPIC mode
export SPECIFY_RISOTECH_MODE=true

# Decompose EPIC into user stories
/speckit.epic

# This creates:
# .specify/specs/001-user-management/
# ├── epic-breakdown.md    # Story decomposition
# └── stories/
#     ├── backlog.json     # Story tracking
#     ├── US-001.md        # MVP: User Authentication
#     ├── US-002.md        # User Profile Management
#     ├── US-003.md        # Role-Based Access Control
#     ├── US-004.md        # Activity Tracking
#     └── US-005.md        # Admin Dashboard

# Review epic-breakdown.md:
# - Story breakdown by priority (P1, P2, P3)
# - Dependency graph
# - Implementation strategy (MVP first)
```

**Step 4: View & Prioritize Stories**

```bash
# List all stories
/speckit.story --list

# Output:
# | Story ID | Title                    | Priority | Status | Progress | Dependencies |
# |----------|--------------------------|----------|--------|----------|--------------|
# | US-001   | User Authentication      | P1       | DRAFT  | 0/10     | -            |
# | US-002   | User Profile Management  | P1       | DRAFT  | 0/8      | US-001       |
# | US-003   | Role-Based Access Control| P2       | DRAFT  | 0/12     | US-001       |
# | US-004   | Activity Tracking        | P2       | DRAFT  | 0/6      | US-002       |
# | US-005   | Admin Dashboard          | P3       | DRAFT  | 0/9      | US-003,US-004|

# Mark MVP story as ready
/speckit.story US-001 --status ready
```

**Step 5: Implement Story-by-Story**

> ⚠️ **Important**: Each story requires its own task breakdown before implementation.
> Stories define **WHAT** to build, tasks define **HOW** to build it.

```bash
# A. Get next ready story
/speckit.story --next
# Output: US-001 (MVP story, no dependencies, status: READY)

# B. Generate tasks for THIS story only
/speckit.tasks --story US-001
# Creates: .specify/specs/001-user-management/tasks.md
# Contains 8-12 tasks specific to US-001:
#   T001: Create User model schema
#   T002: Implement password hashing
#   T003: Create login API endpoint
#   T004: Add JWT token generation
#   T005: Implement login form UI
#   T006: Add error handling
#   T007: Write unit tests
#   T008: Integration testing

# C. Implement the story using generated tasks
/speckit.implement --story US-001
# Reads tasks.md and executes each task
# Auto-updates backlog.json with progress
# Marks tasks complete as you go: [X]

# D. Check implementation progress
/speckit.story US-001
# Output: "Tasks 8/10 (80%), Estimated 20h, Actual 18.5h"

# E. Mark story complete when all tasks done
/speckit.story US-001 --complete
# Validates all tasks marked [X]
# Updates backlog.json: status → COMPLETE
# Auto-unblocks dependent stories (US-002, US-003)

# F. Commit the completed story
git add .
git commit -m "feat: Complete US-001 - User Authentication

Implemented:
- User model with email/password fields
- Password hashing with bcrypt
- Login API with JWT tokens
- Login form with validation
- Full test coverage (unit + integration)

🤖 Generated with Spec Kit
Story: US-001 (10/10 tasks complete, 18.5h actual vs 20h estimated)"

git push origin feature/user-management-system

# G. Move to next story - REPEAT THE CYCLE
/speckit.story --next
# Output: US-002 - User Profile Management (now unblocked)

/speckit.tasks --story US-002
# Generate fresh tasks for US-002 (different from US-001)

/speckit.implement --story US-002
# Implement US-002 tasks

# Continue this cycle until all stories complete:
# story → tasks → implement → complete → next story
```

**Why this approach?**

- ✅ **Focused scope**: Work on 8-12 tasks at a time (not 45+)
- ✅ **Clear progress**: Track completion per story
- ✅ **Smaller PRs**: One PR per story = easier reviews
- ✅ **Better estimates**: Story-level estimation accuracy
- ✅ **Flexible pivots**: Can reprioritize remaining stories anytime

**Step 6: Track Overall Progress**

```bash
# Generate comprehensive progress report
/speckit.status --format markdown --save

# Creates: .specify/specs/001-user-management/progress-report.md
# Contains:
# - Workflow stage progress (specify ✓, plan ✓, epic ✓, stories 3/5...)
# - Story breakdown table (completed, in progress, blocked)
# - Task completion metrics per story
# - Time tracking (estimated vs actual hours)
# - Velocity calculation (stories per week)
# - Risk analysis (blocked stories, overdue tasks)
# - Bottleneck detection (slow stories, dependency chains)
# - Timeline projection (estimated completion date)
# - Next actions (what to do next)

# Quick status check (console output)
/speckit.status

# Example output:
# ╔══════════════════════════════════════════════════════════════╗
# ║  FEATURE PROGRESS: User Management System                    ║
# ╚══════════════════════════════════════════════════════════════╝
#
# Feature ID: 001-user-management
# Current Stage: Implementation (EPIC mode)
# Overall Progress: 60% complete
#
# 📊 Story Progress:
# ┌──────────┬───────────────────────┬──────────┬─────────────┬──────────┐
# │ Story ID │ Title                 │ Priority │ Status      │ Progress │
# ├──────────┼───────────────────────┼──────────┼─────────────┼──────────┤
# │ US-001   │ User Authentication   │ P1       │ ✅ Complete │ 10/10    │
# │ US-002   │ Profile Management    │ P1       │ ✅ Complete │ 8/8      │
# │ US-003   │ Access Control        │ P2       │ ✅ Complete │ 12/12    │
# │ US-004   │ Activity Tracking     │ P2       │ 🔄 Progress │ 4/6      │
# │ US-005   │ Admin Dashboard       │ P3       │ ⏳ Ready    │ 0/9      │
# └──────────┴───────────────────────┴──────────┴─────────────┴──────────┘
#
# 📈 Metrics:
# • Stories: 3/5 complete (60%)
# • Tasks: 34/45 complete (75.6%)
# • Estimated time: 90h total, 68h spent
# • Velocity: 1.2 stories/week
# • Estimated completion: 2025-10-15
#
# ⚠️ Risks & Blockers:
# • US-004 behind schedule (50% over estimate)
# • US-005 blocked by US-004 completion
#
# 🎯 Next Actions:
# 1. Focus on completing US-004 (2 tasks remaining)
# 2. Review US-004 for technical debt
# 3. Prepare US-005 for implementation (review dependencies)
```

**When to check status:**
- Daily standups: Quick `/speckit.status` overview
- Weekly reviews: Generate full report with `--save`
- Before story transitions: Verify dependencies complete
- When estimates feel off: Check velocity and adjust

---

### 3. Update Spec Kit Version

Keep Spec Kit up-to-date with latest features and improvements:

#### Check Current Version

```bash
# Check installed version
uv tool list | grep specify-cli

# Example output:
# specify-cli v0.1.0 (from git+https://github.com/libs-factory/riso-spec-kit.git@main)
```

#### Update to Latest Version

**Method 1: Using uv tool upgrade (Recommended)**

```bash
# Upgrade to latest version from main branch
uv tool upgrade specify-cli --from git+https://github.com/libs-factory/riso-spec-kit.git

# Verify upgrade
uv tool list | grep specify-cli
```

**Method 2: Reinstall from scratch**

```bash
# Uninstall current version
uv tool uninstall specify-cli

# Install latest version
uv tool install specify-cli --from git+https://github.com/libs-factory/riso-spec-kit.git

# Verify installation
uv tool list | grep specify-cli
```

#### Update Project Templates

After upgrading Spec Kit, manually update your project's templates:

```bash
# Navigate to project directory
cd /path/to/your/project

# Backup existing templates (optional but recommended)
cp -r .specify/templates .specify/templates.backup

# Clone or download latest spec kit
cd /tmp
git clone https://github.com/libs-factory/riso-spec-kit.git

# Copy updated templates to your project
cp -r riso-spec-kit/templates/* /path/to/your/project/.specify/templates/

# Verify update
ls -la /path/to/your/project/.specify/templates/

# Review changelog for breaking changes
# https://github.com/libs-factory/riso-spec-kit/blob/main/CHANGELOG.md
```

**Alternative: Re-initialize templates**

```bash
# Navigate to your project
cd /path/to/your/project

# Backup current .specify directory
mv .specify .specify.backup

# Re-initialize (will prompt for AI agent selection)
specify init --here

# Restore your customized files
cp .specify.backup/memory/constitution.md .specify/memory/
cp .specify.backup/memory/project-context.md .specify/memory/
cp .specify.backup/memory/technical-context.md .specify/memory/

# Copy back any custom specs
cp -r .specify.backup/specs/* .specify/specs/ 2>/dev/null || true

# Remove backup after verification
rm -rf .specify.backup
```

---
