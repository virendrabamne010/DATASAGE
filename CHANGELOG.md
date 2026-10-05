# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial public release of DATASAGE
- Core `Analyzer` class with fluent API for cleaning, analysis, visualization, and reporting
- Data cleaning: missing value handling, outlier detection (IQR/Z-score), duplicate removal
- Data profiling: statistics, correlations, categories, trends
- Visualization: charts, distributions, heatmaps
- Reporting: text and PDF report generation
- Streamlit live analyzer app with upload, cleaning, and report features
- Comprehensive documentation (README, API, installation, examples, contributing)
- CI/CD pipeline with testing on Python 3.10/3.11/3.12
- Docker and docker-compose deployment configuration
- PyPI publishing workflow

### Fixed
- Packaging bug where subpackages were excluded from the build
- Placeholder URLs in documentation
- Incorrect author metadata in version module
- Missing streamlit/altair dependencies
- Inconsistent development status classifiers

### Security
- Docker container runs as non-root user
- Docker health checks enabled