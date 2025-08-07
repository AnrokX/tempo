"""
Tempo CLI - Command Line Interface for the activity tracker.
"""
import click
import time
import json
from pathlib import Path
from datetime import datetime, timedelta
import os
import signal
import sys


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
        
        # Send termination signal
        os.kill(pid, signal.SIGTERM)
        PID_FILE.unlink(missing_ok=True)
        return True
    except (ProcessLookupError, ValueError):
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


if __name__ == '__main__':
    cli()