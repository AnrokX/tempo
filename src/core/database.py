"""
SQLite database layer for Tempo.
Handles all data persistence.
"""
import sqlite3
from pathlib import Path
import time


class Database:
    """Manages SQLite database operations for Tempo."""
    
    def __init__(self, db_path):
        """Initialize database with given path."""
        self.db_path = Path(db_path)
        self.conn = None
    
    def initialize(self):
        """Create database schema if it doesn't exist."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
        
        cursor = self.conn.cursor()
        
        # Create applications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT NOT NULL,
                created_at REAL DEFAULT (datetime('now'))
            )
        """)
        
        # Create sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_id INTEGER NOT NULL,
                start_time REAL NOT NULL,
                end_time REAL,
                duration REAL,
                created_at REAL DEFAULT (datetime('now')),
                FOREIGN KEY (app_id) REFERENCES applications (id)
            )
        """)
        
        # Create index for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sessions_time 
            ON sessions (start_time, end_time)
        """)
        
        self.conn.commit()
    
    def save_application(self, name, category):
        """Save or get application ID."""
        cursor = self.conn.cursor()
        
        # Check if application already exists
        cursor.execute("SELECT id FROM applications WHERE name = ?", (name,))
        row = cursor.fetchone()
        
        if row:
            return row[0]
        
        # Insert new application
        cursor.execute(
            "INSERT INTO applications (name, category) VALUES (?, ?)",
            (name, category)
        )
        self.conn.commit()
        
        return cursor.lastrowid
    
    def save_session(self, app_id, start_time, end_time=None):
        """Save a session to the database."""
        cursor = self.conn.cursor()
        
        duration = None
        if end_time:
            duration = end_time - start_time
        
        cursor.execute("""
            INSERT INTO sessions (app_id, start_time, end_time, duration)
            VALUES (?, ?, ?, ?)
        """, (app_id, start_time, end_time, duration))
        
        self.conn.commit()
        
        return cursor.lastrowid
    
    def get_sessions_by_date(self, start_date, end_date):
        """Get all sessions within a date range."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT 
                s.id,
                a.name as app_name,
                a.category,
                s.start_time,
                s.end_time,
                s.duration
            FROM sessions s
            JOIN applications a ON s.app_id = a.id
            WHERE s.start_time >= ? AND s.start_time <= ?
            ORDER BY s.start_time
        """, (start_date, end_date))
        
        sessions = []
        for row in cursor.fetchall():
            sessions.append({
                'id': row['id'],
                'app_name': row['app_name'],
                'category': row['category'],
                'start_time': row['start_time'],
                'end_time': row['end_time'],
                'duration': row['duration']
            })
        
        return sessions
    
    def get_daily_stats(self, start_date, end_date):
        """Calculate daily statistics for a date range."""
        cursor = self.conn.cursor()
        
        # Get total time by category
        cursor.execute("""
            SELECT 
                a.category,
                SUM(s.duration) as total_duration
            FROM sessions s
            JOIN applications a ON s.app_id = a.id
            WHERE s.start_time >= ? AND s.start_time <= ?
                AND s.duration IS NOT NULL
            GROUP BY a.category
        """, (start_date, end_date))
        
        stats = {
            'total_time': 0,
            'productive_time': 0,
            'neutral_time': 0,
            'distracting_time': 0
        }
        
        for row in cursor.fetchall():
            category = row['category']
            duration = row['total_duration'] or 0
            
            stats['total_time'] += duration
            
            if category == 'productive':
                stats['productive_time'] = duration
            elif category == 'neutral':
                stats['neutral_time'] = duration
            elif category == 'distracting':
                stats['distracting_time'] = duration
        
        return stats
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()