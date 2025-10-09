"""Integration tests for full EPIC workflow."""

import pytest
from pathlib import Path
from datetime import datetime
from specify_cli.epic_analyzer import EpicAnalyzer, EpicComplexity
from specify_cli.story_manager import (
    StoryBacklog,
    StoryManager,
    UserStory,
    StoryStatus,
    StoryPriority,
    StoryMetrics
)
from specify_cli.workflow_runner import WorkflowRunner, WorkflowStage


@pytest.fixture
def temp_specs_dir(tmp_path):
    """Create temporary specs directory."""
    specs_dir = tmp_path / ".specify" / "specs"
    specs_dir.mkdir(parents=True)
    return specs_dir


@pytest.fixture
def feature_dir(temp_specs_dir):
    """Create feature directory."""
    feature_dir = temp_specs_dir / "001-test-epic"
    feature_dir.mkdir()
    return feature_dir


class TestEpicWorkflowIntegration:
    """Integration tests for end-to-end EPIC workflow."""

    def test_full_epic_workflow(self, feature_dir):
        """Test complete EPIC workflow from decomposition to completion."""
        # Step 1: Create spec and plan files
        (feature_dir / "spec.md").write_text("# Test EPIC Feature")
        (feature_dir / "plan.md").write_text("# Implementation Plan")

        # Step 2: Analyze complexity
        analyzer = EpicAnalyzer(feature_dir)
        complexity = analyzer.analyze_complexity(
            "Large feature with many components",
            estimated_tasks=35
        )
        assert complexity == EpicComplexity.EPIC

        # Step 3: Create EPIC and stories
        epic = analyzer.create_epic(
            epic_id="EPIC-001",
            title="Test EPIC",
            description="Large feature for testing",
            business_value="Test business value",
            estimated_tasks=35
        )

        # Decompose into stories
        stories = analyzer.decompose_feature_to_stories(
            "Admin and user workflows with CRUD operations",
            estimated_tasks=35,
            context={}
        )

        assert len(stories) > 0

        for story in stories:
            analyzer.add_story_to_epic(epic, story)

        # Step 4: Save EPIC breakdown
        epic_file = feature_dir / "epic-breakdown.md"
        analyzer.save_epic_to_file(epic, epic_file)
        assert epic_file.exists()

        # Step 5: Initialize story backlog
        backlog = StoryBacklog(feature_dir)

        for story_data in stories:
            story = UserStory(
                id=story_data.id,
                epic_id="EPIC-001",
                title=story_data.title,
                description=story_data.description,
                acceptance_criteria=story_data.acceptance_criteria,
                priority=StoryPriority.P1 if story_data.priority == 1 else StoryPriority.P2,
                status=StoryStatus.DRAFT,
                dependencies=story_data.dependencies,
                blocked_by=[],
                metrics=StoryMetrics(
                    estimated_tasks=story_data.estimated_tasks,
                    completed_tasks=0,
                    estimated_hours=story_data.estimated_tasks * 2.0,
                    actual_hours=0.0,
                    test_coverage=0.0
                ),
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            backlog.add_story(story)

        # Step 6: Get next story (should be MVP with no dependencies)
        next_story = backlog.get_next_story()
        assert next_story is None  # All stories are DRAFT

        # Mark first story as READY
        first_story = backlog.stories[stories[0].id]
        first_story.status = StoryStatus.READY
        backlog.update_story(first_story)

        next_story = backlog.get_next_story()
        assert next_story is not None
        assert next_story.id == stories[0].id

        # Step 7: Simulate implementation
        next_story.start_work()
        backlog.update_story(next_story)
        assert next_story.status == StoryStatus.IN_PROGRESS

        # Update progress
        next_story.update_progress(completed_tasks=3, actual_hours=6.0)
        backlog.update_story(next_story)
        assert next_story.metrics.completed_tasks == 3

        # Complete story
        next_story.update_progress(
            completed_tasks=next_story.metrics.estimated_tasks,
            actual_hours=10.0
        )
        backlog.update_story(next_story)
        assert next_story.status == StoryStatus.COMPLETE

        # Step 8: Check workflow runner integration
        workflow = WorkflowRunner(feature_dir)
        assert workflow.epic_mode is True
        assert workflow.backlog is not None

        context = workflow.create_context()
        assert context.epic_mode is True
        assert context.backlog is not None

        summary = workflow.get_workflow_summary()
        assert summary['epic_mode'] is True
        assert 'story_progress' in summary

    def test_story_dependency_workflow(self, feature_dir):
        """Test story workflow with dependencies."""
        backlog = StoryBacklog(feature_dir)

        # Create story 1 (MVP, no dependencies)
        story1 = UserStory(
            id="US-001",
            epic_id="EPIC-001",
            title="MVP Story",
            description="MVP functionality",
            acceptance_criteria=["Criterion 1"],
            priority=StoryPriority.P1,
            status=StoryStatus.READY,
            dependencies=[],
            blocked_by=[],
            metrics=StoryMetrics(5, 0, 10.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        # Create story 2 (depends on story 1)
        story2 = UserStory(
            id="US-002",
            epic_id="EPIC-001",
            title="Enhancement Story",
            description="Enhancement",
            acceptance_criteria=["Criterion 1"],
            priority=StoryPriority.P2,
            status=StoryStatus.READY,
            dependencies=["US-001"],
            blocked_by=[],
            metrics=StoryMetrics(3, 0, 6.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        backlog.add_story(story1)
        backlog.add_story(story2)

        # Update blocked status
        changed = backlog.update_blocked_status()
        assert changed == 1  # Story 2 should be blocked

        updated_story2 = backlog.get_story("US-002")
        assert updated_story2.status == StoryStatus.BLOCKED
        assert "US-001" in updated_story2.blocked_by

        # Complete story 1
        story1.mark_complete()
        backlog.update_story(story1)

        # Update blocked status again
        changed = backlog.update_blocked_status()
        assert changed == 1  # Story 2 should be unblocked

        updated_story2 = backlog.get_story("US-002")
        assert updated_story2.status == StoryStatus.READY
        assert len(updated_story2.blocked_by) == 0

    def test_story_velocity_calculation(self, feature_dir):
        """Test story velocity metrics."""
        backlog = StoryBacklog(feature_dir)

        # Create and complete multiple stories
        for i in range(1, 4):
            story = UserStory(
                id=f"US-{i:03d}",
                epic_id="EPIC-001",
                title=f"Story {i}",
                description=f"Story {i} description",
                acceptance_criteria=["Criterion 1"],
                priority=StoryPriority.P1,
                status=StoryStatus.COMPLETE,
                dependencies=[],
                blocked_by=[],
                metrics=StoryMetrics(5, 5, 10.0, 9.0, 95.0),
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat(),
                completed_at=datetime.now().isoformat()
            )
            backlog.add_story(story)

        # Get backlog summary
        summary = backlog.get_backlog_summary()
        assert summary['total_stories'] == 3
        assert summary['status_counts']['complete'] == 3
        assert summary['completion_rate'] == 100.0

    def test_workflow_runner_story_operations(self, feature_dir):
        """Test workflow runner story operations."""
        # Setup
        (feature_dir / "spec.md").write_text("# Spec")
        (feature_dir / "plan.md").write_text("# Plan")

        backlog = StoryBacklog(feature_dir)

        story = UserStory(
            id="US-001",
            epic_id="EPIC-001",
            title="Test Story",
            description="Test",
            acceptance_criteria=["Criterion 1"],
            priority=StoryPriority.P1,
            status=StoryStatus.READY,
            dependencies=[],
            blocked_by=[],
            metrics=StoryMetrics(10, 0, 20.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        backlog.add_story(story)

        # Create workflow runner
        workflow = WorkflowRunner(feature_dir)

        # Validate story ready
        valid, error = workflow.validate_story_ready("US-001")
        assert valid is True

        # Update progress
        workflow.update_story_progress("US-001", completed_tasks=5, actual_hours=10.5)

        updated_story = backlog.get_story("US-001")
        assert updated_story.metrics.completed_tasks == 5
        assert updated_story.metrics.actual_hours == 10.5

        # Mark complete
        unblocked = workflow.mark_story_complete("US-001", actual_hours=19.0)

        completed_story = backlog.get_story("US-001")
        assert completed_story.status == StoryStatus.COMPLETE
        assert completed_story.metrics.actual_hours == 19.0

    def test_multi_story_parallel_opportunities(self, feature_dir):
        """Test identifying parallel story implementation opportunities."""
        analyzer = EpicAnalyzer(feature_dir)

        # Create stories with dependencies
        stories = [
            analyzer.create_epic("EPIC-001", "Test", "Test", "Value", 10).stories
        ]

        # Generate dependency graph
        backlog = StoryBacklog(feature_dir)

        story1 = UserStory(
            id="US-001",
            epic_id="EPIC-001",
            title="Foundation",
            description="Base",
            acceptance_criteria=[],
            priority=StoryPriority.P1,
            status=StoryStatus.COMPLETE,
            dependencies=[],
            blocked_by=[],
            metrics=StoryMetrics(5, 5, 10.0, 10.0, 100.0),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            completed_at=datetime.now().isoformat()
        )

        story2 = UserStory(
            id="US-002",
            epic_id="EPIC-001",
            title="Feature A",
            description="A",
            acceptance_criteria=[],
            priority=StoryPriority.P2,
            status=StoryStatus.READY,
            dependencies=["US-001"],
            blocked_by=[],
            metrics=StoryMetrics(4, 0, 8.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        story3 = UserStory(
            id="US-003",
            epic_id="EPIC-001",
            title="Feature B",
            description="B",
            acceptance_criteria=[],
            priority=StoryPriority.P2,
            status=StoryStatus.READY,
            dependencies=["US-001"],
            blocked_by=[],
            metrics=StoryMetrics(4, 0, 8.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        backlog.add_story(story1)
        backlog.add_story(story2)
        backlog.add_story(story3)

        # Both story2 and story3 can be implemented in parallel
        # (they only depend on US-001 which is complete)
        ready_stories = backlog.get_ready_stories()
        assert len(ready_stories) == 2
        assert all(s.id in ["US-002", "US-003"] for s in ready_stories)
