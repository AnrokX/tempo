"""
Tests for the export module.
"""
import pytest
import csv
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import time

from src.core.export import DataExporter


class TestDataExporter:
    """Test suite for DataExporter class."""
    
    def test_exporter_initialization(self):
        """Test that exporter initializes correctly."""
        db_path = Path("/tmp/test.db")
        exporter = DataExporter(db_path)
        assert exporter.db_path == db_path
    
    def test_export_to_csv_creates_file(self, tmp_path):
        """Test that CSV export creates a file."""
        db_path = Path("/tmp/test.db")
        exporter = DataExporter(db_path)
        
        output_file = tmp_path / "export.csv"
        
        # Mock database data
        mock_data = [
            {
                'app_name': 'Visual Studio Code',
                'category': 'productive',
                'start_time': 1704067200,
                'end_time': 1704070800,
                'duration': 3600
            },
            {
                'app_name': 'Firefox',
                'category': 'neutral',
                'start_time': 1704070800,
                'end_time': 1704072600,
                'duration': 1800
            }
        ]
        
        with patch.object(exporter, '_get_sessions_data', return_value=mock_data):
            result = exporter.export_to_csv(output_file)
        
        assert result is True
        assert output_file.exists()
    
    def test_csv_export_content(self, tmp_path):
        """Test that CSV export contains correct data."""
        db_path = Path("/tmp/test.db")
        exporter = DataExporter(db_path)
        
        output_file = tmp_path / "export.csv"
        
        mock_data = [
            {
                'app_name': 'Visual Studio Code',
                'category': 'productive',
                'start_time': 1704067200,
                'end_time': 1704070800,
                'duration': 3600
            }
        ]
        
        with patch.object(exporter, '_get_sessions_data', return_value=mock_data):
            exporter.export_to_csv(output_file)
        
        # Read and verify CSV content
        with open(output_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 1
        assert rows[0]['app_name'] == 'Visual Studio Code'
        assert rows[0]['category'] == 'productive'
        assert rows[0]['duration'] == '3600'
    
    def test_export_to_json_creates_file(self, tmp_path):
        """Test that JSON export creates a file."""
        db_path = Path("/tmp/test.db")
        exporter = DataExporter(db_path)
        
        output_file = tmp_path / "export.json"
        
        mock_data = [
            {
                'app_name': 'Visual Studio Code',
                'category': 'productive',
                'start_time': 1704067200,
                'end_time': 1704070800,
                'duration': 3600
            }
        ]
        
        with patch.object(exporter, '_get_sessions_data', return_value=mock_data):
            result = exporter.export_to_json(output_file)
        
        assert result is True
        assert output_file.exists()
    
    def test_json_export_content(self, tmp_path):
        """Test that JSON export contains correct data."""
        db_path = Path("/tmp/test.db")
        exporter = DataExporter(db_path)
        
        output_file = tmp_path / "export.json"
        
        mock_data = [
            {
                'app_name': 'Firefox',
                'category': 'neutral',
                'start_time': 1704070800,
                'end_time': 1704072600,
                'duration': 1800
            }
        ]
        
        with patch.object(exporter, '_get_sessions_data', return_value=mock_data):
            exporter.export_to_json(output_file)
        
        # Read and verify JSON content
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        assert 'sessions' in data
        assert len(data['sessions']) == 1
        assert data['sessions'][0]['app_name'] == 'Firefox'
        assert data['sessions'][0]['duration'] == 1800
    
    def test_export_with_date_filter(self, tmp_path):
        """Test export with date range filter."""
        db_path = Path("/tmp/test.db")
        exporter = DataExporter(db_path)
        
        output_file = tmp_path / "filtered.csv"
        start_date = 1704067200  # 2024-01-01
        end_date = 1704153600    # 2024-01-02
        
        mock_data = [
            {
                'app_name': 'VS Code',
                'category': 'productive',
                'start_time': 1704067200,
                'end_time': 1704070800,
                'duration': 3600
            }
        ]
        
        with patch.object(exporter, '_get_sessions_data', return_value=mock_data) as mock_get:
            exporter.export_to_csv(output_file, start_date=start_date, end_date=end_date)
            mock_get.assert_called_once_with(start_date, end_date)
    
    def test_backup_database(self, tmp_path):
        """Test database backup functionality."""
        # Create a temporary source database
        source_db = tmp_path / "source.db"
        source_db.write_text("fake database content")
        
        exporter = DataExporter(source_db)
        backup_path = tmp_path / "backup.db"
        
        result = exporter.backup_database(backup_path)
        
        assert result is True
        assert backup_path.exists()
        assert backup_path.read_text() == "fake database content"
    
    def test_restore_database(self, tmp_path):
        """Test database restore functionality."""
        # Create backup file
        backup_db = tmp_path / "backup.db"
        backup_db.write_text("backup content")
        
        # Target database
        target_db = tmp_path / "target.db"
        
        exporter = DataExporter(target_db)
        result = exporter.restore_database(backup_db)
        
        assert result is True
        assert target_db.exists()
        assert target_db.read_text() == "backup content"
    
    def test_export_summary_report(self, tmp_path):
        """Test exporting a summary report."""
        db_path = Path("/tmp/test.db")
        exporter = DataExporter(db_path)
        
        output_file = tmp_path / "summary.json"
        
        mock_summary = {
            'total_time': 7200,
            'productive_time': 5400,
            'neutral_time': 1200,
            'distracting_time': 600,
            'productivity_score': 75,
            'top_apps': [
                {'name': 'VS Code', 'duration': 5400},
                {'name': 'Firefox', 'duration': 1200}
            ]
        }
        
        with patch.object(exporter, '_generate_summary', return_value=mock_summary):
            result = exporter.export_summary(output_file)
        
        assert result is True
        assert output_file.exists()
        
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        assert data['productivity_score'] == 75
        assert data['total_time'] == 7200
    
    def test_anonymize_export(self, tmp_path):
        """Test data anonymization during export."""
        db_path = Path("/tmp/test.db")
        exporter = DataExporter(db_path)
        
        output_file = tmp_path / "anonymous.csv"
        
        mock_data = [
            {
                'app_name': 'Visual Studio Code',
                'category': 'productive',
                'start_time': 1704067200,
                'end_time': 1704070800,
                'duration': 3600
            }
        ]
        
        with patch.object(exporter, '_get_sessions_data', return_value=mock_data):
            with patch.object(exporter, '_anonymize_app_name', return_value='App_001'):
                exporter.export_to_csv(output_file, anonymize=True)
        
        with open(output_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert rows[0]['app_name'] == 'App_001'
    
    def test_export_handles_empty_data(self, tmp_path):
        """Test export handles empty dataset gracefully."""
        db_path = Path("/tmp/test.db")
        exporter = DataExporter(db_path)
        
        output_file = tmp_path / "empty.csv"
        
        with patch.object(exporter, '_get_sessions_data', return_value=[]):
            result = exporter.export_to_csv(output_file)
        
        assert result is True
        assert output_file.exists()
        
        with open(output_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        assert len(rows) == 1  # Only header row
    
    def test_export_handles_invalid_path(self):
        """Test export handles invalid output path."""
        import sys
        db_path = Path("/tmp/test.db")
        exporter = DataExporter(db_path)
        
        # Use platform-specific invalid paths
        if sys.platform == "win32":
            # Windows: Use a reserved name that can't be created
            invalid_path = Path("NUL:/export.csv")
        else:
            # Linux/Unix: Use a path with null byte which is invalid
            invalid_path = Path("/dev/null/not_a_directory/export.csv")
        
        with patch.object(exporter, '_get_sessions_data', return_value=[]):
            result = exporter.export_to_csv(invalid_path)
        
        assert result is False