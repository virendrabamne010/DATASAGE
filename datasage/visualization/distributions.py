"""
Distribution plots for DATASAGE.

This module creates distribution visualizations:
- Histograms
- KDE plots
- Box plots
- Violin plots
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datasage.config import config


class DistributionPlotter:
    """Generate distribution plots for numeric data."""
    
    def __init__(self, figsize: tuple = config.FIGURE_SIZE, dpi: int = config.DPI):
        """
        Initialize distribution plotter.
        
        Args:
            figsize: Figure size (width, height)
            dpi: Resolution
        """
        self.figsize = figsize
        self.dpi = dpi
        sns.set_style("whitegrid")
    
    def histogram(self, data: pd.Series, bins: int = 30, 
                 title: str = "Distribution") -> plt.Figure:
        """
        Create a histogram.
        
        Args:
            data: Numeric series
            bins: Number of bins
            title: Chart title
        
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        ax.hist(data.dropna(), bins=bins, color='steelblue', edgecolor='black', alpha=0.7)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(data.name)
        ax.set_ylabel('Frequency')
        plt.tight_layout()
        return fig
    
    def kde_plot(self, data: pd.Series, title: str = "Density Plot") -> plt.Figure:
        """
        Create a KDE (kernel density estimation) plot.
        
        Args:
            data: Numeric series
            title: Chart title
        
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        data.dropna().plot(kind='density', ax=ax, linewidth=2, color='steelblue')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(data.name)
        plt.tight_layout()
        return fig
    
    def box_plot(self, df: pd.DataFrame, title: str = "Box Plot") -> plt.Figure:
        """
        Create a box plot for multiple numeric columns.
        
        Args:
            df: DataFrame with numeric columns
            title: Chart title
        
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        numeric_df = df.select_dtypes(include=[np.number])
        numeric_df.plot(kind='box', ax=ax)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel('Value')
        plt.tight_layout()
        return fig
    
    def violin_plot(self, df: pd.DataFrame, title: str = "Violin Plot") -> plt.Figure:
        """
        Create a violin plot for multiple numeric columns.
        
        Args:
            df: DataFrame with numeric columns
            title: Chart title
        
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        numeric_df = df.select_dtypes(include=[np.number])
        
        # Prepare data for violin plot
        data_dict = {col: numeric_df[col].dropna().values for col in numeric_df.columns}
        positions = range(len(data_dict))
        ax.violinplot(data_dict.values(), positions=positions, showmeans=True)
        
        ax.set_xticks(positions)
        ax.set_xticklabels(data_dict.keys(), rotation=45)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel('Value')
        plt.tight_layout()
        return fig
    
    def save_figure(self, fig: plt.Figure, filepath: str) -> None:
        """Save figure to file."""
        fig.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
        plt.close(fig)
