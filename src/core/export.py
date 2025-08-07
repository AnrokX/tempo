"""
Export module for Tempo activity data.
Handles CSV, JSON export and database backup/restore.
"""
import csv
import json
import shutil
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
import time


class DataExporter:
    """Handles data export operations."""
    
    def __init__(self, db_path: Path):
        """Initialize exporter with database path."""
        self.db_path = db_path
    
    def export_to_csv(self, output_file: Path, start_date: Optional[float] = None, 
                      end_date: Optional[float] = None, anonymize: bool = False) -> bool:
        """Export sessions data to CSV format."""
        try:
            # Create parent directory if needed
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Get session data
            data = self._get_sessions_data(start_date, end_date)
            
            # Write CSV file
            with open(output_file, 'w', newline='') as f:
                if not data:
                    # Write header even for empty data
                    writer = csv.writer(f)
                    writer.writerow(['app_name', 'category', 'start_time', 'end_time', 'duration'])
                    return True
                
                # Write data
                fieldnames = data[0].keys() if data else []
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for row in data:
                    if anonymize and 'app_name' in row:
                        row = row.copy()
                        row['app_name'] = self._anonymize_app_name(row['app_name'])
                    writer.writerow(row)
            
            return True
        except Exception:
            return False
    
    def export_to_json(self, output_file: Path, start_date: Optional[float] = None,
                       end_date: Optional[float] = None) -> bool:
        """Export sessions data to JSON format."""
        try:
            # Create parent directory if needed
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Get session data
            data = self._get_sessions_data(start_date, end_date)
            
            # Create JSON structure
            export_data = {
                'export_date': time.time(),
                'sessions': data,
                'metadata': {
                    'total_sessions': len(data),
                    'date_range': {
                        'start': start_date,
                        'end': end_date
                    }
                }
            }
            
            # Write JSON file
            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            return True
        except Exception:
            return False
    
    def backup_database(self, backup_path: Path) -> bool:
        """Create a backup of the database."""
        try:
            # Create parent directory if needed
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy database file
            shutil.copy2(self.db_path, backup_path)
            return True
        except Exception:
            return False
    
    def restore_database(self, backup_path: Path) -> bool:
        """Restore database from backup."""
        try:
            # Create parent directory if needed
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy backup to database location
            shutil.copy2(backup_path, self.db_path)
            return True
        except Exception:
            return False
    
    def export_summary(self, output_file: Path) -> bool:
        """Export a summary report."""
        try:
            # Create parent directory if needed
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Generate summary
            summary = self._generate_summary()
            
            # Write summary to file
            with open(output_file, 'w') as f:
                json.dump(summary, f, indent=2)
            
            return True
        except Exception:
            return False
    
    def _get_sessions_data(self, start_date: Optional[float] = None,
                          end_date: Optional[float] = None) -> List[Dict[str, Any]]:
        """Get sessions data from database."""
        # This would normally query the database
        # For now, return empty list (will be mocked in tests)
        return []
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate a summary of the data."""
        # This would normally calculate from database
        # For now, return empty dict (will be mocked in tests)
        return {}
    
    def _anonymize_app_name(self, app_name: str) -> str:
        """Anonymize application name."""
        # Simple anonymization for now
        return f"App_{hash(app_name) % 1000:03d}"


# Legacy class name for backward compatibility
class Exporter(DataExporter):
    """Legacy exporter class for backward compatibility."""
    
    def export_sessions_to_csv(self, output_file: Path, start_date: Optional[float] = None,
                               end_date: Optional[float] = None) -> bool:
        """Export sessions to CSV (legacy method)."""
        return self.export_to_csv(output_file, start_date, end_date)
    
    def export_sessions_to_json(self, output_file: Path, start_date: Optional[float] = None,
                                end_date: Optional[float] = None) -> bool:
        """Export sessions to JSON (legacy method)."""
        return self.export_to_json(output_file, start_date, end_date)