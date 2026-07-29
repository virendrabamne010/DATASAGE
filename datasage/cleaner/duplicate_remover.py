"""
Duplicate removal for DATASAGE.

This module handles duplicate detection and removal
with support for different duplicate matching strategies.
"""

import pandas as pd


class DuplicateRemover:
    """Detect and remove duplicate rows."""
    
    def analyze(self, df: pd.DataFrame, subset: list[str] | None = None) -> dict:
        """
        Analyze duplicates in the dataset.
        
        Args:
            df: Input DataFrame
            subset: Specific columns to check for duplicates
                   If None, checks all columns
        
        Returns:
            dict: Report of duplicates found
        """
        total_duplicates = df.duplicated(subset=subset).sum()
        duplicate_rows = df[df.duplicated(subset=subset, keep=False)]
        
        return {
            'total_duplicates': total_duplicates,
            'duplicate_percentage': (total_duplicates / len(df) * 100) if len(df) > 0 else 0,
            'example_duplicates': duplicate_rows.head(5).to_dict('records') if not duplicate_rows.empty else []
        }
    
    def remove(self, df: pd.DataFrame, subset: list[str] | None = None, 
               keep: str = 'first') -> pd.DataFrame:
        """
        Remove duplicate rows.
        
        Args:
            df: Input DataFrame
            subset: Specific columns to check for duplicates
            keep: Which duplicates to keep
                - 'first': Keep first occurrence
                - 'last': Keep last occurrence
                - False: Remove all duplicates
        
        Returns:
            pd.DataFrame: DataFrame with duplicates removed
        """
        return df.drop_duplicates(subset=subset, keep=keep)
