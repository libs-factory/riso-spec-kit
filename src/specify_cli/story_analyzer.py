"""Advanced story analysis for complexity and quality assessment."""

from dataclasses import dataclass
from typing import List, Dict, Optional
from pathlib import Path
import re

from .story_manager import UserStory, StoryBacklog
from .epic_analyzer import EpicComplexity


@dataclass
class ComplexityFactors:
    """Factors contributing to story complexity."""
    entity_count: int = 0
    integration_count: int = 0
    ui_complexity: int = 0  # 0-10 scale
    business_logic_complexity: int = 0  # 0-10 scale
    technical_debt: int = 0  # 0-10 scale
    dependency_count: int = 0

    def total_score(self) -> int:
        """Calculate total complexity score."""
        return (
            self.entity_count * 2 +
            self.integration_count * 3 +
            self.ui_complexity +
            self.business_logic_complexity +
            self.technical_debt +
            self.dependency_count
        )


@dataclass
class StoryQualityMetrics:
    """Quality metrics for a user story."""
    has_clear_acceptance_criteria: bool
    acceptance_criteria_count: int
    has_test_scenario: bool
    has_dependencies_documented: bool
    description_length: int
    title_clarity_score: int  # 0-10

    def quality_score(self) -> float:
        """Calculate quality score (0-100)."""
        score = 0.0

        # Clear acceptance criteria (30 points)
        if self.has_clear_acceptance_criteria:
            score += 20
            if self.acceptance_criteria_count >= 3:
                score += 10

        # Test scenario (20 points)
        if self.has_test_scenario:
            score += 20

        # Dependencies documented (15 points)
        if self.has_dependencies_documented:
            score += 15

        # Description quality (20 points)
        if self.description_length >= 100:
            score += 20
        elif self.description_length >= 50:
            score += 10

        # Title clarity (15 points)
        score += (self.title_clarity_score / 10) * 15

        return score


class StoryAnalyzer:
    """Analyzes user stories for complexity and quality."""

    def __init__(self, backlog: Optional[StoryBacklog] = None):
        """Initialize story analyzer.

        Args:
            backlog: Optional story backlog to analyze
        """
        self.backlog = backlog

    def analyze_complexity(self, story: UserStory) -> ComplexityFactors:
        """Analyze complexity of a user story.

        Args:
            story: Story to analyze

        Returns:
            ComplexityFactors with analysis results
        """
        factors = ComplexityFactors()

        desc_lower = story.description.lower()

        # Count entities (crude heuristic)
        entity_keywords = ['user', 'post', 'comment', 'product', 'order', 'customer']
        factors.entity_count = sum(1 for kw in entity_keywords if kw in desc_lower)

        # Count integrations
        integration_keywords = ['api', 'integration', 'external', 'third-party', 'webhook']
        factors.integration_count = sum(1 for kw in integration_keywords if kw in desc_lower)

        # UI complexity
        ui_keywords = ['form', 'dashboard', 'chart', 'table', 'modal', 'dialog']
        ui_count = sum(1 for kw in ui_keywords if kw in desc_lower)
        factors.ui_complexity = min(ui_count * 2, 10)

        # Business logic complexity
        logic_keywords = ['calculate', 'validate', 'process', 'transform', 'aggregate']
        logic_count = sum(1 for kw in logic_keywords if kw in desc_lower)
        factors.business_logic_complexity = min(logic_count * 2, 10)

        # Technical debt
        debt_keywords = ['refactor', 'legacy', 'migrate', 'upgrade', 'cleanup']
        debt_count = sum(1 for kw in debt_keywords if kw in desc_lower)
        factors.technical_debt = min(debt_count * 3, 10)

        # Dependencies
        factors.dependency_count = len(story.dependencies)

        return factors

    def analyze_quality(self, story: UserStory) -> StoryQualityMetrics:
        """Analyze quality of a user story.

        Args:
            story: Story to analyze

        Returns:
            StoryQualityMetrics with quality assessment
        """
        metrics = StoryQualityMetrics(
            has_clear_acceptance_criteria=len(story.acceptance_criteria) > 0,
            acceptance_criteria_count=len(story.acceptance_criteria),
            has_test_scenario=self._has_test_scenario(story),
            has_dependencies_documented=len(story.dependencies) > 0 or self._mentions_dependencies(story),
            description_length=len(story.description),
            title_clarity_score=self._assess_title_clarity(story.title)
        )

        return metrics

    def _has_test_scenario(self, story: UserStory) -> bool:
        """Check if story has a test scenario."""
        desc_lower = story.description.lower()
        test_keywords = ['given', 'when', 'then', 'test scenario', 'test case']
        return any(kw in desc_lower for kw in test_keywords)

    def _mentions_dependencies(self, story: UserStory) -> bool:
        """Check if story mentions dependencies in description."""
        desc_lower = story.description.lower()
        dep_keywords = ['depends on', 'requires', 'after', 'prerequisite']
        return any(kw in desc_lower for kw in dep_keywords)

    def _assess_title_clarity(self, title: str) -> int:
        """Assess title clarity (0-10).

        Good titles:
        - Start with action verb
        - Are specific
        - Are concise (3-8 words)
        """
        score = 5  # Base score

        words = title.split()
        word_count = len(words)

        # Action verb check
        action_verbs = ['create', 'update', 'delete', 'view', 'manage', 'implement', 'add', 'remove']
        if any(title.lower().startswith(verb) for verb in action_verbs):
            score += 2

        # Length check
        if 3 <= word_count <= 8:
            score += 2
        elif word_count > 12:
            score -= 2

        # Specificity check (has nouns)
        if any(word[0].isupper() for word in words[1:]):  # Proper nouns
            score += 1

        return min(max(score, 0), 10)

    def get_complexity_classification(self, factors: ComplexityFactors) -> EpicComplexity:
        """Classify story complexity.

        Args:
            factors: Complexity factors

        Returns:
            Complexity classification
        """
        score = factors.total_score()

        if score <= 5:
            return EpicComplexity.SMALL
        elif score <= 15:
            return EpicComplexity.MEDIUM
        elif score <= 30:
            return EpicComplexity.LARGE
        else:
            return EpicComplexity.EPIC

    def find_similar_stories(self, story: UserStory, threshold: float = 0.5) -> List[UserStory]:
        """Find similar stories in backlog.

        Args:
            story: Story to compare
            threshold: Similarity threshold (0-1)

        Returns:
            List of similar stories
        """
        if not self.backlog:
            return []

        similar = []
        story_words = set(story.description.lower().split())

        for other in self.backlog.stories.values():
            if other.id == story.id:
                continue

            other_words = set(other.description.lower().split())

            # Jaccard similarity
            intersection = len(story_words & other_words)
            union = len(story_words | other_words)

            if union > 0:
                similarity = intersection / union
                if similarity >= threshold:
                    similar.append(other)

        return similar

    def suggest_story_improvements(self, story: UserStory) -> List[str]:
        """Suggest improvements for a story.

        Args:
            story: Story to improve

        Returns:
            List of improvement suggestions
        """
        suggestions = []

        quality = self.analyze_quality(story)

        if not quality.has_clear_acceptance_criteria:
            suggestions.append("Add clear acceptance criteria (Given-When-Then format)")

        if quality.acceptance_criteria_count < 3:
            suggestions.append("Add more acceptance criteria (aim for 3-5)")

        if not quality.has_test_scenario:
            suggestions.append("Add independent test scenario")

        if quality.description_length < 50:
            suggestions.append("Expand description with more context and details")

        if quality.title_clarity_score < 7:
            suggestions.append("Improve title clarity (use action verb, be specific)")

        if len(story.dependencies) > 0 and not quality.has_dependencies_documented:
            suggestions.append("Document why dependencies are needed in description")

        complexity = self.analyze_complexity(story)
        if complexity.total_score() > 30:
            suggestions.append("Consider breaking down this story (complexity score > 30)")

        return suggestions

    def analyze_backlog(self) -> Dict:
        """Analyze entire backlog.

        Returns:
            Dictionary with backlog analysis
        """
        if not self.backlog:
            return {}

        total_stories = len(self.backlog.stories)
        if total_stories == 0:
            return {'total_stories': 0}

        complexities = []
        quality_scores = []
        needs_improvement = []

        for story in self.backlog.stories.values():
            factors = self.analyze_complexity(story)
            quality = self.analyze_quality(story)

            complexities.append(self.get_complexity_classification(factors))
            quality_scores.append(quality.quality_score())

            if quality.quality_score() < 70:
                needs_improvement.append(story.id)

        # Aggregate stats
        complexity_counts = {}
        for c in EpicComplexity:
            complexity_counts[c.value] = sum(1 for comp in complexities if comp == c)

        return {
            'total_stories': total_stories,
            'complexity_distribution': complexity_counts,
            'average_quality_score': sum(quality_scores) / len(quality_scores),
            'stories_needing_improvement': needs_improvement,
            'improvement_count': len(needs_improvement),
            'high_quality_stories': sum(1 for s in quality_scores if s >= 80)
        }
