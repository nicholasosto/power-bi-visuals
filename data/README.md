# Sample Data Files

This directory contains sample datasets for testing Python visuals locally before using them in Power BI.

## Included Samples

- `sales_data.csv` - Sample sales data with dates, categories, and values
- (Add your own data files here for testing)

## Using Sample Data

To test your Python visuals locally:

1. Load the sample data in your script:
```python
import pandas as pd

# When testing locally
dataset = pd.read_csv('data/sales_data.csv')

# In Power BI, the dataset is provided automatically
# dataset = dataset  # Already available
```

2. Run your script from the command line:
```bash
python scripts/examples/your_script.py
```

## Creating Your Own Sample Data

You can create CSV files that match the structure of your Power BI data:

```python
import pandas as pd

# Create sample data
data = pd.DataFrame({
    'Date': pd.date_range('2024-01-01', periods=30, freq='D'),
    'Category': ['A', 'B', 'C'] * 10,
    'Value': range(30)
})

# Save to CSV
data.to_csv('data/my_sample.csv', index=False)
```

## Data Privacy Note

Add large or sensitive data files to `.gitignore` if you're using version control.
