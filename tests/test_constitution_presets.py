"""Tests for constitution presets."""

import pytest
from pathlib import Path
from src.specify_cli.constitution import (
    Constitution,
    ConstitutionPreset,
    ConstitutionTier
)


class TestConstitutionPresets:
    """Test suite for constitution presets."""

    def test_list_available_presets(self):
        """Test listing available presets."""
        presets = Constitution.list_available_presets()

        assert len(presets) >= 3
        assert "react-typescript" in presets
        assert "nextjs-tailwind" in presets
        assert "django-postgresql" in presets

    def test_get_preset_description(self):
        """Test getting preset descriptions."""
        desc = Constitution.get_preset_description(ConstitutionPreset.REACT_TYPESCRIPT)

        assert "React" in desc
        assert "TypeScript" in desc
        assert len(desc) > 20

    def test_load_react_typescript_preset(self):
        """Test loading React + TypeScript preset."""
        # Get templates directory
        templates_dir = Path(__file__).parent.parent / "templates"

        constitution = Constitution.load_preset(
            ConstitutionPreset.REACT_TYPESCRIPT,
            templates_dir=templates_dir
        )

        # Verify loaded rules
        all_rules = constitution.get_all_rules()
        assert len(all_rules) > 0

        # Check for specific rules
        core_rules = constitution.get_rules_by_tier(ConstitutionTier.CORE)
        assert len(core_rules) > 0

        # Verify some expected rules
        rule_titles = [rule.title for rule in all_rules]
        assert any("Type Safety" in title for title in rule_titles)
        assert any("Component Testing" in title for title in rule_titles)

    def test_load_nextjs_tailwind_preset(self):
        """Test loading Next.js + Tailwind preset."""
        templates_dir = Path(__file__).parent.parent / "templates"

        constitution = Constitution.load_preset(
            ConstitutionPreset.NEXTJS_TAILWIND,
            templates_dir=templates_dir
        )

        all_rules = constitution.get_all_rules()
        assert len(all_rules) > 0

        # Check for Next.js specific rules
        rule_titles = [rule.title for rule in all_rules]
        assert any("App Router" in title or "Server Component" in title for title in rule_titles)

    def test_load_django_postgresql_preset(self):
        """Test loading Django + PostgreSQL preset."""
        templates_dir = Path(__file__).parent.parent / "templates"

        constitution = Constitution.load_preset(
            ConstitutionPreset.DJANGO_POSTGRESQL,
            templates_dir=templates_dir
        )

        all_rules = constitution.get_all_rules()
        assert len(all_rules) > 0

        # Check for Django specific rules
        rule_titles = [rule.title for rule in all_rules]
        assert any("Migration" in title or "ORM" in title or "SQL" in title for title in rule_titles)

    def test_preset_has_all_tiers(self):
        """Test that presets contain rules from all tiers."""
        templates_dir = Path(__file__).parent.parent / "templates"

        for preset in ConstitutionPreset:
            constitution = Constitution.load_preset(preset, templates_dir=templates_dir)

            # Each preset should have rules in all three tiers
            core_rules = constitution.get_rules_by_tier(ConstitutionTier.CORE)
            high_priority_rules = constitution.get_rules_by_tier(ConstitutionTier.HIGH_PRIORITY)
            flexible_rules = constitution.get_rules_by_tier(ConstitutionTier.FLEXIBLE)

            assert len(core_rules) > 0, f"{preset.value} missing CORE rules"
            assert len(high_priority_rules) > 0, f"{preset.value} missing HIGH-PRIORITY rules"
            assert len(flexible_rules) > 0, f"{preset.value} missing FLEXIBLE rules"

    def test_preset_rules_have_rationale(self):
        """Test that preset rules include rationales."""
        templates_dir = Path(__file__).parent.parent / "templates"

        constitution = Constitution.load_preset(
            ConstitutionPreset.REACT_TYPESCRIPT,
            templates_dir=templates_dir
        )

        # Most rules should have rationales
        rules_with_rationale = [r for r in constitution.get_all_rules() if r.rationale]
        assert len(rules_with_rationale) > len(constitution.get_all_rules()) * 0.8

    def test_preset_rules_have_examples(self):
        """Test that preset rules include examples."""
        templates_dir = Path(__file__).parent.parent / "templates"

        constitution = Constitution.load_preset(
            ConstitutionPreset.NEXTJS_TAILWIND,
            templates_dir=templates_dir
        )

        # Most rules should have examples
        rules_with_examples = [r for r in constitution.get_all_rules() if r.examples]
        assert len(rules_with_examples) > len(constitution.get_all_rules()) * 0.8

    def test_load_preset_nonexistent_fails(self, tmp_path):
        """Test that loading from empty directory fails appropriately."""
        with pytest.raises(FileNotFoundError):
            Constitution.load_preset(
                ConstitutionPreset.REACT_TYPESCRIPT,
                templates_dir=tmp_path
            )

    def test_preset_can_be_saved_and_reloaded(self, tmp_path):
        """Test that loaded preset can be saved and reloaded."""
        templates_dir = Path(__file__).parent.parent / "templates"

        # Load preset
        original = Constitution.load_preset(
            ConstitutionPreset.DJANGO_POSTGRESQL,
            templates_dir=templates_dir
        )

        # Save to temp file
        save_path = tmp_path / "constitution.md"
        original.save_to_markdown(save_path)

        # Reload
        reloaded = Constitution()
        reloaded.load_from_markdown(save_path)

        # Compare
        assert len(original.get_all_rules()) == len(reloaded.get_all_rules())

    def test_merge_presets(self):
        """Test merging multiple presets."""
        templates_dir = Path(__file__).parent.parent / "templates"

        # Load two presets
        react_const = Constitution.load_preset(
            ConstitutionPreset.REACT_TYPESCRIPT,
            templates_dir=templates_dir
        )

        django_const = Constitution.load_preset(
            ConstitutionPreset.DJANGO_POSTGRESQL,
            templates_dir=templates_dir
        )

        # Merge
        original_count = len(react_const.get_all_rules())
        react_const.merge_constitution(django_const, conflict_strategy='keep_both')

        # Should have more rules after merge
        assert len(react_const.get_all_rules()) > original_count

    def test_preset_summary_generation(self):
        """Test generating summary for preset."""
        templates_dir = Path(__file__).parent.parent / "templates"

        constitution = Constitution.load_preset(
            ConstitutionPreset.REACT_TYPESCRIPT,
            templates_dir=templates_dir
        )

        summary = constitution.generate_summary()

        assert "Constitution Summary" in summary
        assert "CORE" in summary.upper()
        assert "HIGH-PRIORITY" in summary.upper()
        assert "FLEXIBLE" in summary.upper()
        assert "Total Rules" in summary
