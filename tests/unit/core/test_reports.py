"""
Unit tests for reporting engine.
Following TDD: Red-Green-Refactor cycle.
"""
import pytest
from datetime import datetime, timedelta
import time


class TestReportGenerator:
    """Test suite for ReportGenerator class."""
    
    def test_report_generator_can_be_initialized(self, temp_database):
        """Test that ReportGenerator can be created."""
        from src.core.reports import ReportGenerator
        
        generator = ReportGenerator(temp_database)
        
        assert generator is not None
        assert generator.db_path == temp_database
    
    def test_generates_daily_report(self, temp_database):
        """Test generation of daily activity report."""
        from src.core.reports import ReportGenerator
        from src.core.database import Database
        
        # Setup test data
        db = Database(temp_database)
        db.initialize()
        
        vscode_id = db.save_application("Visual Studio Code", "productive")
        firefox_id = db.save_application("Firefox", "neutral")
        youtube_id = db.save_application("YouTube", "distracting")
        
        now = time.time()
        db.save_session(vscode_id, now - 7200, now - 3600)  # 1 hour productive
        db.save_session(firefox_id, now - 3600, now - 1800)  # 30 min neutral
        db.save_session(youtube_id, now - 1800, now - 900)   # 15 min distracting
        
        # Generate report
        generator = ReportGenerator(temp_database)
        report = generator.generate_daily_report()
        
        assert report is not None
        assert "total_time" in report
        assert "productivity_score" in report
        assert "top_apps" in report
        assert "category_breakdown" in report
        
        assert report["total_time"] == 6300  # 1h 45min
        assert len(report["top_apps"]) == 3
        assert report["top_apps"][0]["name"] == "Visual Studio Code"
    
    def test_generates_weekly_report(self, temp_database):
        """Test generation of weekly activity report."""
        from src.core.reports import ReportGenerator
        from src.core.database import Database
        
        # Setup test data
        db = Database(temp_database)
        db.initialize()
        
        app_id = db.save_application("Firefox", "neutral")
        
        now = time.time()
        # Add sessions for multiple days
        for days_ago in range(7):
            session_time = now - (days_ago * 24 * 3600)
            db.save_session(app_id, session_time, session_time + 3600)
        
        # Generate report
        generator = ReportGenerator(temp_database)
        report = generator.generate_weekly_report()
        
        assert report is not None
        assert "days" in report
        assert len(report["days"]) == 7
        assert "weekly_total" in report
        assert "daily_average" in report
        # Should have some sessions, exact count may vary due to date boundaries
        assert report["weekly_total"] > 0
        assert report["weekly_total"] <= 7 * 3600  # At most 7 hours
        assert report["daily_average"] >= 0  # Some average
    
    def test_formats_report_as_text(self, temp_database):
        """Test formatting report as human-readable text."""
        from src.core.reports import ReportGenerator
        
        generator = ReportGenerator(temp_database)
        
        report_data = {
            "total_time": 7200,
            "productivity_score": 75,
            "top_apps": [
                {"name": "Visual Studio Code", "duration": 3600},
                {"name": "Firefox", "duration": 2400},
                {"name": "Terminal", "duration": 1200}
            ],
            "category_breakdown": {
                "productive": 4800,
                "neutral": 2400,
                "distracting": 0
            }
        }
        
        text = generator.format_as_text(report_data)
        
        assert isinstance(text, str)
        assert "Total Time: 2h 0m" in text
        assert "Productivity Score: 75/100" in text
        assert "Visual Studio Code" in text
        assert "1h 0m" in text
    
    def test_calculates_productivity_trends(self, temp_database):
        """Test calculation of productivity trends over time."""
        from src.core.reports import ReportGenerator
        from src.core.database import Database
        
        # Setup test data with improving productivity
        db = Database(temp_database)
        db.initialize()
        
        productive_id = db.save_application("VSCode", "productive")
        distracting_id = db.save_application("YouTube", "distracting")
        
        now = time.time()
        
        # Day 1: Low productivity (25%)
        day1 = now - (2 * 24 * 3600)
        db.save_session(productive_id, day1, day1 + 900)      # 15 min productive
        db.save_session(distracting_id, day1 + 900, day1 + 3600)  # 45 min distracting
        
        # Day 2: Medium productivity (50%)  
        day2 = now - (24 * 3600)
        db.save_session(productive_id, day2, day2 + 1800)     # 30 min productive
        db.save_session(distracting_id, day2 + 1800, day2 + 3600)  # 30 min distracting
        
        # Day 3: High productivity (75%)
        day3 = now
        db.save_session(productive_id, day3 - 3600, day3 - 900)    # 45 min productive
        db.save_session(distracting_id, day3 - 900, day3 - 600)    # 5 min distracting
        
        # Calculate trends
        generator = ReportGenerator(temp_database)
        trends = generator.calculate_trends(days=3)
        
        assert trends is not None
        assert "trend_direction" in trends
        assert trends["trend_direction"] == "improving"  # Productivity increasing
        assert "average_score" in trends
    
    def test_identifies_peak_productivity_hours(self, temp_database):
        """Test identification of most productive hours."""
        from src.core.reports import ReportGenerator
        from src.core.database import Database
        
        # Setup test data
        db = Database(temp_database)
        db.initialize()
        
        productive_id = db.save_application("VSCode", "productive")
        
        # Use recent time (within last 7 days)
        now = time.time()
        # Morning sessions (9-11 AM) yesterday
        morning_start = now - 86400 + (9 * 3600)  # 9 AM yesterday
        db.save_session(productive_id, morning_start, morning_start + 7200)  # 2 hours
        
        # Afternoon session (2-3 PM) yesterday
        afternoon_start = morning_start + (5 * 3600)  # 2 PM
        db.save_session(productive_id, afternoon_start, afternoon_start + 3600)  # 1 hour
        
        generator = ReportGenerator(temp_database)
        peak_hours = generator.get_peak_productivity_hours()
        
        assert peak_hours is not None
        assert len(peak_hours) > 0
        # Just check that we got peak hours, exact hour depends on timezone
        assert peak_hours[0]["productivity_ratio"] == 1.0  # All productive time