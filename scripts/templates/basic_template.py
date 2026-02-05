"""
Basic Template for Power BI Python Visuals
Use this template as a starting point for creating custom Python visuals.

The 'dataset' variable is automatically provided by Power BI.
"""

import matplotlib.pyplot as plt
import pandas as pd

# Power BI automatically provides the 'dataset' DataFrame
# It contains the data you've added to the Values field in Power BI

# For local testing, create sample data:
# dataset = pd.DataFrame({
#     'Column1': [...],
#     'Column2': [...]
# })

# Print dataset info (useful for debugging)
print("Dataset shape:", dataset.shape)
print("Dataset columns:", dataset.columns.tolist())
print(dataset.head())

# Create your visualization
fig, ax = plt.subplots(figsize=(10, 6))

# Add your plotting code here
# Example: ax.plot(dataset['x'], dataset['y'])

# Customize appearance
ax.set_xlabel('X Label', fontsize=12)
ax.set_ylabel('Y Label', fontsize=12)
ax.set_title('Your Chart Title', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

# Display the plot
plt.tight_layout()
plt.show()
