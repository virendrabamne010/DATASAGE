"""
Main analyzer class for DATASAGE.

This is the primary interface users interact with.
It orchestrates all modules using a clean, intuitive API.
"""

import pandas as pd
import warnings
from typing import Optional, Literal
from datasage.core.utils import validate_dataframe
from datasage.cleaner import MissingValueHandler, OutlierDetector, DuplicateRemover
from datasage.insights import CorrelationAnalyzer, StatisticsAnalyzer, CategoryAnalyzer, TrendAnalyzer
from datasage.visualization import ChartGenerator, DistributionPlotter, HeatmapGenerator
from datasage.report import TextReportGenerator, PDFReportGenerator


class Analyzer:
    """
    Main analyzer class for automated data analysis.
    
    This is the primary interface for DATASAGE. It provides
    a fluent API for cleaning, analyzing, visualizing, and
    reporting on datasets.
    
    Example:
        >>> import pandas as pd
        >>> from datasage import Analyzer
        >>> 
        >>> df = pd.read_csv('data.csv')
        >>> analyzer = Analyzer(df)
        >>> analyzer.clean()
        >>> insights = analyzer.analyze()
        >>> analyzer.visualize()
        >>> analyzer.generate_report('report.pdf')
    """
    
    def __init__(self, dataframe: pd.DataFrame):
        """
        Initialize Analyzer with a DataFrame.
        
        Args:
            dataframe: pandas DataFrame to analyze
            
        Raises:
            InvalidDataError: If input is not a valid DataFrame
        """
        self.original_df = validate_dataframe(dataframe)
        self.df = self.original_df.copy()
        
        # Initialize modules
        self.missing_handler = MissingValueHandler()
        self.outlier_detector = OutlierDetector()
        self.duplicate_remover = DuplicateRemover()
        
        self.corr_analyzer = CorrelationAnalyzer()
        self.stats_analyzer = StatisticsAnalyzer()
        self.category_analyzer = CategoryAnalyzer()
        self.trend_analyzer = TrendAnalyzer()
        
        self.chart_generator = ChartGenerator()
        self.dist_plotter = DistributionPlotter()
        self.heatmap_generator = HeatmapGenerator()
        
        # Store analysis results
        self.analysis_results = {}
        self.cleaning_stats = {}
    
    def info(self) -> dict:
        """
        Get basic information about the dataset.
        
        Returns:
            dict: Dataset metadata
        """
        return {
            'shape': self.df.shape,
            'columns': self.df.columns.tolist(),
            'dtypes': self.df.dtypes.to_dict(),
            'memory_usage_mb': round(self.df.memory_usage(deep=True).sum() / 1024**2, 2),
            'duplicates': self.df.duplicated().sum(),
            'missing_values': self.df.isnull().sum().sum(),
        }
    
    # ======================== CLEANING METHODS ========================
    
    def clean(self, 
             handle_missing: Literal['drop_column', 'drop_row', 'mean', 'median', 'mode'] = 'drop_column',
             handle_outliers: bool = True,
             outlier_strategy: Literal['remove', 'cap'] = 'cap',
             remove_duplicates: bool = True) -> 'Analyzer':
        """
        Clean the dataset by handling missing values, outliers, and duplicates.
        
        Args:
            handle_missing: Strategy for missing values
            handle_outliers: Whether to detect and handle outliers
            outlier_strategy: 'remove' or 'cap'
            remove_duplicates: Whether to remove duplicate rows
        
        Returns:
            Analyzer: Self for method chaining
        """
        print("🧹 Cleaning dataset...")
        
        # Store original shape
        original_shape = self.df.shape
        
        # Handle missing values
        print(f"  ├─ Handling missing values ({handle_missing})")
        missing_report = self.missing_handler.analyze(self.df)
        self.cleaning_stats['missing_before'] = len(missing_report)
        
        if missing_report:
            self.df = self.missing_handler.handle(self.df, strategy=handle_missing)
        
        # Handle outliers
        if handle_outliers:
            print(f"  ├─ Detecting outliers ({outlier_strategy})")
            outlier_report = self.outlier_detector.detect(self.df)
            self.cleaning_stats['outliers_found'] = len(outlier_report)
            
            if outlier_report:
                if outlier_strategy == 'remove':
                    self.df = self.outlier_detector.remove_outliers(self.df)
                else:
                    self.df = self.outlier_detector.cap_outliers(self.df)
        
        # Remove duplicates
        if remove_duplicates:
            print(f"  └─ Removing duplicates")
            dup_report = self.duplicate_remover.analyze(self.df)
            self.cleaning_stats['duplicates_removed'] = dup_report['total_duplicates']
            
            if dup_report['total_duplicates'] > 0:
                self.df = self.duplicate_remover.remove(self.df)
        
        self.cleaning_stats['shape_before'] = original_shape
        self.cleaning_stats['shape_after'] = self.df.shape
        print(f"✅ Cleaning complete: {original_shape} → {self.df.shape}\n")
        
        return self
    
    # ======================== ANALYSIS METHODS ========================
    
    def analyze(self) -> dict:
        """
        Perform comprehensive analysis on cleaned data.
        
        Returns:
            dict: All analysis results
        """
        print("📊 Analyzing dataset...")
        
        # Statistics
        print("  ├─ Computing statistics...")
        self.analysis_results['statistics'] = self.stats_analyzer.analyze(self.df)
        
        # Correlations
        print("  ├─ Analyzing correlations...")
        self.corr_analyzer.compute(self.df)
        self.analysis_results['correlations'] = self.corr_analyzer.find_high_correlations()
        
        # Categories
        print("  ├─ Analyzing categories...")
        self.analysis_results['categories'] = self.category_analyzer.get_top_categories(self.df)
        
        # Trends
        print("  └─ Detecting trends...")
        self.analysis_results['trends'] = self.trend_analyzer.detect_trends_in_columns(self.df)
        
        print(f"✅ Analysis complete!\n")
        
        return self.analysis_results
    
    # ======================== VISUALIZATION METHODS ========================
    
    def visualize(self, output_dir: str = './output') -> 'Analyzer':
        """
        Generate visualizations and save to disk.
        
        Args:
            output_dir: Directory to save visualizations
        
        Returns:
            Analyzer: Self for method chaining
        """
        import os
        from pathlib import Path
        
        print("📈 Generating visualizations...")
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Correlation heatmap
        print("  ├─ Correlation heatmap...")
        fig = self.heatmap_generator.correlation_heatmap(self.df)
        self.heatmap_generator.save_figure(fig, f"{output_dir}/01_correlation_heatmap.png")
        
        # Distribution plots
        print("  ├─ Distribution plots...")
        numeric_cols = self.df.select_dtypes(include=['number']).columns[:3]  # Top 3
        for i, col in enumerate(numeric_cols):
            fig = self.dist_plotter.histogram(self.df[col], title=f"Distribution: {col}")
            self.dist_plotter.save_figure(fig, f"{output_dir}/02_dist_{i}_{col}.png")
        
        # Box plot
        print("  └─ Box plots...")
        fig = self.dist_plotter.box_plot(self.df)
        self.dist_plotter.save_figure(fig, f"{output_dir}/03_boxplot.png")
        
        print(f"✅ Visualizations saved to '{output_dir}'\n")
        self.viz_output_dir = output_dir
        
        return self
    
    # ======================== REPORT METHODS ========================
    
    def generate_report(self, filepath: str, format: Literal['text', 'pdf'] = 'pdf',
                       include_charts: bool = True) -> None:
        """
        Generate comprehensive analysis report.
        
        Args:
            filepath: Output file path (e.g., 'report.pdf' or 'report.txt')
            format: Report format ('text' or 'pdf')
            include_charts: Whether to include visualizations in PDF
        """
        print("📄 Generating report...")
        
        if format == 'text':
            self._generate_text_report(filepath)
        else:
            self._generate_pdf_report(filepath, include_charts)
        
        print(f"✅ Report saved to '{filepath}'\n")
    
    def _generate_text_report(self, filepath: str) -> None:
        """Generate text report."""
        report = TextReportGenerator()
        
        # Dataset overview
        report.add_header("Dataset Overview", level=1)
        report.add_table(pd.DataFrame([self.info()]))
        
        # Cleaning statistics
        if self.cleaning_stats:
            report.add_header("Data Cleaning", level=2)
            report.add_key_value_table(self.cleaning_stats)
        
        # Statistics
        if 'statistics' in self.analysis_results:
            report.add_header("Statistical Summary", level=2)
            for col, stats in self.analysis_results['statistics'].items():
                report.add_key_value_table(stats, f"{col}")
        
        # Correlations
        if self.analysis_results.get('correlations'):
            report.add_header("High Correlations", level=2)
            corr_df = pd.DataFrame(self.analysis_results['correlations'])
            report.add_table(corr_df)
        
        # Categories
        if self.analysis_results.get('categories'):
            report.add_header("Categorical Analysis", level=2)
            for col, data in self.analysis_results['categories'].items():
                report.add_key_value_table(
                    {'total_unique': data['total_unique']},
                    f"{col}"
                )
        
        report.save(filepath)
    
    def _generate_pdf_report(self, filepath: str, include_charts: bool = True) -> None:
        """Generate PDF report."""
        report = PDFReportGenerator(filepath, title="DATASAGE Data Analysis Report")
        report.add_title()
        
        # Dataset overview
        report.add_heading("Dataset Overview")
        info_df = pd.DataFrame([self.info()])
        report.add_table(info_df)
        
        # Cleaning statistics
        if self.cleaning_stats:
            report.add_heading("Data Cleaning Results")
            report.add_paragraph(
                f"Original shape: {self.cleaning_stats['shape_before']} → "
                f"Cleaned shape: {self.cleaning_stats['shape_after']}"
            )
        
        # Statistics summary
        if 'statistics' in self.analysis_results:
            report.add_heading("Statistical Summary")
            for col, stats in list(self.analysis_results['statistics'].items())[:3]:
                stats_df = pd.DataFrame([stats])
                report.add_table(stats_df, title=f"{col}")
        
        # Correlations
        if self.analysis_results.get('correlations'):
            report.add_heading("High Correlations")
            corr_df = pd.DataFrame(self.analysis_results['correlations'])
            report.add_table(corr_df)
        
        # Add visualizations
        if include_charts and hasattr(self, 'viz_output_dir'):
            report.add_page_break()
            report.add_heading("Visualizations")
            import os
            viz_dir = self.viz_output_dir
            
            if os.path.exists(viz_dir):
                for img_file in sorted(os.listdir(viz_dir))[:3]:
                    if img_file.endswith('.png'):
                        report.add_image(os.path.join(viz_dir, img_file))
        
        report.build()
    
    def reset(self) -> 'Analyzer':
        """
        Reset to original data, undoing all cleaning.
        
        Returns:
            Analyzer: Self for method chaining
        """
        self.df = self.original_df.copy()
        self.cleaning_stats = {}
        print("🔄 Reset to original data\n")
        return self
