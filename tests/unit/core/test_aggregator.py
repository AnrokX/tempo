"""
Unit tests for data aggregation.
Following TDD: Red-Green-Refactor cycle.
"""
import pytest
from datetime import datetime, timedelta
import time


class TestAggregator:
    """Test suite for DataAggregator class."""
    
    def test_aggregator_can_be_initialized(self):
        """Test that DataAggregator can be created."""
        from src.core.aggregator import DataAggregator
        
        aggregator = DataAggregator()
        
        assert aggregator is not None
    
    def test_aggregator_merges_consecutive_sessions(self):
        """Test merging consecutive sessions of same app."""
        from src.core.aggregator import DataAggregator
        
        aggregator = DataAggregator()
        
        sessions = [
            {"app_name": "firefox", "start_time": 1000, "end_time": 1100},
            {"app_name": "firefox", "start_time": 1100, "end_time": 1200},  # Consecutive
            {"app_name": "vscode", "start_time": 1200, "end_time": 1300},
            {"app_name": "firefox", "start_time": 1300, "end_time": 1400},  # Not consecutive
        ]
        
        merged = aggregator.merge_consecutive_sessions(sessions)
        
        assert len(merged) == 3  # Firefox sessions 1&2 merged
        assert merged[0]["app_name"] == "firefox"
        assert merged[0]["start_time"] == 1000
        assert merged[0]["end_time"] == 1200  # Merged end time
        assert merged[0]["duration"] == 200
    
    def test_aggregator_handles_gap_threshold(self):
        """Test that small gaps between sessions are merged."""
        from src.core.aggregator import DataAggregator
        
        aggregator = DataAggregator(gap_threshold=30)  # 30 second gap allowed
        
        sessions = [
            {"app_name": "vscode", "start_time": 1000, "end_time": 1100},
            {"app_name": "vscode", "start_time": 1120, "end_time": 1200},  # 20 sec gap
            {"app_name": "vscode", "start_time": 1250, "end_time": 1300},  # 50 sec gap
        ]
        
        merged = aggregator.merge_consecutive_sessions(sessions)
        
        assert len(merged) == 2  # First two merged (gap < 30), third separate
        assert merged[0]["end_time"] == 1200
        assert merged[1]["start_time"] == 1250
    
    def test_aggregator_creates_hourly_summary(self):
        """Test creation of hourly summaries."""
        from src.core.aggregator import DataAggregator
        
        aggregator = DataAggregator()
        
        # Sessions across 2 hours
        sessions = [
            {"app_name": "firefox", "start_time": 0, "end_time": 1800, "duration": 1800},      # 30 min in hour 0
            {"app_name": "vscode", "start_time": 1800, "end_time": 5400, "duration": 3600},    # 30 min hour 0, 60 min hour 1
            {"app_name": "discord", "start_time": 5400, "end_time": 7200, "duration": 1800},   # 30 min in hour 1
        ]
        
        hourly = aggregator.create_hourly_summary(sessions)
        
        assert len(hourly) == 2  # 2 hours
        
        # First hour (0-3600)
        assert hourly[0]["hour_start"] == 0
        assert hourly[0]["total_duration"] == 3600  # Full hour used
        assert len(hourly[0]["apps"]) == 2  # Firefox and vscode
        
        # Second hour (3600-7200)
        assert hourly[1]["hour_start"] == 3600
        assert hourly[1]["total_duration"] == 3600  # Full hour used
        assert len(hourly[1]["apps"]) == 2  # vscode and discord
    
    def test_aggregator_creates_daily_summary(self):
        """Test creation of daily summaries."""
        from src.core.aggregator import DataAggregator
        
        aggregator = DataAggregator()
        
        sessions = [
            {"app_name": "vscode", "duration": 7200, "category": "productive"},
            {"app_name": "firefox", "duration": 3600, "category": "neutral"},
            {"app_name": "youtube", "duration": 1800, "category": "distracting"},
        ]
        
        daily = aggregator.create_daily_summary(sessions)
        
        assert daily["total_time"] == 12600  # 3.5 hours
        assert daily["productive_time"] == 7200
        assert daily["neutral_time"] == 3600
        assert daily["distracting_time"] == 1800
        assert daily["num_sessions"] == 3
        assert daily["num_apps"] == 3
    
    def test_aggregator_filters_short_sessions(self):
        """Test filtering of very short sessions."""
        from src.core.aggregator import DataAggregator
        
        aggregator = DataAggregator(min_duration=60)  # Minimum 1 minute
        
        sessions = [
            {"app_name": "firefox", "duration": 120},  # Keep
            {"app_name": "vscode", "duration": 30},    # Filter out
            {"app_name": "terminal", "duration": 300}, # Keep
            {"app_name": "finder", "duration": 5},     # Filter out
        ]
        
        filtered = aggregator.filter_short_sessions(sessions)
        
        assert len(filtered) == 2
        assert all(s["duration"] >= 60 for s in filtered)
    
    def test_aggregator_compresses_old_data(self):
        """Test compression of old data by removing details."""
        from src.core.aggregator import DataAggregator
        
        aggregator = DataAggregator()
        
        # Old sessions (> 30 days)
        old_time = time.time() - (31 * 24 * 3600)
        
        sessions = [
            {"app_name": "firefox", "start_time": old_time, "end_time": old_time + 100, "duration": 100, "window_title": "Example.com"},
            {"app_name": "vscode", "start_time": old_time + 200, "end_time": old_time + 500, "duration": 300, "window_title": "main.py"},
        ]
        
        compressed = aggregator.compress_old_data(sessions, days_threshold=30)
        
        # Should keep essential data but remove details
        assert len(compressed) == 2
        assert "window_title" not in compressed[0]
        assert "window_title" not in compressed[1]
        assert compressed[0]["app_name"] == "firefox"
        assert compressed[0]["duration"] == 100