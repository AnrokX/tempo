"""
Unit tests for application categorization system.
Following TDD: Red-Green-Refactor cycle.
"""
import pytest
from pathlib import Path
import json


class TestCategorizer:
    """Test suite for AppCategorizer class."""
    
    def test_categorizer_can_be_initialized(self):
        """Test that AppCategorizer can be created."""
        from src.core.categorizer import AppCategorizer
        
        categorizer = AppCategorizer()
        
        assert categorizer is not None
    
    def test_categorizer_has_default_categories(self):
        """Test that categorizer has default app categories."""
        from src.core.categorizer import AppCategorizer
        
        categorizer = AppCategorizer()
        
        # Should have default categories for common apps
        assert categorizer.get_category("Visual Studio Code") == "productive"
        assert categorizer.get_category("Firefox") == "neutral"
        assert categorizer.get_category("YouTube") == "distracting"
    
    def test_categorizer_returns_neutral_for_unknown_apps(self):
        """Test that unknown apps default to neutral category."""
        from src.core.categorizer import AppCategorizer
        
        categorizer = AppCategorizer()
        
        category = categorizer.get_category("UnknownApp123")
        
        assert category == "neutral"
    
    def test_categorizer_can_set_custom_category(self):
        """Test that users can set custom categories for apps."""
        from src.core.categorizer import AppCategorizer
        
        categorizer = AppCategorizer()
        
        # Set custom category
        categorizer.set_category("Discord", "productive")
        
        assert categorizer.get_category("Discord") == "productive"
    
    def test_categorizer_calculates_productivity_score(self):
        """Test productivity score calculation."""
        from src.core.categorizer import AppCategorizer
        
        categorizer = AppCategorizer()
        
        # Test with different time distributions
        # 480 minutes productive (weight 1.0) = 480
        # 60 minutes neutral (weight 0.5) = 30
        # 60 minutes distracting (weight 0.0) = 0
        # Total: 510 / 600 = 0.85 = 85%
        score = categorizer.calculate_productivity_score(
            productive_time=480,   # 8 hours
            neutral_time=60,       # 1 hour
            distracting_time=60    # 1 hour
        )
        
        assert score == 85  # (480*1 + 60*0.5 + 60*0) / 600 * 100
    
    def test_productivity_score_handles_zero_time(self):
        """Test that productivity score handles zero total time."""
        from src.core.categorizer import AppCategorizer
        
        categorizer = AppCategorizer()
        
        score = categorizer.calculate_productivity_score(0, 0, 0)
        
        assert score == 0
    
    def test_categorizer_loads_custom_rules_from_file(self):
        """Test loading custom categorization rules from JSON."""
        from src.core.categorizer import AppCategorizer
        import tempfile
        
        # Create temp config file
        config = {
            "categories": {
                "productive": ["IDE", "Terminal", "Git"],
                "neutral": ["Browser", "Email"],
                "distracting": ["Social Media", "Games"]
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            config_path = f.name
        
        categorizer = AppCategorizer(config_path=config_path)
        
        assert categorizer.get_category("IDE") == "productive"
        assert categorizer.get_category("Games") == "distracting"
        
        # Cleanup
        Path(config_path).unlink()
    
    def test_categorizer_saves_custom_rules(self):
        """Test saving custom categorization rules."""
        from src.core.categorizer import AppCategorizer
        import tempfile
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            config_path = f.name
        
        categorizer = AppCategorizer(config_path=config_path)
        
        # Set custom categories
        categorizer.set_category("MyApp", "productive")
        categorizer.save_rules()
        
        # Load in new instance
        new_categorizer = AppCategorizer(config_path=config_path)
        
        assert new_categorizer.get_category("MyApp") == "productive"
        
        # Cleanup
        Path(config_path).unlink()


class TestCategoryStatistics:
    """Test suite for category-based statistics."""
    
    def test_categorizer_groups_apps_by_category(self):
        """Test grouping applications by category."""
        from src.core.categorizer import AppCategorizer
        
        categorizer = AppCategorizer()
        
        apps = [
            {"name": "Visual Studio Code", "duration": 3600},
            {"name": "Terminal", "duration": 1800},
            {"name": "Firefox", "duration": 1200},
            {"name": "YouTube", "duration": 600}
        ]
        
        grouped = categorizer.group_by_category(apps)
        
        assert "productive" in grouped
        assert "neutral" in grouped
        assert "distracting" in grouped
        
        # Check totals
        assert grouped["productive"]["total_time"] == 5400  # VSCode + Terminal
        assert grouped["neutral"]["total_time"] == 1200     # Firefox
        assert grouped["distracting"]["total_time"] == 600  # YouTube