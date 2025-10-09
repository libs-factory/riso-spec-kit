"""Configuration for Specify CLI features and RisoTech enhancements."""

import os
from typing import Dict, Any


class SpecifyConfig:
    """Configuration for Specify CLI features with support for RisoTech mode."""

    # Feature flags (environment variables or config file)
    ENABLE_TIERED_CONSTITUTION = os.getenv("SPECIFY_TIERED_CONSTITUTION", "false").lower() == "true"
    ENABLE_EPIC_DECOMPOSITION = os.getenv("SPECIFY_EPIC_DECOMPOSITION", "false").lower() == "true"
    ENABLE_CLARIFICATION_GATE = os.getenv("SPECIFY_CLARIFICATION_GATE", "false").lower() == "true"
    ENABLE_VALIDATION_SUBTASKS = os.getenv("SPECIFY_VALIDATION_SUBTASKS", "false").lower() == "true"
    ENABLE_MULTISTORY_BACKLOG = os.getenv("SPECIFY_MULTISTORY_BACKLOG", "false").lower() == "true"

    # RisoTech mode (enables all enhancements)
    RISOTECH_MODE = os.getenv("SPECIFY_RISOTECH_MODE", "false").lower() == "true"

    # Workflow settings
    ENABLE_STORY_TRACKING = os.getenv("SPECIFY_STORY_TRACKING", "false").lower() == "true"
    ENABLE_PROGRESS_REPORTING = os.getenv("SPECIFY_PROGRESS_REPORTING", "false").lower() == "true"
    AUTO_UPDATE_BACKLOG = os.getenv("SPECIFY_AUTO_UPDATE_BACKLOG", "true").lower() == "true"

    # Progress tracking settings
    TRACK_ACTUAL_HOURS = os.getenv("SPECIFY_TRACK_ACTUAL_HOURS", "false").lower() == "true"
    CALCULATE_VELOCITY = os.getenv("SPECIFY_CALCULATE_VELOCITY", "false").lower() == "true"

    # Story workflow settings
    REQUIRE_READY_STATUS = os.getenv("SPECIFY_REQUIRE_READY_STATUS", "true").lower() == "true"
    AUTO_UNBLOCK_STORIES = os.getenv("SPECIFY_AUTO_UNBLOCK_STORIES", "true").lower() == "true"
    BLOCK_ON_INCOMPLETE_DEPS = os.getenv("SPECIFY_BLOCK_ON_INCOMPLETE_DEPS", "true").lower() == "true"

    @classmethod
    def is_feature_enabled(cls, feature_name: str) -> bool:
        """Check if a specific feature is enabled.

        Args:
            feature_name: Name of the feature to check (e.g., 'tiered_constitution')

        Returns:
            True if the feature is enabled, False otherwise
        """
        # Re-read RISOTECH_MODE from environment in case it was changed
        risotech_mode = os.getenv("SPECIFY_RISOTECH_MODE", "false").lower() == "true"
        if risotech_mode:
            return True

        feature_map = {
            'tiered_constitution': cls.ENABLE_TIERED_CONSTITUTION,
            'epic_decomposition': cls.ENABLE_EPIC_DECOMPOSITION,
            'clarification_gate': cls.ENABLE_CLARIFICATION_GATE,
            'validation_subtasks': cls.ENABLE_VALIDATION_SUBTASKS,
            'multistory_backlog': cls.ENABLE_MULTISTORY_BACKLOG,
            'story_tracking': cls.ENABLE_STORY_TRACKING,
            'progress_reporting': cls.ENABLE_PROGRESS_REPORTING,
        }

        return feature_map.get(feature_name, False)

    @classmethod
    def get_workflow_config(cls) -> Dict[str, bool]:
        """Get workflow-specific configuration.

        Returns:
            Dictionary of workflow settings
        """
        return {
            'auto_update_backlog': cls.AUTO_UPDATE_BACKLOG,
            'track_actual_hours': cls.TRACK_ACTUAL_HOURS,
            'calculate_velocity': cls.CALCULATE_VELOCITY,
            'require_ready_status': cls.REQUIRE_READY_STATUS,
            'auto_unblock_stories': cls.AUTO_UNBLOCK_STORIES,
            'block_on_incomplete_deps': cls.BLOCK_ON_INCOMPLETE_DEPS,
        }

    @classmethod
    def get_all_features(cls) -> Dict[str, bool]:
        """Get the status of all features.

        Returns:
            Dictionary mapping feature names to their enabled status
        """
        return {
            'risotech_mode': cls.RISOTECH_MODE,
            'tiered_constitution': cls.is_feature_enabled('tiered_constitution'),
            'epic_decomposition': cls.is_feature_enabled('epic_decomposition'),
            'clarification_gate': cls.is_feature_enabled('clarification_gate'),
            'validation_subtasks': cls.is_feature_enabled('validation_subtasks'),
            'multistory_backlog': cls.is_feature_enabled('multistory_backlog'),
            'story_tracking': cls.is_feature_enabled('story_tracking'),
            'progress_reporting': cls.is_feature_enabled('progress_reporting'),
        }

    @classmethod
    def enable_risotech_mode(cls) -> None:
        """Enable RisoTech mode, which activates all enhancements."""
        os.environ["SPECIFY_RISOTECH_MODE"] = "true"
        cls.RISOTECH_MODE = True

    @classmethod
    def disable_risotech_mode(cls) -> None:
        """Disable RisoTech mode."""
        os.environ["SPECIFY_RISOTECH_MODE"] = "false"
        cls.RISOTECH_MODE = False
