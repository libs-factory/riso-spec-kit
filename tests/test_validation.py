"""Tests for specify_cli.validation module."""

import pytest
from src.specify_cli.validation import (
    ValidationSubtaskGenerator,
    Task,
    ValidationCheck,
    ValidationType
)


class TestValidationSubtaskGenerator:
    """Test suite for ValidationSubtaskGenerator."""

    def test_generate_validation_checks_for_implementation(self):
        """Test generating checks for implementation tasks."""
        generator = ValidationSubtaskGenerator()

        checks = generator.generate_validation_checks(
            "Implement user authentication service",
            task_type="feature"
        )

        assert len(checks) > 0
        assert any(check.check_type == ValidationType.UNIT_TEST for check in checks)
        assert any(check.check_type == ValidationType.CODE_REVIEW for check in checks)
        assert any(check.check_type == ValidationType.DOCUMENTATION for check in checks)

    def test_generate_validation_checks_for_api_task(self):
        """Test generating checks for API tasks."""
        generator = ValidationSubtaskGenerator()

        checks = generator.generate_validation_checks(
            "Create REST API for user management",
            task_type="feature"
        )

        assert any(check.check_type == ValidationType.INTEGRATION_TEST for check in checks)

    def test_generate_validation_checks_for_ui_task(self):
        """Test generating checks for UI tasks."""
        generator = ValidationSubtaskGenerator()

        checks = generator.generate_validation_checks(
            "Build user interface for login page",
            task_type="feature"
        )

        assert any(check.check_type == ValidationType.MANUAL_CHECK for check in checks)

    def test_generate_validation_checks_for_performance_task(self):
        """Test generating checks for performance tasks."""
        generator = ValidationSubtaskGenerator()

        checks = generator.generate_validation_checks(
            "Optimize database query performance",
            task_type="feature"
        )

        assert any(check.check_type == ValidationType.PERFORMANCE for check in checks)

    def test_create_task(self):
        """Test creating a task with validation checks."""
        generator = ValidationSubtaskGenerator()

        task = generator.create_task(
            task_id="T1",
            title="Implement login",
            description="Create login functionality",
            implementation_steps=["Step 1", "Step 2"],
            estimated_hours=8.0,
            task_type="feature"
        )

        assert task.id == "T1"
        assert task.title == "Implement login"
        assert len(task.validation_checks) > 0
        assert task.estimated_hours == 8.0

    def test_task_is_complete(self):
        """Test checking if task is complete."""
        task = Task(
            id="T1",
            title="Test",
            description="Test task",
            implementation_steps=[],
            validation_checks=[
                ValidationCheck("c1", ValidationType.UNIT_TEST, "Test 1", "Pass", True),
                ValidationCheck("c2", ValidationType.CODE_REVIEW, "Test 2", "Pass", True)
            ],
            depends_on=[],
            estimated_hours=4.0
        )

        assert task.is_complete()

    def test_task_not_complete(self):
        """Test checking incomplete task."""
        task = Task(
            id="T1",
            title="Test",
            description="Test task",
            implementation_steps=[],
            validation_checks=[
                ValidationCheck("c1", ValidationType.UNIT_TEST, "Test 1", "Pass", True),
                ValidationCheck("c2", ValidationType.CODE_REVIEW, "Test 2", "Pass", False)
            ],
            depends_on=[],
            estimated_hours=4.0
        )

        assert not task.is_complete()

    def test_task_completion_percentage(self):
        """Test calculating task completion percentage."""
        task = Task(
            id="T1",
            title="Test",
            description="Test task",
            implementation_steps=[],
            validation_checks=[
                ValidationCheck("c1", ValidationType.UNIT_TEST, "Test 1", "Pass", True),
                ValidationCheck("c2", ValidationType.CODE_REVIEW, "Test 2", "Pass", True),
                ValidationCheck("c3", ValidationType.DOCUMENTATION, "Test 3", "Pass", False),
                ValidationCheck("c4", ValidationType.MANUAL_CHECK, "Test 4", "Pass", False)
            ],
            depends_on=[],
            estimated_hours=4.0
        )

        assert task.completion_percentage() == 50.0

    def test_save_and_load_task(self, tmp_path):
        """Test saving and loading task from file."""
        generator = ValidationSubtaskGenerator()

        task = Task(
            id="T1",
            title="Test Task",
            description="Test description",
            implementation_steps=["Step 1", "Step 2"],
            validation_checks=[
                ValidationCheck("c1", ValidationType.UNIT_TEST, "Write tests", "Tests pass", False)
            ],
            depends_on=["T0"],
            estimated_hours=5.0
        )

        # Save
        file_path = tmp_path / "task.md"
        generator.save_task_to_file(task, file_path)

        assert file_path.exists()

        # Load
        content = file_path.read_text()
        loaded_task = generator.load_task_from_text(content)

        assert loaded_task is not None
        assert loaded_task.id == "T1"
        assert loaded_task.title == "Test Task"
        assert len(loaded_task.validation_checks) == 1

    def test_generate_progress_report(self):
        """Test generating progress report."""
        generator = ValidationSubtaskGenerator()

        task1 = Task("T1", "Task 1", "Desc", [], [
            ValidationCheck("c1", ValidationType.UNIT_TEST, "Test", "Pass", True),
            ValidationCheck("c2", ValidationType.CODE_REVIEW, "Review", "Pass", True)
        ], [], 4.0)

        task2 = Task("T2", "Task 2", "Desc", [], [
            ValidationCheck("c1", ValidationType.UNIT_TEST, "Test", "Pass", False)
        ], [], 4.0)

        report = generator.generate_progress_report([task1, task2])

        assert "Task Progress Report" in report
        assert "Total Tasks:** 2" in report
        assert "Completed Tasks:** 1" in report
        assert "Overall Progress:** 50" in report

    def test_validate_task_dependencies_valid(self):
        """Test validating valid task dependencies."""
        generator = ValidationSubtaskGenerator()

        task1 = Task("T1", "Task 1", "Desc", [], [], [], 4.0)
        task2 = Task("T2", "Task 2", "Desc", [], [], ["T1"], 4.0)

        errors = generator.validate_task_dependencies([task1, task2])

        assert len(errors) == 0

    def test_validate_task_dependencies_missing(self):
        """Test validating missing dependencies."""
        generator = ValidationSubtaskGenerator()

        task1 = Task("T1", "Task 1", "Desc", [], [], ["T0"], 4.0)

        errors = generator.validate_task_dependencies([task1])

        assert len(errors) > 0
        assert "T0" in errors[0]


class TestValidationCheck:
    """Test suite for ValidationCheck."""

    def test_validation_check_to_markdown_incomplete(self):
        """Test converting incomplete check to markdown."""
        check = ValidationCheck(
            id="c1",
            check_type=ValidationType.UNIT_TEST,
            description="Write unit tests",
            expected_result="All tests pass"
        )

        md = check.to_markdown()

        assert "⬜" in md
        assert "Unit Test" in md
        assert "Write unit tests" in md
        assert "Expected: All tests pass" in md

    def test_validation_check_to_markdown_complete(self):
        """Test converting complete check to markdown."""
        check = ValidationCheck(
            id="c1",
            check_type=ValidationType.CODE_REVIEW,
            description="Code review",
            expected_result="Approved",
            completed=True,
            notes="Reviewed and approved"
        )

        md = check.to_markdown()

        assert "✅" in md
        assert "Code Review" in md
        assert "Notes: Reviewed and approved" in md
