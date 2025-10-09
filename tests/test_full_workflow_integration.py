"""Full workflow integration tests for RisoTech enhancements."""

import pytest
from pathlib import Path
from datetime import datetime
import json

from specify_cli.config import SpecifyConfig
from specify_cli.constitution import Constitution, ConstitutionTier, ConstitutionRule, ConstitutionPreset
from specify_cli.epic_analyzer import EpicAnalyzer, EpicComplexity
from specify_cli.story_manager import StoryBacklog, UserStory, StoryPriority, StoryStatus, StoryMetrics
from specify_cli.workflow_runner import WorkflowRunner, WorkflowStage
from specify_cli.progress_tracker import ProgressTracker


@pytest.fixture
def feature_dir(tmp_path):
    """Create a temporary feature directory."""
    feature_path = tmp_path / ".specify" / "specs" / "001-test-feature"
    feature_path.mkdir(parents=True)
    return feature_path


@pytest.fixture
def templates_dir():
    """Get templates directory."""
    return Path(__file__).parent.parent / "templates"


class TestConstitutionWorkflow:
    """Test constitution management workflow."""

    def test_constitution_creation_and_application(self, feature_dir, templates_dir):
        """Test creating and applying a constitution to a feature."""
        # Load preset
        constitution = Constitution.load_preset(
            ConstitutionPreset.REACT_TYPESCRIPT,
            templates_dir=templates_dir
        )

        assert len(constitution.get_all_rules()) > 0

        # Merge with custom rules
        custom_constitution = Constitution()
        custom_rule = ConstitutionRule(
            title="Custom Testing Rule",
            description="All components must have unit tests and integration tests",
            tier=ConstitutionTier.CORE,
            rationale="Ensures code quality",
            examples=["jest --coverage"]
        )
        custom_constitution.add_rule(custom_rule)

        constitution.merge_constitution(custom_constitution, conflict_strategy='keep_both')

        # Save to feature directory
        constitution_file = feature_dir / "constitution.md"
        constitution.save_to_markdown(constitution_file)

        assert constitution_file.exists()

        # Validate against a plan
        plan_text = """
        # Plan

        ## Tech Stack
        - React with TypeScript
        - Jest for testing
        - Component-based architecture

        ## Implementation
        1. Create components
        2. Add tests
        3. Add integration tests
        """

        issues = constitution.validate_against_plan(plan_text)
        # Should have minimal issues since plan mentions testing
        assert len(issues) < 3

    def test_constitution_summary(self, templates_dir):
        """Test constitution summary generation."""
        constitution = Constitution.load_preset(
            ConstitutionPreset.NEXTJS_TAILWIND,
            templates_dir=templates_dir
        )

        summary = constitution.generate_summary()

        assert "Constitution Summary" in summary
        assert "CORE" in summary
        assert "HIGH-PRIORITY" in summary
        assert "FLEXIBLE" in summary


class TestEPICDecompositionWorkflow:
    """Test EPIC decomposition workflow."""

    def test_epic_decomposition_and_story_management(self, feature_dir):
        """Test full EPIC decomposition and story management."""
        # Step 1: Analyze complexity
        analyzer = EpicAnalyzer(feature_dir)

        complexity = analyzer.analyze_complexity(
            feature_description="User authentication and authorization system",
            estimated_tasks=45
        )

        assert complexity == EpicComplexity.EPIC

        # Step 2: Create EPIC
        epic = analyzer.create_epic(
            epic_id="EPIC-001",
            title="Authentication System",
            description="Complete authentication and authorization system",
            estimated_tasks=45
        )

        assert epic.id == "EPIC-001"

        # Step 3: Decompose into stories
        stories = analyzer.decompose_feature_to_stories(
            feature_description="""
            Build a complete authentication system with:
            - User registration
            - Email verification
            - Login with JWT
            - Password reset
            - Role-based access control (Admin, Manager, User)
            - OAuth integration (Google, GitHub)
            """,
            estimated_tasks=45,
            context={
                'complexity': EpicComplexity.EPIC,
                'has_roles': True,
                'has_entities': True
            }
        )

        assert len(stories) >= 5  # Should create multiple stories

        # Add stories to EPIC
        for story in stories:
            epic.add_story(story)

        # Step 4: Detect dependencies
        dependencies = analyzer.detect_story_dependencies(stories)
        analyzer.apply_dependencies(stories, dependencies)

        # Check that some stories have dependencies
        stories_with_deps = [s for s in stories if s.dependencies]
        assert len(stories_with_deps) > 0

        # Step 5: Initialize backlog
        backlog = StoryBacklog(feature_dir)
        for story in stories:
            backlog.add_story(story)

        # Verify backlog
        assert len(backlog.stories) == len(stories)

        # Step 6: Get next story (should be MVP foundation with no deps)
        next_story = backlog.get_next_story()
        assert next_story is not None
        assert next_story.status == StoryStatus.READY
        assert len(next_story.dependencies) == 0 or next_story.priority == StoryPriority.P1


class TestStoryImplementationWorkflow:
    """Test story-by-story implementation workflow."""

    def test_story_lifecycle(self, feature_dir):
        """Test complete story lifecycle from DRAFT to COMPLETE."""
        # Create spec and plan files
        (feature_dir / "spec.md").write_text("# Feature Spec")
        (feature_dir / "plan.md").write_text("# Implementation Plan")

        # Initialize backlog with stories
        backlog = StoryBacklog(feature_dir)

        story1 = UserStory(
            id="US-001",
            epic_id="EPIC-001",
            title="User Registration",
            description="Allow users to register",
            acceptance_criteria=["User can submit form", "Email sent"],
            priority=StoryPriority.P1,
            status=StoryStatus.READY,
            dependencies=[],
            blocked_by=[],
            metrics=StoryMetrics(10, 0, 20.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        story2 = UserStory(
            id="US-002",
            epic_id="EPIC-001",
            title="Email Verification",
            description="Verify user email",
            acceptance_criteria=["Token sent", "Token verified"],
            priority=StoryPriority.P1,
            status=StoryStatus.DRAFT,
            dependencies=["US-001"],
            blocked_by=[],
            metrics=StoryMetrics(8, 0, 15.0, 0.0, 0.0),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        backlog.add_story(story1)
        backlog.add_story(story2)

        # Create workflow runner
        workflow = WorkflowRunner(feature_dir)

        # Step 1: Verify prerequisites
        stage = workflow.detect_current_stage()
        assert stage == WorkflowStage.TASKS

        # Step 2: Get next story
        next_story = workflow.get_next_story()
        assert next_story.id == "US-001"

        # Step 3: Validate story ready
        valid, error = workflow.validate_story_ready("US-001")
        assert valid is True

        # Step 4: Start work on story
        story1.start_work()
        backlog.update_story(story1)

        # Step 5: Update progress
        workflow.update_story_progress("US-001", completed_tasks=5, actual_hours=10.0)

        story1_updated = backlog.get_story("US-001")
        assert story1_updated.metrics.completed_tasks == 5
        assert story1_updated.metrics.actual_hours == 10.0

        # Step 6: Complete story
        unblocked = workflow.mark_story_complete("US-001", actual_hours=18.5)

        story1_final = backlog.get_story("US-001")
        assert story1_final.status == StoryStatus.COMPLETE

        # Check if US-002 was unblocked
        story2_updated = backlog.get_story("US-002")
        # Note: US-002 won't auto-unblock because it's still DRAFT, needs manual READY
        assert "US-001" not in story2_updated.blocked_by


class TestProgressReportingWorkflow:
    """Test progress tracking and reporting workflow."""

    def test_progress_tracking(self, feature_dir):
        """Test progress tracking across multiple stories."""
        # Create feature files
        (feature_dir / "spec.md").write_text("# Spec")
        (feature_dir / "plan.md").write_text("# Plan")
        (feature_dir / "tasks.md").write_text("# Tasks")

        # Initialize tracker
        tracker = ProgressTracker(feature_dir)

        # Track phases
        tracker.track_phase_progress("design", 10, 10)
        tracker.track_phase_progress("implementation", 20, 10)
        tracker.track_phase_progress("testing", 15, 0)

        # Get progress
        progress = tracker.get_overall_progress()

        assert progress["total_tasks"] == 45
        assert progress["completed_tasks"] == 20
        assert progress["progress_percentage"] == pytest.approx(44.4, rel=0.1)

        # Get report
        report = tracker.generate_report()

        assert "Overall Progress" in report
        assert "44.4%" in report or "44%" in report

    def test_workflow_status_report(self, feature_dir):
        """Test generating comprehensive workflow status report."""
        # Setup feature
        (feature_dir / "spec.md").write_text("# Spec")
        (feature_dir / "plan.md").write_text("# Plan")
        (feature_dir / "tasks.md").write_text("# Tasks")

        # Create stories
        backlog = StoryBacklog(feature_dir)

        for i in range(1, 6):
            status = StoryStatus.COMPLETE if i <= 2 else (
                StoryStatus.IN_PROGRESS if i == 3 else StoryStatus.READY
            )

            story = UserStory(
                id=f"US-00{i}",
                epic_id="EPIC-001",
                title=f"Story {i}",
                description=f"Description {i}",
                acceptance_criteria=["AC1"],
                priority=StoryPriority.P1,
                status=status,
                dependencies=[],
                blocked_by=[],
                metrics=StoryMetrics(10, 10 if status == StoryStatus.COMPLETE else 5, 20.0, 18.0 if status == StoryStatus.COMPLETE else 10.0, 80.0),
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )

            backlog.add_story(story)

        # Generate workflow summary
        workflow = WorkflowRunner(feature_dir)
        summary = workflow.get_workflow_summary()

        assert summary["current_stage"] == "TASKS"
        assert summary["total_stories"] == 5
        assert summary["completed_stories"] == 2
        assert summary["in_progress_stories"] == 1


class TestEndToEndWorkflow:
    """Test complete end-to-end workflow."""

    def test_full_feature_workflow(self, feature_dir, templates_dir):
        """Test complete workflow from constitution to implementation."""
        # Enable RisoTech mode
        SpecifyConfig.enable_risotech_mode()

        # Step 1: Setup constitution
        constitution = Constitution.load_preset(
            ConstitutionPreset.REACT_TYPESCRIPT,
            templates_dir=templates_dir
        )
        constitution_file = feature_dir / "constitution.md"
        constitution.save_to_markdown(constitution_file)

        # Step 2: Create spec
        spec_file = feature_dir / "spec.md"
        spec_file.write_text("""
        # User Management Feature

        Complete user management system with authentication.
        """)

        # Step 3: Create plan
        plan_file = feature_dir / "plan.md"
        plan_file.write_text("""
        # Implementation Plan

        ## Tech Stack
        - React + TypeScript
        - JWT Authentication
        - Role-based access control

        ## Estimated Tasks: 40
        """)

        # Step 4: Analyze complexity
        analyzer = EpicAnalyzer(feature_dir)
        complexity = analyzer.analyze_complexity(
            "User management with auth",
            estimated_tasks=40
        )
        assert complexity == EpicComplexity.EPIC

        # Step 5: Decompose to stories
        stories = analyzer.decompose_feature_to_stories(
            "User management with registration, login, profile",
            estimated_tasks=40,
            context={'complexity': complexity}
        )
        assert len(stories) >= 3

        # Step 6: Initialize backlog
        backlog = StoryBacklog(feature_dir)
        for story in stories:
            backlog.add_story(story)

        # Step 7: Create workflow
        workflow = WorkflowRunner(feature_dir)

        # Step 8: Implement first story
        next_story = workflow.get_next_story()
        assert next_story is not None

        # Step 9: Track progress
        next_story.start_work()
        backlog.update_story(next_story)

        workflow.update_story_progress(next_story.id, completed_tasks=5, actual_hours=8.0)

        # Step 10: Complete story
        workflow.mark_story_complete(next_story.id, actual_hours=15.0)

        # Step 11: Verify completion
        completed_story = backlog.get_story(next_story.id)
        assert completed_story.status == StoryStatus.COMPLETE

        # Step 12: Get summary
        summary = workflow.get_workflow_summary()
        assert summary["completed_stories"] == 1

        # Cleanup
        SpecifyConfig.disable_risotech_mode()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
