# Power BI Python Visuals Workspace

This workspace is set up for creating Python-based visualizations for Power BI using matplotlib and pandas.

## Prerequisites

- Python 3.8 or higher
- Power BI Desktop (latest version)
- Basic knowledge of Python and matplotlib

## Quick Start

### 1. Initial Setup

Run the setup script to create a virtual environment and install dependencies:

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### 2. Configure Power BI Desktop for Python

1. Open Power BI Desktop
2. Go to **File** → **Options and settings** → **Options**
3. Under **Global** section, select **Python scripting**
4. Set the Python home directory to your virtual environment:
   - Windows: `[workspace-path]\venv`
   - Linux/Mac: `[workspace-path]/venv`
5. Click **OK** to save

### 3. Using Python Visuals in Power BI

1. Load your data into Power BI
2. Click on the **Python visual** icon in the Visualizations pane
3. Add the fields you want to visualize to the **Values** section
4. In the Python script editor that appears, write or paste your Python code
5. Click the **Run** button (play icon) to execute the script

## Project Structure

```
power-bi-visuals/
├── scripts/
│   ├── examples/          # Sample Python visual scripts
│   │   ├── bar_chart.py
│   │   ├── line_chart.py
│   │   └── scatter_plot.py
│   └── templates/         # Template files for new visuals
│       └── basic_template.py
├── data/                  # Sample data files
├── docs/                  # Additional documentation
├── requirements.txt       # Python dependencies
├── setup.bat             # Windows setup script
└── setup.sh              # Linux/Mac setup script
```

## Example Scripts

### Bar Chart (scripts/examples/bar_chart.py)
Creates a simple bar chart from categorical data.
- Required columns: `Category`, `Value`

### Line Chart (scripts/examples/line_chart.py)
Creates a time series line chart with optional multiple series.
- Required columns: `Date`, `Value`
- Optional: `Category` (for multiple lines)

### Scatter Plot (scripts/examples/scatter_plot.py)
Creates a scatter plot with trend line and optional bubble sizing.
- Required columns: `X`, `Y`
- Optional: `Size`, `Category`

## Creating Your Own Visuals

1. Start with the template in `scripts/templates/basic_template.py`
2. Power BI automatically provides your data as a pandas DataFrame named `dataset`
3. Use matplotlib to create your visualization
4. Always end with `plt.show()` to display the visual

### Important Notes

- Power BI passes data as a DataFrame named `dataset`
- Any columns you add to the Values field become columns in the `dataset`
- The script must call `plt.show()` to display the visualization
- Print statements will appear in the output window (useful for debugging)

## Testing Scripts Locally

To test your scripts outside Power BI:

1. Activate the virtual environment:
   - Windows: `venv\Scripts\activate.bat`
   - Linux/Mac: `source venv/bin/activate`

2. Uncomment the sample data section in the script

3. Run the script:
   ```bash
   python scripts/examples/bar_chart.py
   ```

## Common Issues and Solutions

### Python not detected in Power BI
- Make sure you've set the correct Python home directory in Power BI options
- Restart Power BI Desktop after setting the Python directory

### Missing module errors
- Ensure you've activated the virtual environment before installing packages
- Run `pip install -r requirements.txt` again

### Visual not displaying
- Check that your script ends with `plt.show()`
- Look for error messages in the output pane
- Verify column names match what your script expects

### Data type issues
- Use `print(dataset.dtypes)` to check column data types
- Convert data types as needed (e.g., `pd.to_datetime()` for dates)

## Tips for Better Visuals

1. **Keep it Simple**: Complex visuals may be slow to render in Power BI
2. **Use Comments**: Document what your script does for future reference
3. **Handle Missing Data**: Use pandas methods to handle nulls and NaNs
4. **Consistent Styling**: Use consistent colors and fonts across visuals
5. **Test with Real Data**: Always test with actual data that has edge cases

## Additional Resources

- [Power BI Python Integration Documentation](https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-python-visuals)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

## License

This workspace is provided as-is for learning and development purposes.
