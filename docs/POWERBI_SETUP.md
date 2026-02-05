# Configuring Power BI Desktop for Python

This guide walks you through setting up Power BI Desktop to use Python visuals with this workspace.

## Step 1: Locate Your Python Installation

After running the setup script, your Python environment is located in the `venv` folder within this workspace.

**Full path:**
- Windows: `e:\Astrix Code\power-bi-visuals\venv`
- The Python executable is at: `e:\Astrix Code\power-bi-visuals\venv\Scripts\python.exe`

## Step 2: Configure Power BI Desktop

1. **Open Power BI Desktop**

2. **Navigate to Options**
   - Click **File** in the top menu
   - Select **Options and settings**
   - Click **Options**

3. **Configure Python Settings**
   - In the left sidebar, under **Global**, click **Python scripting**
   - You'll see two dropdown menus:
     - **Python home directory**: Select or browse to `e:\Astrix Code\power-bi-visuals\venv`
     - **Python IDE**: (Optional) Select your preferred IDE if you want to edit scripts externally

4. **Verify Installation**
   - Power BI should detect the Python installation automatically
   - If you see a green checkmark or "Detected", you're all set
   - Click **OK** to save your settings

5. **Restart Power BI Desktop** (recommended)
   - Close and reopen Power BI Desktop to ensure settings take effect

## Step 3: Test Your Configuration

1. **Create a Test Visual**
   - Open a new or existing Power BI report
   - Click the **Python visual** icon in the Visualizations pane (looks like a Python logo)
   - You'll see a Python script editor appear at the bottom

2. **Run a Test Script**
   - Paste this simple test code:
   ```python
   import matplotlib.pyplot as plt
   import pandas as pd

   # Test data
   data = pd.DataFrame({'x': [1, 2, 3, 4, 5], 'y': [2, 4, 6, 8, 10]})

   plt.figure(figsize=(8, 6))
   plt.plot(data['x'], data['y'], marker='o')
   plt.title('Test Visual')
   plt.show()
   ```
   - Click the **Run script** button (play icon)
   - If you see a line chart, your setup is working correctly!

## Troubleshooting

### Issue: "Python installation not detected"

**Solution:**
- Verify that you've run the `setup.bat` or `setup.sh` script
- Check that the `venv` folder exists in your workspace
- Make sure you're pointing to the `venv` folder, not `venv\Scripts`

### Issue: "Module not found" errors

**Solution:**
- Ensure all dependencies are installed by running:
  ```bash
  venv\Scripts\activate.bat
  pip install -r requirements.txt
  ```

### Issue: Visual shows an error or blank screen

**Solution:**
- Check the **Output** pane in Power BI for error messages
- Verify your script ends with `plt.show()`
- Make sure there are no syntax errors in your Python code

### Issue: Old Python version detected

**Solution:**
- Uninstall or deactivate other Python installations
- Or specify the exact path: `e:\Astrix Code\power-bi-visuals\venv\Scripts\python.exe`

## Security Settings

Power BI may show security warnings about running Python scripts:

- Click **Enable** or **Allow** when prompted
- This is normal for Python visuals
- Scripts only run locally on your machine

## Next Steps

Once configured, you can:
- Use the example scripts in `scripts/examples/`
- Create your own custom visuals using `scripts/templates/basic_template.py`
- Import real data and build powerful Python-based visualizations

For more information, see the main [README.md](../README.md) file.
