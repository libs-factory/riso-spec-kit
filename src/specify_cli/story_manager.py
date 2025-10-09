"""User story management and tracking for Specify CLI."""

from dataclasses import dataclass, asdict
from enum import Enum
from typing import List, Optional, Dict, Set
from pathlib import Path
import json
from datetime import datetime


class StoryStatus(Enum):
    """Status of a user story."""
    DRAFT = "draft"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    BLOCKED = "blocked"


class StoryPriority(Enum):
    """Priority levels for user stories."""
    P1 = "p1"  # Must Have - MVP
    P2 = "p2"  # Should Have
    P3 = "p3"  # Nice to Have


@dataclass
class StoryMetrics:
    """Metrics tracking for a user story."""
    estimated_tasks: int
    completed_tasks: int
    estimated_hours: float
    actual_hours: float
    test_coverage: float  # Percentage

    def progress_percentage(self) -> float:
        """Calculate progress percentage."""
        if self.estimated_tasks == 0:
            return 0.0
        return (self.completed_tasks / self.estimated_tasks) * 100

    def is_complete(self) -> bool:
        """Check if all tasks are complete."""
        return self.completed_tasks >= self.estimated_tasks


@dataclass
class UserStory:
    """Represents a user story with tracking metadata."""
    id: str
    epic_id: Optional[str]
    title: str
    description: str
    acceptance_criteria: List[str]
    priority: StoryPriority
    status: StoryStatus
    dependencies: List[str]
    blocked_by: List[str]
    metrics: StoryMetrics
    created_at: str
    updated_at: str
    completed_at: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        data = asdict(self)
        data['priority'] = self.priority.value
        data['status'] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> 'UserStory':
        """Create from dictionary."""
        metrics_data = data.pop('metrics')
        metrics = StoryMetrics(**metrics_data)

        data['priority'] = StoryPriority(data['priority'])
        data['status'] = StoryStatus(data['status'])
        data['metrics'] = metrics

        return cls(**data)

    def mark_complete(self) -> None:
        """Mark story as complete."""
        self.status = StoryStatus.COMPLETE
        self.completed_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def mark_blocked(self, blocker_ids: List[str]) -> None:
        """Mark story as blocked."""
        self.status = StoryStatus.BLOCKED
        self.blocked_by = blocker_ids
        self.updated_at = datetime.now().isoformat()

    def unblock(self) -> None:
        """Unblock story."""
        self.blocked_by = []
        self.status = StoryStatus.READY
        self.updated_at = datetime.now().isoformat()

    def start_work(self) -> None:
        """Start working on story."""
        self.status = StoryStatus.IN_PROGRESS
        self.updated_at = datetime.now().isoformat()

    def update_progress(self, completed_tasks: int, actual_hours: float = 0) -> None:
        """Update progress metrics."""
        self.metrics.completed_tasks = completed_tasks
        if actual_hours > 0:
            self.metrics.actual_hours = actual_hours
        self.updated_at = datetime.now().isoformat()

        # Auto-complete if all tasks done
        if self.metrics.is_complete() and self.status != StoryStatus.COMPLETE:
            self.mark_complete()


class StoryBacklog:
    """Manages a backlog of user stories."""

    def __init__(self, feature_dir: Path):
        """Initialize story backlog.

        Args:
            feature_dir: Feature directory containing stories
        """
        self.feature_dir = feature_dir
        self.stories_dir = feature_dir / "stories"
        self.stories_dir.mkdir(parents=True, exist_ok=True)
        self.backlog_file = self.stories_dir / "backlog.json"
        self.stories: Dict[str, UserStory] = {}
        self._load_backlog()

    def _load_backlog(self) -> None:
        """Load stories from backlog file."""
        if self.backlog_file.exists():
            data = json.loads(self.backlog_file.read_text())
            self.stories = {
                story_id: UserStory.from_dict(story_data)
                for story_id, story_data in data.items()
            }

    def _save_backlog(self) -> None:
        """Save stories to backlog file."""
        data = {
            story_id: story.to_dict()
            for story_id, story in self.stories.items()
        }
        self.backlog_file.write_text(json.dumps(data, indent=2))

    def add_story(self, story: UserStory) -> None:
        """Add a story to the backlog.

        Args:
            story: Story to add
        """
        self.stories[story.id] = story
        self._save_backlog()

    def get_story(self, story_id: str) -> Optional[UserStory]:
        """Get a story by ID.

        Args:
            story_id: Story ID

        Returns:
            Story if found, None otherwise
        """
        return self.stories.get(story_id)

    def update_story(self, story: UserStory) -> None:
        """Update a story in the backlog.

        Args:
            story: Updated story
        """
        story.updated_at = datetime.now().isoformat()
        self.stories[story.id] = story
        self._save_backlog()

    def remove_story(self, story_id: str) -> bool:
        """Remove a story from the backlog.

        Args:
            story_id: Story ID to remove

        Returns:
            True if removed, False if not found
        """
        if story_id in self.stories:
            del self.stories[story_id]
            self._save_backlog()
            return True
        return False

    def get_stories_by_status(self, status: StoryStatus) -> List[UserStory]:
        """Get all stories with a specific status.

        Args:
            status: Status to filter by

        Returns:
            List of stories with that status
        """
        return [
            story for story in self.stories.values()
            if story.status == status
        ]

    def get_stories_by_priority(self, priority: StoryPriority) -> List[UserStory]:
        """Get all stories with a specific priority.

        Args:
            priority: Priority to filter by

        Returns:
            List of stories with that priority
        """
        return [
            story for story in self.stories.values()
            if story.priority == priority
        ]

    def get_stories_by_epic(self, epic_id: str) -> List[UserStory]:
        """Get all stories belonging to an epic.

        Args:
            epic_id: EPIC ID

        Returns:
            List of stories in that epic
        """
        return [
            story for story in self.stories.values()
            if story.epic_id == epic_id
        ]

    def get_ready_stories(self) -> List[UserStory]:
        """Get all stories that are ready to work on (no blockers).

        Returns:
            List of ready stories
        """
        return [
            story for story in self.stories.values()
            if story.status == StoryStatus.READY and not story.blocked_by
        ]

    def get_next_story(self) -> Optional[UserStory]:
        """Get the next highest priority ready story.

        Returns:
            Next story to work on, or None if no ready stories
        """
        ready_stories = self.get_ready_stories()
        if not ready_stories:
            return None

        # Sort by priority (P1 > P2 > P3), then by ID
        ready_stories.sort(key=lambda s: (s.priority.value, s.id))
        return ready_stories[0]

    def check_dependencies(self, story_id: str) -> List[str]:
        """Check if a story's dependencies are complete.

        Args:
            story_id: Story ID to check

        Returns:
            List of incomplete dependency IDs
        """
        story = self.get_story(story_id)
        if not story:
            return []

        incomplete_deps = []
        for dep_id in story.dependencies:
            dep_story = self.get_story(dep_id)
            if dep_story and dep_story.status != StoryStatus.COMPLETE:
                incomplete_deps.append(dep_id)

        return incomplete_deps

    def update_blocked_status(self) -> int:
        """Update blocked status for all stories based on dependencies.

        Returns:
            Number of stories that changed status
        """
        changed = 0

        for story in self.stories.values():
            incomplete_deps = self.check_dependencies(story.id)

            # Block if has incomplete dependencies
            if incomplete_deps and story.status != StoryStatus.BLOCKED:
                story.mark_blocked(incomplete_deps)
                changed += 1

            # Unblock if all dependencies complete
            elif not incomplete_deps and story.status == StoryStatus.BLOCKED:
                story.unblock()
                changed += 1

        if changed > 0:
            self._save_backlog()

        return changed

    def get_backlog_summary(self) -> Dict:
        """Get summary statistics for the backlog.

        Returns:
            Dictionary with summary metrics
        """
        total_stories = len(self.stories)

        status_counts = {}
        for status in StoryStatus:
            status_counts[status.value] = len(self.get_stories_by_status(status))

        priority_counts = {}
        for priority in StoryPriority:
            priority_counts[priority.value] = len(self.get_stories_by_priority(priority))

        total_estimated_hours = sum(s.metrics.estimated_hours for s in self.stories.values())
        total_actual_hours = sum(s.metrics.actual_hours for s in self.stories.values())

        completed_stories = len(self.get_stories_by_status(StoryStatus.COMPLETE))
        completion_rate = (completed_stories / total_stories * 100) if total_stories > 0 else 0

        return {
            'total_stories': total_stories,
            'status_counts': status_counts,
            'priority_counts': priority_counts,
            'total_estimated_hours': total_estimated_hours,
            'total_actual_hours': total_actual_hours,
            'completion_rate': completion_rate,
            'next_story': self.get_next_story().id if self.get_next_story() else None
        }

    def generate_dependency_graph(self) -> Dict[str, List[str]]:
        """Generate dependency graph for visualization.

        Returns:
            Dictionary mapping story IDs to their dependencies
        """
        graph = {}
        for story in self.stories.values():
            graph[story.id] = story.dependencies
        return graph

    def find_circular_dependencies(self) -> List[List[str]]:
        """Find circular dependencies in the backlog.

        Returns:
            List of circular dependency chains
        """
        graph = self.generate_dependency_graph()
        visited = set()
        rec_stack = set()
        cycles = []

        def dfs(node: str, path: List[str]):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor, path.copy())
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles.append(cycle)

            rec_stack.remove(node)

        for story_id in graph.keys():
            if story_id not in visited:
                dfs(story_id, [])

        return cycles

    def get_story_velocity(self) -> float:
        """Calculate story completion velocity (stories per week).

        Returns:
            Average stories completed per week
        """
        completed_stories = self.get_stories_by_status(StoryStatus.COMPLETE)

        if not completed_stories:
            return 0.0

        # Calculate time span
        completed_dates = [
            datetime.fromisoformat(s.completed_at)
            for s in completed_stories
            if s.completed_at
        ]

        if len(completed_dates) < 2:
            return 0.0

        earliest = min(completed_dates)
        latest = max(completed_dates)
        weeks = (latest - earliest).days / 7

        if weeks == 0:
            return len(completed_stories)

        return len(completed_stories) / weeks


class StoryManager:
    """High-level manager for user stories and backlogs."""

    def __init__(self, specs_dir: Path):
        """Initialize story manager.

        Args:
            specs_dir: Specifications directory
        """
        self.specs_dir = specs_dir
        self.backlogs: Dict[str, StoryBacklog] = {}

    def get_backlog(self, feature_id: str) -> StoryBacklog:
        """Get or create backlog for a feature.

        Args:
            feature_id: Feature ID

        Returns:
            StoryBacklog instance
        """
        if feature_id not in self.backlogs:
            feature_dir = self.specs_dir / feature_id
            self.backlogs[feature_id] = StoryBacklog(feature_dir)

        return self.backlogs[feature_id]

    def create_story_from_template(
        self,
        story_id: str,
        title: str,
        description: str,
        priority: StoryPriority,
        estimated_tasks: int = 5,
        estimated_hours: float = 10.0,
        epic_id: Optional[str] = None
    ) -> UserStory:
        """Create a new story from template.

        Args:
            story_id: Unique story ID
            title: Story title
            description: Story description
            priority: Story priority
            estimated_tasks: Estimated number of tasks
            estimated_hours: Estimated hours
            epic_id: Optional EPIC ID

        Returns:
            New UserStory instance
        """
        now = datetime.now().isoformat()

        return UserStory(
            id=story_id,
            epic_id=epic_id,
            title=title,
            description=description,
            acceptance_criteria=[],
            priority=priority,
            status=StoryStatus.DRAFT,
            dependencies=[],
            blocked_by=[],
            metrics=StoryMetrics(
                estimated_tasks=estimated_tasks,
                completed_tasks=0,
                estimated_hours=estimated_hours,
                actual_hours=0.0,
                test_coverage=0.0
            ),
            created_at=now,
            updated_at=now
        )

    def list_all_features(self) -> List[str]:
        """List all features with stories.

        Returns:
            List of feature IDs
        """
        features = []

        for item in self.specs_dir.iterdir():
            if item.is_dir() and (item / "stories" / "backlog.json").exists():
                features.append(item.name)

        return features

    def get_overall_summary(self) -> Dict:
        """Get summary across all features.

        Returns:
            Overall summary statistics
        """
        feature_ids = self.list_all_features()

        total_stories = 0
        total_complete = 0
        total_estimated_hours = 0.0
        total_actual_hours = 0.0

        for feature_id in feature_ids:
            backlog = self.get_backlog(feature_id)
            summary = backlog.get_backlog_summary()

            total_stories += summary['total_stories']
            total_complete += summary['status_counts'].get('complete', 0)
            total_estimated_hours += summary['total_estimated_hours']
            total_actual_hours += summary['total_actual_hours']

        completion_rate = (total_complete / total_stories * 100) if total_stories > 0 else 0

        return {
            'total_features': len(feature_ids),
            'total_stories': total_stories,
            'total_complete': total_complete,
            'completion_rate': completion_rate,
            'total_estimated_hours': total_estimated_hours,
            'total_actual_hours': total_actual_hours,
            'features': feature_ids
        }
