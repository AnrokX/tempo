#!/usr/bin/env python3
"""
Demo script to showcase Tempo functionality.
This simulates activity tracking and generates reports.
"""
import time
import random
from pathlib import Path

# Import Tempo components
from src.core.database import Database
from src.core.session import SessionManager
from src.core.categorizer import AppCategorizer
from src.core.aggregator import DataAggregator
from src.core.reports import ReportGenerator


def create_sample_data():
    """Create sample tracking data for demonstration."""
    print("🚀 Creating sample data for demonstration...")
    
    # Setup database
    db_path = Path.home() / '.tempo' / 'demo.db'
    db_path.parent.mkdir(exist_ok=True)
    
    # Initialize components
    db = Database(db_path)
    db.initialize()
    categorizer = AppCategorizer()
    
    # Sample applications with realistic usage patterns
    apps = [
        ("Visual Studio Code", 7200),  # 2 hours
        ("Firefox", 3600),              # 1 hour
        ("Terminal", 2400),             # 40 minutes
        ("Slack", 1800),                # 30 minutes
        ("YouTube", 900),               # 15 minutes
        ("Discord", 600),               # 10 minutes
        ("Spotify", 1200),              # 20 minutes
    ]
    
    print(f"📁 Database created at: {db_path}")
    
    # Add sessions for today
    current_time = time.time()
    start_of_day = current_time - (current_time % 86400)
    
    print("\n📊 Adding sample sessions for today:")
    session_time = start_of_day + (9 * 3600)  # Start at 9 AM
    
    for app_name, duration in apps:
        category = categorizer.get_category(app_name)
        app_id = db.save_application(app_name, category)
        
        # Split into multiple sessions for realism
        remaining = duration
        while remaining > 0:
            session_duration = min(remaining, random.randint(300, 1800))  # 5-30 min sessions
            db.save_session(app_id, session_time, session_time + session_duration)
            
            print(f"  ✓ {app_name:<20} {session_duration//60:3d} min  [{category}]")
            
            session_time += session_duration + random.randint(60, 300)  # Small breaks
            remaining -= session_duration
    
    db.close()
    return db_path


def demonstrate_reports(db_path):
    """Demonstrate report generation."""
    print("\n" + "="*60)
    print("📈 GENERATING REPORTS")
    print("="*60)
    
    generator = ReportGenerator(db_path)
    
    # Daily Report
    print("\n📅 Daily Report:")
    print("-" * 40)
    daily = generator.generate_daily_report()
    
    total_hours = daily['total_time'] / 3600
    print(f"Total Time: {total_hours:.1f} hours")
    print(f"Productivity Score: {daily['productivity_score']}/100")
    print(f"Number of Sessions: {daily['num_sessions']}")
    
    print("\n⏱️ Top Applications:")
    for i, app in enumerate(daily['top_apps'][:5], 1):
        minutes = app['duration'] / 60
        print(f"  {i}. {app['name']:<20} {minutes:6.0f} min")
    
    print("\n📊 Time by Category:")
    for category, seconds in daily['category_breakdown'].items():
        minutes = seconds / 60
        percentage = (seconds / daily['total_time'] * 100) if daily['total_time'] > 0 else 0
        print(f"  {category.capitalize():<15} {minutes:6.0f} min ({percentage:5.1f}%)")
    
    # Productivity Score Calculation
    print("\n🎯 Productivity Analysis:")
    print("-" * 40)
    categorizer = AppCategorizer()
    score = categorizer.calculate_productivity_score(
        daily['category_breakdown']['productive'],
        daily['category_breakdown']['neutral'],
        daily['category_breakdown']['distracting']
    )
    print(f"Calculated Score: {score}/100")
    
    if score >= 80:
        print("Rating: Excellent! 🌟")
    elif score >= 60:
        print("Rating: Good 👍")
    elif score >= 40:
        print("Rating: Fair 📊")
    else:
        print("Rating: Needs Improvement 📈")


def demonstrate_aggregation(db_path):
    """Demonstrate data aggregation features."""
    print("\n" + "="*60)
    print("🔄 DATA AGGREGATION")
    print("="*60)
    
    db = Database(db_path)
    db.initialize()
    aggregator = DataAggregator()
    
    # Get today's sessions
    current_time = time.time()
    start_of_day = current_time - (current_time % 86400)
    sessions = db.get_sessions_by_date(start_of_day, current_time)
    
    # Merge consecutive sessions
    print(f"\n📦 Original sessions: {len(sessions)}")
    merged = aggregator.merge_consecutive_sessions(sessions)
    print(f"📦 After merging: {len(merged)}")
    
    # Create hourly summary
    hourly = aggregator.create_hourly_summary(sessions)
    print(f"\n⏰ Hourly Summary ({len(hourly)} active hours):")
    for hour_data in hourly[:5]:  # Show first 5 hours
        hour = time.strftime("%H:00", time.localtime(hour_data['hour_start']))
        minutes = hour_data['total_duration'] / 60
        print(f"  {hour}: {minutes:.0f} min - {len(hour_data['apps'])} apps")
    
    db.close()


def demonstrate_categorization():
    """Demonstrate app categorization system."""
    print("\n" + "="*60)
    print("🏷️ CATEGORIZATION SYSTEM")
    print("="*60)
    
    categorizer = AppCategorizer()
    
    test_apps = [
        "Visual Studio Code",
        "PyCharm",
        "Firefox",
        "YouTube",
        "Discord",
        "Terminal",
        "Spotify",
        "Microsoft Teams",
        "Steam",
        "Git"
    ]
    
    print("\n📱 Default App Categories:")
    print("-" * 40)
    for app in test_apps:
        category = categorizer.get_category(app)
        emoji = {"productive": "✅", "neutral": "🔵", "distracting": "🔴"}[category]
        print(f"  {emoji} {app:<20} → {category}")
    
    # Custom categorization
    print("\n🔧 Custom Categorization:")
    print("-" * 40)
    categorizer.set_category("Discord", "productive")
    print(f"  Discord recategorized: {categorizer.get_category('Discord')}")


def run_tests():
    """Run the test suite."""
    print("\n" + "="*60)
    print("🧪 RUNNING TEST SUITE")
    print("="*60)
    
    import subprocess
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/", "-v", "--tb=short"],
        capture_output=True,
        text=True
    )
    
    # Parse output for summary
    lines = result.stdout.split('\n')
    for line in lines:
        if 'passed' in line or 'failed' in line or 'error' in line:
            print(f"  {line}")
    
    if result.returncode == 0:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed")
    
    # Coverage report
    print("\n📊 Running coverage report...")
    result = subprocess.run(
        ["python", "-m", "pytest", "--cov=src", "--cov-report=term-missing", "--quiet"],
        capture_output=True,
        text=True
    )
    
    # Extract coverage percentage
    for line in result.stdout.split('\n'):
        if 'TOTAL' in line:
            print(f"  {line}")


def main():
    """Run the full demonstration."""
    print("\n" + "="*60)
    print("  TEMPO - Activity Tracker Demonstration")
    print("="*60)
    
    # Create sample data
    db_path = create_sample_data()
    
    # Demonstrate features
    demonstrate_categorization()
    demonstrate_aggregation(db_path)
    demonstrate_reports(db_path)
    
    # Run tests
    run_tests()
    
    print("\n" + "="*60)
    print("  ✨ Demonstration Complete!")
    print("="*60)
    print(f"\n💡 Try these commands:")
    print(f"  python -m src.cli start    # Start tracking")
    print(f"  python -m src.cli status   # Check status")
    print(f"  python -m src.cli today    # View today's summary")
    print(f"  python -m src.cli stop     # Stop tracking")
    print(f"\n📁 Demo database: {db_path}")


if __name__ == "__main__":
    main()