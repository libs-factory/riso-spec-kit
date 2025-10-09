#!/usr/bin/env bash
# epic-breakdown.sh - Helper script for EPIC decomposition workflow
# Provides feature context for /speckit.epic command

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Default values
JSON_OUTPUT=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Change to project root
cd "$PROJECT_ROOT"

# Find .specify directory
SPECIFY_DIR=".specify"
if [ ! -d "$SPECIFY_DIR" ]; then
    echo "Error: .specify directory not found" >&2
    exit 1
fi

# Get current git branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

# Extract feature ID from branch name (e.g., feature/001-epic-integration -> 001-epic-integration)
FEATURE_ID=""
if [[ "$CURRENT_BRANCH" =~ ^feature/(.+)$ ]]; then
    FEATURE_ID="${BASH_REMATCH[1]}"
elif [[ "$CURRENT_BRANCH" =~ ^([0-9]{3}-.+)$ ]]; then
    FEATURE_ID="${BASH_REMATCH[1]}"
else
    # Default to looking for newest feature directory
    FEATURE_ID=$(ls -1 "$SPECIFY_DIR/specs" 2>/dev/null | sort -r | head -n1 || echo "")
fi

if [ -z "$FEATURE_ID" ]; then
    echo "Error: Could not determine feature ID from branch or specs directory" >&2
    exit 1
fi

# Set feature directory
FEATURE_DIR="$PROJECT_ROOT/$SPECIFY_DIR/specs/$FEATURE_ID"

if [ ! -d "$FEATURE_DIR" ]; then
    echo "Error: Feature directory not found: $FEATURE_DIR" >&2
    exit 1
fi

# Required files
SPEC_FILE="$FEATURE_DIR/spec.md"
PLAN_FILE="$FEATURE_DIR/plan.md"

# Optional files
DATA_MODEL_FILE="$FEATURE_DIR/data-model.md"
TASKS_FILE="$FEATURE_DIR/tasks.md"
EPIC_BREAKDOWN_FILE="$FEATURE_DIR/epic-breakdown.md"
CONTRACTS_DIR="$FEATURE_DIR/contracts"
BACKLOG_FILE="$FEATURE_DIR/stories/backlog.json"

# Check required files
if [ ! -f "$SPEC_FILE" ]; then
    echo "Error: spec.md not found. Run /speckit.specify first." >&2
    exit 1
fi

if [ ! -f "$PLAN_FILE" ]; then
    echo "Error: plan.md not found. Run /speckit.plan first." >&2
    exit 1
fi

# Build available docs list
AVAILABLE_DOCS=()
AVAILABLE_DOCS+=("spec.md")
AVAILABLE_DOCS+=("plan.md")

[ -f "$DATA_MODEL_FILE" ] && AVAILABLE_DOCS+=("data-model.md")
[ -f "$TASKS_FILE" ] && AVAILABLE_DOCS+=("tasks.md")
[ -f "$EPIC_BREAKDOWN_FILE" ] && AVAILABLE_DOCS+=("epic-breakdown.md")
[ -d "$CONTRACTS_DIR" ] && AVAILABLE_DOCS+=("contracts/")
[ -f "$BACKLOG_FILE" ] && AVAILABLE_DOCS+=("stories/backlog.json")

# Output
if [ "$JSON_OUTPUT" = true ]; then
    # Build JSON array for available docs
    DOCS_JSON="["
    for i in "${!AVAILABLE_DOCS[@]}"; do
        [ $i -gt 0 ] && DOCS_JSON+=","
        DOCS_JSON+="\"${AVAILABLE_DOCS[$i]}\""
    done
    DOCS_JSON+="]"

    cat <<EOF
{
  "feature_dir": "$FEATURE_DIR",
  "feature_id": "$FEATURE_ID",
  "spec_file": "$SPEC_FILE",
  "plan_file": "$PLAN_FILE",
  "data_model_file": "$DATA_MODEL_FILE",
  "tasks_file": "$TASKS_FILE",
  "epic_breakdown_file": "$EPIC_BREAKDOWN_FILE",
  "contracts_dir": "$CONTRACTS_DIR",
  "backlog_file": "$BACKLOG_FILE",
  "available_docs": $DOCS_JSON,
  "epic_exists": $([ -f "$EPIC_BREAKDOWN_FILE" ] && echo "true" || echo "false"),
  "backlog_exists": $([ -f "$BACKLOG_FILE" ] && echo "true" || echo "false")
}
EOF
else
    echo "Feature Directory: $FEATURE_DIR"
    echo "Feature ID: $FEATURE_ID"
    echo "Spec File: $SPEC_FILE"
    echo "Plan File: $PLAN_FILE"
    echo ""
    echo "Available Documents:"
    for doc in "${AVAILABLE_DOCS[@]}"; do
        echo "  - $doc"
    done
    echo ""
    [ -f "$EPIC_BREAKDOWN_FILE" ] && echo "EPIC breakdown exists: Yes" || echo "EPIC breakdown exists: No"
    [ -f "$BACKLOG_FILE" ] && echo "Story backlog exists: Yes" || echo "Story backlog exists: No"
fi

exit 0
