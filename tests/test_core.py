"""
Unit tests for DATASAGE core module.
"""

import pytest
import pandas as pd
import numpy as np
from datasage.core.utils import (
    validate_dataframe,
    get_numeric_columns,
    get_categorical_columns,
    safe_divide,
    format_percentage,
)
from datasage.core.exceptions import (
    DatasageError,
    InvalidDataError,
    NoDataError,
)


class TestValidateDataframe:
    """Test dataframe validation."""

    def test_valid_dataframe(self):
        df = pd.DataFrame({'A': [1, 2, 3]})
        result = validate_dataframe(df)
        assert isinstance(result, pd.DataFrame)

    def test_invalid_type(self):
        with pytest.raises(InvalidDataError):
            validate_dataframe("not a dataframe")

    def test_empty_dataframe(self):
        with pytest.raises(NoDataError):
            validate_dataframe(pd.DataFrame())

    def test_exception_hierarchy(self):
        assert issubclass(InvalidDataError, DatasageError)
        assert issubclass(NoDataError, DatasageError)


class TestColumnHelpers:
    """Test column helper functions."""

    def test_get_numeric_columns(self):
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [1.5, 2.5, 3.5],
            'C': ['x', 'y', 'z'],
        })
        numeric = get_numeric_columns(df)
        assert 'A' in numeric
        assert 'B' in numeric
        assert 'C' not in numeric

    def test_get_categorical_columns(self):
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': ['x', 'y', 'z'],
            'C': pd.Categorical(['a', 'b', 'a']),
        })
        categorical = get_categorical_columns(df)
        assert 'B' in categorical
        assert 'C' in categorical
        assert 'A' not in categorical


class TestUtilityFunctions:
    """Test utility functions."""

    def test_safe_divide_normal(self):
        assert safe_divide(10, 5) == 2.0

    def test_safe_divide_by_zero(self):
        assert safe_divide(10, 0) == 0.0

    def test_safe_divide_custom_default(self):
        assert safe_divide(10, 0, default=1.0) == 1.0

    def test_format_percentage(self):
        assert format_percentage(0.5) == "50.00%"
        assert format_percentage(0.1234, decimals=1) == "12.3%"


class TestExceptions:
    """Test custom exceptions."""

    def test_datasage_error(self):
        error = DatasageError("Test error")
        assert str(error) == "Test error"

    def test_analyzer_error_types(self):
        from datasage.core.exceptions import (
            AnalysisError,
            VisualizationError,
            ReportError,
        )
        assert issubclass(AnalysisError, DatasageError)
        assert issubclass(VisualizationError, DatasageError)
        assert issubclass(ReportError, DatasageError)