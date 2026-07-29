"""
PDF report generation for DATASAGE.

This module generates professional PDF reports
using ReportLab for pure Python handling.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from io import BytesIO
from typing import Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors


class PDFReportGenerator:
    """Generate professional PDF reports."""
    
    def __init__(self, filename: str, title: str = "Data Analysis Report"):
        """
        Initialize PDF report generator.
        
        Args:
            filename: Output PDF filename
            title: Report title
        """
        self.filename = filename
        self.title = title
        self.document = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
        )
        self.story = []
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()
    
    def _add_custom_styles(self) -> None:
        """Add custom paragraph styles."""
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        self.styles.add(title_style)
        
        heading2_style = ParagraphStyle(
            'CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        self.styles.add(heading2_style)
    
    def add_title(self) -> None:
        """Add report title and metadata."""
        self.story.append(Paragraph(self.title, self.styles['CustomTitle']))
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.story.append(Paragraph(f"Generated: {timestamp}", self.styles['Normal']))
        self.story.append(Spacer(1, 0.3*inch))
    
    def add_heading(self, text: str, level: int = 2) -> None:
        """
        Add section heading.
        
        Args:
            text: Heading text
            level: Heading level (1 or 2)
        """
        if level == 1:
            self.story.append(Paragraph(text, self.styles['Heading1']))
        else:
            self.story.append(Paragraph(text, self.styles['CustomHeading2']))
        self.story.append(Spacer(1, 0.2*inch))
    
    def add_paragraph(self, text: str) -> None:
        """Add paragraph text."""
        self.story.append(Paragraph(text, self.styles['Normal']))
        self.story.append(Spacer(1, 0.1*inch))
    
    def add_table(self, data: pd.DataFrame | dict, title: str = "", 
                  col_widths: Optional[list] = None) -> None:
        """
        Add table to PDF.
        
        Args:
            data: DataFrame or dict with table data
            title: Table title
            col_widths: Column widths (optional)
        """
        if isinstance(data, dict):
            data = pd.DataFrame([data])
        
        if title:
            self.add_heading(title, level=2)
        
        # Convert DataFrame to list of lists
        table_data = [data.columns.tolist()] + data.values.tolist()

        # Sanitize cell values: ReportLab treats sequences as flowable lists
        # which causes errors for plain tuples/lists/dicts/ndarrays. Convert
        # such values to strings and convert numpy scalar types to native.
        sanitized = []
        for row in table_data:
            new_row = []
            for cell in row:
                if isinstance(cell, (list, tuple, dict, pd.Series, np.ndarray)):
                    new_row.append(str(cell))
                elif isinstance(cell, (np.integer, np.floating, np.bool_)):
                    new_row.append(cell.item())
                else:
                    new_row.append(cell)
            sanitized.append(new_row)
        table_data = sanitized
        
        # Create table
        if col_widths is None:
            col_widths = [5*inch / len(data.columns)] * len(data.columns)
        
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def add_image(self, image_path: str, width: float = 5.5) -> None:
        """
        Add image to PDF.
        
        Args:
            image_path: Path to image file
            width: Image width in inches
        """
        try:
            img = Image(image_path, width=width*inch, height=width*inch*0.6)
            self.story.append(img)
            self.story.append(Spacer(1, 0.2*inch))
        except Exception as e:
            self.add_paragraph(f"[Image could not be loaded: {image_path}]")
    
    def add_page_break(self) -> None:
        """Add page break."""
        self.story.append(PageBreak())
    
    def build(self) -> None:
        """Generate and save PDF."""
        self.document.build(self.story)
