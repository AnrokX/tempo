"""
Unit tests for the ActivityTracker core component.
Following TDD: Red-Green-Refactor cycle.
"""
import pytest
from unittest.mock import Mock, patch


class TestActivityTracker:
    """Test suite for ActivityTracker class."""
    
    def test_tracker_can_be_instantiated(self):
        """Test that ActivityTracker can be created."""
        from src.core.tracker import ActivityTracker
        
        tracker = ActivityTracker()
        
        assert tracker is not None
        assert isinstance(tracker, ActivityTracker)
    
    def test_tracker_gets_active_application(self):
        """Test that tracker can get the currently active application."""
        from src.core.tracker import ActivityTracker
        
        tracker = ActivityTracker()
        app_name = tracker.get_active_application()
        
        # Should return a string (application name) or None
        assert app_name is None or isinstance(app_name, str)