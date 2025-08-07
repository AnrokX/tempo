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
    
    # Cleanup
    if db_path.exists():
        db_path.unlink()


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