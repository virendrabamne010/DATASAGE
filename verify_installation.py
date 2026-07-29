#!/usr/bin/env python
"""Quick test script to verify DATASAGE installation."""

import sys
import os

# Add DATASAGE to path
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("DATASAGE Installation Verification")
print("=" * 60)

try:
    print("\n🔍 Checking imports...")
    
    # Test main import
    from datasage import Analyzer
    print("  ✅ Analyzer imported")
    
    # Test sub-modules
    from datasage.cleaner import MissingValueHandler, OutlierDetector
    print("  ✅ Cleaner modules imported")
    
    from datasage.insights import CorrelationAnalyzer, StatisticsAnalyzer
    print("  ✅ Insights modules imported")
    
    from datasage.visualization import ChartGenerator, HeatmapGenerator
    print("  ✅ Visualization modules imported")
    
    from datasage.report import TextReportGenerator, PDFReportGenerator
    print("  ✅ Report modules imported")
    
    # Check version
    from datasage import __version__
    print(f"\n📦 DATASAGE Version: {__version__}")
    
    # Try basic functionality
    print("\n🧪 Testing basic functionality...")
    import pandas as pd
    import numpy as np
    
    # Create sample data
    df = pd.DataFrame({
        'A': np.random.randn(100),
        'B': np.random.randn(100),
        'C': ['X', 'Y'] * 50
    })
    
    # Test Analyzer initialization
    analyzer = Analyzer(df)
    print("  ✅ Analyzer initialized with sample data")
    
    # Test info method
    info = analyzer.info()
    print(f"  ✅ Dataset info retrieved: {info['shape']}")
    
    # Test clean
    analyzer.clean()
    print("  ✅ Data cleaning completed")
    
    print("\n" + "=" * 60)
    print("✅ ALL CHECKS PASSED!")
    print("=" * 60)
    print("\nDATASAGE is ready to use! 🎉\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
