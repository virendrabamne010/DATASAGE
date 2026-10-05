"""
Unit tests for DATASAGE visualization module.
"""

import pytest
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
from datasage.visualization import ChartGenerator, DistributionPlotter, HeatmapGenerator


@pytest.fixture
def sample_df():
    """Create sample DataFrame for testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'A': np.random.randn(100),
        'B': np.random.randn(100) * 2,
        'C': np.random.choice(['X', 'Y', 'Z'], 100),
    })


class TestChartGenerator:
    """Test chart generator."""

    def test_bar_chart(self, sample_df):
        gen = ChartGenerator()
        fig = gen.bar_chart(sample_df['C'])
        assert fig is not None

    def test_line_chart(self, sample_df):
        gen = ChartGenerator()
        fig = gen.line_chart(sample_df['A'])
        assert fig is not None

    def test_scatter_chart(self, sample_df):
        gen = ChartGenerator()
        fig = gen.scatter_chart(sample_df['A'], sample_df['B'])
        assert fig is not None

    def test_pie_chart(self, sample_df):
        gen = ChartGenerator()
        fig = gen.pie_chart(sample_df['C'])
        assert fig is not None

    def test_save_figure(self, sample_df, tmp_path):
        gen = ChartGenerator()
        fig = gen.bar_chart(sample_df['C'])
        out_path = tmp_path / 'test_chart.png'
        gen.save_figure(fig, str(out_path))
        assert out_path.exists()
        assert out_path.stat().st_size > 0


class TestDistributionPlotter:
    """Test distribution plotter."""

    def test_histogram(self, sample_df):
        plotter = DistributionPlotter()
        fig = plotter.histogram(sample_df['A'])
        assert fig is not None

    def test_kde_plot(self, sample_df):
        plotter = DistributionPlotter()
        fig = plotter.kde_plot(sample_df['A'])
        assert fig is not None

    def test_box_plot(self, sample_df):
        plotter = DistributionPlotter()
        fig = plotter.box_plot(sample_df)
        assert fig is not None

    def test_violin_plot(self, sample_df):
        plotter = DistributionPlotter()
        fig = plotter.violin_plot(sample_df)
        assert fig is not None


class TestHeatmapGenerator:
    """Test heatmap generator."""

    def test_correlation_heatmap(self, sample_df):
        gen = HeatmapGenerator()
        fig = gen.correlation_heatmap(sample_df)
        assert fig is not None

    def test_missing_value_heatmap(self, sample_df):
        gen = HeatmapGenerator()
        fig = gen.missing_value_heatmap(sample_df)
        assert fig is not None