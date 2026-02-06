# Budget Health Dashboard - Report Setup Guide

## Overview

This guide walks through setting up your Power BI Budget Health Dashboard that connects to Projector PSA data and displays project budget status with custom Python visuals.

---

## Report Structure

```
┌─────────────────────────────────────────────────────────────────────┐
│  BUDGET HEALTH DASHBOARD                      📅 As of: Feb 5, 2026 │
├──────────┬──────────┬──────────┬──────────┬─────────────────────────┤
│ 📊 Total │ 🟢 Green │ 🟡 Yellow│ 🔴 Red   │ Budget Utilization      │
│ 10 Proj  │ 4        │ 4        │ 2        │ ████████░░ 53.5%        │
├──────────┴──────────┴──────────┴──────────┴─────────────────────────┤
│                                                                      │
│   [Python Visual: 6-Month Budget Health Rolling Forecast]            │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│ Alert │ Project Name         │ Budget   │ Actual   │ Variance       │
│ 🔴    │ Cloud Infrastructure │ $300K    │ $275K    │ +$30K (10%)    │
│ 🔴    │ API Gateway          │ $180K    │ $165K    │ +$15K (8%)     │
│ 🟡    │ ERP Implementation   │ $500K    │ $85K     │ -$25K (-5%)    │
│ 🟡    │ Data Migration       │ $80K     │ $15K     │ $0 (0%)        │
│ ...   │                      │          │          │                │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Data Source Setup

### Option A: CSV Import (Quick Start)

1. Run the Projector API connector script:
   ```powershell
   cd "E:\Astrix Code\power-bi-visuals"
   python scripts/data_connectors/projector_api_connector.py
   ```

2. In Power BI Desktop:
   - **Get Data** → **Text/CSV**
   - Navigate to `data/projector_exports/budget_health_data.csv`
   - Click **Load**

### Option B: API Direct Connection (Production)

1. Set environment variables:
   ```powershell
   $env:PROJECTOR_API_KEY = "your_api_key"
   $env:PROJECTOR_API_URL = "https://your-instance.projectorpsa.com"
   ```

2. In Power BI Desktop:
   - **Get Data** → **Web**
   - Enter API URL: `https://your-instance.projectorpsa.com/api/v2/reports/portfolio-performance`
   - Add Authorization header with your API key

3. Schedule refresh in Power BI Service (every 2 weeks per your preference)

---

## Step 2: DAX Measures (Already Created!)

Your report now has **18 DAX measures** organized into folders:

### KPI Cards Folder
| Measure | Description | Format |
|---------|-------------|--------|
| Total Projects | Count of all projects | 0 |
| Green Projects | Healthy status count | 0 |
| Yellow Projects | Warning status count | 0 |
| Red Projects | At-risk status count | 0 |
| Total Budget | Sum of all budgets | $#,##0 |
| Total Actual Revenue | Revenue earned to date | $#,##0 |
| Budget Utilization % | Actual/Budget ratio | 0.0% |
| At-Risk Project Count | Yellow + Red | 0 |

### Budget Analysis Folder
| Measure | Description | Format |
|---------|-------------|--------|
| Total Scheduled Revenue 6M | 6-month forecast total | $#,##0 |
| Total Actual Revenue 3M | Last 3 months actual | $#,##0 |
| Budget Variance 3M | Actual - Scheduled (3M) | $#,##0 |
| Budget Variance % 3M | Variance as percentage | 0.0% |
| Remaining Budget | Total - Actual | $#,##0 |
| Avg Project Budget | Average per project | $#,##0 |
| Budget Health Score | % Green projects | 0% |

### Monthly Breakdown Folder
| Measure | Description | Format |
|---------|-------------|--------|
| Actual M1 | Month 1 actual revenue | $#,##0 |
| Actual M2 | Month 2 actual revenue | $#,##0 |
| Actual M3 | Month 3 actual revenue | $#,##0 |

---

## Step 3: Building the Report Page

### Row 1: KPI Cards

1. Insert **Card** visual
2. Add measure: `Total Projects`
3. Duplicate and change to `Green Projects`, `Yellow Projects`, `Red Projects`
4. Format each card with corresponding colors:
   - Green: #28A745
   - Yellow: #FFC107
   - Red: #DC3545

5. Add **Gauge** visual for Budget Utilization:
   - Value: `Budget Utilization %`
   - Maximum: 1 (100%)

### Row 2: Python Visual (6-Month Forecast)

1. Insert **Python visual** from Visualizations pane
2. Drag these fields to **Values**:
   - ProjectName
   - TotalBudget
   - ActualBillingAdjustedRevenueToDate
   - ScheduledRevenue_Month1 through Month6
   - ActualRevenue_Month1 through Month3
   - HoursBudgetAlertLevel

3. Paste the script from: `scripts/examples/budget_health_visual.py`

### Row 3: Project Table

1. Insert **Table** visual
2. Add columns:
   - HoursBudgetAlertLevel (rename to "Alert")
   - ProjectName
   - TotalBudget
   - ActualBillingAdjustedRevenueToDate (rename to "Actual")
   - Budget Variance 3M (measure)
   - Budget Variance % 3M (measure)

3. Apply conditional formatting to Alert column:
   - Rules based on text values (Green/Yellow/Red)

4. Sort by Alert Level (Red first) or Variance % descending

---

## Step 4: Formatting & Polish

### Report Title
- Add Text Box: "Budget Health Dashboard"
- Font: Segoe UI Semibold, 24pt
- Add date slicer or text showing last refresh date

### Color Theme
```json
{
  "dataColors": [
    "#28A745",  // Green - Healthy
    "#FFC107",  // Yellow - Warning  
    "#DC3545",  // Red - At Risk
    "#17A2B8",  // Info accent
    "#6C757D"   // Secondary/neutral
  ]
}
```

### Filters
- Add **Slicer** for HoursBudgetAlertLevel
- Optional: Date range slicer if you add a date dimension

---

## Step 5: Publish & Schedule

### Publish to Power BI Service
1. **File** → **Publish** → **Publish to Power BI**
2. Select your workspace

### Schedule Refresh (Bi-Weekly)
1. Open dataset settings in Power BI Service
2. **Scheduled refresh** → Enable
3. Set frequency: Every 2 weeks
4. Configure data source credentials

### Gateway Setup (if needed)
- If data source is on-premises, install Power BI Gateway
- Configure gateway connection for CSV files or API

---

## File Reference

| File | Purpose |
|------|---------|
| `scripts/data_connectors/projector_api_connector.py` | Fetches data from Projector API |
| `scripts/examples/budget_health_visual.py` | Python visual for 6-month forecast |
| `scripts/examples/project_status.py` | Simpler budget status bar chart |
| `data/projector_exports/budget_health_data.csv` | Exported budget data (generated) |
| `data/projector_exports/kpi_summary.csv` | Summary metrics (generated) |
| `docs/PROJECTOR_PSA_REPORTING_FIELDS.md` | Complete API field reference |

---

## Troubleshooting

### Python Visual Shows "Can't display this visual"
- Ensure Python is installed: `C:\Python312\python.exe`
- Install packages: `pip install --user matplotlib pandas`
- Check Power BI Options → Python scripting path

### Data Not Refreshing
- Verify API credentials in environment variables
- Check network connectivity to Projector instance
- Review refresh history in Power BI Service for errors

### Measures Show Blank
- Ensure BudgetForecast table has data (check Data view)
- Verify column names match exactly (case-sensitive)

---

## Next Steps

1. **Test locally** with sample data (already loaded)
2. **Configure API credentials** when ready for production
3. **Add drill-through page** for individual project details
4. **Create mobile layout** for on-the-go viewing
5. **Set up alerts** in Power BI Service for Red status projects

Need help? The Python scripts include detailed comments and fallback sample data generation for testing.
