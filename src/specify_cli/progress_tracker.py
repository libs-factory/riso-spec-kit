"""Progress tracking for Specify CLI implementation."""

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
import json


@dataclass
class TaskProgress:
    """Progress tracking for a single task."""
    task_id: str
    description: str
    status: str  # pending, in_progress, complete, failed
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    duration_minutes: float = 0.0


@dataclass
class PhaseProgress:
    """Progress tracking for a phase."""
    phase_name: str
    total_tasks: int
    completed_tasks: int
    tasks: List[TaskProgress]

    def progress_percentage(self) -> float:
        """Calculate progress percentage."""
        if self.total_tasks == 0:
            return 0.0
        return (self.completed_tasks / self.total_tasks) * 100


class ProgressTracker:
    """Tracks implementation progress across tasks and phases."""

    def __init__(self, feature_dir: Path):
        """Initialize progress tracker.

        Args:
            feature_dir: Feature directory
        """
        self.feature_dir = feature_dir
        self.progress_file = feature_dir / ".progress.json"
        self.phases: Dict[str, PhaseProgress] = {}
        self._load_progress()

    def _load_progress(self) -> None:
        """Load progress from file."""
        if self.progress_file.exists():
            data = json.loads(self.progress_file.read_text())
            for phase_name, phase_data in data.items():
                tasks = [TaskProgress(**t) for t in phase_data['tasks']]
                self.phases[phase_name] = PhaseProgress(
                    phase_name=phase_data['phase_name'],
                    total_tasks=phase_data['total_tasks'],
                    completed_tasks=phase_data['completed_tasks'],
                    tasks=tasks
                )

    def _save_progress(self) -> None:
        """Save progress to file."""
        data = {}
        for phase_name, phase in self.phases.items():
            data[phase_name] = {
                'phase_name': phase.phase_name,
                'total_tasks': phase.total_tasks,
                'completed_tasks': phase.completed_tasks,
                'tasks': [asdict(t) for t in phase.tasks]
            }
        self.progress_file.write_text(json.dumps(data, indent=2))

    def start_task(self, phase_name: str, task_id: str, description: str) -> None:
        """Mark a task as started."""
        if phase_name not in self.phases:
            self.phases[phase_name] = PhaseProgress(phase_name, 0, 0, [])

        task = TaskProgress(
            task_id=task_id,
            description=description,
            status="in_progress",
            started_at=datetime.now().isoformat()
        )
        self.phases[phase_name].tasks.append(task)
        self.phases[phase_name].total_tasks += 1
        self._save_progress()

    def complete_task(self, phase_name: str, task_id: str) -> None:
        """Mark a task as complete."""
        if phase_name in self.phases:
            for task in self.phases[phase_name].tasks:
                if task.task_id == task_id:
                    task.status = "complete"
                    task.completed_at = datetime.now().isoformat()
                    if task.started_at:
                        start = datetime.fromisoformat(task.started_at)
                        end = datetime.fromisoformat(task.completed_at)
                        task.duration_minutes = (end - start).total_seconds() / 60
                    self.phases[phase_name].completed_tasks += 1
                    break
            self._save_progress()

    def get_overall_progress(self) -> Dict:
        """Get overall progress summary."""
        total_tasks = sum(p.total_tasks for p in self.phases.values())
        completed_tasks = sum(p.completed_tasks for p in self.phases.values())

        return {
            'total_phases': len(self.phases),
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'progress_percentage': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            'phases': {name: p.progress_percentage() for name, p in self.phases.items()}
        }
