"""
Text report generation for DATASAGE.

This module generates human-readable text reports
summarizing data insights and analysis results.
"""

import pandas as pd
from datetime import datetime


class TextReportGenerator:
    """Generate text-based analysis reports."""
    
    def __init__(self):
        """Initialize report generator."""
        self.report_content = []
        self.timestamp = datetime.now()
    
    def add_header(self, title: str, level: int = 1) -> None:
        """
        Add a header to the report.
        
        Args:
            title: Header text
            level: Header level (1=main, 2=section, 3=subsection)
        """
        if level == 1:
            self.report_content.append(f"\n{'='*60}")
            self.report_content.append(f"{title.upper():^60}")
            self.report_content.append(f"{'='*60}\n")
        elif level == 2:
            self.report_content.append(f"\n{'-'*60}")
            self.report_content.append(f"{title}")
            self.report_content.append(f"{'-'*60}\n")
        else:
            self.report_content.append(f"\n{title}")
            self.report_content.append(f"{'~'*len(title)}\n")
    
    def add_paragraph(self, text: str) -> None:
        """Add paragraph text to report."""
        self.report_content.append(text + "\n")
    
    def add_table(self, data: pd.DataFrame | dict, title: str = "") -> None:
        """
        Add a table to the report.
        
        Args:
            data: DataFrame or dict with table data
            title: Table title
        """
        if title:
            self.report_content.append(f"\n{title}")
            self.report_content.append("-" * len(title) + "\n")
        
        if isinstance(data, dict):
            data = pd.DataFrame(data)
        
        # Format dataframe as text table
        self.report_content.append(data.to_string())
        self.report_content.append("\n")
    
    def add_key_value_table(self, data: dict, title: str = "") -> None:
        """
        Add key-value pairs as formatted table.
        
        Args:
            data: Dictionary of key-value pairs
            title: Table title
        """
        if title:
            self.report_content.append(f"\n{title}")
            self.report_content.append("-" * len(title) + "\n")
        
        for key, value in data.items():
            # Format value nicely
            if isinstance(value, float):
                formatted_value = f"{value:.4f}"
            else:
                formatted_value = str(value)
            
            self.report_content.append(f"  {key:.<40} {formatted_value}\n")
    
    def add_divider(self) -> None:
        """Add visual divider."""
        self.report_content.append("\n" + "*" * 60 + "\n")
    
    def generate(self) -> str:
        """
        Generate final report string.
        
        Returns:
            str: Complete report text
        """
        # Add header
        report_text = f"\nDATA ANALYSIS REPORT\n"
        report_text += f"Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
        report_text += "=" * 60 + "\n"
        
        # Add content
        report_text += "".join(self.report_content)
        
        # Add footer
        report_text += "\n" + "=" * 60
        report_text += "\nEnd of Report\n"
        
        return report_text
    
    def save(self, filepath: str) -> None:
        """
        Save report to file.
        
        Args:
            filepath: Where to save (e.g., 'report.txt')
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.generate())
    
    def print(self) -> None:
        """Print report to console."""
        print(self.generate())
