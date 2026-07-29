"""
Outlier detection for DATASAGE.

This module detects outliers using two methods:
- IQR (Interquartile Range) method
- Z-score method
"""

import pandas as pd
import numpy as np
from typing import Literal
from datasage.config import config


class OutlierDetector:
    """Detect and handle outliers in numerical data."""
    
    def __init__(self, method: Literal['iqr', 'zscore'] = config.OUTLIER_METHOD):
        """
        Initialize the detector.
        
        Args:
            method: 'iqr' or 'zscore'
        """
        self.method = method
        self.outlier_bounds = {}
        self.outlier_indices = set()
    
    def detect(self, df: pd.DataFrame) -> dict:
        """
        Detect outliers in numeric columns.
        
        Args:
            df: Input DataFrame
            
        Returns:
            dict: Report of outliers found (column: count)
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        outlier_report = {}
        
        for col in numeric_cols:
            if self.method == 'iqr':
                bounds = self._iqr_bounds(df[col])
            else:  # zscore
                bounds = self._zscore_bounds(df[col])
            
            self.outlier_bounds[col] = bounds
            
            # Find outlier indices
            outliers = (df[col] < bounds['lower']) | (df[col] > bounds['upper'])
            outlier_count = outliers.sum()
            
            if outlier_count > 0:
                outlier_report[col] = outlier_count
                self.outlier_indices.update(df[outliers].index.tolist())
        
        return outlier_report
    
    def _iqr_bounds(self, series: pd.Series) -> dict:
        """Calculate IQR-based bounds."""
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - config.IQR_MULTIPLIER * IQR
        upper = Q3 + config.IQR_MULTIPLIER * IQR
        return {'lower': lower, 'upper': upper}
    
    def _zscore_bounds(self, series: pd.Series) -> dict:
        """Calculate Z-score-based bounds."""
        mean = series.mean()
        std = series.std()
        threshold = config.ZSCORE_THRESHOLD
        lower = mean - threshold * std
        upper = mean + threshold * std
        return {'lower': lower, 'upper': upper}
    
    def remove_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove rows containing outliers.
        
        Args:
            df: Input DataFrame
            
        Returns:
            pd.DataFrame: DataFrame with outlier rows removed
        """
        self.detect(df)
        return df.drop(index=self.outlier_indices)
    
    def cap_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cap outliers to bounds instead of removing rows.
        
        Args:
            df: Input DataFrame
            
        Returns:
            pd.DataFrame: DataFrame with outliers capped
        """
        self.detect(df)
        df = df.copy()
        
        for col, bounds in self.outlier_bounds.items():
            df[col] = df[col].clip(lower=bounds['lower'], upper=bounds['upper'])
        
        return df
