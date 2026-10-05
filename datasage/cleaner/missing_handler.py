"""
Missing value handler for DATASAGE.

This module handles various missing value treatment strategies:
- Drop columns with too many missing values
- Drop rows with any missing values
- Fill with mean/median/mode/forward-fill
"""

import pandas as pd
import numpy as np
from typing import Literal
from datasage.config import config


class MissingValueHandler:
    """Handle missing values in DataFrames."""
    
    def __init__(self, threshold: float = config.MISSING_THRESHOLD):
        """
        Initialize the handler.
        
        Args:
            threshold: Drop columns with missing value percentage > threshold
                      (0.0 to 1.0)
        """
        self.threshold = threshold
        self.missing_report = {}
    
    def analyze(self, df: pd.DataFrame) -> dict:
        """
        Analyze missing values in the dataset.
        
        Args:
            df: Input DataFrame
            
        Returns:
            dict: Report of missing values per column
        """
        missing_count = df.isnull().sum()
        missing_percent = (missing_count / len(df) * 100).round(2)
        
        self.missing_report = {
            col: {
                'count': missing_count[col],
                'percentage': missing_percent[col]
            }
            for col in df.columns if missing_count[col] > 0
        }
        
        return self.missing_report
    
    def handle(self, df: pd.DataFrame, 
               strategy: Literal['drop_column', 'drop_row', 'mean', 'median', 'mode', 'forward_fill'] = 'drop_column'
               ) -> pd.DataFrame:
        """
        Handle missing values using specified strategy.
        
        Args:
            df: Input DataFrame
            strategy: How to handle missing values
                - 'drop_column': Remove columns with >threshold missing
                - 'drop_row': Remove rows with any missing values
                - 'mean': Fill numeric with mean
                - 'median': Fill numeric with median
                - 'mode': Fill with most frequent value
                - 'forward_fill': Forward-fill missing values (for time series)
        
        Returns:
            pd.DataFrame: DataFrame with missing values handled
        """
        df = df.copy()
        
        # Analyze first
        self.analyze(df)
        
        if strategy == 'drop_column':
            # Drop columns exceeding threshold
            cols_to_drop = [
                col for col, stats in self.missing_report.items()
                if stats['percentage'] / 100 > self.threshold
            ]
            df = df.drop(columns=cols_to_drop)
            
        elif strategy == 'drop_row':
            # Remove rows with any missing values
            df = df.dropna()
            
        elif strategy == 'mean':
            # Fill numeric columns with mean
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            
        elif strategy == 'median':
            # Fill numeric columns with median
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
            
        elif strategy == 'mode':
            # Fill with most frequent value
            for col in df.columns:
                if df[col].isnull().any():
                    df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else None)
            
        elif strategy == 'forward_fill':
            # Time series forward fill
            df = df.ffill()
        
        return df
