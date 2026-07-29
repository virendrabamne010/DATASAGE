"""
Global configuration for DATASAGE.

This module contains default settings and constants used across
the entire library. Easily customizable for different use cases.
"""

from dataclasses import dataclass
from typing import Literal

@dataclass
class Config:
    """Central configuration class."""
    
    # Data Cleaning defaults
    MISSING_THRESHOLD: float = 0.5  # Drop columns with >50% missing values
    OUTLIER_METHOD: Literal["iqr", "zscore"] = "iqr"  # IQR or Z-score detection
    IQR_MULTIPLIER: float = 1.5  # Multiplier for IQR outlier detection
    ZSCORE_THRESHOLD: float = 3.0  # Z-score threshold (values > 3 are outliers)
    
    # Insights defaults
    CORRELATION_THRESHOLD: float = 0.7  # High correlation cutoff
    TOP_CATEGORIES_COUNT: int = 5  # Show top N categories
    
    # Visualization defaults
    FIGURE_SIZE: tuple = (12, 6)  # Default figure size (width, height)
    STYLE: str = "seaborn-v0_8-darkgrid"  # Matplotlib style
    DPI: int = 100  # Resolution for saved figures
    
    # Report defaults
    REPORT_INCLUDE_PLOTS: bool = True
    PDF_FONT_SIZE: int = 10


# Global config instance
config = Config()
