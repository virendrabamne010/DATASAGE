# DATASAGE Project Report

## Owner

- Name: Virendra Vijay Bamne
- Education: B.Tech CSE, 4th Year
- College: R V Parankar College of Engineering, Arvi
- Contact: +91 8010516829

---

## Executive Summary

DATASAGE is a professional Python analytics platform that transforms raw CSV and Excel files into clean, meaningful data insights, visualizations, and reports. It is designed for analysts, startups, and enterprises that need a fast, modular, and production-ready solution for dataset cleaning and exploratory analytics.

This repository includes:
- a reusable Python package (`datasage/`)
- a live Streamlit demo app (`streamlit_app.py`)
- example scripts (`examples/`)
- documentation and tests

The codebase is structured for clarity, maintainability, and sale-readiness.

---

## What We Built

### Core Product

1. **DATASAGE Python Library**
   - A modular package for data cleaning, profiling, visualization, and reporting.
   - Exposed via a single user-facing API class: `Analyzer`.

2. **Streamlit Live Analyzer App**
   - `streamlit_app.py` provides an interactive upload-and-analyze experience.
   - Supports CSV and Excel ingestion, malformed CSV fallback parsing, schema inference, wellness dashboard, feature importance, and downloadable reports.

3. **Examples**
   - Usage examples in `examples/basic_usage.py` and `examples/advanced_analysis.py` demonstrate how to use the package.

4. **Documentation and Packaging**
   - Clean repo structure with `README.md`, `requirements.txt`, `pyproject.toml`, `setup.py`, and `LICENSE`.
   - Ready for installation and distribution.

---

## Features

### Data Cleaning

- Missing value handling strategies:
  - `drop_column`
  - `drop_row`
  - `mean`
  - `median`
  - `mode`
  - `forward_fill`
- Duplicate row detection and removal.
- Outlier detection using IQR and Z-score.
- Cap or remove outliers as needed.

### Data Profiling and Insights

- Dataset metadata and health overview.
- Summary statistics for numeric columns.
- Correlation analysis to find strong relationships.
- Category analysis for top values and distributions.
- Trend detection across numeric columns.
- Executive summary generation with remedial recommendations.

### Visualization and Reporting

- Auto-generated charts:
  - bar
  - line
  - scatter
  - pie
- Distribution plots and numerical histograms.
- Heatmaps for correlation and missing values.
- Professional PDF report generation using ReportLab.
- Text report generation with table formatting.
- Cleaned dataset export to CSV and Excel.

### Interactive App

- Upload CSV or Excel files in the browser.
- Select Excel sheets before import.
- View data preview and profile summaries.
- Toggle light/dark theme.
- Health score gauge and dashboard.
- Feature importance panel.
- Download cleaned datasets and generated reports.

---

## Architecture and Modules

### Package Structure

- `datasage/`
  - `core/` - main orchestrator and utilities
  - `cleaner/` - missing value, outlier, duplicate handling
  - `insights/` - statistics, correlations, categories, trends
  - `visualization/` - chart generation, distributions, heatmaps
  - `report/` - text and PDF report creation

### Key Components

#### `datasage/core/analyzer.py`
- Main API class `Analyzer`.
- Coordinates cleaning, analysis, visualization, and reporting.
- Provides method chaining through `clean()`, `analyze()`, `visualize()`, and `generate_report()`.
- Builds an executive summary from analysis results.

#### `datasage/cleaner/missing_handler.py`
- Analyzes missing values per column.
- Handles missing data using common cleaning strategies.

#### `datasage/cleaner/outlier_detector.py`
- Detects outliers in numeric data.
- Supports IQR and Z-score methods.
- Can remove or cap outliers.

#### `datasage/cleaner/duplicate_remover.py`
- Detects duplicate rows.
- Removes duplicates with configurable keep behavior.

#### `datasage/insights/statistics.py`
- Generates descriptive statistics for numeric columns.
- Includes count, mean, median, std, min, max, quartiles, skewness, and kurtosis.

#### `datasage/visualization/charts.py`
- Creates Matplotlib charts for analysis.
- Saves chart figures to disk.

#### `datasage/report/pdf_report.py`
- Generates publish-ready PDF reports.
- Uses ReportLab for formatting text, tables, and images.
- Sanitizes data values for safe PDF rendering.

---

## Implementation Details

### Data Validation

- `datasage/core/utils.py` validates that input data is a non-empty pandas DataFrame.
- Prevents runtime errors from invalid input.

### Configuration

- `datasage/config.py` centralizes default behavior such as:
  - missing-value threshold
  - outlier detection method
  - correlation threshold
  - figure dimensions
  - report options

### Analyzer Workflow

1. `Analyzer(df)` validates and stores the input dataset.
2. `clean()` applies missing-value handling, outlier treatment, and duplicate removal.
3. `analyze()` computes statistics, correlations, categories, and trends.
4. `visualize()` generates charts and saves them as files.
5. `generate_report()` creates text and PDF outputs.

### Streamlit App Flow

- File upload for CSV/Excel.
- Safe parsing with fallback engine for malformed CSV.
- Dataset preview and metrics display.
- Health score calculation from missing, duplicate, and anomaly ratios.
- Executive summary and feature insights.
- Column-level cleaning controls.
- Download buttons for cleaned CSV/Excel.
- Report generation and PDF embed preview.

---

## Technologies Used

- Python 3.10+
- pandas for data ingestion and transformation
- numpy for numeric operations
- matplotlib and seaborn for charts
- reportlab for PDF generation
- Streamlit for the interactive app
- pytest for tests

---

## Use Cases

### 1. Analyst Preprocessing Tool

A business analyst can upload raw CSV or Excel data, review missing values and outliers, apply cleaning strategies, and generate a polished report without writing code.

### 2. Data Quality Dashboard

The Streamlit app provides a quick quality check and executive summary that can be used in stakeholder meetings.

### 3. Automated Report Generation

Generate consistent text and PDF reports for recurring datasets, saving time on manual documentation.

### 4. Rapid Prototyping for Startups

Startups can use DATASAGE as a lightweight analytics engine to inspect early-stage data and validate key metrics before building production pipelines.

---

## What This Gives You

- A sale-ready codebase with clean architecture and modular design.
- A live demo app for product showcase.
- Documentation and structure suitable for IT company evaluation.
- Ownership clearly attributed to Virendra Vijay Bamne.

---

## How to Run

```bash
pip install -r requirements.txt
pip install -e .
streamlit run streamlit_app.py
```

For tests:

```bash
pytest tests/
pytest --cov=datasage tests/
```

---

## Recommended Next Steps

1. Add a `docs/PROJECT_REPORT.md` for investor or buyer-facing product documentation.
2. Add CI workflow status badges in `README.md`.
3. Add a short pitch section and value proposition for potential buyers.
4. Replace any placeholder repository URLs with your own GitHub or company domain.

---

## Notes

This report was generated based on the current repository structure and implementation in `DATASAGE`. It is designed to explain the product, features, implementation, and use cases in a professional format.
