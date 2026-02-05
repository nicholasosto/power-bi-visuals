# Python Visual Best Practices

Guidelines for creating effective and maintainable Python visuals in Power BI.

## Performance Optimization

### 1. Minimize Data Processing
```python
# BAD: Processing data multiple times
for col in dataset.columns:
    dataset[col].mean()
    dataset[col].std()

# GOOD: Cache calculations
summary_stats = dataset.describe()
```

### 2. Limit Data Rows
Power BI Python visuals work best with:
- Less than 150,000 rows for simple visualizations
- Less than 50,000 rows for complex visualizations

Use Power BI's filtering and aggregation before passing data to Python.

### 3. Optimize Figure Size
```python
# Choose appropriate figure size
fig, ax = plt.subplots(figsize=(10, 6))  # Good for most cases
# Avoid very large figures that slow rendering
```

## Code Quality

### 1. Handle Missing Data
```python
# Always check for and handle missing values
dataset = dataset.dropna()  # or
dataset = dataset.fillna(0)

# Check data types
print(dataset.dtypes)
```

### 2. Use Consistent Styling
```python
# Define a consistent color palette
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'warning': '#ffbb00'
}

# Use consistent font sizes
FONT_SIZES = {
    'title': 14,
    'label': 12,
    'tick': 10
}
```

### 3. Add Error Handling
```python
try:
    # Your visualization code
    ax.plot(dataset['Date'], dataset['Value'])
except KeyError as e:
    print(f"Missing column: {e}")
    ax.text(0.5, 0.5, f'Error: Missing column {e}',
            ha='center', va='center', transform=ax.transAxes)
except Exception as e:
    print(f"Error: {e}")
    ax.text(0.5, 0.5, 'Error creating visualization',
            ha='center', va='center', transform=ax.transAxes)
```

## Visualization Design

### 1. Keep It Simple
- Focus on one message per visual
- Avoid cluttered charts with too many elements
- Use legends only when necessary

### 2. Use Appropriate Chart Types
- **Bar/Column**: Comparing categories
- **Line**: Showing trends over time
- **Scatter**: Showing relationships between variables
- **Box Plot**: Showing distributions and outliers

### 3. Make It Readable
```python
# Good practices for readability
ax.set_xlabel('X Label', fontsize=12, fontweight='bold')
ax.set_ylabel('Y Label', fontsize=12, fontweight='bold')
ax.set_title('Clear, Descriptive Title', fontsize=14, fontweight='bold')

# Rotate labels if needed
plt.xticks(rotation=45, ha='right')

# Add gridlines for easier reading
ax.grid(True, alpha=0.3, linestyle='--')

# Use tight layout to prevent label cutoff
plt.tight_layout()
```

## Data Handling

### 1. Column Name Best Practices
```python
# Check available columns
print("Available columns:", dataset.columns.tolist())

# Use case-insensitive column matching
def get_column(df, name):
    """Get column case-insensitively"""
    for col in df.columns:
        if col.lower() == name.lower():
            return col
    raise KeyError(f"Column {name} not found")

date_col = get_column(dataset, 'date')
```

### 2. Date Handling
```python
# Convert to datetime
dataset['Date'] = pd.to_datetime(dataset['Date'])

# Sort by date
dataset = dataset.sort_values('Date')

# Format dates for display
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
```

### 3. Categorical Data
```python
# Sort categories logically
if 'Category' in dataset.columns:
    order = ['Low', 'Medium', 'High']  # Custom order
    dataset['Category'] = pd.Categorical(dataset['Category'],
                                          categories=order,
                                          ordered=True)
    dataset = dataset.sort_values('Category')
```

## Debugging

### 1. Print Debug Information
```python
# Print at the start of your script
print(f"Dataset shape: {dataset.shape}")
print(f"Columns: {dataset.columns.tolist()}")
print(f"Data types:\n{dataset.dtypes}")
print(f"First few rows:\n{dataset.head()}")
print(f"Missing values:\n{dataset.isnull().sum()}")
```

### 2. Test Locally First
Always test your scripts locally before using in Power BI:
1. Create sample data that matches your Power BI dataset
2. Run the script from the command line
3. Verify the output looks correct
4. Then copy to Power BI

### 3. Handle Edge Cases
```python
# Check for empty dataset
if dataset.empty:
    ax.text(0.5, 0.5, 'No data available',
            ha='center', va='center', transform=ax.transAxes,
            fontsize=14)
    plt.show()
    exit()

# Check for minimum data points
if len(dataset) < 2:
    print("Warning: Insufficient data points")
```

## Security Considerations

1. **Never include sensitive credentials in scripts**
2. **Validate data before processing**
3. **Avoid executing arbitrary code strings**
4. **Keep dependencies updated**

## Reusability

### Create Helper Functions
```python
def setup_plot_style(ax, title, xlabel, ylabel):
    """Apply consistent styling to plots"""
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')

# Usage
fig, ax = plt.subplots(figsize=(10, 6))
setup_plot_style(ax, 'Sales by Region', 'Region', 'Sales ($)')
```

### Use Configuration Dictionaries
```python
CHART_CONFIG = {
    'figure_size': (10, 6),
    'title_size': 14,
    'label_size': 12,
    'grid_alpha': 0.3,
    'primary_color': '#1f77b4'
}

fig, ax = plt.subplots(figsize=CHART_CONFIG['figure_size'])
ax.set_title('Title', fontsize=CHART_CONFIG['title_size'])
```

## Version Control

When working in a team:
1. Save scripts as separate `.py` files
2. Use git for version control
3. Include docstrings explaining required columns
4. Document any special requirements or dependencies

## Resources

- Matplotlib gallery: https://matplotlib.org/stable/gallery/index.html
- Pandas documentation: https://pandas.pydata.org/docs/
- Power BI Python visuals: https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-python-visuals
