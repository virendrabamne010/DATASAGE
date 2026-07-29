# Usage Examples

## Example 1: Basic Analysis

```python
from datasage import Analyzer
import pandas as pd

# Load data
df = pd.read_csv('data.csv')

# Create analyzer
analyzer = Analyzer(df)

# Manual steps
analyzer.clean()
insights = analyzer.analyze()
analyzer.visualize()
analyzer.generate_report('report.pdf')
```

## Example 2: One-Liner Analysis

```python
from datasage import Analyzer

analyzer = Analyzer(df)
analyzer.clean().analyze().visualize()
analyzer.generate_report('report.pdf')
```

## Example 3: Custom Cleaning

```python
from datasage import Analyzer

analyzer = Analyzer(df)

analyzer.clean(
    handle_missing='median',       # Fill with median
    handle_outliers=True,
    outlier_strategy='remove',     # Remove outlier rows
    remove_duplicates=True
)

insights = analyzer.analyze()
```

## Example 4: Module-Level Control

```python
from datasage.cleaner import MissingValueHandler, OutlierDetector
from datasage.insights import CorrelationAnalyzer

# Handle missing values
missing_handler = MissingValueHandler(threshold=0.3)
df = missing_handler.handle(df, strategy='mean')

# Detect outliers
detector = OutlierDetector(method='zscore')
df = detector.cap_outliers(df)

# Analyze correlations
corr = CorrelationAnalyzer(threshold=0.6)
corr.compute(df)
print(corr.find_high_correlations())
```

## Example 5: Custom Report

```python
from datasage.report import TextReportGenerator
import pandas as pd

report = TextReportGenerator()

report.add_header("Sales Analysis Q1 2024", level=1)

report.add_header("Executive Summary", level=2)
report.add_paragraph(
    "Quarterly sales report showing revenue trends and "
    "performance metrics across all regions."
)

report.add_header("Key Metrics", level=2)
report.add_key_value_table({
    'Total Revenue': '$1,250,000',
    'Growth Rate': '15.2%',
    'Customer Count': '3,450',
})

report.add_header("Regional Performance", level=2)
report.add_table(regional_df)

report.save('sales_report.txt')
print("✅ Report saved!")
```

## Example 6: PDF Report with Charts

```python
from datasage.report import PDFReportGenerator
import matplotlib.pyplot as plt

report = PDFReportGenerator('analysis.pdf', title='Data Analysis Report')

report.add_title()
report.add_heading("Dataset Overview")
report.add_paragraph("This report contains a comprehensive analysis...")

report.add_heading("Visualizations")
report.add_image('correlation_heatmap.png')
report.add_image('distribution.png')

report.add_page_break()
report.add_heading("Statistics")
report.add_table(stats_df)

report.build()
```

## Example 7: Data Exploration

```python
from datasage import Analyzer

analyzer = Analyzer(df)

# Get dataset info
info = analyzer.info()
print(f"Shape: {info['shape']}")
print(f"Memory: {info['memory_usage_mb']}MB")
print(f"Missing values: {info['missing_values']}")

# Clean data
analyzer.clean()

# Analyze without visualization
insights = analyzer.analyze()

# Explore results
print("High correlations:")
for corr in insights['correlations']:
    print(f"  {corr['variable1']} ↔ {corr['variable2']}: {corr['correlation']}")

print("\nTop categories:")
for col, data in insights['categories'].items():
    print(f"  {col}: {data['total_unique']} unique values")

print("\nTrends detected:")
for col, trend in insights['trends'].items():
    print(f"  {col}: {trend['trend']} (p={trend['p_value']})")
```

## Example 8: Time Series Analysis

```python
from datasage.insights import TrendAnalyzer
import pandas as pd

# Time series data
ts_data = pd.read_csv('stock_prices.csv', parse_dates=['Date'])
ts_data = ts_data.set_index('Date')

trend_analyzer = TrendAnalyzer()

# Detect trends
for column in ts_data.columns:
    result = trend_analyzer.detect_trend(ts_data[column])
    print(f"{column}: {result['trend']}")

# Calculate growth rates
growth = trend_analyzer.calculate_growth_rate(ts_data['Price'])
print(f"Mean growth rate: {growth['mean_growth_rate']:.2%}")
```

## Example 9: Categorical Focus

```python
from datasage.insights import CategoryAnalyzer

cat_analyzer = CategoryAnalyzer(top_n=10)

# Top categories
top = cat_analyzer.get_top_categories(df)
print("Top categories per column:")
for col, data in top.items():
    print(f"  {col}:")
    for cat, count in data['top_categories'].items():
        pct = data['top_percentages'][cat]
        print(f"    {cat}: {count} ({pct}%)")

# Diversity metrics
diversity = cat_analyzer.get_diversity(df)
print("\nDiversity metrics:")
for col, metrics in diversity.items():
    print(f"  {col}: {metrics['diversity_ratio']:.2%} diversity")
```

## Example 10: Reset and Compare

```python
from datasage import Analyzer

analyzer = Analyzer(df)

# First analysis
analyzer.clean()
insights1 = analyzer.analyze()
original_stats = insights1['statistics']

# Reset to original
analyzer.reset()

# Try different cleaning strategy
analyzer.clean(handle_missing='drop_row', handle_outliers=True)
insights2 = analyzer.analyze()
new_stats = insights2['statistics']

print("Before cleaning:", len(df))
print("After cleaning (drop_row):", len(analyzer.df))

# Compare insights
print("\nComparison complete!")
```

---

For API details, see [API.md](API.md).
