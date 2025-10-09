"""Tests for specify_cli.epic_analyzer module."""

import pytest
from pathlib import Path
from src.specify_cli.epic_analyzer import (
    EpicAnalyzer,
    Epic,
    Story,
    EpicComplexity
)


class TestEpicAnalyzer:
    """Test suite for EpicAnalyzer."""

    def test_analyze_complexity_small(self):
        """Test complexity analysis for small features."""
        analyzer = EpicAnalyzer()
        complexity = analyzer.analyze_complexity("Simple feature", 3)

        assert complexity == EpicComplexity.SMALL

    def test_analyze_complexity_medium(self):
        """Test complexity analysis for medium features."""
        analyzer = EpicAnalyzer()
        complexity = analyzer.analyze_complexity("Medium feature", 10)

        assert complexity == EpicComplexity.MEDIUM

    def test_analyze_complexity_large(self):
        """Test complexity analysis for large features."""
        analyzer = EpicAnalyzer()
        complexity = analyzer.analyze_complexity("Large feature", 25)

        assert complexity == EpicComplexity.LARGE

    def test_analyze_complexity_epic(self):
        """Test complexity analysis for epic features."""
        analyzer = EpicAnalyzer()
        complexity = analyzer.analyze_complexity("Epic feature", 40)

        assert complexity == EpicComplexity.EPIC

    def test_should_decompose_large(self):
        """Test that large features should be decomposed."""
        analyzer = EpicAnalyzer()

        assert analyzer.should_decompose(25, EpicComplexity.LARGE)
        assert analyzer.should_decompose(40, EpicComplexity.EPIC)

    def test_should_not_decompose_small(self):
        """Test that small features should not be decomposed."""
        analyzer = EpicAnalyzer()

        assert not analyzer.should_decompose(3, EpicComplexity.SMALL)
        assert not analyzer.should_decompose(10, EpicComplexity.MEDIUM)

    def test_create_epic(self):
        """Test creating an epic."""
        analyzer = EpicAnalyzer()

        epic = analyzer.create_epic(
            epic_id="001",
            title="User Authentication",
            description="Implement user authentication system",
            business_value="Secure user access",
            estimated_tasks=25
        )

        assert epic.id == "001"
        assert epic.title == "User Authentication"
        assert epic.complexity == EpicComplexity.LARGE
        assert len(epic.stories) == 0

    def test_add_story_to_epic(self):
        """Test adding a story to an epic."""
        analyzer = EpicAnalyzer()

        epic = analyzer.create_epic("001", "Title", "Desc", "Value", 25)
        story = Story(
            id="S1",
            title="Login",
            description="Implement login",
            acceptance_criteria=["User can log in"],
            estimated_tasks=5,
            dependencies=[],
            priority=1
        )

        analyzer.add_story_to_epic(epic, story)

        assert len(epic.stories) == 1
        assert epic.stories[0].id == "S1"

    def test_save_and_load_epic(self, tmp_path):
        """Test saving and loading epic from file."""
        analyzer = EpicAnalyzer()

        epic = Epic(
            id="001",
            title="Test Epic",
            description="Test description",
            business_value="Test value",
            complexity=EpicComplexity.LARGE,
            stories=[
                Story(
                    id="S1",
                    title="Story 1",
                    description="Story desc",
                    acceptance_criteria=["AC1", "AC2"],
                    estimated_tasks=5,
                    dependencies=[],
                    priority=1
                )
            ]
        )

        # Save
        file_path = tmp_path / "epic.md"
        analyzer.save_epic_to_file(epic, file_path)

        assert file_path.exists()

        # Load
        loaded_epic = analyzer.load_epic_from_file(file_path)

        assert loaded_epic.id == "001"
        assert loaded_epic.title == "Test Epic"
        assert len(loaded_epic.stories) == 1
        assert loaded_epic.stories[0].title == "Story 1"

    def test_generate_story_sequence_with_dependencies(self):
        """Test generating story sequence respecting dependencies."""
        analyzer = EpicAnalyzer()

        story1 = Story("S1", "Story 1", "Desc 1", [], 5, [], 1)
        story2 = Story("S2", "Story 2", "Desc 2", [], 5, ["S1"], 1)
        story3 = Story("S3", "Story 3", "Desc 3", [], 5, ["S2"], 1)

        epic = Epic("001", "Title", "Desc", "Value", EpicComplexity.LARGE, [story3, story1, story2])

        sequence = analyzer.generate_story_sequence(epic)

        assert len(sequence) == 3
        assert sequence[0].id == "S1"
        assert sequence[1].id == "S2"
        assert sequence[2].id == "S3"

    def test_generate_story_sequence_by_priority(self):
        """Test generating story sequence by priority."""
        analyzer = EpicAnalyzer()

        story1 = Story("S1", "Low Priority", "Desc", [], 5, [], 3)
        story2 = Story("S2", "High Priority", "Desc", [], 5, [], 1)
        story3 = Story("S3", "Medium Priority", "Desc", [], 5, [], 2)

        epic = Epic("001", "Title", "Desc", "Value", EpicComplexity.LARGE, [story1, story2, story3])

        sequence = analyzer.generate_story_sequence(epic)

        # Higher priority (lower number) should come first
        assert sequence[0].id == "S2"  # Priority 1
        assert sequence[1].id == "S3"  # Priority 2
        assert sequence[2].id == "S1"  # Priority 3

    def test_estimate_epic_duration(self):
        """Test estimating epic duration."""
        analyzer = EpicAnalyzer()

        epic = Epic(
            id="001",
            title="Title",
            description="Desc",
            business_value="Value",
            complexity=EpicComplexity.LARGE,
            stories=[
                Story("S1", "Story 1", "Desc", [], 5, [], 1),
                Story("S2", "Story 2", "Desc", [], 10, [], 1),
                Story("S3", "Story 3", "Desc", [], 7, [], 1),
            ]
        )

        estimate = analyzer.estimate_epic_duration(epic, tasks_per_day=3)

        assert estimate['total_tasks'] == 22
        assert estimate['estimated_days'] == 8  # 22 tasks / 3 per day = 7.33, rounded up
        assert estimate['estimated_weeks'] == 2  # 8 days / 5 days per week = 1.6, rounded up
        assert estimate['stories_count'] == 3


class TestStory:
    """Test suite for Story."""

    def test_story_to_markdown(self):
        """Test converting story to markdown."""
        story = Story(
            id="S1",
            title="User Login",
            description="Implement user login functionality",
            acceptance_criteria=["User can enter credentials", "User is authenticated"],
            estimated_tasks=5,
            dependencies=["S0"],
            priority=1
        )

        md = story.to_markdown()

        assert "## Story S1: User Login" in md
        assert "**Priority:** 1/5" in md
        assert "**Estimated Tasks:** 5" in md
        assert "Implement user login functionality" in md
        assert "1. User can enter credentials" in md
        assert "- Story S0" in md
