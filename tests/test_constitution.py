"""Tests for specify_cli.constitution module."""

import pytest
from pathlib import Path
from src.specify_cli.constitution import (
    Constitution,
    ConstitutionRule,
    ConstitutionTier
)


class TestConstitutionRule:
    """Test suite for ConstitutionRule."""

    def test_create_rule(self):
        """Test creating a constitution rule."""
        rule = ConstitutionRule(
            title="Test Rule",
            description="This is a test rule",
            tier=ConstitutionTier.CORE
        )

        assert rule.title == "Test Rule"
        assert rule.description == "This is a test rule"
        assert rule.tier == ConstitutionTier.CORE

    def test_rule_to_markdown(self):
        """Test converting rule to markdown."""
        rule = ConstitutionRule(
            title="Security First",
            description="All code must be secure",
            tier=ConstitutionTier.CORE,
            rationale="Security is critical",
            examples=["Use HTTPS", "Sanitize inputs"]
        )

        md = rule.to_markdown()

        assert "### Security First" in md
        assert "**Tier:** `core`" in md
        assert "All code must be secure" in md
        assert "**Rationale:** Security is critical" in md
        assert "- Use HTTPS" in md
        assert "- Sanitize inputs" in md


class TestConstitution:
    """Test suite for Constitution."""

    def test_create_constitution(self):
        """Test creating a constitution."""
        constitution = Constitution()

        assert len(constitution.rules) == 3
        assert ConstitutionTier.CORE in constitution.rules
        assert ConstitutionTier.HIGH_PRIORITY in constitution.rules
        assert ConstitutionTier.FLEXIBLE in constitution.rules

    def test_add_rule(self):
        """Test adding a rule to constitution."""
        constitution = Constitution()
        rule = ConstitutionRule(
            title="Test Rule",
            description="Test description",
            tier=ConstitutionTier.CORE
        )

        constitution.add_rule(rule)

        assert len(constitution.rules[ConstitutionTier.CORE]) == 1
        assert constitution.rules[ConstitutionTier.CORE][0] == rule

    def test_get_rules_by_tier(self):
        """Test getting rules by tier."""
        constitution = Constitution()

        core_rule = ConstitutionRule("Core", "Core rule", ConstitutionTier.CORE)
        hp_rule = ConstitutionRule("HP", "High priority", ConstitutionTier.HIGH_PRIORITY)

        constitution.add_rule(core_rule)
        constitution.add_rule(hp_rule)

        core_rules = constitution.get_rules_by_tier(ConstitutionTier.CORE)
        assert len(core_rules) == 1
        assert core_rules[0].title == "Core"

    def test_get_all_rules(self):
        """Test getting all rules."""
        constitution = Constitution()

        constitution.add_rule(ConstitutionRule("R1", "D1", ConstitutionTier.CORE))
        constitution.add_rule(ConstitutionRule("R2", "D2", ConstitutionTier.HIGH_PRIORITY))
        constitution.add_rule(ConstitutionRule("R3", "D3", ConstitutionTier.FLEXIBLE))

        all_rules = constitution.get_all_rules()
        assert len(all_rules) == 3

    def test_save_and_load_markdown(self, tmp_path):
        """Test saving and loading constitution from markdown."""
        constitution = Constitution()

        rule = ConstitutionRule(
            title="Test Rule",
            description="Test description",
            tier=ConstitutionTier.CORE,
            rationale="Test rationale",
            examples=["Example 1", "Example 2"]
        )
        constitution.add_rule(rule)

        # Save
        file_path = tmp_path / "constitution.md"
        constitution.save_to_markdown(file_path)

        assert file_path.exists()

        # Load
        new_constitution = Constitution()
        new_constitution.load_from_markdown(file_path)

        loaded_rules = new_constitution.get_rules_by_tier(ConstitutionTier.CORE)
        assert len(loaded_rules) == 1
        assert loaded_rules[0].title == "Test Rule"
        assert loaded_rules[0].description == "Test description"

    def test_validate_against_plan(self):
        """Test validating a plan against constitution."""
        constitution = Constitution()

        rule = ConstitutionRule(
            title="Testing Required",
            description="All code must have tests with Testing framework",
            tier=ConstitutionTier.CORE
        )
        constitution.add_rule(rule)

        # Plan without testing mention
        plan_without_tests = "This is a plan that doesn't mention testing"
        issues = constitution.validate_against_plan(plan_without_tests)

        assert len(issues) > 0
        assert any("Testing" in issue for issue in issues)

    def test_merge_constitution_keep_existing(self):
        """Test merging constitutions with keep_existing strategy."""
        const1 = Constitution()
        const1.add_rule(ConstitutionRule("Rule 1", "Desc 1", ConstitutionTier.CORE))

        const2 = Constitution()
        const2.add_rule(ConstitutionRule("Rule 1", "Different desc", ConstitutionTier.CORE))
        const2.add_rule(ConstitutionRule("Rule 2", "Desc 2", ConstitutionTier.CORE))

        const1.merge_constitution(const2, conflict_strategy='keep_existing')

        rules = const1.get_rules_by_tier(ConstitutionTier.CORE)
        assert len(rules) == 2
        assert rules[0].description == "Desc 1"  # Kept existing

    def test_merge_constitution_prefer_new(self):
        """Test merging constitutions with prefer_new strategy."""
        const1 = Constitution()
        const1.add_rule(ConstitutionRule("Rule 1", "Desc 1", ConstitutionTier.CORE))

        const2 = Constitution()
        const2.add_rule(ConstitutionRule("Rule 1", "Different desc", ConstitutionTier.CORE))

        const1.merge_constitution(const2, conflict_strategy='prefer_new')

        rules = const1.get_rules_by_tier(ConstitutionTier.CORE)
        assert len(rules) == 1
        assert rules[0].description == "Different desc"  # Preferred new

    def test_generate_summary(self):
        """Test generating constitution summary."""
        constitution = Constitution()
        constitution.add_rule(ConstitutionRule("R1", "D1", ConstitutionTier.CORE))
        constitution.add_rule(ConstitutionRule("R2", "D2", ConstitutionTier.CORE))
        constitution.add_rule(ConstitutionRule("R3", "D3", ConstitutionTier.HIGH_PRIORITY))

        summary = constitution.generate_summary()

        assert "Constitution Summary" in summary
        assert "2 rule(s)" in summary  # 2 core rules
        assert "Total Rules:** 3" in summary
