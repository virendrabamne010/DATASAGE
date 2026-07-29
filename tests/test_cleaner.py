"""
Unit tests for DATASAGE cleaner module.

Tests for missing value handling, outlier detection, and duplicate removal.
"""

import pytest
import pandas as pd
import numpy as np
from datasage.cleaner import MissingValueHandler, OutlierDetector, DuplicateRemover


class TestMissingValueHandler:
    """Test missing value handling."""
    
    @pytest.fixture
    def df_with_missing(self):
        """Create DataFrame with missing values."""
        return pd.DataFrame({
            'A': [1, 2, np.nan, 4],
            'B': [5, np.nan, np.nan, 8],
            'C': [9, 10, 11, 12],
        })
    
    def test_missing_analysis(self, df_with_missing):
        """Test missing value analysis."""
        handler = MissingValueHandler()
        report = handler.analyze(df_with_missing)
        
        assert 'A' in report
        assert 'B' in report
        assert report['A']['count'] == 1
        assert report['B']['count'] == 2
    
    def test_drop_row_strategy(self, df_with_missing):
        """Test drop row strategy."""
        handler = MissingValueHandler()
        result = handler.handle(df_with_missing, strategy='drop_row')
        
        assert len(result) == 2
        assert result.isnull().sum().sum() == 0


class TestOutlierDetector:
    """Test outlier detection."""
    
    @pytest.fixture
    def df_with_outliers(self):
        """Create DataFrame with outliers."""
        return pd.DataFrame({
            'Normal': [1, 2, 3, 4, 5, 100],  # 100 is outlier
            'Data': [10, 12, 11, 13, 12, 14],
        })
    
    def test_outlier_detection(self, df_with_outliers):
        """Test outlier detection."""
        detector = OutlierDetector(method='iqr')
        report = detector.detect(df_with_outliers)
        
        assert len(report) > 0


class TestDuplicateRemover:
    """Test duplicate removal."""
    
    @pytest.fixture
    def df_with_duplicates(self):
        """Create DataFrame with duplicates."""
        return pd.DataFrame({
            'A': [1, 1, 2, 3],
            'B': [4, 4, 5, 6],
        })
    
    def test_duplicate_analysis(self, df_with_duplicates):
        """Test duplicate analysis."""
        remover = DuplicateRemover()
        report = remover.analyze(df_with_duplicates)
        
        assert report['total_duplicates'] == 1
    
    def test_remove_duplicates(self, df_with_duplicates):
        """Test duplicate removal."""
        remover = DuplicateRemover()
        result = remover.remove(df_with_duplicates)
        
        assert len(result) == 3
