"""
Unit tests for DATASAGE report generation.

Verifies PDFReportGenerator can build PDFs when tables contain complex
cell types (lists, numpy arrays, numpy scalars) which previously caused
ReportLab flowable errors.
"""

import os
import tempfile
import numpy as np
import pandas as pd
from datasage.report.pdf_report import PDFReportGenerator


def test_pdf_generator_handles_complex_table_values(tmp_path):
    # Create complex data with lists and numpy arrays
    df = pd.DataFrame({
        'A': [1, 2],
        'B': [[1, 2], [3, 4]],
        'C': [np.array([5, 6]), np.array([7, 8])],
        'D': [np.int64(10), np.int64(20)],
    })

    # Create temporary file path
    tmp_file = tmp_path / "test_report.pdf"

    gen = PDFReportGenerator(str(tmp_file), title="Test Report")
    gen.add_title()
    gen.add_table(df, title="Complex Table")

    # Build should not raise and should produce a file > 0 bytes
    gen.build()

    assert tmp_file.exists()
    assert tmp_file.stat().st_size > 0
