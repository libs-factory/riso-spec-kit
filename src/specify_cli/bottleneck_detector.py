"""Bottleneck detection for workflow optimization."""

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional, Tuple
from collections import defaultdict

from .story_manager import StoryBacklog, StoryStatus, UserStory


class BottleneckType(Enum):
    """Types of bottlenecks."""
    DEPENDENCY = "dependency"  # Story blocking many others
    COMPLEXITY = "complexity"  # Very complex story slowing progress
    RESOURCE = "resource"  # Resource constraint
    BLOCKING_STATUS = "blocking_status"  # Stories stuck in same status
    LONG_DURATION = "long_duration"  # Story taking too long


@dataclass
class Bottleneck:
    """Represents a bottleneck in the workflow."""
    id: str
    type: BottleneckType
    severity: float  # 0-1 (how much it's blocking)
    description: str
    affected_stories: List[str]
    recommendations: List[str]

    def impact_score(self) -> float:
        """Calculate impact score based on severity and affected stories."""
        return self.severity * len(self.affected_stories)


class BottleneckDetector:
    """Detects workflow bottlenecks."""

    def __init__(self, backlog: StoryBacklog):
        """Initialize bottleneck detector.

        Args:
            backlog: Story backlog to analyze
        """
        self.backlog = backlog

    def detect_dependency_bottlenecks(self) -> List[Bottleneck]:
        """Detect stories that are blocking many others.

        Returns:
            List of dependency bottlenecks
        """
        bottlenecks = []

        # Count how many stories each story is blocking
        blocking_count = defaultdict(list)

        for story in self.backlog.stories.values():
            for dep_id in story.dependencies:
                dep_story = self.backlog.get_story(dep_id)
                if dep_story and dep_story.status != StoryStatus.COMPLETE:
                    blocking_count[dep_id].append(story.id)

        # Identify bottlenecks (blocking 3+ stories)
        for story_id, blocked_stories in blocking_count.items():
            if len(blocked_stories) >= 3:
                story = self.backlog.get_story(story_id)
                if story:
                    severity = min(len(blocked_stories) / 10, 1.0)

                    bottlenecks.append(Bottleneck(
                        id=f"BTL-DEP-{story_id}",
                        type=BottleneckType.DEPENDENCY,
                        severity=severity,
                        description=f"Story {story_id} ({story.title}) is blocking {len(blocked_stories)} other stories",
                        affected_stories=blocked_stories,
                        recommendations=[
                            f"Prioritize completing {story_id}",
                            "Consider breaking down this story for parallel work",
                            "Review if all dependencies are necessary"
                        ]
                    ))

        return bottlenecks

    def detect_complexity_bottlenecks(self) -> List[Bottleneck]:
        """Detect overly complex stories slowing progress.

        Returns:
            List of complexity bottlenecks
        """
        bottlenecks = []

        for story in self.backlog.stories.values():
            if story.status == StoryStatus.IN_PROGRESS:
                # Check if story is complex (>20 tasks)
                if story.metrics.estimated_tasks > 20:
                    progress = story.metrics.progress_percentage()

                    # If progress is slow (<30% after starting)
                    if progress < 30:
                        severity = (story.metrics.estimated_tasks - 20) / 30
                        severity = min(severity, 1.0)

                        bottlenecks.append(Bottleneck(
                            id=f"BTL-CPX-{story.id}",
                            type=BottleneckType.COMPLEXITY,
                            severity=severity,
                            description=f"Story {story.id} has high complexity ({story.metrics.estimated_tasks} tasks) with slow progress ({progress:.1f}%)",
                            affected_stories=[story.id],
                            recommendations=[
                                "Break down story into smaller sub-stories",
                                "Assign additional team members",
                                "Focus team effort on completing this story"
                            ]
                        ))

        return bottlenecks

    def detect_status_bottlenecks(self) -> List[Bottleneck]:
        """Detect stories stuck in the same status for too long.

        Returns:
            List of status bottlenecks
        """
        bottlenecks = []

        # Group stories by status
        status_groups = defaultdict(list)
        for story in self.backlog.stories.values():
            status_groups[story.status].append(story)

        # Check for too many in-progress stories (potential context switching)
        in_progress = status_groups[StoryStatus.IN_PROGRESS]
        if len(in_progress) > 5:
            severity = min(len(in_progress) / 10, 1.0)

            bottlenecks.append(Bottleneck(
                id="BTL-STA-001",
                type=BottleneckType.BLOCKING_STATUS,
                severity=severity,
                description=f"{len(in_progress)} stories are in progress simultaneously",
                affected_stories=[s.id for s in in_progress],
                recommendations=[
                    "Reduce work-in-progress (WIP) limit",
                    "Focus on completing stories before starting new ones",
                    "Consider team capacity constraints"
                ]
            ))

        # Check for too many blocked stories
        blocked = status_groups[StoryStatus.BLOCKED]
        if len(blocked) > 3:
            severity = min(len(blocked) / 5, 1.0)

            bottlenecks.append(Bottleneck(
                id="BTL-STA-002",
                type=BottleneckType.BLOCKING_STATUS,
                severity=severity,
                description=f"{len(blocked)} stories are blocked",
                affected_stories=[s.id for s in blocked],
                recommendations=[
                    "Prioritize unblocking stories",
                    "Review and resolve dependencies",
                    "Consider working on independent stories"
                ]
            ))

        return bottlenecks

    def detect_duration_bottlenecks(self) -> List[Bottleneck]:
        """Detect stories taking significantly longer than estimated.

        Returns:
            List of duration bottlenecks
        """
        bottlenecks = []

        for story in self.backlog.stories.values():
            if story.status == StoryStatus.IN_PROGRESS:
                if story.metrics.actual_hours > story.metrics.estimated_hours * 1.5:
                    # Story taking >150% of estimated time
                    overage = story.metrics.actual_hours / story.metrics.estimated_hours
                    severity = min((overage - 1.0) / 2.0, 1.0)

                    bottlenecks.append(Bottleneck(
                        id=f"BTL-DUR-{story.id}",
                        type=BottleneckType.LONG_DURATION,
                        severity=severity,
                        description=f"Story {story.id} is taking {overage:.1f}x longer than estimated ({story.metrics.actual_hours:.1f}h vs {story.metrics.estimated_hours:.1f}h)",
                        affected_stories=[story.id],
                        recommendations=[
                            "Review if scope has increased",
                            "Check for unexpected technical challenges",
                            "Consider pairing/mob programming",
                            "Re-estimate remaining work"
                        ]
                    ))

        return bottlenecks

    def find_critical_path(self) -> Tuple[List[str], float]:
        """Find the critical path through story dependencies.

        Returns:
            Tuple of (story_ids_in_critical_path, total_estimated_hours)
        """
        # Build dependency graph
        graph = {}
        for story in self.backlog.stories.values():
            graph[story.id] = {
                'dependencies': story.dependencies,
                'hours': story.metrics.estimated_hours,
                'status': story.status
            }

        # Find longest path (critical path)
        def longest_path(story_id: str, visited: set) -> Tuple[List[str], float]:
            if story_id in visited:
                return ([], 0.0)

            visited.add(story_id)

            if story_id not in graph:
                return ([story_id], 0.0)

            story_info = graph[story_id]

            # If already complete, no hours remaining
            hours = 0.0 if story_info['status'] == StoryStatus.COMPLETE else story_info['hours']

            if not story_info['dependencies']:
                return ([story_id], hours)

            max_path = []
            max_hours = 0.0

            for dep_id in story_info['dependencies']:
                dep_path, dep_hours = longest_path(dep_id, visited.copy())
                if dep_hours > max_hours:
                    max_hours = dep_hours
                    max_path = dep_path

            return (max_path + [story_id], max_hours + hours)

        # Find critical path starting from stories with no dependents
        critical_path = []
        critical_hours = 0.0

        # Find stories that aren't dependencies of any other story
        all_deps = set()
        for story in self.backlog.stories.values():
            all_deps.update(story.dependencies)

        leaf_stories = [s.id for s in self.backlog.stories.values() if s.id not in all_deps]

        for story_id in leaf_stories:
            path, hours = longest_path(story_id, set())
            if hours > critical_hours:
                critical_hours = hours
                critical_path = path

        return (critical_path, critical_hours)

    def get_all_bottlenecks(self) -> List[Bottleneck]:
        """Get all detected bottlenecks.

        Returns:
            List of all bottlenecks sorted by impact
        """
        bottlenecks = []
        bottlenecks.extend(self.detect_dependency_bottlenecks())
        bottlenecks.extend(self.detect_complexity_bottlenecks())
        bottlenecks.extend(self.detect_status_bottlenecks())
        bottlenecks.extend(self.detect_duration_bottlenecks())

        # Sort by impact score
        bottlenecks.sort(key=lambda b: b.impact_score(), reverse=True)

        return bottlenecks

    def generate_bottleneck_report(self) -> Dict:
        """Generate comprehensive bottleneck report.

        Returns:
            Dictionary with bottleneck analysis
        """
        bottlenecks = self.get_all_bottlenecks()
        critical_path, critical_hours = self.find_critical_path()

        bottleneck_by_type = defaultdict(int)
        for b in bottlenecks:
            bottleneck_by_type[b.type.value] += 1

        return {
            'total_bottlenecks': len(bottlenecks),
            'bottleneck_by_type': dict(bottleneck_by_type),
            'critical_path_stories': critical_path,
            'critical_path_hours': critical_hours,
            'highest_impact_bottleneck': {
                'id': bottlenecks[0].id,
                'type': bottlenecks[0].type.value,
                'impact': bottlenecks[0].impact_score(),
                'description': bottlenecks[0].description
            } if bottlenecks else None,
            'top_bottlenecks': [
                {
                    'id': b.id,
                    'type': b.type.value,
                    'severity': b.severity,
                    'impact': b.impact_score(),
                    'description': b.description,
                    'affected_count': len(b.affected_stories)
                }
                for b in bottlenecks[:5]
            ]
        }
