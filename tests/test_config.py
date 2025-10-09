"""Tests for specify_cli.config module."""

import os
import pytest
from src.specify_cli.config import SpecifyConfig


class TestSpecifyConfig:
    """Test suite for SpecifyConfig."""

    def test_default_feature_flags_disabled(self):
        """Test that all feature flags are disabled by default."""
        # Clear environment variables
        for key in [
            "SPECIFY_TIERED_CONSTITUTION",
            "SPECIFY_EPIC_DECOMPOSITION",
            "SPECIFY_CLARIFICATION_GATE",
            "SPECIFY_VALIDATION_SUBTASKS",
            "SPECIFY_MULTISTORY_BACKLOG",
            "SPECIFY_RISOTECH_MODE",
        ]:
            os.environ.pop(key, None)

        # Reload config
        from src.specify_cli import config
        import importlib
        importlib.reload(config)

        assert not config.SpecifyConfig.RISOTECH_MODE
        assert not config.SpecifyConfig.ENABLE_TIERED_CONSTITUTION
        assert not config.SpecifyConfig.ENABLE_EPIC_DECOMPOSITION

    def test_risotech_mode_enables_all_features(self, monkeypatch):
        """Test that RisoTech mode enables all features."""
        monkeypatch.setenv("SPECIFY_RISOTECH_MODE", "true")

        assert SpecifyConfig.is_feature_enabled('tiered_constitution')
        assert SpecifyConfig.is_feature_enabled('epic_decomposition')
        assert SpecifyConfig.is_feature_enabled('clarification_gate')
        assert SpecifyConfig.is_feature_enabled('validation_subtasks')
        assert SpecifyConfig.is_feature_enabled('multistory_backlog')

    def test_individual_feature_flags(self, monkeypatch):
        """Test that individual features can be enabled."""
        monkeypatch.setenv("SPECIFY_RISOTECH_MODE", "false")
        monkeypatch.setenv("SPECIFY_TIERED_CONSTITUTION", "true")

        # Need to reload to pick up environment changes
        from src.specify_cli import config
        import importlib
        importlib.reload(config)

        assert config.SpecifyConfig.is_feature_enabled('tiered_constitution')
        assert not config.SpecifyConfig.is_feature_enabled('epic_decomposition')

    def test_get_all_features(self):
        """Test getting status of all features."""
        features = SpecifyConfig.get_all_features()

        assert isinstance(features, dict)
        assert 'risotech_mode' in features
        assert 'tiered_constitution' in features
        assert 'epic_decomposition' in features
        assert 'clarification_gate' in features
        assert 'validation_subtasks' in features
        assert 'multistory_backlog' in features

    def test_enable_risotech_mode(self):
        """Test enabling RisoTech mode programmatically."""
        SpecifyConfig.enable_risotech_mode()

        assert SpecifyConfig.RISOTECH_MODE
        assert os.environ.get("SPECIFY_RISOTECH_MODE") == "true"

    def test_disable_risotech_mode(self):
        """Test disabling RisoTech mode programmatically."""
        SpecifyConfig.enable_risotech_mode()
        SpecifyConfig.disable_risotech_mode()

        assert not SpecifyConfig.RISOTECH_MODE
        assert os.environ.get("SPECIFY_RISOTECH_MODE") == "false"

    def test_is_feature_enabled_unknown_feature(self):
        """Test that unknown feature returns False."""
        assert not SpecifyConfig.is_feature_enabled('unknown_feature')
