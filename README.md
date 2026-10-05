# DATASAGE

[![CI](https://github.com/virendravijaybamne/datasage/actions/workflows/ci.yml/badge.svg)](https://github.com/virendravijaybamne/datasage/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/datasage.svg)](https://pypi.org/project/datasage/)
[![Python Versions](https://img.shields.io/pypi/pyversions/datasage.svg)](https://pypi.org/project/datasage/)
[![License](https://img.shields.io/pypi/l/datasage.svg)](https://github.com/virendravijaybamne/datasage/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**DATASAGE** is a polished, professional Python analytics platform for automated dataset cleaning, insight generation, visualization, and reporting.

This repository is owned and maintained by **Virendra Vijay Bamne**.

---

## Summary

DATASAGE converts raw CSV and Excel datasets into clean, actionable analytics with a modern, production-ready workflow.

It is ideal for analysts, startups, and enterprises that need:
- Rapid data preparation
- Automated data profiling
- Feature-level insights
- Professional downloadable reports
- Interactive Streamlit exploration

---

## Core Features

- **Data quality and cleaning**
  - Missing value strategies: drop, mean, median, mode, forward-fill
  - Duplicate detection and removal
  - Outlier detection with cap/remove handling

- **Data profiling and insights**
  - Column type inference and schema recommendations
  - Summary statistics and correlation analysis
  - Feature importance scoring and health scoring
  - Executive recommendations and data quality guidance

- **Visualization and reporting**
  - Auto-generated charts and dashboards
  - Numeric distribution histograms and wellness gauges
  - Text and PDF report generation
  - Cleaned dataset download support

- **Interactive live demo**
  - Streamlit app for upload, cleaning, and reporting
  - Malformed CSV fallback parsing
  - Excel sheet selection and preview
  - Premium dashboard experience

---

## Installation

Install the package in editable mode:

```bash
pip install -e .
```

Install runtime dependencies:

```bash
pip install -r requirements.txt
```

Install with all optional features:

```bash
pip install -e ".[all]"
```

---

## Quick Start

```python
import pandas as pd
from datasage import Analyzer

# Load data
df = pd.read_csv('data.csv')

# Run analysis
analyzer = Analyzer(df)
analyzer.clean()
analyzer.analyze()
analyzer.visualize()
analyzer.generate_report('report.pdf')
```

---

## Run the Live Streamlit App

```bash
streamlit run streamlit_app.py
```

The app supports:
- CSV and Excel upload
- Schema suggestions and guided cleaning
- Health scoring and premium dashboards
- Cleaned data and report downloads

---

## Docker Deployment

Build and run with Docker:

```bash
docker build -t datasage .
docker run -p 8501:8501 datasage
```

Or use Docker Compose:

```bash
docker-compose up -d
```

---

## Project Structure

```
.
├── datasage/               # Core library package
├── docs/                   # Supporting documentation
├── examples/               # Example scripts and sample datasets
├── tests/                  # Unit tests and fixtures
├── streamlit_app.py        # Live Streamlit demo application
├── pyproject.toml          # Package metadata and dependencies
├── requirements.txt        # Environment dependencies
├── setup.py                # Install compatibility
├── Dockerfile              # Container deployment
├── docker-compose.yml      # Multi-service deployment
├── CHANGELOG.md            # Version history
├── SECURITY.md             # Security policy
├── CODE_OF_CONDUCT.md      # Community guidelines
├── LICENSE                 # MIT license
└── README.md               # Project overview and usage
```

---

## Testing

Run tests with:

```bash
pytest tests/
```

For coverage:

```bash
pytest --cov=datasage tests/
```

---

## Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [API Reference](docs/API.md)
- [Usage Examples](docs/EXAMPLES.md)
- [Contributing Guide](docs/CONTRIBUTING.md)

---

## Contact & Ownership

**Owner:** Virendra Vijay Bamne

**Education:** B.Tech CSE, 4th Year

**College:** R V Parankar College of Engineering, Arvi

**Contact:** +91 8010516829

This repository and source code are owned by Virendra Vijay Bamne.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.