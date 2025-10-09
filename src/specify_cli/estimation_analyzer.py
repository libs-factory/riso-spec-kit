"""Estimation accuracy analysis and improvement recommendations."""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from statistics import mean, stdev

from .story_manager import StoryBacklog, StoryStatus


@dataclass
class EstimationMetrics:
    """Metrics for estimation accuracy."""
    story_count: int
    total_estimated_hours: float
    total_actual_hours: float
    accuracy_ratio: float  # actual/estimated
    variance: float
    stories_over_estimated: int
    stories_under_estimated: int
    average_overrun_percentage: float

    def is_accurate(self) -> bool:
        """Check if estimation is reasonably accurate (0.8-1.2x)."""
        return 0.8 <= self.accuracy_ratio <= 1.2


@dataclass
class EstimationPattern:
    """Pattern in estimation errors."""
    pattern_type: str
    description: str
    affected_stories: List[str]
    recommendation: str


class EstimationAnalyzer:
    """Analyzes estimation accuracy and provides improvement recommendations."""

    def __init__(self, backlog: StoryBacklog):
        """Initialize estimation analyzer.

        Args:
            backlog: Story backlog to analyze
        """
        self.backlog = backlog

    def calculate_overall_metrics(self) -> Optional[EstimationMetrics]:
        """Calculate overall estimation metrics.

        Returns:
            EstimationMetrics or None if insufficient data
        """
        completed_stories = self.backlog.get_stories_by_status(StoryStatus.COMPLETE)

        if len(completed_stories) < 3:
            return None  # Not enough data

        total_estimated = 0.0
        total_actual = 0.0
        over_estimated = 0
        under_estimated = 0
        overrun_percentages = []

        for story in completed_stories:
            estimated = story.metrics.estimated_hours
            actual = story.metrics.actual_hours

            if estimated == 0:
                continue

            total_estimated += estimated
            total_actual += actual

            ratio = actual / estimated

            if ratio > 1.1:
                under_estimated += 1
                overrun_percentages.append((ratio - 1.0) * 100)
            elif ratio < 0.9:
                over_estimated += 1
                overrun_percentages.append((1.0 - ratio) * 100)

        if total_estimated == 0:
            return None

        accuracy_ratio = total_actual / total_estimated
        avg_overrun = mean(overrun_percentages) if overrun_percentages else 0.0

        # Calculate variance in estimation ratios
        ratios = [s.metrics.actual_hours / s.metrics.estimated_hours
                  for s in completed_stories
                  if s.metrics.estimated_hours > 0]
        variance = stdev(ratios) if len(ratios) > 1 else 0.0

        return EstimationMetrics(
            story_count=len(completed_stories),
            total_estimated_hours=total_estimated,
            total_actual_hours=total_actual,
            accuracy_ratio=accuracy_ratio,
            variance=variance,
            stories_over_estimated=over_estimated,
            stories_under_estimated=under_estimated,
            average_overrun_percentage=avg_overrun
        )

    def identify_patterns(self) -> List[EstimationPattern]:
        """Identify patterns in estimation errors.

        Returns:
            List of identified patterns
        """
        patterns = []
        completed_stories = self.backlog.get_stories_by_status(StoryStatus.COMPLETE)

        if len(completed_stories) < 3:
            return patterns

        # Pattern 1: Consistently under-estimating
        under_estimated = []
        for story in completed_stories:
            if story.metrics.estimated_hours > 0:
                ratio = story.metrics.actual_hours / story.metrics.estimated_hours
                if ratio > 1.2:
                    under_estimated.append(story.id)

        if len(under_estimated) >= 3:
            patterns.append(EstimationPattern(
                pattern_type="systematic_under_estimation",
                description=f"Consistently under-estimating stories ({len(under_estimated)} out of {len(completed_stories)})",
                affected_stories=under_estimated,
                recommendation="Add 20-30% buffer to estimates, review what's being missed in planning"
            ))

        # Pattern 2: High variance in estimation accuracy
        ratios = [s.metrics.actual_hours / s.metrics.estimated_hours
                  for s in completed_stories
                  if s.metrics.estimated_hours > 0]

        if len(ratios) > 2:
            variance = stdev(ratios)
            if variance > 0.5:
                patterns.append(EstimationPattern(
                    pattern_type="high_variance",
                    description=f"High variance in estimation accuracy (stdev: {variance:.2f})",
                    affected_stories=[s.id for s in completed_stories],
                    recommendation="Improve estimation consistency: use story points, reference similar past stories, involve team in estimation"
                ))

        # Pattern 3: Complex stories consistently under-estimated
        complex_under = []
        for story in completed_stories:
            if story.metrics.estimated_tasks > 10:
                if story.metrics.estimated_hours > 0:
                    ratio = story.metrics.actual_hours / story.metrics.estimated_hours
                    if ratio > 1.3:
                        complex_under.append(story.id)

        if len(complex_under) >= 2:
            patterns.append(EstimationPattern(
                pattern_type="complex_story_under_estimation",
                description=f"Complex stories (>10 tasks) consistently under-estimated ({len(complex_under)} stories)",
                affected_stories=complex_under,
                recommendation="Break down complex stories before estimation, add extra buffer for integration complexity"
            ))

        return patterns

    def get_estimation_by_complexity(self) -> Dict[str, Dict]:
        """Analyze estimation accuracy by story complexity.

        Returns:
            Dictionary with metrics grouped by complexity
        """
        completed_stories = self.backlog.get_stories_by_status(StoryStatus.COMPLETE)

        complexity_groups = {
            'simple': [],  # 1-5 tasks
            'medium': [],  # 6-10 tasks
            'complex': []  # 11+ tasks
        }

        for story in completed_stories:
            if story.metrics.estimated_hours == 0:
                continue

            ratio = story.metrics.actual_hours / story.metrics.estimated_hours
            tasks = story.metrics.estimated_tasks

            if tasks <= 5:
                complexity_groups['simple'].append(ratio)
            elif tasks <= 10:
                complexity_groups['medium'].append(ratio)
            else:
                complexity_groups['complex'].append(ratio)

        result = {}
        for complexity, ratios in complexity_groups.items():
            if ratios:
                result[complexity] = {
                    'count': len(ratios),
                    'avg_ratio': mean(ratios),
                    'accuracy': 'good' if 0.8 <= mean(ratios) <= 1.2 else 'poor'
                }

        return result

    def suggest_improvements(self) -> List[str]:
        """Suggest improvements to estimation process.

        Returns:
            List of improvement suggestions
        """
        suggestions = []
        metrics = self.calculate_overall_metrics()

        if not metrics:
            suggestions.append("Complete at least 3 stories to analyze estimation accuracy")
            return suggestions

        # Check overall accuracy
        if metrics.accuracy_ratio > 1.2:
            suggestions.append(f"Stories taking {metrics.accuracy_ratio:.1f}x longer than estimated - add 20-30% buffer to estimates")
        elif metrics.accuracy_ratio < 0.8:
            suggestions.append(f"Over-estimating by {(1.0 - metrics.accuracy_ratio) * 100:.1f}% - refine estimates to be more aggressive")

        # Check variance
        if metrics.variance > 0.5:
            suggestions.append("High variance in estimates - establish estimation baseline using reference stories")

        # Check patterns
        patterns = self.identify_patterns()
        for pattern in patterns:
            suggestions.append(f"{pattern.pattern_type.replace('_', ' ').title()}: {pattern.recommendation}")

        # Check sample size
        if metrics.story_count < 5:
            suggestions.append(f"Only {metrics.story_count} completed stories - complete more stories for better analysis")

        return suggestions

    def predict_story_duration(self, estimated_hours: float, task_count: int) -> Tuple[float, float]:
        """Predict actual duration based on historical data.

        Args:
            estimated_hours: Initial estimate
            task_count: Number of tasks

        Returns:
            Tuple of (predicted_hours, confidence_interval)
        """
        metrics = self.calculate_overall_metrics()

        if not metrics or metrics.story_count < 3:
            # Not enough data, return estimate with wide confidence interval
            return (estimated_hours, estimated_hours * 0.5)

        # Adjust based on historical accuracy
        predicted = estimated_hours * metrics.accuracy_ratio

        # Adjust based on complexity
        complexity_metrics = self.get_estimation_by_complexity()

        if task_count <= 5 and 'simple' in complexity_metrics:
            predicted *= complexity_metrics['simple']['avg_ratio'] / metrics.accuracy_ratio
        elif task_count <= 10 and 'medium' in complexity_metrics:
            predicted *= complexity_metrics['medium']['avg_ratio'] / metrics.accuracy_ratio
        elif 'complex' in complexity_metrics:
            predicted *= complexity_metrics['complex']['avg_ratio'] / metrics.accuracy_ratio

        # Confidence interval based on variance
        confidence = predicted * metrics.variance

        return (predicted, confidence)

    def generate_report(self) -> Dict:
        """Generate comprehensive estimation analysis report.

        Returns:
            Dictionary with estimation analysis
        """
        metrics = self.calculate_overall_metrics()

        if not metrics:
            return {
                'status': 'insufficient_data',
                'message': 'Need at least 3 completed stories for analysis'
            }

        patterns = self.identify_patterns()
        by_complexity = self.get_estimation_by_complexity()
        suggestions = self.suggest_improvements()

        return {
            'status': 'analyzed',
            'overall_metrics': {
                'story_count': metrics.story_count,
                'total_estimated_hours': metrics.total_estimated_hours,
                'total_actual_hours': metrics.total_actual_hours,
                'accuracy_ratio': metrics.accuracy_ratio,
                'accuracy_status': 'good' if metrics.is_accurate() else 'needs_improvement',
                'variance': metrics.variance,
                'over_estimated_count': metrics.stories_over_estimated,
                'under_estimated_count': metrics.stories_under_estimated,
                'average_overrun_percentage': metrics.average_overrun_percentage
            },
            'patterns': [
                {
                    'type': p.pattern_type,
                    'description': p.description,
                    'affected_count': len(p.affected_stories),
                    'recommendation': p.recommendation
                }
                for p in patterns
            ],
            'by_complexity': by_complexity,
            'suggestions': suggestions
        }
