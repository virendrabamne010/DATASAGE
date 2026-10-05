# Contributing Guide

Thank you for your interest in contributing to DATASAGE! This guide will help you get started.

## Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/virendravijaybamne/datasage.git
cd datasage
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Development Dependencies

```bash
pip install -e ".[dev]"
```

## Development Workflow

### Before Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make sure all tests pass:
   ```bash
   pytest tests/
   ```

### Code Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) and use:

- **Black** for code formatting
- **isort** for import organization
- **Flake8** for linting
- **MyPy** for type checking

Before committing:

```bash
# Format code
black datasage/ tests/

# Sort imports
isort datasage/ tests/

# Check style
flake8 datasage/

# Type checking
mypy datasage/
```

### Writing Tests

Place tests in `tests/` following the naming convention `test_*.py`:

```python
# tests/test_my_feature.py
import pytest
from datasage import MyFeature

class TestMyFeature:
    def test_basic_functionality(self):
        result = MyFeature().do_something()
        assert result is not None
```

Run tests with coverage:

```bash
pytest --cov=datasage tests/
```

### Documentation

- Add docstrings using Google style:

```python
def my_function(param1: str, param2: int) -> dict:
    """
    Brief description.
    
    Longer description if needed.
    
    Args:
        param1: Description
        param2: Description
    
    Returns:
        dict: Description
    """
```

- Update relevant markdown files in `docs/`

## Commit Guidelines

Follow conventional commits:

```
feat: Add new feature
fix: Fix bug
docs: Update documentation
test: Add tests
refactor: Refactor code
style: Format code
```

Example:
```
feat: Add support for handling categorical datetime columns

- Implement TimeCategories class
- Add unit tests
- Update documentation
```

## Pull Request Process

1. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**:
   - Clear title and description
   - Link related issues
   - Reference any related PRs

3. **Code Review**:
   - Address feedback
   - Keep commits clean
   - Update based on comments

4. **Merge**:
   - Ensure all checks pass
   - Squash commits if needed
   - Merge to main

## Areas for Contribution

- 🐛 **Bug Fixes**: Report and fix bugs
- ✨ **Features**: New analysis methods or visualizations
- 📚 **Documentation**: Improve docs and examples
- 🧪 **Tests**: Increase test coverage
- ⚡ **Performance**: Optimize code
- 🌐 **Integration**: Add support for other libraries

## Project Structure

```
datasage/
├── cleaner/          # Data cleaning logic
├── insights/         # Analysis algorithms
├── visualization/    # Chart generation
├── report/           # Report generation
├── core/             # Core utilities
└── __init__.py       # Package exports

tests/                # Test files
examples/             # Example scripts
docs/                 # Documentation
```

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Respect others' time and effort
- Focus on technical merit

## Questions?

- 📖 Check existing [documentation](../README.md)
- 🔍 Search [closed issues](https://github.com/virendravijaybamne/datasage/issues)
- 💬 Open a [discussion](https://github.com/virendravijaybamne/datasage/discussions)

---

**Thank you for contributing to DATASAGE! 🙏**
