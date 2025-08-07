"""
Application categorization system for Tempo.
Manages productivity scoring and app categories.
"""
import json
from pathlib import Path
from typing import Dict, List, Optional


class AppCategorizer:
    """Categorizes applications and calculates productivity scores."""
    
    # Default categories for common applications
    DEFAULT_CATEGORIES = {
        "productive": [
            "Visual Studio Code", "VSCode", "Code",
            "PyCharm", "IntelliJ", "Eclipse", "Sublime Text",
            "Terminal", "Console", "iTerm", "PowerShell",
            "Git", "GitHub Desktop",
            "Vim", "Emacs", "Nano",
            "Xcode", "Android Studio",
            "Postman", "Docker Desktop",
            "Microsoft Word", "Microsoft Excel", "Microsoft PowerPoint",
            "Google Docs", "Google Sheets",
            "Notion", "Obsidian", "Roam Research"
        ],
        "neutral": [
            "Firefox", "Chrome", "Safari", "Edge", "Brave",
            "Thunderbird", "Mail", "Outlook",
            "Slack", "Microsoft Teams", "Zoom",
            "Finder", "Explorer", "File Manager",
            "Settings", "System Preferences",
            "Spotify", "Apple Music"
        ],
        "distracting": [
            "YouTube", "Netflix", "Twitch", "Disney+",
            "Facebook", "Twitter", "Instagram", "TikTok",
            "Reddit", "Discord",
            "Steam", "Epic Games", "League of Legends",
            "WhatsApp", "Telegram", "Signal"
        ]
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize categorizer with optional config file."""
        self.config_path = Path(config_path) if config_path else None
        self.categories = {}
        self.custom_rules = {}
        
        # Load default categories
        self._load_defaults()
        
        # Load custom rules if config exists
        if self.config_path and self.config_path.exists():
            self._load_custom_rules()
    
    def _load_defaults(self):
        """Load default category mappings."""
        for category, apps in self.DEFAULT_CATEGORIES.items():
            for app in apps:
                self.categories[app.lower()] = category
    
    def _load_custom_rules(self):
        """Load custom rules from config file."""
        if not self.config_path or not self.config_path.exists():
            return
        
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                
            if 'categories' in config:
                for category, apps in config['categories'].items():
                    for app in apps:
                        self.custom_rules[app.lower()] = category
        except (json.JSONDecodeError, IOError):
            pass  # Ignore invalid config files
    
    def get_category(self, app_name: str) -> str:
        """Get category for an application."""
        app_lower = app_name.lower()
        
        # Check custom rules first
        if app_lower in self.custom_rules:
            return self.custom_rules[app_lower]
        
        # Check default categories
        if app_lower in self.categories:
            return self.categories[app_lower]
        
        # Check partial matches for common apps
        for key in self.categories:
            if key in app_lower or app_lower in key:
                return self.categories[key]
        
        # Default to neutral for unknown apps
        return "neutral"
    
    def set_category(self, app_name: str, category: str):
        """Set custom category for an application."""
        if category not in ["productive", "neutral", "distracting"]:
            raise ValueError(f"Invalid category: {category}")
        
        self.custom_rules[app_name.lower()] = category
    
    def save_rules(self):
        """Save custom rules to config file."""
        if not self.config_path:
            return
        
        # Organize custom rules by category
        config = {"categories": {"productive": [], "neutral": [], "distracting": []}}
        
        for app, category in self.custom_rules.items():
            # Use original case from first occurrence
            for original_app, cat in self.custom_rules.items():
                if original_app.lower() == app and cat == category:
                    config["categories"][category].append(original_app.title())
                    break
        
        # Save to file
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def calculate_productivity_score(
        self, 
        productive_time: float, 
        neutral_time: float, 
        distracting_time: float
    ) -> float:
        """
        Calculate productivity score (0-100).
        
        Formula:
        - Productive time: 100% weight (1.0)
        - Neutral time: 50% weight (0.5)
        - Distracting time: 0% weight (0.0)
        """
        total_time = productive_time + neutral_time + distracting_time
        
        if total_time == 0:
            return 0
        
        weighted_productive = productive_time * 1.0
        weighted_neutral = neutral_time * 0.5
        weighted_distracting = distracting_time * 0.0
        
        weighted_total = weighted_productive + weighted_neutral + weighted_distracting
        
        score = (weighted_total / total_time) * 100
        
        return round(score)
    
    def group_by_category(self, apps: List[Dict]) -> Dict:
        """
        Group applications by category with statistics.
        
        Args:
            apps: List of dicts with 'name' and 'duration' keys
            
        Returns:
            Dict with categories as keys and aggregated stats
        """
        grouped = {
            "productive": {"apps": [], "total_time": 0},
            "neutral": {"apps": [], "total_time": 0},
            "distracting": {"apps": [], "total_time": 0}
        }
        
        for app in apps:
            category = self.get_category(app["name"])
            grouped[category]["apps"].append(app)
            grouped[category]["total_time"] += app.get("duration", 0)
        
        return grouped