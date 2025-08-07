"""
Tempo CLI - Command Line Interface for the activity tracker.
"""
import click
import time
import json
from pathlib import Path
from datetime import datetime, timedelta
import os
import sys
import signal


# Configuration
CONFIG_DIR = Path.home() / '.tempo'
DB_PATH = CONFIG_DIR / 'tempo.db'
PID_FILE = CONFIG_DIR / 'tempo.pid'


def ensure_config_dir():
    """Ensure configuration directory exists."""
    CONFIG_DIR.mkdir(exist_ok=True)


def is_tracking_running():
    """Check if tracking is already running."""
    if not PID_FILE.exists():
        return False
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read())
        
        # Check if process is running
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, ValueError):
        # Process not running, clean up PID file
        PID_FILE.unlink(missing_ok=True)
        return False


def start_tracking():
    """Start the tracking process."""
    ensure_config_dir()
    
    # Save PID
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))
    
    return True


def stop_tracking():
    """Stop the tracking process."""
    if not PID_FILE.exists():
        return False
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read())
        
        # Send termination signal (cross-platform)
        if sys.platform == "win32":
            # On Windows, use SIGTERM if available, otherwise use signal 15
            import signal
            term_signal = getattr(signal, 'SIGTERM', 15)
        else:
            # On Unix-like systems, use SIGTERM
            term_signal = signal.SIGTERM
            
        os.kill(pid, term_signal)
        PID_FILE.unlink(missing_ok=True)
        return True
    except (ProcessLookupError, ValueError, OSError):
        PID_FILE.unlink(missing_ok=True)
        return False


def get_tracker_status():
    """Get current tracker status."""
    if not is_tracking_running():
        return {'running': False}
    
    return {
        'running': True,
        'current_app': 'firefox',  # Placeholder
        'session_duration': 300  # Placeholder
    }


def get_today_summary():
    """Get today's activity summary."""
    # Placeholder implementation
    return {
        'total_time': 3600,
        'productive_time': 2400,
        'apps': [
            {'name': 'vscode', 'duration': 2400},
            {'name': 'firefox', 'duration': 1200}
        ]
    }


def format_duration(seconds):
    """Format duration in seconds to human readable string."""
    if seconds is None:
        return "0m"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"


@click.group(name='tempo')
def cli():
    """Tempo - Your time. Your data. Your rhythm."""
    pass


@cli.command()
def start():
    """Start tracking your activity."""
    if is_tracking_running():
        click.echo("Tempo is already running.")
        return
    
    if start_tracking():
        click.echo("Tempo tracking started.")
    else:
        click.echo("Failed to start Tempo.", err=True)


@cli.command()
def stop():
    """Stop tracking your activity."""
    if not is_tracking_running():
        click.echo("Tempo is not running.")
        return
    
    if stop_tracking():
        click.echo("Tempo tracking stopped.")
    else:
        click.echo("Failed to stop Tempo.", err=True)


@cli.command()
def status():
    """Show current tracking status."""
    status_info = get_tracker_status()
    
    if not status_info['running']:
        click.echo("Tempo is not running.")
        return
    
    click.echo("Tempo is running.")
    
    if 'current_app' in status_info:
        click.echo(f"Current app: {status_info['current_app']}")
    
    if 'session_duration' in status_info:
        duration = format_duration(status_info['session_duration'])
        click.echo(f"Session duration: {duration}")


@cli.command()
def today():
    """Show today's activity summary."""
    summary = get_today_summary()
    
    click.echo("\n" + "="*50)
    click.echo("TODAY'S ACTIVITY SUMMARY")
    click.echo("="*50)
    
    total = format_duration(summary.get('total_time', 0))
    productive = format_duration(summary.get('productive_time', 0))
    
    click.echo(f"\nTotal Time: {total}")
    click.echo(f"Productive Time: {productive}")
    
    if 'apps' in summary and summary['apps']:
        click.echo("\nTop Applications:")
        click.echo("-" * 30)
        
        for i, app in enumerate(summary['apps'][:5], 1):
            duration = format_duration(app['duration'])
            click.echo(f"{i}. {app['name']:<20} {duration}")
    
    click.echo("")


@cli.group()
def export():
    """Export tracking data in various formats."""
    pass


@export.command('csv')
@click.option('--output', '-o', type=click.Path(), required=True, help='Output file path')
@click.option('--start', type=str, help='Start date (YYYY-MM-DD)')
@click.option('--end', type=str, help='End date (YYYY-MM-DD)')
def export_csv(output, start, end):
    """Export data to CSV format."""
    try:
        from src.core.export import DataExporter
        
        if not DB_PATH.exists():
            click.echo("No tracking data found.")
            return
        
        exporter = DataExporter(DB_PATH)
        
        # Parse dates if provided
        start_time = None
        end_time = None
        if start:
            start_time = datetime.strptime(start, '%Y-%m-%d').timestamp()
        if end:
            end_time = datetime.strptime(end, '%Y-%m-%d').timestamp()
        
        output_path = Path(output)
        if exporter.export_to_csv(output_path, start_time, end_time):
            click.echo(f"Data exported to {output_path}")
        else:
            click.echo("Export failed.", err=True)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@export.command('json')
@click.option('--output', '-o', type=click.Path(), required=True, help='Output file path')
@click.option('--start', type=str, help='Start date (YYYY-MM-DD)')
@click.option('--end', type=str, help='End date (YYYY-MM-DD)')
def export_json(output, start, end):
    """Export data to JSON format."""
    try:
        from src.core.export import DataExporter
        
        if not DB_PATH.exists():
            click.echo("No tracking data found.")
            return
        
        exporter = DataExporter(DB_PATH)
        
        # Parse dates if provided
        start_time = None
        end_time = None
        if start:
            start_time = datetime.strptime(start, '%Y-%m-%d').timestamp()
        if end:
            end_time = datetime.strptime(end, '%Y-%m-%d').timestamp()
        
        output_path = Path(output)
        if exporter.export_to_json(output_path, start_time, end_time):
            click.echo(f"Data exported to {output_path}")
        else:
            click.echo("Export failed.", err=True)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@cli.command()
@click.option('--output', '-o', type=click.Path(), required=True, help='Backup file path')
def backup(output):
    """Create a backup of the database."""
    try:
        from src.core.export import DataExporter
        
        if not DB_PATH.exists():
            click.echo("No database to backup.")
            return
        
        exporter = DataExporter(DB_PATH)
        output_path = Path(output)
        
        if exporter.backup_database(output_path):
            click.echo(f"Database backed up to {output_path}")
        else:
            click.echo("Backup failed.", err=True)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@cli.command()
@click.option('--input', '-i', 'input_file', type=click.Path(exists=True), required=True, help='Backup file to restore')
def restore(input_file):
    """Restore database from backup."""
    try:
        from src.core.export import DataExporter
        
        backup_path = Path(input_file)
        
        if DB_PATH.exists():
            if not click.confirm("This will overwrite existing data. Continue?"):
                return
        
        ensure_config_dir()
        exporter = DataExporter(DB_PATH)
        
        if exporter.restore_database(backup_path):
            click.echo(f"Database restored from {backup_path}")
        else:
            click.echo("Restore failed.", err=True)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


if __name__ == '__main__':
    cli()