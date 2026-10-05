"""
Unit tests for DATASAGE report generation.
"""

import os
import tempfile
import pytest
import numpy as np
import pandas as pd
from datasage.report.text_report import TextReportGenerator
from datasage.report.pdf_report import PDFReportGenerator


class TestTextReportGenerator:
    """Test text report generator."""

    def test_add_header(self):
        report = TextReportGenerator()
        report.add_header("Test Header", level=1)
        content = report.generate()
        assert "TEST HEADER" in content.upper()

    def test_add_paragraph(self):
        report = TextReportGenerator()
        report.add_paragraph("Hello World")
        content = report.generate()
        assert "Hello World" in content

    def test_add_table(self):
        report = TextReportGenerator()
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        report.add_table(df, title="Test Table")
        content = report.generate()
        assert "Test Table" in content

    def test_add_key_value_table(self):
        report = TextReportGenerator()
        report.add_key_value_table({'key1': 'value1'})
        content = report.generate()
        assert "key1" in content
        assert "value1" in content

    def test_add_divider(self):
        report = TextReportGenerator()
        report.add_divider()
        content = report.generate()
        assert "*" * 60 in content

    def test_save_to_file(self, tmp_path):
        report = TextReportGenerator()
        report.add_header("Test", level=1)
        out_path = tmp_path / 'test_report.txt'
        report.save(str(out_path))
        assert out_path.exists()
        assert out_path.stat().st_size > 0

    def test_generate_returns_string(self):
        report = TextReportGenerator()
        result = report.generate()
        assert isinstance(result, str)
        assert "DATA ANALYSIS REPORT" in result.upper()


class TestPDFReportGenerator:
    """Test PDF report generator."""

    def test_pdf_generator_handles_complex_table_values(self, tmp_path):
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

    def test_pdf_with_heading_and_paragraph(self, tmp_path):
        tmp_file = tmp_path / "test_heading.pdf"
        gen = PDFReportGenerator(str(tmp_file), title="Test Report")
        gen.add_title()
        gen.add_heading("Section One")
        gen.add_paragraph("This is test content.")
        gen.build()
        assert tmp_file.exists()
        assert tmp_file.stat().st_size > 0

    def test_pdf_with_image(self, tmp_path):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        # Create a test image
        img_path = tmp_path / "test_image.png"
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [4, 5, 6])
        fig.savefig(img_path)
        plt.close(fig)

        # Create PDF with image
        tmp_file = tmp_path / "test_image.pdf"
        gen = PDFReportGenerator(str(tmp_file), title="Test Report")
        gen.add_title()
        gen.add_image(str(img_path))
        gen.build()
        assert tmp_file.exists()
        assert tmp_file.stat().st_size > 0

    def test_pdf_with_page_break(self, tmp_path):
        tmp_file = tmp_path / "test_pagebreak.pdf"
        gen = PDFReportGenerator(str(tmp_file))
        gen.add_heading("Page 1")
        gen.add_page_break()
        gen.add_heading("Page 2")
        gen.build()
        assert tmp_file.exists()
        assert tmp_file.stat().st_size > 0