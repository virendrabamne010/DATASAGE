"""
DATASAGE Advanced Usage Example

This script demonstrates advanced features of the DATASAGE library,
including module-level control and custom workflows.

Run: python examples/advanced_analysis.py
"""

import pandas as pd
import numpy as np
from datasage import (
    Analyzer,
    MissingValueHandler,
    OutlierDetector,
    CorrelationAnalyzer,
    ChartGenerator,
    TextReportGenerator,
)

print("=" * 60)
print("DATASAGE - Advanced Usage Example")
print("=" * 60)

# ============================================================================
# Create Sample Data
# ============================================================================
np.random.seed(42)
data = pd.DataFrame({
    'Revenue': np.random.normal(100000, 30000, 100),
    'Traffic': np.random.randint(1000, 10000, 100),
    'Conversion': np.random.uniform(0.01, 0.1, 100),
    'Marketing_Cost': np.random.normal(5000, 2000, 100),
    'Channel': np.random.choice(['Web', 'Mobile', 'Email'], 100),
})

# Add some anomalies
data.loc[0, 'Revenue'] = 1000000  # Outlier
data.loc[np.random.choice(data.index, 5), 'Traffic'] = np.nan

print("\n📂 Dataset created")
print(f"   Shape: {data.shape}\n")

# ============================================================================
# EXAMPLE 1: Unit Module Usage
# ============================================================================
print("💡 Example 1: Using Individual Modules")
print("-" * 60)

# Use missing handler directly
missing_handler = MissingValueHandler(threshold=0.3)
missing_report = missing_handler.analyze(data)
print(f"Missing values found: {len(missing_report)}")

if missing_report:
    for col, stats in missing_report.items():
        print(f"  {col}: {stats['percentage']:.1f}% missing")

# Handle missing values
data_cleaned = missing_handler.handle(data, strategy='median')
print(f"✅ Missing values handled\n")

# ============================================================================
# EXAMPLE 2: Custom Cleaning Pipeline
# ============================================================================
print("💡 Example 2: Custom Cleaning Pipeline")
print("-" * 60)

outlier_detector = OutlierDetector(method='zscore')
outlier_report = outlier_detector.detect(data_cleaned)
print(f"Outliers detected in: {len(outlier_report)} columns")

# Cap outliers (don't remove rows)
data_cleaned = outlier_detector.cap_outliers(data_cleaned)
print(f"✅ Outliers capped\n")

# ============================================================================
# EXAMPLE 3: Advanced Correlation Analysis
# ============================================================================
print("💡 Example 3: Advanced Correlation Analysis")
print("-" * 60)

corr_analyzer = CorrelationAnalyzer(threshold=0.5)
corr_matrix = corr_analyzer.compute(data_cleaned)

print("Correlation Matrix:")
print(corr_matrix.round(3))

high_corrs = corr_analyzer.find_high_correlations()
if high_corrs:
    print(f"\nHigh correlations found:")
    for pair in high_corrs:
        print(f"  {pair['variable1']} ↔ {pair['variable2']}: {pair['correlation']}")
else:
    print("No high correlations found")

print()

# ============================================================================
# EXAMPLE 4: Custom Report Generation
# ============================================================================
print("💡 Example 4: Custom Report Generation")
print("-" * 60)

report = TextReportGenerator()
report.add_header("Custom Data Analysis Report", level=1)

report.add_header("Executive Summary", level=2)
report.add_paragraph(
    "This report demonstrates the DATASAGE library's custom "
    "reporting capabilities with individually crafted content."
)

report.add_header("Dataset Overview", level=2)
report.add_key_value_table({
    'Total Records': len(data_cleaned),
    'Features': data_cleaned.shape[1],
    'Data Types': data_cleaned.dtypes.nunique(),
})

report.add_header("Numeric Summary", level=2)
report.add_table(data_cleaned.describe().round(2))

report.add_header("Insights", level=2)
report.add_paragraph(f"Found {len(high_corrs)} high correlation pairs.")

# Save report
report.save('./examples/output/custom_report.txt')
print("✅ Custom report saved: ./examples/output/custom_report.txt\n")

# ============================================================================
# EXAMPLE 5: Using Main Analyzer with Custom Parameters
# ============================================================================
print("💡 Example 5: Full Analysis with Custom Parameters")
print("-" * 60)

analyzer = Analyzer(data)
analyzer.clean(handle_missing='median', handle_outliers=True, outlier_strategy='remove')
insights = analyzer.analyze()

print(f"Cleaning stats: {analyzer.cleaning_stats}")
print(f"Analysis completed with {len(insights)} result categories\n")

print("=" * 60)
print("✅ Advanced Examples Complete!")
print("=" * 60)
