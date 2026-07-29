# Installation Guide

## System Requirements

- **Python**: 3.10 or higher
- **OS**: Windows, macOS, Linux
- **Disk Space**: ~200MB for all dependencies

## Installation Methods

### 1. Install from PyPI (Recommended)

```bash
pip install datasage
```

### 2. Install from Source

Clone the repository and install in development mode:

```bash
git clone https://github.com/yourusername/datasage.git
cd datasage
pip install -e .
```

### 3. Install with Development Tools

For development work including testing and linting:

```bash
pip install -e ".[dev]"
```

## Verify Installation

```python
import datasage
print(datasage.__version__)

from datasage import Analyzer
print("✅ DATASAGE installed successfully!")
```

## Troubleshooting

### Import Error

If you get `ModuleNotFoundError`, ensure all dependencies are installed:

```bash
pip install pandas numpy matplotlib seaborn scipy reportlab
```

### Version Compatibility

Check your Python version:

```bash
python --version
```

Must be 3.10 or higher.

### Graphics Issues

If visualizations don't work, you may need matplotlib backend:

```bash
pip install --upgrade matplotlib
```

## Getting Started

After installation, try the basic example:

```python
import pandas as pd
from datasage import Analyzer

# Create sample data
df = pd.DataFrame({
    'A': range(100),
    'B': range(100, 200),
    'C': ['X', 'Y'] * 50
})

# Analyze
analyzer = Analyzer(df)
analyzer.clean()
analyzer.analyze()
print("✅ Ready to use!")
```

For more details, see the [main documentation](README.md).
