"""
Correlation heatmaps for DATASAGE.

This module creates heatmap visualizations of correlations
between numeric variables.
"""

import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datasage.config import config


class HeatmapGenerator:
    """Generate heatmap visualizations."""
    
    def __init__(self, figsize: tuple = config.FIGURE_SIZE, dpi: int = config.DPI):
        """
        Initialize heatmap generator.
        
        Args:
            figsize: Figure size (width, height)
            dpi: Resolution
        """
        self.figsize = figsize
        self.dpi = dpi
        sns.set_style("whitegrid")
    
    def correlation_heatmap(self, df: pd.DataFrame, 
                           title: str = "Correlation Heatmap") -> plt.Figure:
        """
        Create correlation heatmap for all numeric columns.
        
        Args:
            df: Input DataFrame
            title: Chart title
        
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        # Get numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        # Compute correlation
        corr = numeric_df.corr()
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        with warnings.catch_warnings():
            # Suppress seaborn's internal cmap.set_bad deprecation warning
            warnings.filterwarnings(
                "ignore",
                message="The set_bad function will be deprecated",
                category=PendingDeprecationWarning,
            )
            sns.heatmap(
                corr,
                annot=True,  # Show correlation values
                fmt='.2f',   # 2 decimal places
                cmap='coolwarm',
                center=0,
                square=True,
                linewidths=1,
                cbar_kws={"shrink": 0.8},
                ax=ax
            )
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        return fig
    
    def missing_value_heatmap(self, df: pd.DataFrame, 
                             title: str = "Missing Values Heatmap") -> plt.Figure:
        """
        Create heatmap showing missing values in dataset.
        
        Args:
            df: Input DataFrame
            title: Chart title
        
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        # Create binary matrix: 1 = missing, 0 = present
        missing_matrix = df.isnull().astype(int)
        
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        with warnings.catch_warnings():
            # Suppress seaborn's internal cmap.set_bad deprecation warning
            warnings.filterwarnings(
                "ignore",
                message="The set_bad function will be deprecated",
                category=PendingDeprecationWarning,
            )
            sns.heatmap(
                missing_matrix,
                cbar=True,
                cmap='RdYlGn_r',
                yticklabels=False,
                ax=ax
            )
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Columns')
        plt.tight_layout()
        return fig
    
    def save_figure(self, fig: plt.Figure, filepath: str) -> None:
        """Save figure to file."""
        fig.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
        plt.close(fig)
