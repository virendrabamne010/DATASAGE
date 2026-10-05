"""
Unit tests for DATASAGE insights module.
"""

import pytest
import pandas as pd
import numpy as np
from datasage.insights import (
    StatisticsAnalyzer,
    CorrelationAnalyzer,
    CategoryAnalyzer,
    TrendAnalyzer,
)


@pytest.fixture
def sample_df():
    """Create sample DataFrame for testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'A': np.random.randn(100),
        'B': np.random.randn(100) * 2,
        'C': np.random.choice(['X', 'Y', 'Z'], 100),
        'D': pd.date_range('2024-01-01', periods=100),
    })


class TestStatisticsAnalyzer:
    """Test statistics analyzer."""

    def test_analyze_returns_stats(self, sample_df):
        stats = StatisticsAnalyzer().analyze(sample_df)
        assert 'A' in stats
        assert 'B' in stats
        assert 'count' in stats['A']
        assert 'mean' in stats['A']
        assert 'median' in stats['A']

    def test_analyze_skips_non_numeric(self, sample_df):
        stats = StatisticsAnalyzer().analyze(sample_df)
        assert 'C' not in stats
        assert 'D' not in stats

    def test_describe_returns_dataframe(self, sample_df):
        result = StatisticsAnalyzer().describe(sample_df)
        assert isinstance(result, pd.DataFrame)


class TestCorrelationAnalyzer:
    """Test correlation analyzer."""

    def test_compute_correlation(self, sample_df):
        corr = CorrelationAnalyzer()
        matrix = corr.compute(sample_df)
        assert isinstance(matrix, pd.DataFrame)

    def test_find_high_correlations(self, sample_df):
        corr = CorrelationAnalyzer(threshold=0.5)
        corr.compute(sample_df)
        high = corr.find_high_correlations()
        assert isinstance(high, list)

    def test_find_high_correlations_requires_compute(self):
        corr = CorrelationAnalyzer()
        with pytest.raises(ValueError):
            corr.find_high_correlations()


class TestCategoryAnalyzer:
    """Test category analyzer."""

    def test_get_top_categories(self, sample_df):
        cat = CategoryAnalyzer(top_n=2)
        result = cat.get_top_categories(sample_df)
        assert 'C' in result
        assert result['C']['total_unique'] == 3

    def test_get_diversity(self, sample_df):
        cat = CategoryAnalyzer()
        result = cat.get_diversity(sample_df)
        assert 'C' in result
        assert 'unique_values' in result['C']
        assert result['C']['unique_values'] == 3


class TestTrendAnalyzer:
    """Test trend analyzer."""

    def test_detect_increasing_trend(self):
        series = pd.Series(np.arange(1, 50))
        trend = TrendAnalyzer()
        result = trend.detect_trend(series)
        assert result['trend'] == 'increasing'
        assert bool(result['significant']) is True

    def test_detect_decreasing_trend(self):
        series = pd.Series(np.arange(50, 1, -1))
        trend = TrendAnalyzer()
        result = trend.detect_trend(series)
        assert result['trend'] == 'decreasing'

    def test_detect_trend_insufficient_data(self):
        trend = TrendAnalyzer()
        result = trend.detect_trend(pd.Series([1]))
        assert result['trend'] == 'insufficient_data'

    def test_calculate_growth_rate(self):
        series = pd.Series([100, 110, 121])
        trend = TrendAnalyzer()
        result = trend.calculate_growth_rate(series)
        assert 'mean_growth_rate' in result
        assert 'total_change' in result

    def test_detect_trends_in_columns(self, sample_df):
        trend = TrendAnalyzer()
        result = trend.detect_trends_in_columns(sample_df)
        assert 'A' in result
        assert 'B' in result