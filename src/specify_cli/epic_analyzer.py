"""EPIC (large feature) decomposition logic for Specify CLI."""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict
from pathlib import Path
import re


class EpicComplexity(Enum):
    """Complexity levels for EPIC features."""
    SMALL = "small"        # 1-5 tasks
    MEDIUM = "medium"      # 6-15 tasks
    LARGE = "large"        # 16-30 tasks
    EPIC = "epic"          # 30+ tasks


@dataclass
class Story:
    """Represents a user story decomposed from an EPIC."""
    id: str
    title: str
    description: str
    acceptance_criteria: List[str]
    estimated_tasks: int
    dependencies: List[str]
    priority: int  # 1-5, where 1 is highest

    def to_markdown(self) -> str:
        """Convert story to markdown format."""
        md = f"## Story {self.id}: {self.title}\n\n"
        md += f"**Priority:** {self.priority}/5\n"
        md += f"**Estimated Tasks:** {self.estimated_tasks}\n\n"
        md += f"### Description\n\n{self.description}\n\n"

        if self.acceptance_criteria:
            md += "### Acceptance Criteria\n\n"
            for i, criterion in enumerate(self.acceptance_criteria, 1):
                md += f"{i}. {criterion}\n"
            md += "\n"

        if self.dependencies:
            md += "### Dependencies\n\n"
            for dep in self.dependencies:
                md += f"- Story {dep}\n"
            md += "\n"

        return md


@dataclass
class Epic:
    """Represents a large feature that needs decomposition."""
    id: str
    title: str
    description: str
    business_value: str
    complexity: EpicComplexity
    stories: List[Story]

    def to_markdown(self) -> str:
        """Convert epic to markdown format."""
        md = f"# EPIC {self.id}: {self.title}\n\n"
        md += f"**Complexity:** {self.complexity.value}\n\n"
        md += f"## Business Value\n\n{self.business_value}\n\n"
        md += f"## Description\n\n{self.description}\n\n"
        md += f"## Story Breakdown ({len(self.stories)} stories)\n\n"

        for story in self.stories:
            md += story.to_markdown()
            md += "---\n\n"

        return md


class EpicAnalyzer:
    """Analyzes and decomposes EPIC features into manageable stories."""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()

    def analyze_complexity(self, description: str, estimated_tasks: int) -> EpicComplexity:
        """Analyze the complexity of a feature based on description and task estimate.

        Args:
            description: Feature description text
            estimated_tasks: Estimated number of tasks

        Returns:
            EpicComplexity level
        """
        if estimated_tasks <= 5:
            return EpicComplexity.SMALL
        elif estimated_tasks <= 15:
            return EpicComplexity.MEDIUM
        elif estimated_tasks <= 30:
            return EpicComplexity.LARGE
        else:
            return EpicComplexity.EPIC

    def should_decompose(self, estimated_tasks: int, complexity: EpicComplexity) -> bool:
        """Determine if a feature should be decomposed into stories.

        Args:
            estimated_tasks: Estimated number of tasks
            complexity: Complexity level of the feature

        Returns:
            True if decomposition is recommended
        """
        return complexity in [EpicComplexity.LARGE, EpicComplexity.EPIC]

    def create_epic(
        self,
        epic_id: str,
        title: str,
        description: str,
        business_value: str,
        estimated_tasks: int
    ) -> Epic:
        """Create an EPIC instance.

        Args:
            epic_id: Unique identifier for the epic
            title: Epic title
            description: Detailed description
            business_value: Business justification
            estimated_tasks: Estimated number of tasks

        Returns:
            Epic instance
        """
        complexity = self.analyze_complexity(description, estimated_tasks)

        return Epic(
            id=epic_id,
            title=title,
            description=description,
            business_value=business_value,
            complexity=complexity,
            stories=[]
        )

    def add_story_to_epic(self, epic: Epic, story: Story) -> None:
        """Add a story to an epic.

        Args:
            epic: Epic to add the story to
            story: Story to add
        """
        epic.stories.append(story)

    def extract_stories_from_text(self, text: str) -> List[Story]:
        """Extract story definitions from markdown text.

        Expected format:
        ## Story <id>: <title>
        **Priority:** <1-5>/5
        **Estimated Tasks:** <number>
        ### Description
        <description>
        ### Acceptance Criteria
        1. <criterion>
        ### Dependencies
        - Story <id>
        """
        stories = []
        story_sections = re.split(r'\n## Story ', text)

        for section in story_sections[1:]:  # Skip first split
            lines = section.split('\n')

            # Extract ID and title
            id_title_match = re.match(r'([^\:]+):\s*(.+)', lines[0])
            if not id_title_match:
                continue

            story_id = id_title_match.group(1).strip()
            title = id_title_match.group(2).strip()

            # Extract priority
            priority_match = re.search(r'\*\*Priority:\*\*\s+(\d+)/5', section)
            priority = int(priority_match.group(1)) if priority_match else 3

            # Extract estimated tasks
            tasks_match = re.search(r'\*\*Estimated Tasks:\*\*\s+(\d+)', section)
            estimated_tasks = int(tasks_match.group(1)) if tasks_match else 5

            # Extract description
            desc_match = re.search(r'### Description\s+(.+?)(?=###|$)', section, re.DOTALL)
            description = desc_match.group(1).strip() if desc_match else ""

            # Extract acceptance criteria
            criteria = []
            criteria_match = re.search(
                r'### Acceptance Criteria\s+(.+?)(?=###|$)',
                section,
                re.DOTALL
            )
            if criteria_match:
                criteria_text = criteria_match.group(1).strip()
                criteria = [
                    line.strip().lstrip('0123456789. ')
                    for line in criteria_text.split('\n')
                    if line.strip()
                ]

            # Extract dependencies
            dependencies = []
            deps_match = re.search(
                r'### Dependencies\s+(.+?)(?=###|$)',
                section,
                re.DOTALL
            )
            if deps_match:
                deps_text = deps_match.group(1).strip()
                dep_matches = re.findall(r'Story\s+([^\n]+)', deps_text)
                dependencies = [d.strip() for d in dep_matches]

            story = Story(
                id=story_id,
                title=title,
                description=description,
                acceptance_criteria=criteria,
                estimated_tasks=estimated_tasks,
                dependencies=dependencies,
                priority=priority
            )
            stories.append(story)

        return stories

    def load_epic_from_file(self, file_path: Path) -> Epic:
        """Load an EPIC from a markdown file.

        Args:
            file_path: Path to the epic markdown file

        Returns:
            Epic instance
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Epic file not found: {file_path}")

        content = file_path.read_text()

        # Extract epic metadata
        title_match = re.search(r'# EPIC\s+([^\:]+):\s*(.+)', content)
        if not title_match:
            raise ValueError("Invalid epic format: missing title")

        epic_id = title_match.group(1).strip()
        title = title_match.group(2).strip()

        # Extract complexity
        complexity_match = re.search(r'\*\*Complexity:\*\*\s+(\w+)', content)
        complexity = EpicComplexity(complexity_match.group(1)) if complexity_match else EpicComplexity.MEDIUM

        # Extract business value
        business_match = re.search(r'## Business Value\s+(.+?)(?=##|$)', content, re.DOTALL)
        business_value = business_match.group(1).strip() if business_match else ""

        # Extract description
        desc_match = re.search(r'## Description\s+(.+?)(?=##|$)', content, re.DOTALL)
        description = desc_match.group(1).strip() if desc_match else ""

        # Create epic
        epic = Epic(
            id=epic_id,
            title=title,
            description=description,
            business_value=business_value,
            complexity=complexity,
            stories=[]
        )

        # Extract stories
        stories = self.extract_stories_from_text(content)
        for story in stories:
            self.add_story_to_epic(epic, story)

        return epic

    def save_epic_to_file(self, epic: Epic, file_path: Path) -> None:
        """Save an EPIC to a markdown file.

        Args:
            epic: Epic to save
            file_path: Path to save the file
        """
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(epic.to_markdown())

    def generate_story_sequence(self, epic: Epic) -> List[Story]:
        """Generate an ordered sequence of stories based on dependencies and priority.

        Args:
            epic: Epic containing stories to sequence

        Returns:
            Ordered list of stories
        """
        # Create a dependency graph
        story_map = {story.id: story for story in epic.stories}
        sequenced = []
        processed = set()

        def process_story(story: Story):
            if story.id in processed:
                return

            # Process dependencies first
            for dep_id in story.dependencies:
                if dep_id in story_map and dep_id not in processed:
                    process_story(story_map[dep_id])

            sequenced.append(story)
            processed.add(story.id)

        # Sort by priority first, then process
        sorted_stories = sorted(epic.stories, key=lambda s: (s.priority, s.id))
        for story in sorted_stories:
            process_story(story)

        return sequenced

    def estimate_epic_duration(self, epic: Epic, tasks_per_day: int = 3) -> Dict[str, int]:
        """Estimate duration for an epic.

        Args:
            epic: Epic to estimate
            tasks_per_day: Average tasks completed per day

        Returns:
            Dictionary with duration estimates
        """
        total_tasks = sum(story.estimated_tasks for story in epic.stories)
        total_days = (total_tasks + tasks_per_day - 1) // tasks_per_day  # Round up
        total_weeks = (total_days + 4) // 5  # Assume 5 working days per week

        return {
            'total_tasks': total_tasks,
            'estimated_days': total_days,
            'estimated_weeks': total_weeks,
            'stories_count': len(epic.stories)
        }

    def decompose_feature_to_stories(
        self,
        feature_description: str,
        estimated_tasks: int,
        context: Optional[Dict] = None
    ) -> List[Story]:
        """Decompose a feature into user stories based on complexity.

        Args:
            feature_description: Description of the feature to decompose
            estimated_tasks: Estimated number of tasks
            context: Optional context (spec.md, data-model.md, etc.)

        Returns:
            List of decomposed user stories
        """
        complexity = self.analyze_complexity(feature_description, estimated_tasks)

        # For small/medium features, no decomposition needed
        if not self.should_decompose(estimated_tasks, complexity):
            return []

        stories = []
        context = context or {}

        # Strategy 1: Decompose by user roles/personas
        stories.extend(self._decompose_by_user_roles(feature_description, context))

        # Strategy 2: Decompose by functional areas
        if not stories:
            stories.extend(self._decompose_by_functional_areas(feature_description, context))

        # Strategy 3: Decompose by data entities (if data-model available)
        if not stories and 'data_model' in context:
            stories.extend(self._decompose_by_entities(feature_description, context))

        # Fallback: Create MVP + enhancement stories
        if not stories:
            stories = self._create_mvp_stories(feature_description, estimated_tasks)

        # Assign priorities and task estimates
        self._assign_priorities_and_estimates(stories, estimated_tasks)

        return stories

    def _decompose_by_user_roles(self, description: str, context: Dict) -> List[Story]:
        """Decompose by identifying different user roles/personas."""
        stories = []

        # Common role keywords
        role_keywords = ['admin', 'user', 'guest', 'manager', 'developer', 'viewer', 'editor']

        found_roles = []
        desc_lower = description.lower()
        for role in role_keywords:
            if role in desc_lower:
                found_roles.append(role.capitalize())

        # Create story per role if multiple roles found
        if len(found_roles) >= 2:
            for i, role in enumerate(found_roles, 1):
                story = Story(
                    id=f"US-{i:03d}",
                    title=f"{role} Workflow",
                    description=f"Implement functionality for {role} persona",
                    acceptance_criteria=[
                        f"{role} can access appropriate features",
                        f"{role} permissions enforced correctly"
                    ],
                    estimated_tasks=5,
                    dependencies=[],
                    priority=1 if i == 1 else 2
                )
                stories.append(story)

        return stories

    def _decompose_by_functional_areas(self, description: str, context: Dict) -> List[Story]:
        """Decompose by functional areas (CRUD, reporting, integration, etc.)."""
        stories = []

        # Identify functional patterns
        functional_patterns = {
            'create': ('Data Creation', ['Users can create new records', 'Validation rules enforced']),
            'read': ('Data Viewing', ['Users can view existing records', 'Search and filtering available']),
            'update': ('Data Modification', ['Users can update records', 'Change history tracked']),
            'delete': ('Data Removal', ['Users can delete records', 'Soft delete implemented']),
            'search': ('Search Functionality', ['Users can search records', 'Results ranked by relevance']),
            'export': ('Data Export', ['Users can export data', 'Multiple formats supported']),
            'import': ('Data Import', ['Users can import data', 'Validation on import']),
            'report': ('Reporting', ['Users can generate reports', 'Reports exportable'])
        }

        desc_lower = description.lower()
        story_id = 1

        for keyword, (title, criteria) in functional_patterns.items():
            if keyword in desc_lower:
                story = Story(
                    id=f"US-{story_id:03d}",
                    title=title,
                    description=f"Implement {keyword} functionality",
                    acceptance_criteria=criteria,
                    estimated_tasks=4,
                    dependencies=[],
                    priority=1 if keyword in ['create', 'read'] else 2
                )
                stories.append(story)
                story_id += 1

        return stories

    def _decompose_by_entities(self, description: str, context: Dict) -> List[Story]:
        """Decompose by data entities from data model."""
        stories = []

        # Extract entities from context (if data-model.md provided)
        entities = context.get('entities', [])

        for i, entity in enumerate(entities, 1):
            story = Story(
                id=f"US-{i:03d}",
                title=f"{entity} Management",
                description=f"Implement CRUD operations for {entity}",
                acceptance_criteria=[
                    f"Users can create {entity}",
                    f"Users can view {entity} list",
                    f"Users can update {entity}",
                    f"Users can delete {entity}"
                ],
                estimated_tasks=6,
                dependencies=[],
                priority=1 if i == 1 else 2
            )
            stories.append(story)

        return stories

    def _create_mvp_stories(self, description: str, estimated_tasks: int) -> List[Story]:
        """Create default MVP + enhancement stories."""
        mvp_tasks = max(5, estimated_tasks // 3)

        stories = [
            Story(
                id="US-001",
                title="MVP - Core Functionality",
                description="Implement minimum viable product with core features",
                acceptance_criteria=[
                    "Basic functionality works end-to-end",
                    "Happy path scenarios covered",
                    "Essential user workflows complete"
                ],
                estimated_tasks=mvp_tasks,
                dependencies=[],
                priority=1
            ),
            Story(
                id="US-002",
                title="Enhanced Features",
                description="Add enhanced features beyond MVP",
                acceptance_criteria=[
                    "Additional user workflows implemented",
                    "Edge cases handled",
                    "User experience improved"
                ],
                estimated_tasks=estimated_tasks - mvp_tasks - 5,
                dependencies=["US-001"],
                priority=2
            ),
            Story(
                id="US-003",
                title="Polish & Optimization",
                description="Performance optimization and final polish",
                acceptance_criteria=[
                    "Performance targets met",
                    "Error handling comprehensive",
                    "Documentation complete"
                ],
                estimated_tasks=5,
                dependencies=["US-001", "US-002"],
                priority=3
            )
        ]

        return stories

    def _assign_priorities_and_estimates(self, stories: List[Story], total_tasks: int) -> None:
        """Assign realistic priorities and task estimates to stories."""
        if not stories:
            return

        # Distribute tasks across stories
        tasks_per_story = max(3, total_tasks // len(stories))
        remaining_tasks = total_tasks

        for i, story in enumerate(stories):
            # First story gets slightly more (MVP foundation)
            if i == 0:
                story.estimated_tasks = min(remaining_tasks, tasks_per_story + 2)
            else:
                story.estimated_tasks = min(remaining_tasks, tasks_per_story)

            remaining_tasks -= story.estimated_tasks

            # Ensure minimum 3 tasks per story
            if story.estimated_tasks < 3 and remaining_tasks > 0:
                story.estimated_tasks = 3
                remaining_tasks -= 3

    def detect_story_dependencies(self, stories: List[Story]) -> Dict[str, List[str]]:
        """Detect dependencies between stories based on descriptions and entities.

        Args:
            stories: List of stories to analyze

        Returns:
            Dictionary mapping story IDs to their dependency IDs
        """
        dependencies = {}

        for story in stories:
            story_deps = []

            # Check for explicit dependency keywords
            desc_lower = story.description.lower()

            for other_story in stories:
                if story.id == other_story.id:
                    continue

                # MVP foundation dependency
                if 'mvp' in other_story.title.lower() and story.id != other_story.id:
                    if 'mvp' not in story.title.lower():
                        story_deps.append(other_story.id)

                # Entity dependency (e.g., "Comment" depends on "Post")
                # Look for mentions of other story titles in description
                other_title_lower = other_story.title.lower()
                if other_title_lower in desc_lower and other_story.priority < story.priority:
                    story_deps.append(other_story.id)

            dependencies[story.id] = story_deps

        return dependencies

    def apply_dependencies(self, stories: List[Story], dependencies: Dict[str, List[str]]) -> None:
        """Apply detected dependencies to stories.

        Args:
            stories: List of stories to update
            dependencies: Dictionary of story dependencies
        """
        story_map = {s.id: s for s in stories}

        for story_id, deps in dependencies.items():
            if story_id in story_map:
                # Merge with existing dependencies
                existing = set(story_map[story_id].dependencies)
                existing.update(deps)
                story_map[story_id].dependencies = list(existing)
