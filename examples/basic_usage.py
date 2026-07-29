"""
DATASAGE Basic Usage Example

This script demonstrates basic usage of the DATASAGE library
for a quick, end-to-end analysis of a dataset.

Run: python examples/basic_usage.py
"""

import pandas as pd
import numpy as np
from datasage import Analyzer

# ============================================================================
# STEP 1: Create or Load Sample Data
# ============================================================================
print("=" * 60)
print("DATASAGE - Basic Usage Example")
print("=" * 60)

# For this example, create sample data
np.random.seed(42)
data = pd.DataFrame({
    'Age': np.random.randint(20, 65, 500),
    'Salary': np.random.normal(60000, 20000, 500),
    'Experience': np.random.randint(0, 30, 500),
    'Department': np.random.choice(['Sales', 'IT', 'HR', 'Finance'], 500),
    'Performance_Score': np.random.uniform(1, 5, 500),
})

# Add some missing values and outliers
data.loc[np.random.choice(data.index, 20), 'Salary'] = np.nan
data.loc[0, 'Salary'] = 500000  # Outlier

print("\n📂 Dataset loaded")
print(f"   Shape: {data.shape}")
print(f"   Columns: {data.columns.tolist()}\n")

# ============================================================================
# STEP 2: Initialize Analyzer
# ============================================================================
analyzer = Analyzer(data)
print("✅ Analyzer initialized\n")

# ============================================================================
# STEP 3: Clean Data
# ============================================================================
print("🧹 Cleaning data...")
analyzer.clean(
    handle_missing='mean',
    handle_outliers=True,
    outlier_strategy='cap',
    remove_duplicates=True
)

print(f"   Cleaning stats: {analyzer.cleaning_stats}\n")

# ============================================================================
# STEP 4: Analyze Data
# ============================================================================
print("📊 Performing analysis...")
insights = analyzer.analyze()

print(f"\n   ✓ Statistics computed")
print(f"   ✓ Correlations found: {len(insights.get('correlations', []))} high correlations")
print(f"   ✓ Categories analyzed")
print(f"   ✓ Trends detected\n")

# Print sample insights
if insights.get('statistics'):
    print("📈 Sample Statistics (Age column):")
    age_stats = insights['statistics'].get('Age', {})
    for key, value in list(age_stats.items())[:3]:
        print(f"   {key}: {value}")

if insights.get('correlations'):
    print("\n🔗 High Correlations Found:")
    for corr in insights['correlations'][:2]:
        print(f"   {corr['variable1']} ↔ {corr['variable2']}: {corr['correlation']}")

# ============================================================================
# STEP 5: Generate Visualizations
# ============================================================================
print("\n📈 Generating visualizations...")
analyzer.visualize(output_dir='./examples/output')
print("   Saved to: ./examples/output")

# ============================================================================
# STEP 6: Generate Report
# ============================================================================
print("\n📄 Generating reports...")
analyzer.generate_report(
    filepath='./examples/output/analysis_report.pdf',
    format='pdf',
    include_charts=True
)
analyzer.generate_report(
    filepath='./examples/output/analysis_report.txt',
    format='text'
)
print("   ✓ PDF Report: ./examples/output/analysis_report.pdf")
print("   ✓ Text Report: ./examples/output/analysis_report.txt")

print("\n" + "=" * 60)
print("✅ Analysis Complete!")
print("=" * 60)
print("\nCheck the ./examples/output folder for results.\n")
