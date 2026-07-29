"""Test package initialization."""

import pytest
from datasage import Analyzer, MissingValueHandler, CorrelationAnalyzer


def test_imports():
    """Test that main classes can be imported."""
    assert Analyzer is not None
    assert MissingValueHandler is not None
    assert CorrelationAnalyzer is not None
