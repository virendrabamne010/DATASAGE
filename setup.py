"""
Setup configuration for DATASAGE.

This file defines how the package is built and distributed.
Uses the modern pyproject.toml approach.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="datasage",
    version="0.1.0",
    author="Virendra Vijay Bamne",
    author_email="virendrabamne@gmail.com",
    description="Automated data analytics library for insights, visualizations, and reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/virendravijaybamne/datasage",
    project_urls={
        "Bug Tracker": "https://github.com/virendravijaybamne/datasage/issues",
        "Documentation": "https://github.com/virendravijaybamne/datasage#readme",
        "Source Code": "https://github.com/virendravijaybamne/datasage",
        "Changelog": "https://github.com/virendravijaybamne/datasage/blob/main/CHANGELOG.md",
    },
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "pandas>=1.3.0,<3.0",
        "numpy>=1.21.0,<3.0",
        "matplotlib>=3.4.0,<4.0",
        "seaborn>=0.11.0,<1.0",
        "scipy>=1.7.0,<2.0",
        "reportlab>=3.6.0,<5.0",
        "openpyxl>=3.0.0,<4.0",
        "xlrd>=2.0.0,<3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.900",
            "isort>=5.0",
        ],
        "app": [
            "streamlit>=1.30.0",
            "altair>=5.0.0",
        ],
        "all": [
            "streamlit>=1.30.0",
            "altair>=5.0.0",
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.900",
            "isort>=5.0",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="data-analysis insights visualization reporting pandas data-cleaning data-profiling",
    license="MIT",
)