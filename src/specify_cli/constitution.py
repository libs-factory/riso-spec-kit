"""Tiered constitution management for Specify CLI."""

from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional
import re
import pkg_resources


class ConstitutionTier(Enum):
    """Constitution tiers with different priorities."""
    CORE = "core"
    HIGH_PRIORITY = "high-priority"
    FLEXIBLE = "flexible"


class ConstitutionPreset(Enum):
    """Available constitution presets."""
    REACT_TYPESCRIPT = "react-typescript"
    NEXTJS_TAILWIND = "nextjs-tailwind"
    DJANGO_POSTGRESQL = "django-postgresql"


class ConstitutionRule:
    """Represents a single constitution rule."""

    def __init__(
        self,
        title: str,
        description: str,
        tier: ConstitutionTier,
        rationale: Optional[str] = None,
        examples: Optional[List[str]] = None
    ):
        self.title = title
        self.description = description
        self.tier = tier
        self.rationale = rationale or ""
        self.examples = examples or []

    def to_markdown(self) -> str:
        """Convert rule to markdown format."""
        md = f"### {self.title}\n\n"
        md += f"**Tier:** `{self.tier.value}`\n\n"
        md += f"{self.description}\n\n"

        if self.rationale:
            md += f"**Rationale:** {self.rationale}\n\n"

        if self.examples:
            md += "**Examples:**\n"
            for example in self.examples:
                md += f"- {example}\n"
            md += "\n"

        return md


class Constitution:
    """Manages tiered constitution rules."""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()
        self.rules: Dict[ConstitutionTier, List[ConstitutionRule]] = {
            ConstitutionTier.CORE: [],
            ConstitutionTier.HIGH_PRIORITY: [],
            ConstitutionTier.FLEXIBLE: [],
        }

    def add_rule(self, rule: ConstitutionRule) -> None:
        """Add a rule to the constitution."""
        self.rules[rule.tier].append(rule)

    def get_rules_by_tier(self, tier: ConstitutionTier) -> List[ConstitutionRule]:
        """Get all rules for a specific tier."""
        return self.rules.get(tier, [])

    def get_all_rules(self) -> List[ConstitutionRule]:
        """Get all rules across all tiers."""
        all_rules = []
        for tier in ConstitutionTier:
            all_rules.extend(self.rules[tier])
        return all_rules

    def load_from_markdown(self, file_path: Path) -> None:
        """Load constitution from a markdown file.

        Expected format:
        ### Rule Title
        **Tier:** `core|high-priority|flexible`
        Rule description...
        **Rationale:** ...
        **Examples:**
        - Example 1
        - Example 2
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Constitution file not found: {file_path}")

        content = file_path.read_text()
        sections = re.split(r'\n### ', content)

        for section in sections[1:]:  # Skip first split (before first ###)
            lines = section.split('\n')
            title = lines[0].strip()

            # Extract tier
            tier_match = re.search(r'\*\*Tier:\*\*\s+`(core|high-priority|flexible)`', section)
            if not tier_match:
                continue

            tier = ConstitutionTier(tier_match.group(1))

            # Extract description (text before Rationale or Examples)
            desc_parts = []
            rationale = None
            examples = []

            in_rationale = False
            in_examples = False

            for line in lines[1:]:
                if line.startswith('**Tier:**'):
                    continue
                elif line.startswith('**Rationale:**'):
                    in_rationale = True
                    in_examples = False
                    rationale = line.replace('**Rationale:**', '').strip()
                elif line.startswith('**Examples:**'):
                    in_rationale = False
                    in_examples = True
                elif in_examples and line.strip().startswith('- '):
                    examples.append(line.strip()[2:])
                elif in_rationale:
                    rationale += " " + line.strip()
                elif not in_rationale and not in_examples and line.strip():
                    desc_parts.append(line.strip())

            description = ' '.join(desc_parts)

            if title and description:
                rule = ConstitutionRule(
                    title=title,
                    description=description,
                    tier=tier,
                    rationale=rationale,
                    examples=examples
                )
                self.add_rule(rule)

    def save_to_markdown(self, file_path: Path) -> None:
        """Save constitution to a markdown file."""
        content = "# Project Constitution\n\n"
        content += "This document defines the governing principles for this project, organized by priority tiers.\n\n"

        for tier in ConstitutionTier:
            tier_rules = self.get_rules_by_tier(tier)
            if tier_rules:
                content += f"## {tier.value.replace('-', ' ').title()} Rules\n\n"
                content += self._get_tier_description(tier) + "\n\n"

                for rule in tier_rules:
                    content += rule.to_markdown()

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)

    def _get_tier_description(self, tier: ConstitutionTier) -> str:
        """Get description for each tier."""
        descriptions = {
            ConstitutionTier.CORE: (
                "**CORE** rules are non-negotiable and must be followed in all circumstances. "
                "Violations of core rules should block implementation."
            ),
            ConstitutionTier.HIGH_PRIORITY: (
                "**HIGH-PRIORITY** rules should be followed unless there is a strong, documented "
                "reason to deviate. Deviations require explicit acknowledgment and justification."
            ),
            ConstitutionTier.FLEXIBLE: (
                "**FLEXIBLE** rules are guidelines that can be adapted based on context. "
                "They represent best practices but allow for pragmatic exceptions."
            ),
        }
        return descriptions.get(tier, "")

    def validate_against_plan(self, plan_content: str) -> List[str]:
        """Validate a plan against constitution rules.

        Returns:
            List of validation issues found
        """
        issues = []

        # Check core rules (strict validation)
        for rule in self.get_rules_by_tier(ConstitutionTier.CORE):
            # Simple keyword-based validation (can be enhanced)
            keywords = self._extract_keywords(rule.description)
            for keyword in keywords:
                if keyword.lower() not in plan_content.lower():
                    issues.append(
                        f"CORE rule '{rule.title}' may not be addressed (keyword '{keyword}' not found)"
                    )

        return issues

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract key validation terms from rule descriptions."""
        # Simple extraction - can be enhanced with NLP
        important_words = []
        words = text.split()
        for word in words:
            clean_word = word.strip('.,;:')
            # Extract capitalized words that are 4+ characters or ALL_CAPS
            if len(clean_word) >= 4 and (word.isupper() or (clean_word and clean_word[0].isupper())):
                important_words.append(clean_word)
        return important_words[:5]  # Top 5 keywords

    def merge_constitution(self, other: 'Constitution', conflict_strategy: str = 'keep_existing') -> None:
        """Merge another constitution into this one.

        Args:
            other: Another Constitution instance to merge
            conflict_strategy: How to handle conflicts ('keep_existing', 'prefer_new', 'keep_both')
        """
        for tier in ConstitutionTier:
            other_rules = other.get_rules_by_tier(tier)
            for other_rule in other_rules:
                # Check for existing rule with same title
                existing = next(
                    (r for r in self.rules[tier] if r.title == other_rule.title),
                    None
                )

                if existing is None:
                    self.add_rule(other_rule)
                elif conflict_strategy == 'prefer_new':
                    self.rules[tier].remove(existing)
                    self.add_rule(other_rule)
                elif conflict_strategy == 'keep_both':
                    # Rename the new rule to avoid conflicts
                    other_rule.title = f"{other_rule.title} (merged)"
                    self.add_rule(other_rule)
                # else: keep_existing - do nothing

    def generate_summary(self) -> str:
        """Generate a summary of the constitution."""
        summary = "# Constitution Summary\n\n"

        tier_names = {
            ConstitutionTier.CORE: "CORE",
            ConstitutionTier.HIGH_PRIORITY: "HIGH-PRIORITY",
            ConstitutionTier.FLEXIBLE: "FLEXIBLE"
        }

        for tier in ConstitutionTier:
            tier_rules = self.get_rules_by_tier(tier)
            count = len(tier_rules)
            tier_name = tier_names[tier]
            summary += f"- **{tier_name}**: {count} rule(s)\n"

        summary += f"\n**Total Rules:** {len(self.get_all_rules())}\n"

        return summary

    @staticmethod
    def load_preset(preset: ConstitutionPreset, templates_dir: Optional[Path] = None) -> 'Constitution':
        """Load a constitution from a preset.

        Args:
            preset: The preset to load
            templates_dir: Directory containing templates (defaults to package templates)

        Returns:
            Constitution instance loaded from preset

        Raises:
            FileNotFoundError: If preset file doesn't exist
        """
        if templates_dir is None:
            # Try to find templates in package
            try:
                # When installed as package
                import specify_cli
                package_root = Path(specify_cli.__file__).parent.parent
                templates_dir = package_root / "templates"
            except (ImportError, AttributeError):
                # Fallback to relative path (development)
                templates_dir = Path(__file__).parent.parent.parent / "templates"

        preset_file = templates_dir / "risotech" / "constitution-presets" / f"{preset.value}.md"

        if not preset_file.exists():
            raise FileNotFoundError(f"Preset file not found: {preset_file}")

        constitution = Constitution()
        constitution.load_from_markdown(preset_file)

        return constitution

    @staticmethod
    def list_available_presets() -> List[str]:
        """List all available constitution presets.

        Returns:
            List of preset names
        """
        return [preset.value for preset in ConstitutionPreset]

    @staticmethod
    def get_preset_description(preset: ConstitutionPreset) -> str:
        """Get description for a preset.

        Args:
            preset: The preset to describe

        Returns:
            Human-readable description
        """
        descriptions = {
            ConstitutionPreset.REACT_TYPESCRIPT: (
                "React + TypeScript: Modern frontend development with type safety, "
                "component testing, and React best practices"
            ),
            ConstitutionPreset.NEXTJS_TAILWIND: (
                "Next.js + Tailwind CSS: Full-stack React framework with utility-first CSS, "
                "server components, and SEO optimization"
            ),
            ConstitutionPreset.DJANGO_POSTGRESQL: (
                "Django + PostgreSQL: Python backend with ORM, REST APIs, "
                "database migrations, and security best practices"
            ),
        }
        return descriptions.get(preset, "No description available")
