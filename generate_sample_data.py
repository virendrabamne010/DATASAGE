import pandas as pd
import numpy as np

# Create sample dataset for testing
np.random.seed(42)

n_rows = 1000

sample_data = pd.DataFrame({
    'Age': np.random.randint(18, 80, n_rows),
    'Income': np.random.normal(50000, 15000, n_rows),
    'Experience': np.random.randint(0, 40, n_rows),
    'Score': np.random.uniform(0, 100, n_rows),
    'Department': np.random.choice(['Sales', 'IT', 'HR', 'Finance'], n_rows),
    'Performance': np.random.choice(['Low', 'Medium', 'High'], n_rows),
})

# Add some missing values
sample_data.loc[np.random.choice(sample_data.index, 50), 'Score'] = np.nan
sample_data.loc[np.random.choice(sample_data.index, 30), 'Income'] = np.nan

# Add some outliers
sample_data.loc[0, 'Income'] = 500000
sample_data.loc[1, 'Age'] = 150

sample_data.to_csv('tests/fixtures/sample_data.csv', index=False)
print("✅ Sample data created: tests/fixtures/sample_data.csv")
