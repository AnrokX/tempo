"""
Unit tests for Export functionality.
Following TDD: Red-Green-Refactor cycle.
"""
import pytest
import csv
import json
from pathlib import Path
import tempfile
import time
from datetime import datetime


class TestExporter:
    """Test suite for Exporter class."""
    
    def test_exporter_can_be_initialized(self):
        """Test that Exporter can be created."""
        from src.core.export import Exporter
        
        exporter = Exporter()
        
        assert exporter is not None
    
    def test_exporter_exports_sessions_to_csv(self, temp_database):
        """Test exporting sessions data to CSV format."""
        from src.core.export import Exporter
        from src.core.database import Database
        
        # Arrange - Set up test data
        db = Database(temp_database)
        db.initialize()
        
        # Add some test sessions
        app_id = db.save_application("firefox", "neutral")
        now = time.time()
        db.save_session(app_id, now - 3600, now - 3000)
        db.save_session(app_id, now - 2000, now - 1000)
        
        exporter = Exporter(db)
        
        # Act - Export to CSV
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as tmp:
            csv_path = Path(tmp.name)
        
        result = exporter.export_to_csv(csv_path, now - 4000, now)
        
        # Assert - Verify the CSV was created and has correct data
        assert result is True
        assert csv_path.exists()
        
        # Read and verify CSV contents
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            assert len(rows) == 2
            assert 'app_name' in rows[0]
            assert 'category' in rows[0]
            assert 'start_time' in rows[0]
            assert 'end_time' in rows[0]
            assert 'duration' in rows[0]
            
            assert rows[0]['app_name'] == 'firefox'
            assert rows[0]['category'] == 'neutral'
        
        # Cleanup
        csv_path.unlink()
    
    def test_exporter_handles_empty_data_csv(self, temp_database):
        """Test CSV export with no sessions returns empty file with headers."""
        from src.core.export import Exporter
        from src.core.database import Database
        
        # Arrange
        db = Database(temp_database)
        db.initialize()
        exporter = Exporter(db)
        
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as tmp:
            csv_path = Path(tmp.name)
        
        # Act
        now = time.time()
        result = exporter.export_to_csv(csv_path, now - 3600, now)
        
        # Assert
        assert result is True
        assert csv_path.exists()
        
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 0  # No data rows
            assert reader.fieldnames is not None  # But headers exist
        
        # Cleanup
        csv_path.unlink()
    
    def test_exporter_formats_csv_timestamps_correctly(self, temp_database):
        """Test that timestamps in CSV export are human-readable."""
        from src.core.export import Exporter
        from src.core.database import Database
        
        # Arrange
        db = Database(temp_database)
        db.initialize()
        
        app_id = db.save_application("vscode", "productive")
        start_time = 1640995200.0  # Known timestamp: 2022-01-01 00:00:00 UTC
        end_time = start_time + 3600  # 1 hour later
        db.save_session(app_id, start_time, end_time)
        
        exporter = Exporter(db)
        
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as tmp:
            csv_path = Path(tmp.name)
        
        # Act
        result = exporter.export_to_csv(csv_path, start_time - 100, end_time + 100)
        
        # Assert
        assert result is True
        
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            row = next(reader)
            
            # Check that timestamps are formatted as readable dates
            assert '2022-01-01' in row['start_time']
            assert '2022-01-01' in row['end_time']
            assert row['duration'] == '3600.0'  # Should be in seconds
        
        # Cleanup
        csv_path.unlink()