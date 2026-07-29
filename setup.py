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
    author="Data Analytics Team",
    author_email="your.email@example.com",
    description="Automated data analytics library for insights, visualizations, and reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/datasage",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/datasage/issues",
        "Documentation": "https://github.com/yourusername/datasage#readme",
        "Source Code": "https://github.com/yourusername/datasage",
    },
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "scipy>=1.7.0",
        "reportlab>=3.6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.900",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    keywords="data-analysis insights visualization reporting pandas",
    license="MIT",
)
