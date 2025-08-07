"""
Data aggregation for Tempo.
Handles data compression and summarization.
"""
import time
from typing import List, Dict, Optional
from collections import defaultdict


class DataAggregator:
    """Aggregates and compresses tracking data."""
    
    def __init__(
        self,
        gap_threshold: int = 10,
        min_duration: int = 30,
    ):
        """
        Initialize aggregator with thresholds.
        
        Args:
            gap_threshold: Maximum gap (seconds) to merge sessions
            min_duration: Minimum session duration to keep (seconds)
        """
        self.gap_threshold = gap_threshold
        self.min_duration = min_duration
    
    def merge_consecutive_sessions(self, sessions: List[Dict]) -> List[Dict]:
        """
        Merge consecutive sessions of the same application.
        
        Args:
            sessions: List of session dictionaries
            
        Returns:
            List of merged sessions
        """
        if not sessions:
            return []
        
        # Sort by start time
        sorted_sessions = sorted(sessions, key=lambda x: x.get("start_time", 0))
        
        merged = []
        current = None
        
        for session in sorted_sessions:
            if current is None:
                # Start first session
                current = session.copy()
            elif (
                session["app_name"] == current["app_name"] and
                session.get("start_time", 0) - current.get("end_time", 0) <= self.gap_threshold
            ):
                # Merge with current session
                current["end_time"] = session.get("end_time", session.get("start_time", 0))
                current["duration"] = current["end_time"] - current["start_time"]
            else:
                # Different app or gap too large, save current and start new
                if "duration" not in current and "start_time" in current and "end_time" in current:
                    current["duration"] = current["end_time"] - current["start_time"]
                merged.append(current)
                current = session.copy()
        
        # Add last session
        if current:
            if "duration" not in current and "start_time" in current and "end_time" in current:
                current["duration"] = current["end_time"] - current["start_time"]
            merged.append(current)
        
        return merged
    
    def create_hourly_summary(self, sessions: List[Dict]) -> List[Dict]:
        """
        Create hourly summaries from sessions.
        
        Args:
            sessions: List of session dictionaries
            
        Returns:
            List of hourly summaries
        """
        if not sessions:
            return []
        
        hourly_data = defaultdict(lambda: {
            "apps": {},
            "total_duration": 0,
            "hour_start": 0
        })
        
        for session in sessions:
            start_time = session.get("start_time", 0)
            end_time = session.get("end_time", start_time)
            app_name = session.get("app_name", "unknown")
            
            # Determine which hours this session spans
            start_hour = int(start_time // 3600) * 3600
            end_hour = int(end_time // 3600) * 3600
            
            if start_hour == end_hour:
                # Session within single hour
                duration = end_time - start_time
                hourly_data[start_hour]["apps"][app_name] = \
                    hourly_data[start_hour]["apps"].get(app_name, 0) + duration
                hourly_data[start_hour]["total_duration"] += duration
                hourly_data[start_hour]["hour_start"] = start_hour
            else:
                # Session spans multiple hours
                # First hour
                first_hour_duration = (start_hour + 3600) - start_time
                hourly_data[start_hour]["apps"][app_name] = \
                    hourly_data[start_hour]["apps"].get(app_name, 0) + first_hour_duration
                hourly_data[start_hour]["total_duration"] += first_hour_duration
                hourly_data[start_hour]["hour_start"] = start_hour
                
                # Middle hours (if any)
                current_hour = start_hour + 3600
                while current_hour < end_hour:
                    hourly_data[current_hour]["apps"][app_name] = \
                        hourly_data[current_hour]["apps"].get(app_name, 0) + 3600
                    hourly_data[current_hour]["total_duration"] += 3600
                    hourly_data[current_hour]["hour_start"] = current_hour
                    current_hour += 3600
                
                # Last hour
                last_hour_duration = end_time - end_hour
                if last_hour_duration > 0:
                    hourly_data[end_hour]["apps"][app_name] = \
                        hourly_data[end_hour]["apps"].get(app_name, 0) + last_hour_duration
                    hourly_data[end_hour]["total_duration"] += last_hour_duration
                    hourly_data[end_hour]["hour_start"] = end_hour
        
        # Convert to list and sort by hour
        result = []
        for hour_start in sorted(hourly_data.keys()):
            summary = hourly_data[hour_start]
            # Convert apps dict to list
            summary["apps"] = [
                {"name": app, "duration": duration}
                for app, duration in summary["apps"].items()
            ]
            result.append(summary)
        
        return result
    
    def create_daily_summary(self, sessions: List[Dict]) -> Dict:
        """
        Create daily summary from sessions.
        
        Args:
            sessions: List of session dictionaries with categories
            
        Returns:
            Daily summary dictionary
        """
        summary = {
            "total_time": 0,
            "productive_time": 0,
            "neutral_time": 0,
            "distracting_time": 0,
            "num_sessions": len(sessions),
            "num_apps": 0
        }
        
        apps_seen = set()
        
        for session in sessions:
            duration = session.get("duration", 0)
            category = session.get("category", "neutral")
            app_name = session.get("app_name", "unknown")
            
            summary["total_time"] += duration
            apps_seen.add(app_name)
            
            if category == "productive":
                summary["productive_time"] += duration
            elif category == "neutral":
                summary["neutral_time"] += duration
            elif category == "distracting":
                summary["distracting_time"] += duration
        
        summary["num_apps"] = len(apps_seen)
        
        return summary
    
    def filter_short_sessions(self, sessions: List[Dict]) -> List[Dict]:
        """
        Filter out sessions shorter than minimum duration.
        
        Args:
            sessions: List of session dictionaries
            
        Returns:
            Filtered list of sessions
        """
        return [
            session for session in sessions
            if session.get("duration", 0) >= self.min_duration
        ]
    
    def compress_old_data(
        self,
        sessions: List[Dict],
        days_threshold: int = 30
    ) -> List[Dict]:
        """
        Compress old data by removing non-essential details.
        
        Args:
            sessions: List of session dictionaries
            days_threshold: Age threshold in days
            
        Returns:
            Compressed list of sessions
        """
        current_time = time.time()
        threshold_time = current_time - (days_threshold * 24 * 3600)
        
        compressed = []
        
        for session in sessions:
            session_copy = session.copy()
            
            if session_copy.get("start_time", current_time) < threshold_time:
                # Remove non-essential fields for old data
                fields_to_keep = [
                    "app_name", "start_time", "end_time", 
                    "duration", "category"
                ]
                session_copy = {
                    k: v for k, v in session_copy.items()
                    if k in fields_to_keep
                }
            
            compressed.append(session_copy)
        
        return compressed