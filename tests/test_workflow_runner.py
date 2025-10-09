"""Tests for workflow_runner module."""

import pytest
from pathlib import Path
from datetime import datetime
from specify_cli.workflow_runner import (
    WorkflowStage,
    WorkflowContext,
    WorkflowRunner
)
from specify_cli.story_manager import (
    StoryBacklog,
    UserStory,
    StoryStatus,
    StoryPriority,
    StoryMetrics
)


@pytest.fixture
def temp_feature_dir(tmp_path):
    """Create temporary feature directory."""
    feature_dir = tmp_path / ".specify" / "specs" / "001-test-feature"
    feature_dir.mkdir(parents=True)
    return feature_dir


@pytest.fixture
def workflow_runner(temp_feature_dir):
    """Create workflow runner instance."""
    return WorkflowRunner(temp_feature_dir)


class TestWorkflowContext:
    """Tests for WorkflowContext class."""

    def test_is_stage_complete(self):
        """Test stage completion check."""
        context = WorkflowContext(
            feature_dir=Path("/test"),
            feature_id="test",
            current_stage=WorkflowStage.TASKS,
            completed_stages=[WorkflowStage.SPECIFY, WorkflowStage.PLAN]
        )

        assert context.is_stage_complete(WorkflowStage.SPECIFY) is True
        assert context.is_stage_complete(WorkflowStage.PLAN) is True
        assert context.is_stage_complete(WorkflowStage.TASKS) is False

    def test_can_proceed_to(self):
        """Test can proceed to stage."""
        context = WorkflowContext(
            feature_dir=Path("/test"),
            feature_id="test",
            current_stage=WorkflowStage.PLAN,
            completed_stages=[WorkflowStage.SPECIFY]
        )

        # Can proceed to PLAN (SPECIFY is complete)
        assert context.can_proceed_to(WorkflowStage.PLAN) is True

        # Cannot proceed to IMPLEMENT (PLAN and TASKS not complete)
        assert context.can_proceed_to(WorkflowStage.IMPLEMENT) is False


class TestWorkflowRunner:
    """Tests for WorkflowRunner class."""

    def test_detect_current_stage_specify(self, workflow_runner, temp_feature_dir):
        """Test stage detection when no files exist."""
        stage = workflow_runner.detect_current_stage()
        assert stage == WorkflowStage.SPECIFY

    def test_detect_current_stage_plan(self, workflow_runner, temp_feature_dir):
        """Test stage detection when spec.md exists."""
        (temp_feature_dir / "spec.md").write_text("# Spec")
        stage = workflow_runner.detect_current_stage()
        assert stage == WorkflowStage.PLAN

    def test_detect_current_stage_tasks(self, workflow_runner, temp_feature_dir):
        """Test stage detection when plan.md exists."""
        (temp_feature_dir / "spec.md").write_text("# Spec")
        (temp_feature_dir / "plan.md").write_text("# Plan")
        stage = workflow_runner.detect_current_stage()
        assert stage == WorkflowStage.TASKS

    def test_detect_current_stage_implement(self, workflow_runner, temp_feature_dir):
        """Test stage detection when tasks.md exists."""
        (temp_feature_dir / "spec.md").write_text("# Spec")
        (temp_feature_dir / "plan.md").write_text("# Plan")
        (temp_feature_dir / "tasks.md").write_text("# Tasks")
        stage = workflow_runner.detect_current_stage()
        assert stage == WorkflowStage.IMPLEMENT

    def test_get_completed_stages(self, workflow_runner, temp_feature_dir):
        """Test getting completed stages."""
        (temp_feature_dir / "spec.md").write_text("# Spec")
        (temp_feature_dir / "plan.md").write_text("# Plan")

        completed = workflow_runner.get_completed_stages()
        assert WorkflowStage.SPECIFY in completed
        assert WorkflowStage.PLAN in completed
        assert WorkflowStage.TASKS not in completed

    def test_validate_prerequisites_success(self, workflow_runner, temp_feature_dir):
        """Test prerequisite validation success."""
        (temp_feature_dir / "spec.md").write_text("# Spec")
        (temp_feature_dir / "plan.md").write_text("# Plan")

        valid, error = workflow_runner.validate_prerequisites(WorkflowStage.TASKS)
        assert valid is True
        assert error is None

    def test_validate_prerequisites_failure(self, workflow_runner, temp_feature_dir):
        """Test prerequisite validation failure."""
        # No files exist, try to go to IMPLEMENT
        valid, error = workflow_runner.validate_prerequisites(WorkflowStage.IMPLEMENT)
        assert valid is False
        assert error is not None
        assert "Missing prerequisites" in error

    def test_validate_story_ready_no_backlog(self, workflow_runner):
        """Test story validation with no backlog."""
        valid, error = workflow_runner.validate_story_ready("US-001")
        assert valid is False
        assert "not initialized" in error

    def test_validate_story_ready_not_found(self, workflow_runner, temp_feature_dir):
        """Test story validation when story not found."""
        # Create backlog
        backlog = StoryBacklog(temp_feature_dir)
        workflow_runner.backlog = backlog

        valid, error = workflow_runner.validate_story_ready("US-999")
        assert valid is False
        assert "not found" in error

    def test_validate_story_ready_wrong_status(self, workflow_runner, temp_feature_dir):
        """Test story validation with wrong status."""
        backlog = StoryBacklog(temp_feature_dir)
        workflow_runner.backlog = backlog

        story = UserStory(
            id="US-001",
            epic_id=None,
            title="Test Story",
            description="Test",
            acceptance_criteria=[],
            priority=StoryPriority.P1,
            status=StoryStatus.DRAFT,
            dependencies=[],
            blocked_by=[],
            metrics=StoryMetrics(5, 0, 10.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        backlog.add_story(story)

        valid, error = workflow_runner.validate_story_ready("US-001")
        assert valid is False
        assert "status is draft" in error.lower()

    def test_validate_story_ready_success(self, workflow_runner, temp_feature_dir):
        """Test story validation success."""
        backlog = StoryBacklog(temp_feature_dir)
        workflow_runner.backlog = backlog

        story = UserStory(
            id="US-001",
            epic_id=None,
            title="Test Story",
            description="Test",
            acceptance_criteria=[],
            priority=StoryPriority.P1,
            status=StoryStatus.READY,
            dependencies=[],
            blocked_by=[],
            metrics=StoryMetrics(5, 0, 10.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        backlog.add_story(story)

        valid, error = workflow_runner.validate_story_ready("US-001")
        assert valid is True
        assert error is None

    def test_get_next_story(self, workflow_runner, temp_feature_dir):
        """Test getting next story."""
        backlog = StoryBacklog(temp_feature_dir)
        workflow_runner.backlog = backlog

        story1 = UserStory(
            id="US-001",
            epic_id=None,
            title="Story 1",
            description="Test",
            acceptance_criteria=[],
            priority=StoryPriority.P2,
            status=StoryStatus.READY,
            dependencies=[],
            blocked_by=[],
            metrics=StoryMetrics(5, 0, 10.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        story2 = UserStory(
            id="US-002",
            epic_id=None,
            title="Story 2",
            description="Test",
            acceptance_criteria=[],
            priority=StoryPriority.P1,
            status=StoryStatus.READY,
            dependencies=[],
            blocked_by=[],
            metrics=StoryMetrics(3, 0, 6.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        backlog.add_story(story1)
        backlog.add_story(story2)

        next_story = workflow_runner.get_next_story()
        assert next_story is not None
        assert next_story.id == "US-002"  # P1 has higher priority

    def test_update_story_progress(self, workflow_runner, temp_feature_dir):
        """Test updating story progress."""
        backlog = StoryBacklog(temp_feature_dir)
        workflow_runner.backlog = backlog

        story = UserStory(
            id="US-001",
            epic_id=None,
            title="Test Story",
            description="Test",
            acceptance_criteria=[],
            priority=StoryPriority.P1,
            status=StoryStatus.IN_PROGRESS,
            dependencies=[],
            blocked_by=[],
            metrics=StoryMetrics(10, 0, 20.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        backlog.add_story(story)

        workflow_runner.update_story_progress("US-001", completed_tasks=5, actual_hours=10.5)

        updated_story = backlog.get_story("US-001")
        assert updated_story.metrics.completed_tasks == 5
        assert updated_story.metrics.actual_hours == 10.5

    def test_mark_story_complete(self, workflow_runner, temp_feature_dir):
        """Test marking story complete."""
        backlog = StoryBacklog(temp_feature_dir)
        workflow_runner.backlog = backlog

        story1 = UserStory(
            id="US-001",
            epic_id=None,
            title="Story 1",
            description="Test",
            acceptance_criteria=[],
            priority=StoryPriority.P1,
            status=StoryStatus.IN_PROGRESS,
            dependencies=[],
            blocked_by=[],
            metrics=StoryMetrics(5, 5, 10.0, 9.5, 100.0),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        story2 = UserStory(
            id="US-002",
            epic_id=None,
            title="Story 2",
            description="Test",
            acceptance_criteria=[],
            priority=StoryPriority.P2,
            status=StoryStatus.BLOCKED,
            dependencies=["US-001"],
            blocked_by=["US-001"],
            metrics=StoryMetrics(3, 0, 6.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        backlog.add_story(story1)
        backlog.add_story(story2)

        unblocked = workflow_runner.mark_story_complete("US-001", actual_hours=9.5)

        # Check story 1 is complete
        completed_story = backlog.get_story("US-001")
        assert completed_story.status == StoryStatus.COMPLETE

        # Check story 2 is unblocked
        assert "US-002" in unblocked
        unblocked_story = backlog.get_story("US-002")
        assert unblocked_story.status == StoryStatus.READY

    def test_get_workflow_summary(self, workflow_runner, temp_feature_dir):
        """Test getting workflow summary."""
        (temp_feature_dir / "spec.md").write_text("# Spec")
        (temp_feature_dir / "plan.md").write_text("# Plan")

        summary = workflow_runner.get_workflow_summary()

        assert summary['feature_id'] == "001-test-feature"
        assert summary['current_stage'] == 'tasks'
        assert len(summary['completed_stages']) == 2
        assert summary['epic_mode'] is False

    def test_generate_status_report(self, workflow_runner, temp_feature_dir):
        """Test generating status report."""
        (temp_feature_dir / "spec.md").write_text("# Spec")

        report = workflow_runner.generate_status_report()

        assert "Workflow Status" in report
        assert "001-test-feature" in report
        assert "Current Stage" in report
        assert "Progress" in report
