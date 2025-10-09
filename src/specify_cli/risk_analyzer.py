"""Risk assessment and management for project planning."""

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional
from datetime import datetime, timedelta

from .story_manager import StoryBacklog, StoryStatus
from .workflow_runner import WorkflowRunner


class RiskLevel(Enum):
    """Risk severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskCategory(Enum):
    """Categories of project risks."""
    SCHEDULE = "schedule"
    TECHNICAL = "technical"
    DEPENDENCIES = "dependencies"
    QUALITY = "quality"
    RESOURCE = "resource"
    SCOPE = "scope"


@dataclass
class Risk:
    """Represents a project risk."""
    id: str
    title: str
    description: str
    category: RiskCategory
    level: RiskLevel
    probability: float  # 0-1
    impact: float  # 0-1
    mitigation: str
    owner: str = "Team"
    status: str = "Open"  # Open, Mitigated, Accepted, Resolved

    def risk_score(self) -> float:
        """Calculate risk score (probability * impact)."""
        return self.probability * self.impact


class RiskAnalyzer:
    """Analyzes project for risks."""

    def __init__(self, workflow: Optional[WorkflowRunner] = None, backlog: Optional[StoryBacklog] = None):
        """Initialize risk analyzer.

        Args:
            workflow: Workflow runner
            backlog: Story backlog
        """
        self.workflow = workflow
        self.backlog = backlog

    def analyze_schedule_risks(self) -> List[Risk]:
        """Analyze schedule-related risks.

        Returns:
            List of schedule risks
        """
        risks = []

        if not self.backlog:
            return risks

        # Check velocity trend
        velocity = self.backlog.get_story_velocity()
        if velocity < 1.0:  # Less than 1 story per week
            risks.append(Risk(
                id="RISK-SCH-001",
                title="Low Velocity",
                description=f"Story completion velocity is {velocity:.2f} stories/week, below target",
                category=RiskCategory.SCHEDULE,
                level=RiskLevel.HIGH,
                probability=0.8,
                impact=0.7,
                mitigation="Break down stories into smaller tasks, remove blockers, increase team capacity"
            ))

        # Check blocked stories
        blocked_count = len(self.backlog.get_stories_by_status(StoryStatus.BLOCKED))
        total_count = len(self.backlog.stories)

        if total_count > 0 and blocked_count / total_count > 0.2:
            risks.append(Risk(
                id="RISK-SCH-002",
                title="High Blocked Story Percentage",
                description=f"{blocked_count} out of {total_count} stories ({blocked_count/total_count*100:.1f}%) are blocked",
                category=RiskCategory.SCHEDULE,
                level=RiskLevel.MEDIUM,
                probability=0.7,
                impact=0.6,
                mitigation="Resolve dependencies, re-prioritize stories, work on independent stories"
            ))

        return risks

    def analyze_technical_risks(self) -> List[Risk]:
        """Analyze technical risks.

        Returns:
            List of technical risks
        """
        risks = []

        if not self.backlog:
            return risks

        # Check for stories with high complexity
        complex_count = 0
        for story in self.backlog.stories.values():
            if story.metrics.estimated_tasks > 15:
                complex_count += 1

        if complex_count > 0:
            risks.append(Risk(
                id="RISK-TECH-001",
                title="High Complexity Stories",
                description=f"{complex_count} stories have high complexity (>15 tasks)",
                category=RiskCategory.TECHNICAL,
                level=RiskLevel.MEDIUM,
                probability=0.6,
                impact=0.7,
                mitigation="Break down complex stories, conduct technical spikes, involve senior developers"
            ))

        return risks

    def analyze_dependency_risks(self) -> List[Risk]:
        """Analyze dependency-related risks.

        Returns:
            List of dependency risks
        """
        risks = []

        if not self.backlog:
            return risks

        # Check for circular dependencies
        cycles = self.backlog.find_circular_dependencies()
        if cycles:
            risks.append(Risk(
                id="RISK-DEP-001",
                title="Circular Dependencies Detected",
                description=f"Found {len(cycles)} circular dependency chain(s)",
                category=RiskCategory.DEPENDENCIES,
                level=RiskLevel.CRITICAL,
                probability=1.0,
                impact=0.9,
                mitigation="Break circular dependencies, refactor story boundaries, reorder implementation"
            ))

        # Check for long dependency chains
        max_chain_length = 0
        for story in self.backlog.stories.values():
            chain_length = self._calculate_dependency_chain_length(story.id)
            if chain_length > max_chain_length:
                max_chain_length = chain_length

        if max_chain_length > 5:
            risks.append(Risk(
                id="RISK-DEP-002",
                title="Long Dependency Chains",
                description=f"Longest dependency chain is {max_chain_length} stories deep",
                category=RiskCategory.DEPENDENCIES,
                level=RiskLevel.MEDIUM,
                probability=0.7,
                impact=0.6,
                mitigation="Parallelize work where possible, reduce coupling between stories"
            ))

        return risks

    def analyze_quality_risks(self) -> List[Risk]:
        """Analyze quality-related risks.

        Returns:
            List of quality risks
        """
        risks = []

        if not self.backlog:
            return risks

        # Check test coverage
        total_coverage = 0
        story_count = 0
        for story in self.backlog.stories.values():
            if story.status == StoryStatus.COMPLETE:
                total_coverage += story.metrics.test_coverage
                story_count += 1

        if story_count > 0:
            avg_coverage = total_coverage / story_count
            if avg_coverage < 70:
                risks.append(Risk(
                    id="RISK-QUA-001",
                    title="Low Test Coverage",
                    description=f"Average test coverage is {avg_coverage:.1f}%, below 70% target",
                    category=RiskCategory.QUALITY,
                    level=RiskLevel.HIGH,
                    probability=0.8,
                    impact=0.8,
                    mitigation="Increase test writing, require tests before code review, add coverage gates"
                ))

        return risks

    def analyze_estimation_risks(self) -> List[Risk]:
        """Analyze estimation accuracy risks.

        Returns:
            List of estimation risks
        """
        risks = []

        if not self.backlog:
            return risks

        # Check estimation accuracy
        total_estimated = 0
        total_actual = 0
        completed_count = 0

        for story in self.backlog.stories.values():
            if story.status == StoryStatus.COMPLETE:
                total_estimated += story.metrics.estimated_hours
                total_actual += story.metrics.actual_hours
                completed_count += 1

        if completed_count >= 3:  # Need at least 3 completed stories
            if total_estimated > 0:
                accuracy = total_actual / total_estimated

                if accuracy > 1.5 or accuracy < 0.5:
                    risks.append(Risk(
                        id="RISK-EST-001",
                        title="Poor Estimation Accuracy",
                        description=f"Estimation accuracy is {accuracy:.2f}x (actual/estimated), significantly off target",
                        category=RiskCategory.SCHEDULE,
                        level=RiskLevel.MEDIUM,
                        probability=0.8,
                        impact=0.6,
                        mitigation="Review estimation process, use historical data, involve team in estimation"
                    ))

        return risks

    def _calculate_dependency_chain_length(self, story_id: str, visited: Optional[set] = None) -> int:
        """Calculate the length of dependency chain for a story.

        Args:
            story_id: Story ID
            visited: Set of visited story IDs (for cycle detection)

        Returns:
            Length of dependency chain
        """
        if not self.backlog:
            return 0

        if visited is None:
            visited = set()

        if story_id in visited:
            return 0  # Circular dependency

        visited.add(story_id)

        story = self.backlog.get_story(story_id)
        if not story or not story.dependencies:
            return 1

        max_depth = 0
        for dep_id in story.dependencies:
            depth = self._calculate_dependency_chain_length(dep_id, visited.copy())
            if depth > max_depth:
                max_depth = depth

        return max_depth + 1

    def get_all_risks(self) -> List[Risk]:
        """Get all identified risks.

        Returns:
            List of all risks
        """
        risks = []
        risks.extend(self.analyze_schedule_risks())
        risks.extend(self.analyze_technical_risks())
        risks.extend(self.analyze_dependency_risks())
        risks.extend(self.analyze_quality_risks())
        risks.extend(self.analyze_estimation_risks())

        # Sort by risk score (descending)
        risks.sort(key=lambda r: r.risk_score(), reverse=True)

        return risks

    def get_critical_risks(self) -> List[Risk]:
        """Get only critical and high risks.

        Returns:
            List of critical/high risks
        """
        all_risks = self.get_all_risks()
        return [r for r in all_risks if r.level in [RiskLevel.CRITICAL, RiskLevel.HIGH]]

    def generate_risk_report(self) -> Dict:
        """Generate risk assessment report.

        Returns:
            Dictionary with risk report
        """
        all_risks = self.get_all_risks()

        risk_by_level = {}
        for level in RiskLevel:
            risk_by_level[level.value] = len([r for r in all_risks if r.level == level])

        risk_by_category = {}
        for category in RiskCategory:
            risk_by_category[category.value] = len([r for r in all_risks if r.category == category])

        critical_risks = self.get_critical_risks()

        return {
            'total_risks': len(all_risks),
            'risk_by_level': risk_by_level,
            'risk_by_category': risk_by_category,
            'critical_risk_count': len(critical_risks),
            'highest_risk_score': all_risks[0].risk_score() if all_risks else 0.0,
            'top_risks': [
                {
                    'id': r.id,
                    'title': r.title,
                    'level': r.level.value,
                    'score': r.risk_score()
                }
                for r in all_risks[:5]
            ]
        }
