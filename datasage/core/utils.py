"""
Utility functions for DATASAGE.

This module contains helper functions used across the library,
including type checking, data validation, and common operations.
"""

from typing import Any, Union
import pandas as pd
import numpy as np
from datasage.core.exceptions import InvalidDataError, NoDataError


def validate_dataframe(df: Any) -> pd.DataFrame:
    """
    Validate that input is a valid pandas DataFrame.
    
    Args:
        df: Input data (should be pandas DataFrame)
        
    Returns:
        pd.DataFrame: The validated dataframe
        
    Raises:
        InvalidDataError: If input is not a DataFrame
        NoDataError: If DataFrame is empty
    """
    if not isinstance(df, pd.DataFrame):
        raise InvalidDataError(
            f"Expected pandas DataFrame, got {type(df).__name__}. "
            "Please convert your data to a DataFrame first."
        )
    
    if df.empty:
        raise NoDataError("DataFrame is empty. Please provide data to analyze.")
    
    return df


def get_numeric_columns(df: pd.DataFrame) -> list[str]:
    """
    Get list of numeric column names.
    
    Args:
        df: Input DataFrame
        
    Returns:
        list[str]: Names of numeric columns
    """
    return df.select_dtypes(include=[np.number]).columns.tolist()


def get_categorical_columns(df: pd.DataFrame) -> list[str]:
    """
    Get list of categorical column names.
    
    Args:
        df: Input DataFrame
        
    Returns:
        list[str]: Names of categorical columns
    """
    return df.select_dtypes(include=['object', 'category']).columns.tolist()


def safe_divide(numerator: Union[int, float], denominator: Union[int, float], 
                default: float = 0.0) -> float:
    """
    Safely divide two numbers, avoiding division by zero.
    
    Args:
        numerator: Number to divide
        denominator: Number to divide by
        default: Value to return if denominator is 0
        
    Returns:
        float: Result of division or default value
    """
    return numerator / denominator if denominator != 0 else default


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format a float as a percentage string.
    
    Args:
        value: Number between 0 and 1
        decimals: Number of decimal places
        
    Returns:
        str: Formatted percentage (e.g., "45.32%")
    """
    return f"{value * 100:.{decimals}f}%"
