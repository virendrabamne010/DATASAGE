"""Insights module for DATASAGE."""

from datasage.insights.correlations import CorrelationAnalyzer
from datasage.insights.statistics import StatisticsAnalyzer
from datasage.insights.categories import CategoryAnalyzer
from datasage.insights.trends import TrendAnalyzer

__all__ = [
    "CorrelationAnalyzer",
    "StatisticsAnalyzer",
    "CategoryAnalyzer",
    "TrendAnalyzer",
]
