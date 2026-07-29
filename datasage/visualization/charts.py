"""
Auto-generated charts for DATASAGE.

This module creates various chart types automatically
based on data characteristics.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datasage.config import config


class ChartGenerator:
    """Generate various chart types for data visualization."""
    
    def __init__(self, figsize: tuple = config.FIGURE_SIZE, dpi: int = config.DPI):
        """
        Initialize chart generator.
        
        Args:
            figsize: Figure size (width, height)
            dpi: Resolution for saved figures
        """
        self.figsize = figsize
        self.dpi = dpi
        sns.set_style("whitegrid")
    
    def bar_chart(self, data: pd.Series, title: str = "Bar Chart") -> plt.Figure:
        """
        Create a bar chart.
        
        Args:
            data: Series with categorical or numeric data
            title: Chart title
        
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        data.value_counts().head(10).plot(kind='bar', ax=ax, color='steelblue')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Category')
        ax.set_ylabel('Count')
        plt.tight_layout()
        return fig
    
    def line_chart(self, data: pd.Series, title: str = "Line Chart") -> plt.Figure:
        """
        Create a line chart (for time series).
        
        Args:
            data: Series with numeric time series data
            title: Chart title
        
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        data.plot(ax=ax, color='steelblue', linewidth=2)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel('Value')
        plt.tight_layout()
        return fig
    
    def scatter_chart(self, x: pd.Series, y: pd.Series, 
                     title: str = "Scatter Plot") -> plt.Figure:
        """
        Create a scatter plot.
        
        Args:
            x: X-axis data
            y: Y-axis data
            title: Chart title
        
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        ax.scatter(x, y, alpha=0.6, s=50, color='steelblue')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(x.name)
        ax.set_ylabel(y.name)
        plt.tight_layout()
        return fig
    
    def pie_chart(self, data: pd.Series, title: str = "Pie Chart") -> plt.Figure:
        """
        Create a pie chart.
        
        Args:
            data: Series with values to display
            title: Chart title
        
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        data.value_counts().head(8).plot(
            kind='pie', 
            ax=ax, 
            autopct='%1.1f%%',
            colors=sns.color_palette("husl", len(data.value_counts().head(8)))
        )
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel('')
        plt.tight_layout()
        return fig
    
    def save_figure(self, fig: plt.Figure, filepath: str) -> None:
        """
        Save figure to file.
        
        Args:
            fig: Matplotlib figure
            filepath: Where to save (e.g., 'chart.png')
        """
        fig.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
        plt.close(fig)
