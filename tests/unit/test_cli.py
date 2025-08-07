"""
Unit tests for CLI commands.
Following TDD: Red-Green-Refactor cycle.
"""
import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
import json
from pathlib import Path
from src.cli import cli


class TestCLI:
    """Test suite for CLI commands."""
    
    def test_cli_can_be_invoked(self):
        """Test that CLI can be invoked without errors."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        
        assert result.exit_code == 0
        assert 'tempo' in result.output.lower()
    
    def test_start_command_begins_tracking(self):
        """Test that 'tempo start' begins tracking."""
        runner = CliRunner()
        
        with patch('src.cli.start_tracking') as mock_start:
            mock_start.return_value = True
            result = runner.invoke(cli, ['start'])
            
            assert result.exit_code == 0
            assert 'started' in result.output.lower()
            mock_start.assert_called_once()
    
    def test_stop_command_stops_tracking(self):
        """Test that 'tempo stop' stops tracking."""
        runner = CliRunner()
        
        with patch('src.cli.is_tracking_running') as mock_running, \
             patch('src.cli.stop_tracking') as mock_stop:
            mock_running.return_value = True
            mock_stop.return_value = True
            result = runner.invoke(cli, ['stop'])
            
            assert result.exit_code == 0
            assert 'stopped' in result.output.lower()
            mock_stop.assert_called_once()
    
    def test_status_command_shows_tracking_status(self):
        """Test that 'tempo status' shows current status."""
        runner = CliRunner()
        
        with patch('src.cli.get_tracker_status') as mock_status:
            mock_status.return_value = {
                'running': True,
                'current_app': 'firefox',
                'session_duration': 300
            }
            
            result = runner.invoke(cli, ['status'])
            
            assert result.exit_code == 0
            assert 'running' in result.output.lower()
            assert 'firefox' in result.output.lower()
    
    def test_today_command_shows_daily_summary(self):
        """Test that 'tempo today' shows today's activity."""
        runner = CliRunner()
        
        with patch('src.cli.get_today_summary') as mock_today:
            mock_today.return_value = {
                'total_time': 3600,
                'productive_time': 2400,
                'apps': [
                    {'name': 'vscode', 'duration': 2400},
                    {'name': 'firefox', 'duration': 1200}
                ]
            }
            
            result = runner.invoke(cli, ['today'])
            
            assert result.exit_code == 0
            assert 'vscode' in result.output.lower()
            assert 'firefox' in result.output.lower()
    
    @patch('src.cli.is_tracking_running')
    def test_start_prevents_double_start(self, mock_is_running):
        """Test that start command prevents double starting."""
        runner = CliRunner()
        mock_is_running.return_value = True
        
        result = runner.invoke(cli, ['start'])
        
        assert result.exit_code == 0
        assert 'already running' in result.output.lower()
    
    @patch('src.cli.is_tracking_running')
    def test_stop_when_not_running(self, mock_is_running):
        """Test that stop command handles when not running."""
        runner = CliRunner()
        mock_is_running.return_value = False
        
        result = runner.invoke(cli, ['stop'])
        
        assert result.exit_code == 0
        assert 'not running' in result.output.lower()