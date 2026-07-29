"""
Custom exceptions for DATASAGE.

These exceptions provide clear error messages for common issues
and help users debug their code more easily.
"""


class DatasageError(Exception):
    """Base exception for all DATASAGE errors."""
    pass


class InvalidDataError(DatasageError):
    """Raised when input data is invalid or incompatible."""
    pass


class NoDataError(DatasageError):
    """Raised when no data is provided to analyze."""
    pass


class AnalysisError(DatasageError):
    """Raised when analysis operations fail."""
    pass


class VisualizationError(DatasageError):
    """Raised when visualization creation fails."""
    pass


class ReportError(DatasageError):
    """Raised when report generation fails."""
    pass
