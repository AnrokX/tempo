"""
Unit tests for Database layer.
Following TDD: Red-Green-Refactor cycle.
"""
import pytest
import sqlite3
from pathlib import Path
import tempfile
import time


class TestDatabase:
    """Test suite for Database class."""
    
    def test_database_can_be_initialized(self, temp_database):
        """Test that Database can be created with a path."""
        from src.core.database import Database
        
        db = Database(temp_database)
        
        assert db is not None
        assert db.db_path == temp_database
    
    def test_database_creates_schema_on_init(self, temp_database):
        """Test that database schema is created on initialization."""
        from src.core.database import Database
        
        db = Database(temp_database)
        db.initialize()
        
        # Check tables exist
        conn = sqlite3.connect(temp_database)
        cursor = conn.cursor()
        
        # Check applications table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='applications'")
        assert cursor.fetchone() is not None
        
        # Check sessions table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sessions'")
        assert cursor.fetchone() is not None
        
        conn.close()
    
    def test_database_saves_application(self, temp_database):
        """Test saving application to database."""
        from src.core.database import Database
        
        db = Database(temp_database)
        db.initialize()
        
        app_id = db.save_application("firefox", "neutral")
        
        assert app_id is not None
        assert app_id > 0
    
    def test_database_prevents_duplicate_applications(self, temp_database):
        """Test that duplicate applications are not created."""
        from src.core.database import Database
        
        db = Database(temp_database)
        db.initialize()
        
        app_id1 = db.save_application("vscode", "productive")
        app_id2 = db.save_application("vscode", "productive")
        
        assert app_id1 == app_id2  # Should return same ID
    
    def test_database_saves_session(self, temp_database):
        """Test saving session to database."""
        from src.core.database import Database
        
        db = Database(temp_database)
        db.initialize()
        
        # First save the application
        app_id = db.save_application("terminal", "productive")
        
        # Then save a session
        start_time = time.time()
        end_time = start_time + 300
        
        session_id = db.save_session(app_id, start_time, end_time)
        
        assert session_id is not None
        assert session_id > 0
    
    def test_database_retrieves_sessions_by_date(self, temp_database):
        """Test retrieving sessions for a specific date range."""
        from src.core.database import Database
        
        db = Database(temp_database)
        db.initialize()
        
        # Save test data
        app_id = db.save_application("chrome", "neutral")
        
        now = time.time()
        session1_id = db.save_session(app_id, now - 3600, now - 3000)
        session2_id = db.save_session(app_id, now - 2000, now - 1000)
        
        # Retrieve sessions
        sessions = db.get_sessions_by_date(now - 4000, now)
        
        assert len(sessions) == 2
        assert all('app_name' in s for s in sessions)
        assert all('start_time' in s for s in sessions)
    
    def test_database_calculates_daily_stats(self, temp_database):
        """Test calculation of daily statistics."""
        from src.core.database import Database
        
        db = Database(temp_database)
        db.initialize()
        
        # Save test data
        productive_id = db.save_application("vscode", "productive")
        neutral_id = db.save_application("firefox", "neutral")
        
        now = time.time()
        db.save_session(productive_id, now - 3600, now - 1800)  # 30 min productive
        db.save_session(neutral_id, now - 1800, now - 900)      # 15 min neutral
        
        # Get daily stats
        stats = db.get_daily_stats(now - 7200, now)
        
        assert stats is not None
        assert stats['total_time'] == 2700  # 45 minutes
        assert stats['productive_time'] == 1800  # 30 minutes
        assert stats['neutral_time'] == 900  # 15 minutes