"""
Line Chart Example for Power BI Python Visual
This script creates a time series line chart from Power BI data.

Expected columns in dataset:
- Date: Date or datetime values
- Value: Numeric values to plot
- (Optional) Category: For multiple lines
"""

import matplotlib.pyplot as plt
import pandas as pd

# Power BI passes the dataset as a DataFrame named 'dataset'
# For testing outside Power BI, uncomment the sample data below:
# dataset = pd.DataFrame({
#     'Date': pd.date_range('2024-01-01', periods=10, freq='D'),
#     'Value': [23, 45, 56, 48, 52, 61, 58, 67, 72, 68]
# })

# Ensure Date column is datetime type
dataset['Date'] = pd.to_datetime(dataset['Date'])

# Sort by date
dataset = dataset.sort_values('Date')

# Create the plot
fig, ax = plt.subplots(figsize=(12, 6))

# Check if we have multiple categories
if 'Category' in dataset.columns:
    # Plot multiple lines
    for category in dataset['Category'].unique():
        data = dataset[dataset['Category'] == category]
        ax.plot(data['Date'], data['Value'], marker='o', label=category, linewidth=2)
    ax.legend(fontsize=10)
else:
    # Plot single line
    ax.plot(dataset['Date'], dataset['Value'], marker='o', color='steelblue', linewidth=2, markersize=6)

# Customize the plot
ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Value', fontsize=12, fontweight='bold')
ax.set_title('Time Series Line Chart', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()
