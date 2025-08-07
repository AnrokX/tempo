"""
Platform detection and OS-specific window tracking.
Minimal implementation for TDD (GREEN phase).
"""
import sys


def get_platform():
    """Detect the current operating system."""
    platform = sys.platform
    
    if platform == 'win32':
        return 'windows'
    elif platform == 'linux':
        return 'linux'
    elif platform == 'darwin':
        return 'macos'
    else:
        return 'unknown'


def get_active_window():
    """Get information about the currently active window."""
    platform = get_platform()
    
    if platform == 'unknown':
        return None
    
    # Minimal implementation - return None for now
    return None