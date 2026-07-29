"""
Category analysis for DATASAGE.

This module analyzes categorical variables:
- Value counts
- Top categories
- Category distributions
"""

import pandas as pd
from datasage.config import config


class CategoryAnalyzer:
    """Analyze categorical variables."""
    
    def __init__(self, top_n: int = config.TOP_CATEGORIES_COUNT):
        """
        Initialize the analyzer.
        
        Args:
            top_n: Number of top categories to report
        """
        self.top_n = top_n
    
    def get_top_categories(self, df: pd.DataFrame) -> dict:
        """
        Get top categories for all categorical columns.
        
        Args:
            df: Input DataFrame
        
        Returns:
            dict: Top categories per column
        """
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        
        results = {}
        for col in categorical_cols:
            value_counts = df[col].value_counts()
            top = value_counts.head(self.top_n)
            
            results[col] = {
                'total_unique': df[col].nunique(),
                'top_categories': top.to_dict(),
                'top_percentages': (top / len(df) * 100).round(2).to_dict()
            }
        
        return results
    
    def get_diversity(self, df: pd.DataFrame) -> dict:
        """
        Calculate diversity metrics for categorical columns.
        
        Args:
            df: Input DataFrame
        
        Returns:
            dict: Diversity metrics
        """
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        
        results = {}
        for col in categorical_cols:
            unique_count = df[col].nunique()
            diversity_ratio = unique_count / len(df)
            results[col] = {
                'unique_values': unique_count,
                'diversity_ratio': round(diversity_ratio, 4),
                'coverage': f"{unique_count} out of {len(df)} rows"
            }
        
        return results
