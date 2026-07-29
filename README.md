# DATASAGE - Automated Data Analytics Library

![CI](https://github.com/yourusername/datasage/actions/workflows/ci.yml/badge.svg)

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Alpha-yellow)

**DATASAGE** is a production-ready Python library for automated data analytics that automatically cleans datasets, generates statistical insights, creates visualizations, and produces professional reports—all with minimal code.

## 🎯 Key Fe
 atures

- **🧹 Intelligent Data Cleaning**
  - Automatic missing value handling (drop, fill, interpolate)
  - Outlier detection and treatment (IQR, Z-score methods)
  - Duplicate identification and removal

- **📊 Comprehensive Insights**
  - Statistical summaries (mean, median, std, skewness, kurtosis)
  - Correlation analysis between variables
  - Categorical variable analysis
  -  Trend detection and growth rate calculation

- **📈 Beautiful Visualizations**
  - Auto-generated charts (bar, line, scatter, pie)
  - Distribution plots (histograms, KDE, box plots)
  - Correlation heatmaps and missing value visualizations

- **📄 Professional Reports**
  - Formatted text reports
  - High-quality PDF reports with embedded visualizations
  - Customizable reporting components

## 🚀 Quick Start

### Installation

```bash
pip install datasage
```

Or install from source:

```bash
git clone https://github.com/yourusername/datasage.git
cd datasage
pip install -e .
```

### 5-Minute Tutorial

```python
import pandas as pd
from datasage import Analyzer

# Load your data
df = pd.read_csv('data.csv')

# Initialize analyzer
analyzer = Analyzer(df)

# Clean data
analyzer.clean()

# Analyze
insights = analyzer.analyze()

# Visualize
analyzer.visualize()

# Generate report
analyzer.generate_report('report.pdf')
```

That's it! You now have a complete analysis with visualizations and a professional report.

## 📚 Documentation

- [Installation Guide](INSTALLATION.md)
- [API Reference](API.md)
- [Usage Examples](EXAMPLES.md)
- [Contributing Guide](CONTRIBUTING.md)

## 🏗️ Architecture

DATASAGE is built with modular, production-grade architecture:

```
datasage/
├── cleaner/          # Data preprocessing
├── insights/         # Statistical analysis
├── visualization/    # Chart generation
├── report/           # Report generation
└── core/             # Orchestrator & utilities
```

Each module:
- ✅ Has a single responsibility
- ✅ Can be used independently
- ✅ Follows best practices
- ✅ Is fully documented
- ✅ Is tested

## 💻 Requirements

- Python 3.10+
- pandas ≥ 1.3.0
- numpy ≥ 1.21.0
- matplotlib ≥ 3.4.0
- seaborn ≥ 0.11.0
- scipy ≥ 1.7.0
- reportlab ≥ 3.6.0

## 📖 Usage Examples

### Basic Analysis

```python
from datasage import Analyzer
import pandas as pd

df = pd.read_csv('sales.csv')
analyzer = Analyzer(df)

# One-liner analysis
analyzer.clean().analyze().visualize()

# Generate report
analyzer.generate_report('sales_analysis.pdf')
```

### Custom Workflows

```python
from datasage.cleaner import MissingValueHandler, OutlierDetector
from datasage.insights import CorrelationAnalyzer

# Use individual modules
handler = MissingValueHandler()
handler.analyze(df)  # See what's missing
df_clean = handler.handle(df, strategy='median')

detector = OutlierDetector(method='iqr')
df_clean = detector.cap_outliers(df_clean)

# Analyze correlations
corr = CorrelationAnalyzer(threshold=0.7)
corr.compute(df_clean)
high_corrs = corr.find_high_correlations()
```

### Custom Reports

```python
from datasage.report import TextReportGenerator

report = TextReportGenerator()
report.add_header("My Analysis")
report.add_paragraph("Key findings...")
report.add_table(results_df)
report.save('my_report.txt')
```

## 🧪 Testing

Run tests with pytest:

```bash
pytest tests/
pytest --cov=datasage tests/  # With coverage
```

## ▶️ Run Locally

Quick script to create a virtual environment, install dependencies, and run the basic example:

PowerShell:

```powershell
.\scripts\setup_and_run.ps1
```

Windows (cmd):

```bat
run_example.bat
```

Reports and visualizations are saved to `./examples/output`.

## 📦 Publishing

### Build Distribution

```bash
pip install build
python -m build
```

### Upload to PyPI

```bash
pip install twine
twine upload dist/*
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

Built with ❤️ using pandas, matplotlib, seaborn, and scipy.

## 📧 Support

- 📖 [Documentation](https://github.com/yourusername/datasage)
- 🐛 [Report Issues](https://github.com/yourusername/datasage/issues)
- 💬 [Discussions](https://github.com/yourusername/datasage/discussions)

---

**Happy Analyzing! 🎉**
