# API Reference

## Main Classes

### `Analyzer`

The primary interface for DATASAGE.

```python
from datasage import Analyzer

analyzer = Analyzer(dataframe)
analyzer.clean()
analyzer.analyze()
analyzer.visualize()
analyzer.generate_report('report.pdf')
```

#### Methods

##### `clean()`

```python
analyzer.clean(
    handle_missing='drop_column',  # 'drop_column', 'drop_row', 'mean', 'median', 'mode'
    handle_outliers=True,
    outlier_strategy='cap',        # 'cap' or 'remove'
    remove_duplicates=True
)
```

Cleans the dataset by handling missing values, outliers, and duplicates.

##### `analyze()`

```python
insights = analyzer.analyze()
```

Returns dict with:
- `statistics`: Descriptive statistics
- `correlations`: High correlation pairs
- `categories`: Top categories
- `trends`: Trend analysis

##### `visualize()`

```python
analyzer.visualize(output_dir='./output')
```

Generates and saves visualizations to directory.

##### `generate_report()`

```python
analyzer.generate_report(
    filepath='report.pdf',
    format='pdf',              # 'pdf' or 'text'
    include_charts=True
)
```

Generates professional report.

---

## Cleaner Module

### `MissingValueHandler`

```python
from datasage.cleaner import MissingValueHandler

handler = MissingValueHandler(threshold=0.5)

# Analyze
report = handler.analyze(df)

# Handle
df_clean = handler.handle(df, strategy='mean')
```

**Strategies**: `drop_column`, `drop_row`, `mean`, `median`, `mode`, `forward_fill`

### `OutlierDetector`

```python
from datasage.cleaner import OutlierDetector

detector = OutlierDetector(method='iqr')

# Detect
report = detector.detect(df)

# Remove or cap
df_clean = detector.remove_outliers(df)
df_capped = detector.cap_outliers(df)
```

**Methods**: `iqr`, `zscore`

### `DuplicateRemover`

```python
from datasage.cleaner import DuplicateRemover

remover = DuplicateRemover()

# Analyze
report = remover.analyze(df)

# Remove
df_clean = remover.remove(df, keep='first')
```

---

## Insights Module

### `StatisticsAnalyzer`

```python
from datasage.insights import StatisticsAnalyzer

stats = StatisticsAnalyzer()
results = stats.analyze(df)
```

Returns: mean, median, std, skewness, kurtosis, quantiles

### `CorrelationAnalyzer`

```python
from datasage.insights import CorrelationAnalyzer

corr = CorrelationAnalyzer(threshold=0.7)
matrix = corr.compute(df)
high_corrs = corr.find_high_correlations()
```

### `CategoryAnalyzer`

```python
from datasage.insights import CategoryAnalyzer

cat = CategoryAnalyzer(top_n=5)
top = cat.get_top_categories(df)
diversity = cat.get_diversity(df)
```

### `TrendAnalyzer`

```python
from datasage.insights import TrendAnalyzer

trend = TrendAnalyzer()
result = trend.detect_trend(df['column'])
growth = trend.calculate_growth_rate(df['column'])
```

---

## Visualization Module

### `ChartGenerator`

```python
from datasage.visualization import ChartGenerator

gen = ChartGenerator(figsize=(12, 6))

fig = gen.bar_chart(data)
fig = gen.line_chart(data)
fig = gen.scatter_chart(x, y)
fig = gen.pie_chart(data)

gen.save_figure(fig, 'chart.png')
```

### `DistributionPlotter`

```python
from datasage.visualization import DistributionPlotter

plotter = DistributionPlotter()

fig = plotter.histogram(data, bins=30)
fig = plotter.kde_plot(data)
fig = plotter.box_plot(df)
fig = plotter.violin_plot(df)
```

### `HeatmapGenerator`

```python
from datasage.visualization import HeatmapGenerator

gen = HeatmapGenerator()

fig = gen.correlation_heatmap(df)
fig = gen.missing_value_heatmap(df)
```

---

## Report Module

### `TextReportGenerator`

```python
from datasage.report import TextReportGenerator

report = TextReportGenerator()
report.add_header("Title")
report.add_paragraph("Text")
report.add_table(df)
report.add_key_value_table({'key': 'value'})
report.save('report.txt')
```

### `PDFReportGenerator`

```python
from datasage.report import PDFReportGenerator

report = PDFReportGenerator('report.pdf')
report.add_title()
report.add_heading("Section")
report.add_paragraph("Text")
report.add_table(df)
report.add_image('chart.png')
report.build()
```

---

## Configuration

Global settings in `datasage.config.Config`:

```python
from datasage.config import config

config.MISSING_THRESHOLD = 0.5
config.OUTLIER_METHOD = 'iqr'
config.CORRELATION_THRESHOLD = 0.7
```

---

For more examples, see [EXAMPLES.md](EXAMPLES.md).
