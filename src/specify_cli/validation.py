"""Validation sub-task generation and management for Specify CLI."""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict
from pathlib import Path
import re


class ValidationType(Enum):
    """Types of validation checks."""
    UNIT_TEST = "unit_test"
    INTEGRATION_TEST = "integration_test"
    MANUAL_CHECK = "manual_check"
    CODE_REVIEW = "code_review"
    DOCUMENTATION = "documentation"
    PERFORMANCE = "performance"


@dataclass
class ValidationCheck:
    """Represents a single validation check."""
    id: str
    check_type: ValidationType
    description: str
    expected_result: str
    completed: bool = False
    notes: Optional[str] = None

    def to_markdown(self) -> str:
        """Convert validation check to markdown format."""
        status = "✅" if self.completed else "⬜"
        md = f"{status} **{self.check_type.value.replace('_', ' ').title()}**: {self.description}\n"
        md += f"   - Expected: {self.expected_result}\n"
        if self.notes:
            md += f"   - Notes: {self.notes}\n"
        return md


@dataclass
class Task:
    """Represents an implementation task with validation sub-tasks."""
    id: str
    title: str
    description: str
    implementation_steps: List[str]
    validation_checks: List[ValidationCheck]
    depends_on: List[str]
    estimated_hours: float

    def to_markdown(self) -> str:
        """Convert task to markdown format."""
        md = f"## Task {self.id}: {self.title}\n\n"
        md += f"**Estimated Hours:** {self.estimated_hours}\n\n"

        if self.depends_on:
            md += "**Dependencies:** " + ", ".join([f"Task {dep}" for dep in self.depends_on]) + "\n\n"

        md += f"### Description\n\n{self.description}\n\n"

        if self.implementation_steps:
            md += "### Implementation Steps\n\n"
            for i, step in enumerate(self.implementation_steps, 1):
                md += f"{i}. {step}\n"
            md += "\n"

        if self.validation_checks:
            md += "### Validation Checklist\n\n"
            for check in self.validation_checks:
                md += check.to_markdown()
            md += "\n"

        return md

    def is_complete(self) -> bool:
        """Check if all validation checks are complete."""
        return all(check.completed for check in self.validation_checks)

    def completion_percentage(self) -> float:
        """Calculate completion percentage based on validation checks."""
        if not self.validation_checks:
            return 0.0
        completed = sum(1 for check in self.validation_checks if check.completed)
        return (completed / len(self.validation_checks)) * 100


class ValidationSubtaskGenerator:
    """Generates validation sub-tasks for implementation tasks."""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()

    def generate_validation_checks(
        self,
        task_description: str,
        task_type: str = "feature"
    ) -> List[ValidationCheck]:
        """Generate validation checks for a task based on its description.

        Args:
            task_description: Description of the task
            task_type: Type of task (feature, bugfix, refactor, etc.)

        Returns:
            List of validation checks
        """
        checks = []

        # Always include unit tests for code tasks
        if any(keyword in task_description.lower() for keyword in ['implement', 'create', 'add', 'build']):
            checks.append(ValidationCheck(
                id="unit_test",
                check_type=ValidationType.UNIT_TEST,
                description="Write and run unit tests covering main functionality",
                expected_result="All unit tests pass with ≥80% coverage"
            ))

        # Add integration tests for features that interact with other components
        if any(keyword in task_description.lower() for keyword in ['api', 'database', 'service', 'integration']):
            checks.append(ValidationCheck(
                id="integration_test",
                check_type=ValidationType.INTEGRATION_TEST,
                description="Test integration with dependent components",
                expected_result="Integration tests pass and components communicate correctly"
            ))

        # Add manual checks for UI/UX features
        if any(keyword in task_description.lower() for keyword in ['ui', 'interface', 'page', 'component', 'display']):
            checks.append(ValidationCheck(
                id="manual_ui_check",
                check_type=ValidationType.MANUAL_CHECK,
                description="Manually verify UI/UX meets requirements",
                expected_result="UI is functional, responsive, and matches design specs"
            ))

        # Add performance checks for performance-critical tasks
        if any(keyword in task_description.lower() for keyword in ['performance', 'optimize', 'cache', 'scale']):
            checks.append(ValidationCheck(
                id="performance_check",
                check_type=ValidationType.PERFORMANCE,
                description="Verify performance meets requirements",
                expected_result="Performance benchmarks meet or exceed targets"
            ))

        # Add documentation check for new features
        if task_type == "feature":
            checks.append(ValidationCheck(
                id="documentation",
                check_type=ValidationType.DOCUMENTATION,
                description="Update relevant documentation",
                expected_result="Documentation is complete and accurate"
            ))

        # Always include code review
        checks.append(ValidationCheck(
            id="code_review",
            check_type=ValidationType.CODE_REVIEW,
            description="Code review completed",
            expected_result="Code follows style guide and best practices"
        ))

        return checks

    def create_task(
        self,
        task_id: str,
        title: str,
        description: str,
        implementation_steps: List[str],
        depends_on: Optional[List[str]] = None,
        estimated_hours: float = 4.0,
        task_type: str = "feature"
    ) -> Task:
        """Create a task with auto-generated validation checks.

        Args:
            task_id: Unique task identifier
            title: Task title
            description: Detailed description
            implementation_steps: List of implementation steps
            depends_on: List of task IDs this depends on
            estimated_hours: Estimated hours to complete
            task_type: Type of task (feature, bugfix, refactor)

        Returns:
            Task instance with validation checks
        """
        validation_checks = self.generate_validation_checks(description, task_type)

        return Task(
            id=task_id,
            title=title,
            description=description,
            implementation_steps=implementation_steps,
            validation_checks=validation_checks,
            depends_on=depends_on or [],
            estimated_hours=estimated_hours
        )

    def load_task_from_text(self, text: str) -> Optional[Task]:
        """Load a task from markdown text.

        Expected format:
        ## Task <id>: <title>
        **Estimated Hours:** <number>
        **Dependencies:** Task <id>, Task <id>
        ### Description
        <description>
        ### Implementation Steps
        1. <step>
        ### Validation Checklist
        ⬜/✅ **<type>**: <description>
           - Expected: <expected>
           - Notes: <notes>
        """
        # Extract task ID and title
        title_match = re.search(r'## Task\s+([^\:]+):\s*(.+)', text)
        if not title_match:
            return None

        task_id = title_match.group(1).strip()
        title = title_match.group(2).strip()

        # Extract estimated hours
        hours_match = re.search(r'\*\*Estimated Hours:\*\*\s+([\d.]+)', text)
        estimated_hours = float(hours_match.group(1)) if hours_match else 4.0

        # Extract dependencies
        deps_match = re.search(r'\*\*Dependencies:\*\*\s+(.+)', text)
        depends_on = []
        if deps_match:
            deps_text = deps_match.group(1)
            dep_matches = re.findall(r'Task\s+([^,\n]+)', deps_text)
            depends_on = [d.strip() for d in dep_matches]

        # Extract description
        desc_match = re.search(r'### Description\s+(.+?)(?=###|$)', text, re.DOTALL)
        description = desc_match.group(1).strip() if desc_match else ""

        # Extract implementation steps
        steps = []
        steps_match = re.search(r'### Implementation Steps\s+(.+?)(?=###|$)', text, re.DOTALL)
        if steps_match:
            steps_text = steps_match.group(1).strip()
            steps = [
                line.strip().lstrip('0123456789. ')
                for line in steps_text.split('\n')
                if line.strip() and not line.strip().startswith('#')
            ]

        # Extract validation checks
        validation_checks = []
        checks_match = re.search(r'### Validation Checklist\s+(.+?)(?=###|$)', text, re.DOTALL)
        if checks_match:
            checks_text = checks_match.group(1)
            check_lines = checks_text.split('\n')

            current_check = None
            for line in check_lines:
                # Check for status line
                status_match = re.match(r'([⬜✅])\s+\*\*([^:]+):\*\*\s+(.+)', line)
                if status_match:
                    if current_check:
                        validation_checks.append(current_check)

                    completed = status_match.group(1) == "✅"
                    check_type_str = status_match.group(2).strip()
                    description = status_match.group(3).strip()

                    # Try to match the type by converting to proper enum format
                    try:
                        # Convert "Unit Test" to "unit_test"
                        enum_str = check_type_str.lower().replace(' ', '_')
                        check_type = ValidationType(enum_str)
                    except ValueError:
                        check_type = ValidationType.MANUAL_CHECK

                    current_check = ValidationCheck(
                        id=f"check_{len(validation_checks) + 1}",
                        check_type=check_type,
                        description=description,
                        expected_result="",
                        completed=completed
                    )
                elif current_check:
                    # Extract expected result and notes
                    expected_match = re.match(r'\s+- Expected:\s+(.+)', line)
                    notes_match = re.match(r'\s+- Notes:\s+(.+)', line)

                    if expected_match:
                        current_check.expected_result = expected_match.group(1).strip()
                    elif notes_match:
                        current_check.notes = notes_match.group(1).strip()

            if current_check:
                validation_checks.append(current_check)

        return Task(
            id=task_id,
            title=title,
            description=description,
            implementation_steps=steps,
            validation_checks=validation_checks,
            depends_on=depends_on,
            estimated_hours=estimated_hours
        )

    def save_task_to_file(self, task: Task, file_path: Path) -> None:
        """Save a task to a markdown file.

        Args:
            task: Task to save
            file_path: Path to save the file
        """
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(task.to_markdown())

    def generate_progress_report(self, tasks: List[Task]) -> str:
        """Generate a progress report for a list of tasks.

        Args:
            tasks: List of tasks to report on

        Returns:
            Markdown formatted progress report
        """
        report = "# Task Progress Report\n\n"

        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task.is_complete())
        overall_progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        report += f"## Summary\n\n"
        report += f"- **Total Tasks:** {total_tasks}\n"
        report += f"- **Completed Tasks:** {completed_tasks}\n"
        report += f"- **Overall Progress:** {overall_progress:.1f}%\n\n"

        report += "## Task Details\n\n"

        for task in tasks:
            status_icon = "✅" if task.is_complete() else "🔄"
            progress = task.completion_percentage()
            report += f"### {status_icon} Task {task.id}: {task.title}\n"
            report += f"- **Progress:** {progress:.1f}%\n"
            report += f"- **Estimated Hours:** {task.estimated_hours}\n"

            if task.validation_checks:
                completed_checks = sum(1 for check in task.validation_checks if check.completed)
                report += f"- **Validation:** {completed_checks}/{len(task.validation_checks)} checks passed\n"

            report += "\n"

        return report

    def validate_task_dependencies(self, tasks: List[Task]) -> List[str]:
        """Validate that task dependencies are valid.

        Args:
            tasks: List of tasks to validate

        Returns:
            List of validation errors
        """
        errors = []
        task_ids = {task.id for task in tasks}

        for task in tasks:
            for dep in task.depends_on:
                if dep not in task_ids:
                    errors.append(
                        f"Task {task.id} depends on non-existent task {dep}"
                    )

        # Check for circular dependencies (simple check)
        for task in tasks:
            visited = set()
            stack = [task.id]

            while stack:
                current = stack.pop()
                if current in visited:
                    errors.append(f"Circular dependency detected involving Task {task.id}")
                    break
                visited.add(current)

                # Find task and add its dependencies
                current_task = next((t for t in tasks if t.id == current), None)
                if current_task:
                    stack.extend(current_task.depends_on)

        return errors
