"""
Unit tests for platform detection and OS-specific functionality.
Following TDD: Red-Green-Refactor cycle.
"""
import pytest
from unittest.mock import patch, MagicMock


class TestPlatformDetection:
    """Test suite for platform detection utilities."""
    
    def test_detects_current_platform(self):
        """Test that platform detection returns valid OS identifier."""
        from src.utils.platform import get_platform
        
        platform = get_platform()
        
        assert platform in ['windows', 'linux', 'macos', 'unknown']
    
    @patch('sys.platform', 'win32')
    def test_detects_windows_platform(self):
        """Test Windows platform detection."""
        from src.utils.platform import get_platform
        
        platform = get_platform()
        
        assert platform == 'windows'
    
    @patch('sys.platform', 'linux')
    def test_detects_linux_platform(self):
        """Test Linux platform detection."""
        from src.utils.platform import get_platform
        
        platform = get_platform()
        
        assert platform == 'linux'
    
    @patch('sys.platform', 'darwin')
    def test_detects_macos_platform(self):
        """Test macOS platform detection."""
        from src.utils.platform import get_platform
        
        platform = get_platform()
        
        assert platform == 'macos'


class TestWindowTracking:
    """Test suite for window tracking functionality."""
    
    def test_get_active_window_returns_app_info(self):
        """Test that get_active_window returns application information."""
        from src.utils.platform import get_active_window
        
        window_info = get_active_window()
        
        # Should return dict with app_name or None
        assert window_info is None or isinstance(window_info, dict)
        if window_info:
            assert 'app_name' in window_info
    
    @patch('src.utils.platform.get_platform')
    def test_unsupported_platform_returns_none(self, mock_platform):
        """Test that unsupported platforms return None gracefully."""
        from src.utils.platform import get_active_window
        
        mock_platform.return_value = 'unknown'
        
        window_info = get_active_window()
        
        assert window_info is None