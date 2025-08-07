"""
Report generation for Tempo.
Creates productivity reports and analytics.
"""
import time
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict
from datetime import datetime, timedelta

from src.core.database import Database
from src.core.categorizer import AppCategorizer
from src.core.aggregator import DataAggregator


class ReportGenerator:
    """Generates various activity and productivity reports."""
    
    def __init__(self, db_path):
        """Initialize report generator with database path."""
        self.db_path = Path(db_path)
        self.db = Database(self.db_path)
        self.db.initialize()
        self.categorizer = AppCategorizer()
        self.aggregator = DataAggregator()
    
    def generate_daily_report(self, date: Optional[float] = None) -> Dict:
        """
        Generate daily activity report.
        
        Args:
            date: Unix timestamp for the day (defaults to today)
            
        Returns:
            Daily report dictionary
        """
        if date is None:
            date = time.time()
        
        # Get start and end of day
        day_start = date - (date % 86400)
        day_end = day_start + 86400
        
        # Get sessions for the day
        sessions = self.db.get_sessions_by_date(day_start, day_end)
        
        # Calculate statistics
        total_time = sum(s.get("duration", 0) for s in sessions if s.get("duration"))
        
        # Group by category
        category_times = {"productive": 0, "neutral": 0, "distracting": 0}
        app_times = defaultdict(float)
        
        for session in sessions:
            duration = session.get("duration", 0)
            if duration:
                app_name = session.get("app_name", "unknown")
                category = session.get("category", self.categorizer.get_category(app_name))
                
                category_times[category] += duration
                app_times[app_name] += duration
        
        # Calculate productivity score
        productivity_score = self.categorizer.calculate_productivity_score(
            category_times["productive"],
            category_times["neutral"],
            category_times["distracting"]
        )
        
        # Get top apps
        top_apps = sorted(
            [{"name": name, "duration": duration} for name, duration in app_times.items()],
            key=lambda x: x["duration"],
            reverse=True
        )
        
        return {
            "date": date,
            "total_time": total_time,
            "productivity_score": productivity_score,
            "top_apps": top_apps,
            "category_breakdown": category_times,
            "num_sessions": len(sessions)
        }
    
    def generate_weekly_report(self) -> Dict:
        """Generate weekly activity report."""
        now = time.time()
        week_start = now - (7 * 86400)
        
        days = []
        weekly_total = 0
        
        for i in range(7):
            day_time = week_start + (i * 86400)
            daily_report = self.generate_daily_report(day_time)
            
            days.append({
                "date": day_time,
                "total_time": daily_report["total_time"],
                "productivity_score": daily_report["productivity_score"]
            })
            
            weekly_total += daily_report["total_time"]
        
        daily_average = weekly_total / 7 if weekly_total > 0 else 0
        
        return {
            "days": days,
            "weekly_total": weekly_total,
            "daily_average": daily_average,
            "start_date": week_start,
            "end_date": now
        }
    
    def format_as_text(self, report_data: Dict) -> str:
        """
        Format report data as human-readable text.
        
        Args:
            report_data: Report dictionary
            
        Returns:
            Formatted text report
        """
        lines = []
        lines.append("=" * 50)
        lines.append("ACTIVITY REPORT")
        lines.append("=" * 50)
        lines.append("")
        
        # Total time
        total_time = report_data.get("total_time", 0)
        hours = int(total_time // 3600)
        minutes = int((total_time % 3600) // 60)
        lines.append(f"Total Time: {hours}h {minutes}m")
        
        # Productivity score
        score = report_data.get("productivity_score", 0)
        lines.append(f"Productivity Score: {score}/100")
        lines.append("")
        
        # Top applications
        if "top_apps" in report_data and report_data["top_apps"]:
            lines.append("Top Applications:")
            lines.append("-" * 30)
            
            for i, app in enumerate(report_data["top_apps"][:5], 1):
                duration = app["duration"]
                h = int(duration // 3600)
                m = int((duration % 3600) // 60)
                lines.append(f"{i}. {app['name']:<25} {h}h {m}m")
        
        lines.append("")
        
        # Category breakdown
        if "category_breakdown" in report_data:
            lines.append("Time by Category:")
            lines.append("-" * 30)
            
            for category, duration in report_data["category_breakdown"].items():
                h = int(duration // 3600)
                m = int((duration % 3600) // 60)
                percentage = (duration / total_time * 100) if total_time > 0 else 0
                lines.append(f"{category.capitalize():<15} {h}h {m}m ({percentage:.0f}%)")
        
        return "\n".join(lines)
    
    def calculate_trends(self, days: int = 7) -> Dict:
        """
        Calculate productivity trends over specified days.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Trend analysis dictionary
        """
        now = time.time()
        scores = []
        
        for i in range(days):
            day_time = now - (i * 86400)
            report = self.generate_daily_report(day_time)
            
            if report["total_time"] > 0:  # Only count days with activity
                scores.append(report["productivity_score"])
        
        if len(scores) < 2:
            return {
                "trend_direction": "insufficient_data",
                "average_score": scores[0] if scores else 0
            }
        
        # Reverse to get chronological order
        scores.reverse()
        
        # Calculate trend
        first_half_avg = sum(scores[:len(scores)//2]) / (len(scores)//2)
        second_half_avg = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)
        
        if second_half_avg > first_half_avg + 5:
            trend = "improving"
        elif second_half_avg < first_half_avg - 5:
            trend = "declining"
        else:
            trend = "stable"
        
        return {
            "trend_direction": trend,
            "average_score": sum(scores) / len(scores),
            "scores": scores
        }
    
    def get_peak_productivity_hours(self) -> List[Dict]:
        """
        Identify hours of day with highest productivity.
        
        Returns:
            List of peak hours with productivity data
        """
        # Get last 7 days of data
        now = time.time()
        week_start = now - (7 * 86400)
        
        sessions = self.db.get_sessions_by_date(week_start, now)
        
        # Group by hour of day
        hourly_data = defaultdict(lambda: {"productive": 0, "total": 0})
        
        for session in sessions:
            if not session.get("duration"):
                continue
            
            start_time = session.get("start_time", 0)
            hour = datetime.fromtimestamp(start_time).hour
            duration = session["duration"]
            category = session.get("category", self.categorizer.get_category(session.get("app_name", "")))
            
            hourly_data[hour]["total"] += duration
            if category == "productive":
                hourly_data[hour]["productive"] += duration
        
        # Calculate productivity ratio for each hour
        peak_hours = []
        for hour, data in hourly_data.items():
            if data["total"] > 0:
                ratio = data["productive"] / data["total"]
                peak_hours.append({
                    "hour": hour,
                    "productivity_ratio": ratio,
                    "total_time": data["total"]
                })
        
        # Sort by productivity ratio
        peak_hours.sort(key=lambda x: x["productivity_ratio"], reverse=True)
        
        return peak_hours[:5]  # Top 5 hours