"""
Summary statistics for DATASAGE.

This module computes comprehensive statistical summaries
including mean, median, std, min, max, quartiles, and skewness.
"""

import pandas as pd
import numpy as np


class StatisticsAnalyzer:
    """Generate summary statistics for the dataset."""
    
    def analyze(self, df: pd.DataFrame) -> dict:
        """
        Generate comprehensive statistics for all numeric columns.
        
        Args:
            df: Input DataFrame
        
        Returns:
            dict: Summary statistics per column
        """
        numeric_df = df.select_dtypes(include=[np.number])
        
        stats = {}
        for col in numeric_df.columns:
            stats[col] = self._column_stats(numeric_df[col])
        
        return stats
    
    def _column_stats(self, series: pd.Series) -> dict:
        """Calculate statistics for a single column."""
        return {
            'count': int(series.count()),
            'mean': round(series.mean(), 4),
            'median': round(series.median(), 4),
            'std': round(series.std(), 4),
            'min': round(series.min(), 4),
            'max': round(series.max(), 4),
            'q25': round(series.quantile(0.25), 4),
            'q75': round(series.quantile(0.75), 4),
            'skewness': round(series.skew(), 4),
            'kurtosis': round(series.kurtosis(), 4),
        }
    
    def describe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get pandas describe() output formatted nicely.
        
        Args:
            df: Input DataFrame
        
        Returns:
            pd.DataFrame: Statistical summary
        """
        return df.describe().round(4)
