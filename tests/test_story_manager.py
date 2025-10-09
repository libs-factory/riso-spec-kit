"""Tests for story_manager module."""

import pytest
from pathlib import Path
import json
from datetime import datetime
from specify_cli.story_manager import (
    StoryStatus,
    StoryPriority,
    StoryMetrics,
    UserStory,
    StoryBacklog,
    StoryManager
)


@pytest.fixture
def temp_feature_dir(tmp_path):
    """Create temporary feature directory."""
    feature_dir = tmp_path / "feature-001"
    feature_dir.mkdir()
    return feature_dir


@pytest.fixture
def sample_story():
    """Create sample user story."""
    return UserStory(
        id="US-001",
        epic_id="EPIC-001",
        title="User Login",
        description="Implement user login functionality",
        acceptance_criteria=[
            "Users can login with email/password",
            "Invalid credentials show error"
        ],
        priority=StoryPriority.P1,
        status=StoryStatus.DRAFT,
        dependencies=[],
        blocked_by=[],
        metrics=StoryMetrics(
            estimated_tasks=5,
            completed_tasks=0,
            estimated_hours=10.0,
            actual_hours=0.0,
            test_coverage=0.0
        ),
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )


class TestStoryMetrics:
    """Tests for StoryMetrics class."""

    def test_progress_percentage(self):
        """Test progress calculation."""
        metrics = StoryMetrics(
            estimated_tasks=10,
            completed_tasks=5,
            estimated_hours=20.0,
            actual_hours=10.0,
            test_coverage=80.0
        )

        assert metrics.progress_percentage() == 50.0

    def test_progress_percentage_zero_tasks(self):
        """Test progress with zero tasks."""
        metrics = StoryMetrics(
            estimated_tasks=0,
            completed_tasks=0,
            estimated_hours=0.0,
            actual_hours=0.0,
            test_coverage=0.0
        )

        assert metrics.progress_percentage() == 0.0

    def test_is_complete(self):
        """Test completion check."""
        metrics = StoryMetrics(
            estimated_tasks=5,
            completed_tasks=5,
            estimated_hours=10.0,
            actual_hours=12.0,
            test_coverage=95.0
        )

        assert metrics.is_complete() is True

    def test_is_not_complete(self):
        """Test incomplete check."""
        metrics = StoryMetrics(
            estimated_tasks=5,
            completed_tasks=3,
            estimated_hours=10.0,
            actual_hours=8.0,
            test_coverage=60.0
        )

        assert metrics.is_complete() is False


class TestUserStory:
    """Tests for UserStory class."""

    def test_to_dict(self, sample_story):
        """Test conversion to dictionary."""
        data = sample_story.to_dict()

        assert data['id'] == "US-001"
        assert data['title'] == "User Login"
        assert data['priority'] == "p1"
        assert data['status'] == "draft"

    def test_from_dict(self, sample_story):
        """Test creation from dictionary."""
        data = sample_story.to_dict()
        restored = UserStory.from_dict(data)

        assert restored.id == sample_story.id
        assert restored.title == sample_story.title
        assert restored.priority == sample_story.priority
        assert restored.status == sample_story.status

    def test_mark_complete(self, sample_story):
        """Test marking story complete."""
        sample_story.mark_complete()

        assert sample_story.status == StoryStatus.COMPLETE
        assert sample_story.completed_at is not None

    def test_mark_blocked(self, sample_story):
        """Test marking story blocked."""
        blockers = ["US-002", "US-003"]
        sample_story.mark_blocked(blockers)

        assert sample_story.status == StoryStatus.BLOCKED
        assert sample_story.blocked_by == blockers

    def test_unblock(self, sample_story):
        """Test unblocking story."""
        sample_story.mark_blocked(["US-002"])
        sample_story.unblock()

        assert sample_story.status == StoryStatus.READY
        assert sample_story.blocked_by == []

    def test_start_work(self, sample_story):
        """Test starting work on story."""
        sample_story.start_work()

        assert sample_story.status == StoryStatus.IN_PROGRESS

    def test_update_progress(self, sample_story):
        """Test updating progress."""
        sample_story.update_progress(completed_tasks=3, actual_hours=6.0)

        assert sample_story.metrics.completed_tasks == 3
        assert sample_story.metrics.actual_hours == 6.0

    def test_update_progress_auto_complete(self, sample_story):
        """Test auto-completion on full progress."""
        sample_story.update_progress(completed_tasks=5)

        assert sample_story.status == StoryStatus.COMPLETE
        assert sample_story.completed_at is not None


class TestStoryBacklog:
    """Tests for StoryBacklog class."""

    def test_add_and_get_story(self, temp_feature_dir, sample_story):
        """Test adding and retrieving story."""
        backlog = StoryBacklog(temp_feature_dir)
        backlog.add_story(sample_story)

        retrieved = backlog.get_story("US-001")
        assert retrieved is not None
        assert retrieved.id == "US-001"
        assert retrieved.title == "User Login"

    def test_update_story(self, temp_feature_dir, sample_story):
        """Test updating story."""
        backlog = StoryBacklog(temp_feature_dir)
        backlog.add_story(sample_story)

        sample_story.title = "Updated Login"
        backlog.update_story(sample_story)

        retrieved = backlog.get_story("US-001")
        assert retrieved.title == "Updated Login"

    def test_remove_story(self, temp_feature_dir, sample_story):
        """Test removing story."""
        backlog = StoryBacklog(temp_feature_dir)
        backlog.add_story(sample_story)

        removed = backlog.remove_story("US-001")
        assert removed is True

        retrieved = backlog.get_story("US-001")
        assert retrieved is None

    def test_get_stories_by_status(self, temp_feature_dir):
        """Test filtering by status."""
        backlog = StoryBacklog(temp_feature_dir)

        story1 = UserStory(
            id="US-001", epic_id=None, title="Story 1", description="",
            acceptance_criteria=[], priority=StoryPriority.P1, status=StoryStatus.READY,
            dependencies=[], blocked_by=[],
            metrics=StoryMetrics(5, 0, 10.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(), updated_at=datetime.now().isoformat()
        )
        story2 = UserStory(
            id="US-002", epic_id=None, title="Story 2", description="",
            acceptance_criteria=[], priority=StoryPriority.P2, status=StoryStatus.COMPLETE,
            dependencies=[], blocked_by=[],
            metrics=StoryMetrics(3, 3, 6.0, 7.0, 100.0),
            created_at=datetime.now().isoformat(), updated_at=datetime.now().isoformat()
        )

        backlog.add_story(story1)
        backlog.add_story(story2)

        ready_stories = backlog.get_stories_by_status(StoryStatus.READY)
        assert len(ready_stories) == 1
        assert ready_stories[0].id == "US-001"

    def test_get_stories_by_priority(self, temp_feature_dir):
        """Test filtering by priority."""
        backlog = StoryBacklog(temp_feature_dir)

        story1 = UserStory(
            id="US-001", epic_id=None, title="Story 1", description="",
            acceptance_criteria=[], priority=StoryPriority.P1, status=StoryStatus.READY,
            dependencies=[], blocked_by=[],
            metrics=StoryMetrics(5, 0, 10.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(), updated_at=datetime.now().isoformat()
        )
        story2 = UserStory(
            id="US-002", epic_id=None, title="Story 2", description="",
            acceptance_criteria=[], priority=StoryPriority.P2, status=StoryStatus.READY,
            dependencies=[], blocked_by=[],
            metrics=StoryMetrics(3, 0, 6.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(), updated_at=datetime.now().isoformat()
        )

        backlog.add_story(story1)
        backlog.add_story(story2)

        p1_stories = backlog.get_stories_by_priority(StoryPriority.P1)
        assert len(p1_stories) == 1
        assert p1_stories[0].id == "US-001"

    def test_get_next_story(self, temp_feature_dir):
        """Test getting next priority story."""
        backlog = StoryBacklog(temp_feature_dir)

        story1 = UserStory(
            id="US-001", epic_id=None, title="Story 1", description="",
            acceptance_criteria=[], priority=StoryPriority.P2, status=StoryStatus.READY,
            dependencies=[], blocked_by=[],
            metrics=StoryMetrics(5, 0, 10.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(), updated_at=datetime.now().isoformat()
        )
        story2 = UserStory(
            id="US-002", epic_id=None, title="Story 2", description="",
            acceptance_criteria=[], priority=StoryPriority.P1, status=StoryStatus.READY,
            dependencies=[], blocked_by=[],
            metrics=StoryMetrics(3, 0, 6.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(), updated_at=datetime.now().isoformat()
        )

        backlog.add_story(story1)
        backlog.add_story(story2)

        next_story = backlog.get_next_story()
        assert next_story is not None
        assert next_story.id == "US-002"  # P1 has higher priority

    def test_check_dependencies(self, temp_feature_dir):
        """Test dependency checking."""
        backlog = StoryBacklog(temp_feature_dir)

        story1 = UserStory(
            id="US-001", epic_id=None, title="Story 1", description="",
            acceptance_criteria=[], priority=StoryPriority.P1, status=StoryStatus.IN_PROGRESS,
            dependencies=[], blocked_by=[],
            metrics=StoryMetrics(5, 2, 10.0, 5.0, 40.0),
            created_at=datetime.now().isoformat(), updated_at=datetime.now().isoformat()
        )
        story2 = UserStory(
            id="US-002", epic_id=None, title="Story 2", description="",
            acceptance_criteria=[], priority=StoryPriority.P2, status=StoryStatus.READY,
            dependencies=["US-001"], blocked_by=[],
            metrics=StoryMetrics(3, 0, 6.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(), updated_at=datetime.now().isoformat()
        )

        backlog.add_story(story1)
        backlog.add_story(story2)

        incomplete_deps = backlog.check_dependencies("US-002")
        assert len(incomplete_deps) == 1
        assert "US-001" in incomplete_deps

    def test_update_blocked_status(self, temp_feature_dir):
        """Test automatic blocked status updates."""
        backlog = StoryBacklog(temp_feature_dir)

        story1 = UserStory(
            id="US-001", epic_id=None, title="Story 1", description="",
            acceptance_criteria=[], priority=StoryPriority.P1, status=StoryStatus.IN_PROGRESS,
            dependencies=[], blocked_by=[],
            metrics=StoryMetrics(5, 2, 10.0, 5.0, 40.0),
            created_at=datetime.now().isoformat(), updated_at=datetime.now().isoformat()
        )
        story2 = UserStory(
            id="US-002", epic_id=None, title="Story 2", description="",
            acceptance_criteria=[], priority=StoryPriority.P2, status=StoryStatus.READY,
            dependencies=["US-001"], blocked_by=[],
            metrics=StoryMetrics(3, 0, 6.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(), updated_at=datetime.now().isoformat()
        )

        backlog.add_story(story1)
        backlog.add_story(story2)

        changed = backlog.update_blocked_status()

        assert changed == 1
        story2_updated = backlog.get_story("US-002")
        assert story2_updated.status == StoryStatus.BLOCKED

    def test_get_backlog_summary(self, temp_feature_dir, sample_story):
        """Test backlog summary."""
        backlog = StoryBacklog(temp_feature_dir)
        backlog.add_story(sample_story)

        summary = backlog.get_backlog_summary()

        assert summary['total_stories'] == 1
        assert summary['status_counts']['draft'] == 1
        assert summary['priority_counts']['p1'] == 1

    def test_find_circular_dependencies(self, temp_feature_dir):
        """Test circular dependency detection."""
        backlog = StoryBacklog(temp_feature_dir)

        story1 = UserStory(
            id="US-001", epic_id=None, title="Story 1", description="",
            acceptance_criteria=[], priority=StoryPriority.P1, status=StoryStatus.READY,
            dependencies=["US-002"], blocked_by=[],
            metrics=StoryMetrics(5, 0, 10.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(), updated_at=datetime.now().isoformat()
        )
        story2 = UserStory(
            id="US-002", epic_id=None, title="Story 2", description="",
            acceptance_criteria=[], priority=StoryPriority.P2, status=StoryStatus.READY,
            dependencies=["US-001"], blocked_by=[],
            metrics=StoryMetrics(3, 0, 6.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(), updated_at=datetime.now().isoformat()
        )

        backlog.add_story(story1)
        backlog.add_story(story2)

        cycles = backlog.find_circular_dependencies()
        assert len(cycles) > 0


class TestStoryManager:
    """Tests for StoryManager class."""

    def test_get_backlog(self, tmp_path):
        """Test getting backlog for feature."""
        specs_dir = tmp_path / ".specify" / "specs"
        specs_dir.mkdir(parents=True)

        manager = StoryManager(specs_dir)
        backlog = manager.get_backlog("feature-001")

        assert backlog is not None
        assert backlog.feature_dir.name == "feature-001"

    def test_create_story_from_template(self, tmp_path):
        """Test creating story from template."""
        specs_dir = tmp_path / ".specify" / "specs"
        specs_dir.mkdir(parents=True)

        manager = StoryManager(specs_dir)
        story = manager.create_story_from_template(
            story_id="US-001",
            title="User Registration",
            description="Implement user registration",
            priority=StoryPriority.P1,
            estimated_tasks=8,
            estimated_hours=16.0,
            epic_id="EPIC-001"
        )

        assert story.id == "US-001"
        assert story.title == "User Registration"
        assert story.priority == StoryPriority.P1
        assert story.metrics.estimated_tasks == 8

    def test_persistence(self, temp_feature_dir):
        """Test that backlog persists across instances."""
        backlog1 = StoryBacklog(temp_feature_dir)

        story = UserStory(
            id="US-001", epic_id=None, title="Persistent Story", description="",
            acceptance_criteria=[], priority=StoryPriority.P1, status=StoryStatus.READY,
            dependencies=[], blocked_by=[],
            metrics=StoryMetrics(5, 0, 10.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(), updated_at=datetime.now().isoformat()
        )
        backlog1.add_story(story)

        # Create new instance
        backlog2 = StoryBacklog(temp_feature_dir)
        retrieved = backlog2.get_story("US-001")

        assert retrieved is not None
        assert retrieved.title == "Persistent Story"
