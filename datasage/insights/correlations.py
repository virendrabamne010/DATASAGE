"""
Correlation analysis for DATASAGE.

This module computes and analyzes correlations between
numeric variables using Pearson, Spearman, and Kendall methods.
"""

import pandas as pd
import numpy as np
from typing import Literal
from datasage.config import config


class CorrelationAnalyzer:
    """Analyze correlations between numeric variables."""
    
    def __init__(self, threshold: float = config.CORRELATION_THRESHOLD):
        """
        Initialize the analyzer.
        
        Args:
            threshold: Correlation coefficients above this are "high"
        """
        self.threshold = threshold
        self.correlation_matrix = None
    
    def compute(self, df: pd.DataFrame, 
                method: Literal['pearson', 'spearman', 'kendall'] = 'pearson'
                ) -> pd.DataFrame:
        """
        Compute correlation matrix.
        
        Args:
            df: Input DataFrame (numeric columns)
            method: Correlation method
        
        Returns:
            pd.DataFrame: Correlation matrix
        """
        numeric_df = df.select_dtypes(include=[np.number])
        self.correlation_matrix = numeric_df.corr(method=method)
        return self.correlation_matrix
    
    def find_high_correlations(self) -> list[dict]:
        """
        Find highly correlated variable pairs.
        
        Returns:
            list[dict]: List of high correlation pairs
        """
        if self.correlation_matrix is None:
            raise ValueError("Call compute() first")
        
        high_corr = []
        
        # Get upper triangle to avoid duplicates
        for i in range(len(self.correlation_matrix.columns)):
            for j in range(i + 1, len(self.correlation_matrix.columns)):
                corr_value = self.correlation_matrix.iloc[i, j]
                if abs(corr_value) >= self.threshold:
                    high_corr.append({
                        'variable1': self.correlation_matrix.columns[i],
                        'variable2': self.correlation_matrix.columns[j],
                        'correlation': round(corr_value, 4)
                    })
        
        return sorted(high_corr, key=lambda x: abs(x['correlation']), reverse=True)
