"""
Scatter Plot Example for Power BI Python Visual
This script creates a scatter plot with optional trend line.

Expected columns in dataset:
- X: Numeric values for x-axis
- Y: Numeric values for y-axis
- (Optional) Size: Numeric values for bubble size
- (Optional) Category: For color coding
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Power BI passes the dataset as a DataFrame named 'dataset'
# For testing outside Power BI, uncomment the sample data below:
# dataset = pd.DataFrame({
#     'X': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
#     'Y': [2.3, 4.1, 5.8, 7.2, 9.1, 10.5, 12.3, 14.1, 15.8, 17.5],
#     'Size': [100, 150, 200, 120, 180, 160, 140, 190, 170, 210]
# })

# Create the plot
fig, ax = plt.subplots(figsize=(10, 8))

# Determine if we have size and category columns
has_size = 'Size' in dataset.columns
has_category = 'Category' in dataset.columns

if has_category:
    # Create scatter with color coding by category
    categories = dataset['Category'].unique()
    colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))

    for idx, category in enumerate(categories):
        data = dataset[dataset['Category'] == category]
        size = data['Size'] if has_size else 100
        ax.scatter(data['X'], data['Y'], s=size, alpha=0.6,
                  c=[colors[idx]], label=category, edgecolors='black', linewidth=1)
    ax.legend(fontsize=10)
else:
    # Simple scatter plot
    size = dataset['Size'] if has_size else 100
    ax.scatter(dataset['X'], dataset['Y'], s=size, alpha=0.6,
              c='steelblue', edgecolors='black', linewidth=1)

# Add trend line
z = np.polyfit(dataset['X'], dataset['Y'], 1)
p = np.poly1d(z)
ax.plot(dataset['X'], p(dataset['X']), "r--", alpha=0.8, linewidth=2, label='Trend')

# Customize the plot
ax.set_xlabel('X Variable', fontsize=12, fontweight='bold')
ax.set_ylabel('Y Variable', fontsize=12, fontweight='bold')
ax.set_title('Scatter Plot with Trend Line', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')

if not has_category:
    ax.legend(['Trend'], fontsize=10)

plt.tight_layout()
plt.show()
