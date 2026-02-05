"""
Simple Bar Chart Example for Power BI Python Visual
This script creates a bar chart from the dataset passed by Power BI.

Expected columns in dataset:
- Category: Categorical data for x-axis
- Value: Numeric data for y-axis
"""

import matplotlib.pyplot as plt
import pandas as pd

# Power BI passes the dataset as a DataFrame named 'dataset'
# For testing outside Power BI, uncomment the sample data below:
# dataset = pd.DataFrame({
#     'Category': ['A', 'B', 'C', 'D', 'E'],
#     'Value': [23, 45, 56, 78, 32]
# })

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Create bar chart
ax.bar(dataset['Category'], dataset['Value'], color='steelblue', edgecolor='black')

# Customize the plot
ax.set_xlabel('Category', fontsize=12, fontweight='bold')
ax.set_ylabel('Value', fontsize=12, fontweight='bold')
ax.set_title('Bar Chart Visualization', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on top of bars
for i, v in enumerate(dataset['Value']):
    ax.text(i, v + 1, str(v), ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.show()
