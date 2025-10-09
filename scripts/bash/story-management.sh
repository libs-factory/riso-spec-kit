#!/usr/bin/env bash
# story-management.sh - Helper script for story management workflow
# Provides story and backlog context for /speckit.story command

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Default values
JSON_OUTPUT=false
STORY_ID=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        --story)
            STORY_ID="$2"
            shift 2
            ;;
        *)
            # Could be story ID without --story flag
            if [[ $1 =~ ^US-[0-9]{3}$ ]]; then
                STORY_ID="$1"
            fi
            shift
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

# Extract feature ID from branch name
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

# Story-related files
BACKLOG_FILE="$FEATURE_DIR/stories/backlog.json"
EPIC_BREAKDOWN_FILE="$FEATURE_DIR/epic-breakdown.md"
STORIES_DIR="$FEATURE_DIR/stories"

# Check if story management is initialized
BACKLOG_EXISTS=false
EPIC_EXISTS=false

if [ -f "$BACKLOG_FILE" ]; then
    BACKLOG_EXISTS=true
fi

if [ -f "$EPIC_BREAKDOWN_FILE" ]; then
    EPIC_EXISTS=true
fi

# If no backlog and no epic, error
if [ "$BACKLOG_EXISTS" = false ] && [ "$EPIC_EXISTS" = false ]; then
    echo "Error: Story backlog not initialized. Run /speckit.epic first." >&2
    exit 1
fi

# Build story file path if story ID provided
STORY_FILE=""
if [ -n "$STORY_ID" ]; then
    STORY_FILE="$STORIES_DIR/${STORY_ID}.md"
fi

# Count total stories (from backlog or epic)
TOTAL_STORIES=0
if [ "$BACKLOG_EXISTS" = true ]; then
    # Count stories in backlog.json
    TOTAL_STORIES=$(jq 'length' "$BACKLOG_FILE" 2>/dev/null || echo "0")
elif [ "$EPIC_EXISTS" = true ]; then
    # Count user story headers in epic-breakdown.md
    TOTAL_STORIES=$(grep -c "^### Story [0-9]" "$EPIC_BREAKDOWN_FILE" 2>/dev/null || echo "0")
fi

# Output
if [ "$JSON_OUTPUT" = true ]; then
    cat <<EOF
{
  "feature_dir": "$FEATURE_DIR",
  "feature_id": "$FEATURE_ID",
  "backlog_file": "$BACKLOG_FILE",
  "epic_breakdown_file": "$EPIC_BREAKDOWN_FILE",
  "stories_dir": "$STORIES_DIR",
  "story_id": "$STORY_ID",
  "story_file": "$STORY_FILE",
  "backlog_exists": $BACKLOG_EXISTS,
  "epic_exists": $EPIC_EXISTS,
  "total_stories": $TOTAL_STORIES
}
EOF
else
    echo "Feature Directory: $FEATURE_DIR"
    echo "Feature ID: $FEATURE_ID"
    echo ""
    echo "Story Management:"
    echo "  Backlog: $([ "$BACKLOG_EXISTS" = true ] && echo "Initialized" || echo "Not initialized")"
    echo "  EPIC: $([ "$EPIC_EXISTS" = true ] && echo "Exists" || echo "Not exists")"
    echo "  Total Stories: $TOTAL_STORIES"
    echo ""
    if [ -n "$STORY_ID" ]; then
        echo "Target Story: $STORY_ID"
        [ -f "$STORY_FILE" ] && echo "  Story file: Exists" || echo "  Story file: Not found"
    fi
fi

exit 0
