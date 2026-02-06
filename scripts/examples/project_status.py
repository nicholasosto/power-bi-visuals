import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import pandas as pd
from datetime import datetime
import numpy as np

# Power BI provides data in a 'dataset' dataframe
# This script handles multiple column naming conventions and Power BI's aggregation behavior

# For local testing: create sample data if 'dataset' is not defined
if 'dataset' not in dir():
    dataset = pd.DataFrame({
        'Project Start Date': [pd.Timestamp('2025-01-15')],
        'Actual Start Date': [pd.Timestamp('2025-01-22')],
        'Sum of BAR Budget': [500000],
        'Sum of Scheduled Revenue': [350000],
        'Sum of Billed Billing Adjusted Revenue': [125000]
    })

# Helper function to find column by partial match
def find_column(df, patterns):
    """Find first column matching any of the patterns (case-insensitive)"""
    for pattern in patterns:
        for col in df.columns:
            if pattern.lower() in col.lower():
                return col
    return None

# Find the relevant columns (handles "Sum of" prefix and various naming)
project_start_col = find_column(dataset, ['Project Start Date', 'ProjectStartDate'])
actual_start_col = find_column(dataset, ['Actual Start Date', 'ActualStartDate'])
budget_col = find_column(dataset, ['BAR Budget', 'TotalBudget', 'Budget'])
scheduled_col = find_column(dataset, ['Scheduled Revenue', 'ScheduledRevenue'])
actual_col = find_column(dataset, ['Billed Billing Adjusted Revenue', 'Actual Revenue', 'ActualRevenue'])

# Get the first row of data (Power BI often aggregates to one row per filter context)
if len(dataset) > 0:
    row = dataset.iloc[0]
    
    # Extract values with fallbacks
    try:
        project_start = pd.to_datetime(row[project_start_col]) if project_start_col else pd.Timestamp('2025-01-01')
    except:
        project_start = pd.Timestamp('2025-01-01')
    
    try:
        actual_start = pd.to_datetime(row[actual_start_col]) if actual_start_col else pd.Timestamp('2025-01-01')
    except:
        actual_start = pd.Timestamp('2025-01-01')
    
    total_budget = float(row[budget_col]) if budget_col else 1
    scheduled_revenue = float(row[scheduled_col]) if scheduled_col else 0
    actual_revenue = float(row[actual_col]) if actual_col else 0
    
    # Prevent division by zero
    if total_budget == 0:
        total_budget = 1
    
    # Calculate day difference
    day_diff = (actual_start - project_start).days
    diff_text = f"+{day_diff} days" if day_diff >= 0 else f"{day_diff} days"
    
    # Calculate percentages
    actual_percent = (actual_revenue / total_budget) * 100
    scheduled_percent = (scheduled_revenue / total_budget) * 100
    unscheduled_percent = 100 - scheduled_percent
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Bar parameters
    bar_y = 4
    bar_height = 2
    
    # Draw unscheduled portion (striped pattern)
    unscheduled_start = scheduled_percent
    unscheduled_width = unscheduled_percent
    
    # Create hatched rectangle for unscheduled
    unscheduled_rect = Rectangle(
        (unscheduled_start, bar_y), 
        unscheduled_width, 
        bar_height,
        facecolor='#f3f4f6',
        edgecolor='#d1d5db',
        linewidth=2,
        hatch='///',
        fill=True
    )
    ax.add_patch(unscheduled_rect)
    
    # Draw scheduled amount (light green)
    scheduled_rect = Rectangle(
        (0, bar_y), 
        scheduled_percent, 
        bar_height,
        facecolor='#86efac',
        edgecolor='#d1d5db',
        linewidth=2
    )
    ax.add_patch(scheduled_rect)
    
    # Draw actual amount (dark green)
    actual_rect = Rectangle(
        (0, bar_y), 
        actual_percent, 
        bar_height,
        facecolor='#15803d',
        edgecolor='#d1d5db',
        linewidth=2
    )
    ax.add_patch(actual_rect)
    
    # Add date indicator lines (you can adjust positions as needed)
    # For demo, placing at 15% and 35%
    project_line_pos = 15
    actual_line_pos = 35
    
    ax.plot([project_line_pos, project_line_pos], [bar_y, bar_y + bar_height], 
            color='#2563eb', linewidth=3, label='Project Start')
    ax.plot([actual_line_pos, actual_line_pos], [bar_y, bar_y + bar_height], 
            color='#9333ea', linewidth=3, label='Actual Start')
    
    # Day difference badge
    badge_color = '#fee2e2' if day_diff > 0 else '#dcfce7' if day_diff < 0 else '#f3f4f6'
    text_color = '#991b1b' if day_diff > 0 else '#166534' if day_diff < 0 else '#374151'
    
    ax.text(50, bar_y + bar_height + 1, diff_text,
            ha='center', va='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=badge_color, 
                     edgecolor='none'), color=text_color)
    
    # Add title
    ax.text(50, 9, 'Project Status Bar', 
            ha='center', va='top', fontsize=16, fontweight='bold')
    
    # Add date labels
    ax.text(project_line_pos, bar_y - 0.5, 
            f"Project: {project_start.strftime('%Y-%m-%d')}", 
            ha='center', va='top', fontsize=9, color='#2563eb')
    ax.text(actual_line_pos, bar_y - 0.5, 
            f"Actual: {actual_start.strftime('%Y-%m-%d')}", 
            ha='center', va='top', fontsize=9, color='#9333ea')
    
    # Legend at bottom
    legend_y = 2
    
    # Format currency
    def format_currency(amount):
        return f"${amount:,.0f}"
    
    ax.text(10, legend_y, f"● Actual: {format_currency(actual_revenue)} ({actual_percent:.1f}%)",
            fontsize=10, color='#15803d', fontweight='bold')
    ax.text(40, legend_y, f"● Scheduled: {format_currency(scheduled_revenue)} ({scheduled_percent:.1f}%)",
            fontsize=10, color='#86efac', fontweight='bold')
    ax.text(72, legend_y, f"▨ Unscheduled: {format_currency(total_budget - scheduled_revenue)} ({unscheduled_percent:.1f}%)",
            fontsize=10, color='#6b7280', fontweight='bold')
    
    # Summary stats at bottom
    stats_y = 0.5
    col_width = 25
    
    ax.text(0, stats_y, f"Total Budget\n{format_currency(total_budget)}", 
            fontsize=9, ha='left', va='center', color='#374151')
    ax.text(col_width, stats_y, f"Remaining\n{format_currency(total_budget - scheduled_revenue)}", 
            fontsize=9, ha='left', va='center', color='#374151')
    ax.text(col_width*2, stats_y, f"Variance\n{format_currency(scheduled_revenue - actual_revenue)}", 
            fontsize=9, ha='left', va='center', color='#374151')
    ax.text(col_width*3, stats_y, f"Completion\n{actual_percent:.1f}%", 
            fontsize=9, ha='left', va='center', color='#374151')
    
    plt.tight_layout()
    plt.show()
else:
    # No data message
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.text(0.5, 0.5, 'No data available', 
            ha='center', va='center', fontsize=14, color='#6b7280')
    ax.axis('off')
    plt.show()