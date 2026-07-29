"""
Unit tests for DATASAGE analyzer module.

Tests for the main Analyzer orchestrator class.
"""

import pytest
import pandas as pd
import numpy as np
from datasage import Analyzer


@pytest.fixture
def sample_df():
    """Create sample DataFrame for testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'Age': np.random.randint(20, 60, 100),
        'Income': np.random.normal(50000, 10000, 100),
        'Score': np.random.uniform(0, 100, 100),
        'Category': np.random.choice(['A', 'B', 'C'], 100),
    })


class TestAnalyzer:
    """Test Analyzer class."""
    
    def test_analyzer_initialization(self, sample_df):
        """Test Analyzer initialization."""
        analyzer = Analyzer(sample_df)
        assert analyzer.df.shape == sample_df.shape
    
    def test_info_method(self, sample_df):
        """Test info method."""
        analyzer = Analyzer(sample_df)
        info = analyzer.info()
        
        assert 'shape' in info
        assert info['shape'] == sample_df.shape
        assert 'columns' in info
    
    def test_clean_method(self, sample_df):
        """Test clean method."""
        analyzer = Analyzer(sample_df)
        result = analyzer.clean()
        
        assert isinstance(result, Analyzer)  # Method chaining
        assert analyzer.cleaning_stats  # Stats recorded
    
    def test_analyze_method(self, sample_df):
        """Test analyze method."""
        analyzer = Analyzer(sample_df)
        analyzer.clean()
        results = analyzer.analyze()
        
        assert 'statistics' in results
        assert 'categories' in results
    
    def test_method_chaining(self, sample_df):
        """Test method chaining."""
        analyzer = Analyzer(sample_df)
        result = analyzer.clean().analyze()
        
        assert isinstance(result, dict)
