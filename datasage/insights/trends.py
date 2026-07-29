"""
Trend detection for DATASAGE.

This module detects trends in time series or sequential data:
- Increasing/decreasing trends
- Seasonality detection
- Growth rates
"""

import pandas as pd
import numpy as np
from scipy import stats


class TrendAnalyzer:
    """Detect trends in numeric sequences."""
    
    def detect_trend(self, series: pd.Series) -> dict:
        """
        Detect if a series has a significant trend.
        
        Args:
            series: Time series or sequential numeric data
        
        Returns:
            dict: Trend analysis results
        """
        # Remove NaN values
        series = series.dropna()
        
        if len(series) < 2:
            return {'trend': 'insufficient_data', 'slope': None, 'p_value': None}
        
        # Calculate linear regression
        x = np.arange(len(series))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, series.values)
        
        # Determine trend direction
        if p_value < 0.05:  # Statistically significant
            if slope > 0:
                trend = 'increasing'
            elif slope < 0:
                trend = 'decreasing'
            else:
                trend = 'flat'
        else:
            trend = 'no_significant_trend'
        
        return {
            'trend': trend,
            'slope': round(slope, 4),
            'r_squared': round(r_value ** 2, 4),
            'p_value': round(p_value, 4),
            'significant': p_value < 0.05
        }
    
    def detect_trends_in_columns(self, df: pd.DataFrame) -> dict:
        """
        Detect trends for all numeric columns.
        
        Args:
            df: Input DataFrame
        
        Returns:
            dict: Trends per column
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        trends = {}
        for col in numeric_cols:
            trends[col] = self.detect_trend(df[col])
        
        return trends
    
    def calculate_growth_rate(self, series: pd.Series) -> dict:
        """
        Calculate growth rate statistics.
        
        Args:
            series: Time series data
        
        Returns:
            dict: Growth rate metrics
        """
        series = series.dropna()
        
        if len(series) < 2:
            return {'error': 'insufficient_data'}
        
        # Calculate period-over-period growth
        pct_change = series.pct_change()
        
        return {
            'mean_growth_rate': round(pct_change.mean(), 4),
            'median_growth_rate': round(pct_change.median(), 4),
            'growth_volatility': round(pct_change.std(), 4),
            'total_change': round((series.iloc[-1] - series.iloc[0]) / series.iloc[0], 4)
        }
