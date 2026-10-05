"""
DATASAGE - Automated Data Analytics Library

A production-ready Python library that automatically analyzes datasets,
generates insights, creates visualizations, and produces reports.

Quick Start:
    >>> import pandas as pd
    >>> from datasage import Analyzer
    >>> 
    >>> df = pd.read_csv('data.csv')
    >>> analyzer = Analyzer(df)
    >>> analyzer.clean()
    >>> analyzer.analyze()
    >>> analyzer.visualize()
    >>> analyzer.generate_report('report.pdf')

Documentation: https://github.com/virendravijaybamne/datasage
License: MIT
"""

from datasage.version import __version__, __author__, __license__
from datasage.core.analyzer import Analyzer
from datasage.cleaner import MissingValueHandler, OutlierDetector, DuplicateRemover
from datasage.insights import CorrelationAnalyzer, StatisticsAnalyzer, CategoryAnalyzer, TrendAnalyzer
from datasage.visualization import ChartGenerator, DistributionPlotter, HeatmapGenerator
from datasage.report import TextReportGenerator, PDFReportGenerator

__all__ = [
    # Main API
    "Analyzer",
    
    # Cleaner modules
    "MissingValueHandler",
    "OutlierDetector",
    "DuplicateRemover",
    
    # Insight modules
    "CorrelationAnalyzer",
    "StatisticsAnalyzer",
    "CategoryAnalyzer",
    "TrendAnalyzer",
    
    # Visualization modules
    "ChartGenerator",
    "DistributionPlotter",
    "HeatmapGenerator",
    
    # Report modules
    "TextReportGenerator",
    "PDFReportGenerator",
    
    # Version info
    "__version__",
    "__author__",
    "__license__",
]