"""
Unit tests for Session tracking.
Following TDD: Red-Green-Refactor cycle.
"""
import pytest
from datetime import datetime
import time


class TestSession:
    """Test suite for Session class."""
    
    def test_session_can_be_created(self):
        """Test that a Session can be instantiated."""
        from src.core.session import Session
        
        session = Session(app_name="firefox", start_time=time.time())
        
        assert session is not None
        assert session.app_name == "firefox"
        assert session.start_time > 0
    
    def test_session_calculates_duration(self):
        """Test that session duration is calculated correctly."""
        from src.core.session import Session
        
        start = time.time()
        end = start + 300  # 5 minutes later
        
        session = Session(app_name="vscode", start_time=start)
        session.end_time = end
        
        assert session.duration == 300
    
    def test_session_without_end_time_has_no_duration(self):
        """Test that ongoing sessions return None for duration."""
        from src.core.session import Session
        
        session = Session(app_name="terminal", start_time=time.time())
        
        assert session.end_time is None
        assert session.duration is None
    
    def test_session_to_dict_serialization(self):
        """Test that session can be serialized to dictionary."""
        from src.core.session import Session
        
        start = time.time()
        session = Session(app_name="chrome", start_time=start)
        
        data = session.to_dict()
        
        assert isinstance(data, dict)
        assert data['app_name'] == "chrome"
        assert data['start_time'] == start
        assert 'end_time' in data
        assert 'duration' in data


class TestSessionManager:
    """Test suite for SessionManager class."""
    
    def test_session_manager_tracks_current_session(self):
        """Test that SessionManager maintains current session."""
        from src.core.session import SessionManager
        
        manager = SessionManager()
        
        # Initially no session
        assert manager.current_session is None
        
        # Start a session
        manager.start_session("firefox")
        
        assert manager.current_session is not None
        assert manager.current_session.app_name == "firefox"
    
    def test_session_manager_switches_applications(self):
        """Test that SessionManager handles app switches correctly."""
        from src.core.session import SessionManager
        
        manager = SessionManager()
        
        # Start with firefox
        manager.start_session("firefox")
        first_session = manager.current_session
        
        # Switch to vscode
        manager.switch_application("vscode")
        
        # First session should be ended
        assert first_session.end_time is not None
        
        # New session should be current
        assert manager.current_session.app_name == "vscode"
        assert manager.current_session != first_session
    
    def test_session_manager_handles_same_app(self):
        """Test that staying in same app doesn't create new session."""
        from src.core.session import SessionManager
        
        manager = SessionManager()
        
        manager.start_session("terminal")
        first_session = manager.current_session
        
        # Same app - should not create new session
        manager.switch_application("terminal")
        
        assert manager.current_session == first_session
        assert first_session.end_time is None  # Still ongoing