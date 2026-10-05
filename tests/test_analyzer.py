"""
Unit tests for DATASAGE analyzer module.

Tests for the main Analyzer orchestrator class.
"""

import pytest
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
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


@pytest.fixture
def dirty_df():
    """Create DataFrame with missing values, outliers, and duplicates."""
    np.random.seed(7)
    df = pd.DataFrame({
        'A': np.random.randn(50),
        'B': np.random.randn(50) * 2,
        'C': np.random.choice(['x', 'y', 'z'], 50),
    })
    # Add missing values
    df.loc[0, 'A'] = np.nan
    df.loc[1, 'B'] = np.nan
    # Add outliers
    df.loc[2, 'A'] = 100.0
    df.loc[3, 'B'] = -100.0
    # Add duplicates
    df = pd.concat([df, df.iloc[[4, 5]]], ignore_index=True)
    return df


@pytest.fixture
def categorical_only_df():
    """Create DataFrame with only categorical columns."""
    return pd.DataFrame({
        'Color': ['red', 'blue', 'green', 'red', 'blue'],
        'Size': ['S', 'M', 'L', 'M', 'S'],
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


class TestAnalyzerCleaning:
    """Test Analyzer cleaning edge cases."""
    
    def test_clean_with_missing_and_outliers(self, dirty_df):
        """Test clean handles missing values, outliers, and duplicates."""
        analyzer = Analyzer(dirty_df)
        analyzer.clean()
        
        # Cleaning stats should be recorded
        assert 'shape_before' in analyzer.cleaning_stats
        assert 'shape_after' in analyzer.cleaning_stats
        assert 'outliers_found' in analyzer.cleaning_stats
        assert 'duplicates_removed' in analyzer.cleaning_stats
    
    def test_clean_forward_fill_strategy(self):
        """Test clean with forward_fill missing strategy."""
        df = pd.DataFrame({
            'A': [1.0, np.nan, 3.0, np.nan, 5.0],
            'B': [10, 20, 30, 40, 50],
        })
        analyzer = Analyzer(df)
        analyzer.clean(handle_missing='forward_fill', handle_outliers=False, remove_duplicates=False)
        
        # Forward fill should fill NaN with previous value
        assert analyzer.df['A'].isnull().sum() == 0
        assert analyzer.df['A'].iloc[1] == 1.0
    
    def test_clean_remove_outlier_strategy(self):
        """Test clean with remove outlier strategy."""
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 100],  # 100 is an outlier
            'B': [5, 6, 7, 8, 9],
        })
        analyzer = Analyzer(df)
        analyzer.clean(handle_outliers=True, outlier_strategy='remove', remove_duplicates=False)
        
        # Outlier row should be removed
        assert 100 not in analyzer.df['A'].values
    
    def test_clean_cap_outlier_strategy(self):
        """Test clean with cap outlier strategy."""
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 100],  # 100 is an outlier
            'B': [5, 6, 7, 8, 9],
        })
        analyzer = Analyzer(df)
        analyzer.clean(handle_outliers=True, outlier_strategy='cap', remove_duplicates=False)
        
        # Outlier should be capped, not removed
        assert len(analyzer.df) == 5
        assert analyzer.df['A'].max() < 100
    
    def test_clean_no_outliers(self, sample_df):
        """Test clean when no outliers present."""
        analyzer = Analyzer(sample_df)
        analyzer.clean(handle_outliers=True)
        
        assert 'outliers_found' in analyzer.cleaning_stats


class TestAnalyzerSummarize:
    """Test Analyzer summarize method."""
    
    def test_summarize_returns_expected_keys(self, sample_df):
        """Test summarize returns all expected keys."""
        analyzer = Analyzer(sample_df)
        analyzer.clean()
        analyzer.analyze()
        summary = analyzer.summarize()
        
        assert 'shape' in summary
        assert 'missing_columns' in summary
        assert 'missing_preview' in summary
        assert 'duplicate_rows' in summary
        assert 'outliers' in summary
        assert 'top_correlations' in summary
        assert 'trends' in summary
        assert 'summary_lines' in summary
        assert 'recommendations' in summary
        assert 'cleaning_actions' in summary
    
    def test_summarize_trends_handles_dict(self, sample_df):
        """Test summarize handles trends dict correctly (regression test)."""
        analyzer = Analyzer(sample_df)
        analyzer.clean()
        analyzer.analyze()
        summary = analyzer.summarize()
        
        # trends should be a dict of column -> trend info
        assert isinstance(summary['trends'], dict)
        # summary_lines should not crash and should contain trend info
        assert any('Trend analysis' in line for line in summary['summary_lines'])
    
    def test_summarize_no_crash_on_categorical(self, categorical_only_df):
        """Test summarize doesn't crash on categorical-only data."""
        analyzer = Analyzer(categorical_only_df)
        analyzer.clean(handle_outliers=False, remove_duplicates=False)
        analyzer.analyze()
        summary = analyzer.summarize()
        
        assert 'summary_lines' in summary
        assert 'recommendations' in summary


class TestAnalyzerVisualization:
    """Test Analyzer visualization methods."""
    
    def test_visualize_creates_output(self, sample_df, tmp_path):
        """Test visualize creates output files."""
        analyzer = Analyzer(sample_df)
        analyzer.clean()
        analyzer.visualize(output_dir=str(tmp_path))
        
        # Output directory should contain PNG files
        png_files = list(tmp_path.glob('*.png'))
        assert len(png_files) > 0
        assert analyzer.viz_output_dir == str(tmp_path)
    
    def test_visualize_categorical_only(self, categorical_only_df, tmp_path):
        """Test visualize doesn't crash on categorical-only data."""
        analyzer = Analyzer(categorical_only_df)
        analyzer.clean(handle_outliers=False, remove_duplicates=False)
        analyzer.visualize(output_dir=str(tmp_path))
        
        # Should not crash; output dir may be empty of PNGs
        assert analyzer.viz_output_dir == str(tmp_path)
    
    def test_visualize_returns_self(self, sample_df, tmp_path):
        """Test visualize returns self for chaining."""
        analyzer = Analyzer(sample_df)
        result = analyzer.visualize(output_dir=str(tmp_path))
        assert isinstance(result, Analyzer)


class TestAnalyzerReports:
    """Test Analyzer report generation."""
    
    def test_generate_text_report(self, sample_df, tmp_path):
        """Test text report generation."""
        analyzer = Analyzer(sample_df)
        analyzer.clean()
        analyzer.analyze()
        
        report_path = tmp_path / 'report.txt'
        analyzer.generate_report(str(report_path), format='text')
        
        assert report_path.exists()
        assert report_path.stat().st_size > 0
    
    def test_generate_pdf_report(self, sample_df, tmp_path):
        """Test PDF report generation."""
        analyzer = Analyzer(sample_df)
        analyzer.clean()
        analyzer.analyze()
        
        report_path = tmp_path / 'report.pdf'
        analyzer.generate_report(str(report_path), format='pdf')
        
        assert report_path.exists()
        assert report_path.stat().st_size > 0
    
    def test_generate_pdf_report_with_charts(self, sample_df, tmp_path):
        """Test PDF report with charts included."""
        analyzer = Analyzer(sample_df)
        analyzer.clean()
        analyzer.analyze()
        analyzer.visualize(output_dir=str(tmp_path / 'viz'))
        
        report_path = tmp_path / 'report_with_charts.pdf'
        analyzer.generate_report(str(report_path), format='pdf', include_charts=True)
        
        assert report_path.exists()
        assert report_path.stat().st_size > 0


class TestAnalyzerReset:
    """Test Analyzer reset method."""
    
    def test_reset_restores_original_data(self, dirty_df):
        """Test reset restores original data."""
        analyzer = Analyzer(dirty_df)
        original_shape = analyzer.df.shape
        analyzer.clean()
        
        # After cleaning, shape may differ
        assert analyzer.df.shape != original_shape or analyzer.cleaning_stats
        
        analyzer.reset()
        
        # After reset, data should match original
        assert analyzer.df.shape == original_shape
        assert analyzer.cleaning_stats == {}
    
    def test_reset_returns_self(self, sample_df):
        """Test reset returns self for chaining."""
        analyzer = Analyzer(sample_df)
        result = analyzer.reset()
        assert isinstance(result, Analyzer)