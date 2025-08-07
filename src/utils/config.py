"""
Configuration management for Tempo.
"""
import json
from pathlib import Path
from typing import Any, Dict, Optional
import copy


class ConfigManager:
    """Manages application configuration."""
    
    # Default configuration
    DEFAULTS = {
        'tracking': {
            'sample_interval': 10,      # seconds between samples
            'idle_timeout': 300,         # seconds before marking as idle
            'min_duration': 60,          # minimum session duration to record
        },
        'database': {
            'path': '~/.tempo/tempo.db',
            'backup': {
                'enabled': False,
                'interval_days': 7,
            }
        },
        'export': {
            'default_format': 'csv',
            'auto_backup': False,
            'backup_interval_days': 7,
        },
        'categories': {
            'productive': [],
            'neutral': [],
            'distracting': [],
        },
        'goals': {
            'daily_productive_hours': 0,
            'max_distracting_hours': 0,
        }
    }
    
    VALID_EXPORT_FORMATS = ['csv', 'json', 'pdf']
    
    def __init__(self, config_file: Optional[Path] = None):
        """Initialize configuration manager."""
        self.config_file = config_file
        self.config = copy.deepcopy(self.DEFAULTS)
        
        if config_file:
            self._load_from_file()
    
    def _load_from_file(self):
        """Load configuration from file."""
        if not self.config_file or not self.config_file.exists():
            return
        
        try:
            with open(self.config_file, 'r') as f:
                loaded_config = json.load(f)
                self._merge_config(loaded_config)
        except (json.JSONDecodeError, IOError):
            # Use defaults on error
            pass
    
    def _merge_config(self, updates: Dict[str, Any]):
        """Merge updates into configuration."""
        def merge_dict(base: dict, updates: dict):
            for key, value in updates.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    merge_dict(base[key], value)
                else:
                    base[key] = value
        
        merge_dict(self.config, updates)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation."""
        # Validate specific keys
        if key == 'tracking.sample_interval' and value <= 0:
            raise ValueError("Sample interval must be positive")
        
        if key == 'export.default_format' and value not in self.VALID_EXPORT_FORMATS:
            raise ValueError(f"Export format must be one of {self.VALID_EXPORT_FORMATS}")
        
        # Set the value
        keys = key.split('.')
        config = self.config
        
        # Create nested structure
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def update(self, updates: Dict[str, Any]):
        """Update configuration from dictionary."""
        self._merge_config(updates)
    
    def save(self):
        """Save configuration to file."""
        if not self.config_file:
            return
        
        # Create parent directory if needed
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration."""
        return copy.deepcopy(self.config)
    
    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self.config = copy.deepcopy(self.DEFAULTS)