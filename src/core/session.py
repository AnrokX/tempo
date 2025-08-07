"""
Session tracking for Tempo.
Manages application usage sessions.
"""
import time


class Session:
    """Represents a single application usage session."""
    
    def __init__(self, app_name, start_time):
        """Initialize a new session."""
        self.app_name = app_name
        self.start_time = start_time
        self.end_time = None
    
    @property
    def duration(self):
        """Calculate session duration in seconds."""
        if self.end_time is None:
            return None
        return self.end_time - self.start_time
    
    def to_dict(self):
        """Convert session to dictionary for serialization."""
        return {
            'app_name': self.app_name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration
        }


class SessionManager:
    """Manages tracking of application sessions."""
    
    def __init__(self):
        """Initialize the session manager."""
        self.current_session = None
        self.sessions = []
    
    def start_session(self, app_name):
        """Start a new session for an application."""
        if self.current_session:
            self.end_current_session()
        
        self.current_session = Session(app_name, time.time())
        self.sessions.append(self.current_session)
    
    def switch_application(self, app_name):
        """Handle switching to a different application."""
        if self.current_session and self.current_session.app_name == app_name:
            # Same app, continue current session
            return
        
        # Different app, start new session
        self.start_session(app_name)
    
    def end_current_session(self):
        """End the current session."""
        if self.current_session and self.current_session.end_time is None:
            self.current_session.end_time = time.time()