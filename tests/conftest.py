"""
Shared fixtures and configuration for Tempo tests.
"""
import pytest
import tempfile
import sqlite3
from pathlib import Path
from unittest.mock import MagicMock, patch


@pytest.fixture
def temp_database():
    """Create a temporary SQLite database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = Path(tmp.name)
    
    yield db_path
    
    # Cleanup - Force close any lingering connections
    # This is needed on Windows where file locks are stricter
    import gc
    import sys
    gc.collect()  # Force garbage collection to close any lingering connections
    
    # Now delete the file with retries for Windows
    if db_path.exists():
        import time
        # Retry a few times on Windows in case of lingering locks
        for attempt in range(5):
            try:
                db_path.unlink()
                break
            except PermissionError as e:
                if attempt < 4:
                    time.sleep(0.2)  # Wait a bit longer
                else:
                    # Last attempt - on Windows, we might need to accept this
                    if sys.platform == 'win32':
                        # Windows sometimes holds locks even after close
                        print(f"Warning: Could not delete {db_path} on Windows: {e}")
                    else:
                        raise


@pytest.fixture
def mock_platform_windows():
    """Mock Windows platform detection."""
    with patch('sys.platform', 'win32'):
        yield


@pytest.fixture
def mock_platform_linux():
    """Mock Linux platform detection."""
    with patch('sys.platform', 'linux'):
        yield


@pytest.fixture
def sample_applications():
    """Sample application data for testing."""
    return [
        {"name": "Visual Studio Code", "category": "productive"},
        {"name": "Firefox", "category": "neutral"},
        {"name": "Discord", "category": "distracting"},
        {"name": "Terminal", "category": "productive"},
        {"name": "Spotify", "category": "neutral"}
    ]