"""
Tests for configuration management.
"""
import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import tempfile

from src.utils.config import ConfigManager


class TestConfigManager:
    """Test suite for ConfigManager."""
    
    def test_config_manager_initialization(self):
        """Test that ConfigManager initializes correctly."""
        config = ConfigManager()
        assert config is not None
        assert hasattr(config, 'config')
    
    def test_config_has_default_values(self):
        """Test that config has sensible defaults."""
        config = ConfigManager()
        
        # Check tracking defaults
        assert config.get('tracking.sample_interval') == 10
        assert config.get('tracking.idle_timeout') == 300
        assert config.get('tracking.min_duration') == 60
        
        # Check export defaults
        assert config.get('export.default_format') == 'csv'
        assert config.get('export.auto_backup') == False
    
    def test_config_loads_from_file(self, tmp_path):
        """Test loading configuration from JSON file."""
        config_file = tmp_path / "config.json"
        config_data = {
            "tracking": {
                "sample_interval": 30,
                "idle_timeout": 600
            },
            "export": {
                "default_format": "json"
            }
        }
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        config = ConfigManager(config_file)
        assert config.get('tracking.sample_interval') == 30
        assert config.get('tracking.idle_timeout') == 600
        assert config.get('export.default_format') == 'json'
    
    def test_config_saves_to_file(self, tmp_path):
        """Test saving configuration to file."""
        config_file = tmp_path / "config.json"
        
        config = ConfigManager(config_file)
        config.set('tracking.sample_interval', 20)
        config.set('export.default_format', 'pdf')
        config.save()
        
        # Verify file was created and contains correct data
        assert config_file.exists()
        
        with open(config_file, 'r') as f:
            saved_data = json.load(f)
        
        assert saved_data['tracking']['sample_interval'] == 20
        assert saved_data['export']['default_format'] == 'pdf'
    
    def test_config_get_nested_value(self):
        """Test getting nested configuration values."""
        config = ConfigManager()
        config.set('database.path', '/tmp/test.db')
        config.set('database.backup.enabled', True)
        
        assert config.get('database.path') == '/tmp/test.db'
        assert config.get('database.backup.enabled') == True
    
    def test_config_get_with_default(self):
        """Test getting config value with default fallback."""
        config = ConfigManager()
        
        # Non-existent key returns default
        assert config.get('nonexistent.key', default='fallback') == 'fallback'
        
        # Existing key ignores default
        config.set('existing.key', 'value')
        assert config.get('existing.key', default='fallback') == 'value'
    
    def test_config_set_creates_nested_structure(self):
        """Test that set creates nested dictionaries as needed."""
        config = ConfigManager()
        config.set('deeply.nested.config.value', 42)
        
        assert config.config['deeply']['nested']['config']['value'] == 42
    
    def test_config_update_from_dict(self):
        """Test updating config from dictionary."""
        config = ConfigManager()
        
        updates = {
            'tracking': {
                'sample_interval': 5,
                'new_option': True
            },
            'new_section': {
                'option': 'value'
            }
        }
        
        config.update(updates)
        
        assert config.get('tracking.sample_interval') == 5
        assert config.get('tracking.new_option') == True
        assert config.get('new_section.option') == 'value'
    
    def test_config_validates_values(self):
        """Test that config validates values."""
        config = ConfigManager()
        
        # Sample interval should be positive
        with pytest.raises(ValueError):
            config.set('tracking.sample_interval', -1)
        
        # Export format should be valid
        with pytest.raises(ValueError):
            config.set('export.default_format', 'invalid')
    
    def test_config_handles_missing_file_gracefully(self):
        """Test that missing config file uses defaults."""
        config = ConfigManager(Path('/nonexistent/config.json'))
        
        # Should use defaults
        assert config.get('tracking.sample_interval') == 10
    
    def test_config_handles_invalid_json(self, tmp_path):
        """Test handling of invalid JSON in config file."""
        config_file = tmp_path / "invalid.json"
        config_file.write_text("{ invalid json }")
        
        # Should use defaults on invalid JSON
        config = ConfigManager(config_file)
        assert config.get('tracking.sample_interval') == 10
    
    def test_config_get_all_returns_full_config(self):
        """Test getting entire configuration."""
        config = ConfigManager()
        config.set('test.value', 123)
        
        all_config = config.get_all()
        assert isinstance(all_config, dict)
        assert 'tracking' in all_config
        assert all_config['test']['value'] == 123
    
    def test_config_reset_to_defaults(self):
        """Test resetting configuration to defaults."""
        config = ConfigManager()
        config.set('tracking.sample_interval', 999)
        
        config.reset_to_defaults()
        
        assert config.get('tracking.sample_interval') == 10