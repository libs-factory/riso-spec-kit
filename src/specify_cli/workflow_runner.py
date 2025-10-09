"""Workflow orchestration for Specify CLI commands."""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict, Callable
from pathlib import Path
import json
from datetime import datetime

from .config import SpecifyConfig
from .story_manager import StoryBacklog, UserStory, StoryStatus


class WorkflowStage(Enum):
    """Stages in the Specify workflow."""
    SPECIFY = "specify"          # /speckit.specify
    CLARIFY = "clarify"          # /speckit.clarify
    PLAN = "plan"                # /speckit.plan
    TASKS = "tasks"              # /speckit.tasks
    IMPLEMENT = "implement"      # /speckit.implement


@dataclass
class WorkflowContext:
    """Context for workflow execution."""
    feature_dir: Path
    feature_id: str
    current_stage: WorkflowStage
    completed_stages: List[WorkflowStage]
    story_id: Optional[str] = None
    epic_mode: bool = False
    backlog: Optional[StoryBacklog] = None

    def is_stage_complete(self, stage: WorkflowStage) -> bool:
        """Check if a stage is complete."""
        return stage in self.completed_stages

    def can_proceed_to(self, stage: WorkflowStage) -> bool:
        """Check if we can proceed to a given stage."""
        stage_order = [
            WorkflowStage.SPECIFY,
            WorkflowStage.PLAN,
            WorkflowStage.TASKS,
            WorkflowStage.IMPLEMENT
        ]

        try:
            target_index = stage_order.index(stage)
            # All previous stages must be complete
            for i in range(target_index):
                if not self.is_stage_complete(stage_order[i]):
                    return False
            return True
        except ValueError:
            return False


class WorkflowRunner:
    """Orchestrates the full Specify workflow."""

    def __init__(self, feature_dir: Path):
        """Initialize workflow runner.

        Args:
            feature_dir: Feature directory
        """
        self.feature_dir = feature_dir
        self.feature_id = feature_dir.name
        self.config = SpecifyConfig()

        # Check if EPIC mode
        self.epic_breakdown = feature_dir / "epic-breakdown.md"
        self.epic_mode = self.epic_breakdown.exists()

        # Load backlog if exists
        backlog_file = feature_dir / "stories" / "backlog.json"
        self.backlog = StoryBacklog(feature_dir) if backlog_file.exists() else None

    def detect_current_stage(self) -> WorkflowStage:
        """Detect the current workflow stage based on existing files.

        Returns:
            Current workflow stage
        """
        spec_file = self.feature_dir / "spec.md"
        plan_file = self.feature_dir / "plan.md"
        tasks_file = self.feature_dir / "tasks.md"

        if not spec_file.exists():
            return WorkflowStage.SPECIFY
        elif not plan_file.exists():
            return WorkflowStage.PLAN
        elif not tasks_file.exists():
            return WorkflowStage.TASKS
        else:
            return WorkflowStage.IMPLEMENT

    def get_completed_stages(self) -> List[WorkflowStage]:
        """Get list of completed workflow stages.

        Returns:
            List of completed stages
        """
        completed = []

        spec_file = self.feature_dir / "spec.md"
        plan_file = self.feature_dir / "plan.md"
        tasks_file = self.feature_dir / "tasks.md"

        if spec_file.exists():
            completed.append(WorkflowStage.SPECIFY)
        if plan_file.exists():
            completed.append(WorkflowStage.PLAN)
        if tasks_file.exists():
            completed.append(WorkflowStage.TASKS)

        # Check if implementation is complete (all tasks marked done)
        if tasks_file.exists():
            content = tasks_file.read_text()
            # Simple heuristic: if no unchecked tasks remain
            if "- [ ]" not in content:
                completed.append(WorkflowStage.IMPLEMENT)

        return completed

    def create_context(self, story_id: Optional[str] = None) -> WorkflowContext:
        """Create workflow context.

        Args:
            story_id: Optional story ID for single-story workflow

        Returns:
            WorkflowContext instance
        """
        return WorkflowContext(
            feature_dir=self.feature_dir,
            feature_id=self.feature_id,
            current_stage=self.detect_current_stage(),
            completed_stages=self.get_completed_stages(),
            story_id=story_id,
            epic_mode=self.epic_mode,
            backlog=self.backlog
        )

    def validate_prerequisites(self, stage: WorkflowStage) -> tuple[bool, Optional[str]]:
        """Validate prerequisites for a workflow stage.

        Args:
            stage: Stage to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        context = self.create_context()

        if not context.can_proceed_to(stage):
            missing_stages = []
            stage_order = [WorkflowStage.SPECIFY, WorkflowStage.PLAN, WorkflowStage.TASKS, WorkflowStage.IMPLEMENT]
            target_index = stage_order.index(stage)

            for i in range(target_index):
                if stage_order[i] not in context.completed_stages:
                    missing_stages.append(stage_order[i].value)

            error_msg = f"Missing prerequisites: {', '.join(missing_stages)}. Complete these stages first."
            return False, error_msg

        # Stage-specific validations
        if stage == WorkflowStage.TASKS:
            spec_file = self.feature_dir / "spec.md"
            plan_file = self.feature_dir / "plan.md"

            if not spec_file.exists():
                return False, "spec.md not found. Run /speckit.specify first."
            if not plan_file.exists():
                return False, "plan.md not found. Run /speckit.plan first."

        elif stage == WorkflowStage.IMPLEMENT:
            tasks_file = self.feature_dir / "tasks.md"
            if not tasks_file.exists():
                return False, "tasks.md not found. Run /speckit.tasks first."

        return True, None

    def validate_story_ready(self, story_id: str) -> tuple[bool, Optional[str]]:
        """Validate that a story is ready for implementation.

        Args:
            story_id: Story ID to validate

        Returns:
            Tuple of (is_ready, error_message)
        """
        if not self.backlog:
            return False, "Story backlog not initialized. Run /speckit.epic first."

        story = self.backlog.get_story(story_id)
        if not story:
            return False, f"Story {story_id} not found in backlog."

        # Check status
        if self.config.REQUIRE_READY_STATUS:
            if story.status not in [StoryStatus.READY, StoryStatus.IN_PROGRESS]:
                return False, f"Story {story_id} status is {story.status.value}. Mark as READY first."

        # Check dependencies
        incomplete_deps = self.backlog.check_dependencies(story_id)
        if incomplete_deps:
            return False, f"Story {story_id} has incomplete dependencies: {', '.join(incomplete_deps)}"

        return True, None

    def get_next_story(self) -> Optional[UserStory]:
        """Get the next story to implement.

        Returns:
            Next story or None if no ready stories
        """
        if not self.backlog:
            return None

        return self.backlog.get_next_story()

    def update_story_progress(
        self,
        story_id: str,
        completed_tasks: int,
        actual_hours: float = 0
    ) -> None:
        """Update progress for a story.

        Args:
            story_id: Story ID
            completed_tasks: Number of completed tasks
            actual_hours: Actual hours spent
        """
        if not self.backlog or not self.config.AUTO_UPDATE_BACKLOG:
            return

        story = self.backlog.get_story(story_id)
        if story:
            story.update_progress(completed_tasks, actual_hours)
            self.backlog.update_story(story)

    def mark_story_complete(self, story_id: str, actual_hours: float = 0) -> List[str]:
        """Mark a story as complete and unblock dependent stories.

        Args:
            story_id: Story ID to mark complete
            actual_hours: Actual hours spent

        Returns:
            List of unblocked story IDs
        """
        if not self.backlog:
            return []

        story = self.backlog.get_story(story_id)
        if not story:
            return []

        # Update actual hours if provided
        if actual_hours > 0:
            story.metrics.actual_hours = actual_hours

        # Mark complete
        story.mark_complete()
        self.backlog.update_story(story)

        # Find and unblock dependent stories
        unblocked = []
        if self.config.AUTO_UNBLOCK_STORIES:
            for other_story in self.backlog.stories.values():
                if story_id in other_story.dependencies:
                    incomplete_deps = self.backlog.check_dependencies(other_story.id)
                    if not incomplete_deps and other_story.status == StoryStatus.BLOCKED:
                        other_story.unblock()
                        self.backlog.update_story(other_story)
                        unblocked.append(other_story.id)

        return unblocked

    def get_workflow_summary(self) -> Dict:
        """Get summary of workflow progress.

        Returns:
            Dictionary with workflow summary
        """
        context = self.create_context()

        summary = {
            'feature_id': self.feature_id,
            'current_stage': context.current_stage.value,
            'completed_stages': [s.value for s in context.completed_stages],
            'epic_mode': self.epic_mode,
            'progress_percentage': len(context.completed_stages) / 4 * 100
        }

        if self.backlog:
            backlog_summary = self.backlog.get_backlog_summary()
            summary['story_progress'] = {
                'total_stories': backlog_summary['total_stories'],
                'completed_stories': backlog_summary['status_counts'].get('complete', 0),
                'completion_rate': backlog_summary['completion_rate'],
                'next_story': backlog_summary['next_story']
            }

        return summary

    def generate_status_report(self) -> str:
        """Generate human-readable status report.

        Returns:
            Formatted status report
        """
        summary = self.get_workflow_summary()

        report = []
        report.append(f"# Workflow Status: {self.feature_id}")
        report.append("")
        report.append(f"**Current Stage:** {summary['current_stage']}")
        report.append(f"**Progress:** {summary['progress_percentage']:.1f}% ({len(summary['completed_stages'])}/4 stages)")
        report.append("")

        report.append("## Completed Stages")
        for stage in summary['completed_stages']:
            report.append(f"- ✅ {stage}")
        report.append("")

        if self.epic_mode:
            report.append("## EPIC Mode")
            report.append(f"- EPIC decomposition: Active")

            if 'story_progress' in summary:
                sp = summary['story_progress']
                report.append(f"- Total stories: {sp['total_stories']}")
                report.append(f"- Completed: {sp['completed_stories']} ({sp['completion_rate']:.1f}%)")
                if sp['next_story']:
                    report.append(f"- Next story: {sp['next_story']}")
            report.append("")

        return "\n".join(report)
