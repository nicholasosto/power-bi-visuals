import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ============================================================================
# PROJECTOR PSA - Rolling 6-Month Budget Health Visual
# ============================================================================
# Shows project budget consumption over a rolling 6-month period with:
# - Monthly demarcation lines
# - Scheduled vs Unscheduled revenue/time
# - Visual indication of budget overrun risk
# ============================================================================

# For local testing
if 'dataset' not in dir():
    dataset = pd.DataFrame({
        'ProjectName': ['Website Redesign'],
        'ProjectStartDate': [pd.Timestamp('2026-01-01')],
        'ProjectEndDate': [pd.Timestamp('2026-06-30')],
        'TotalBudget': [120000],
        'ActualBillingAdjustedRevenueToDate': [45000],
        'ScheduledRevenue_Month1': [20000],
        'ScheduledRevenue_Month2': [20000],
        'ScheduledRevenue_Month3': [20000],
        'ScheduledRevenue_Month4': [20000],
        'ScheduledRevenue_Month5': [10000],
        'ScheduledRevenue_Month6': [0],
        'ActualRevenue_Month1': [20000],
        'ActualRevenue_Month2': [20000],
        'ActualRevenue_Month3': [5000],
        'HoursBudgetAlertLevel': ['Green']
    })

# Helper to find columns
def find_col(df, patterns):
    for p in patterns:
        for c in df.columns:
            if p.lower() in c.lower():
                return c
    return None

# Color scheme
COLORS = {
    'actual': '#15803d',           # Dark green - actual revenue
    'scheduled': '#86efac',        # Light green - scheduled revenue
    'unscheduled': '#fef3c7',      # Light yellow - unscheduled (warning)
    'overbudget': '#fee2e2',       # Light red - over budget zone
    'month_line': '#6b7280',       # Gray - month demarcation
    'today_line': '#2563eb',       # Blue - today marker
    'text': '#374151',             # Dark gray text
    'green': '#22c55e',
    'yellow': '#eab308',
    'red': '#ef4444'
}

# Get current date for "today" marker
today = datetime.now()
report_end = today + timedelta(days=180)  # Rolling 6 months

if len(dataset) > 0:
    row = dataset.iloc[0]
    
    # Extract project info
    project_name = row.get('ProjectName', row.get('Project', 'Project'))
    
    # Budget fields
    total_budget = float(row.get('TotalBudget', row.get('BudgetedBillingAdjustedRevenueAtCompletion', 100000)))
    actual_revenue = float(row.get('ActualBillingAdjustedRevenueToDate', row.get('ActualRevenue', 0)))
    
    # Get monthly scheduled amounts
    monthly_scheduled = []
    for i in range(1, 7):
        col = f'ScheduledRevenue_Month{i}'
        if col in row.index:
            monthly_scheduled.append(float(row[col]))
        else:
            monthly_scheduled.append(0)
    
    # Get monthly actuals
    monthly_actuals = []
    for i in range(1, 7):
        col = f'ActualRevenue_Month{i}'
        if col in row.index:
            monthly_actuals.append(float(row[col]))
        else:
            monthly_actuals.append(0)
    
    # Get project dates
    try:
        project_start = pd.to_datetime(row.get('ProjectStartDate', today - timedelta(days=60)))
        project_end = pd.to_datetime(row.get('ProjectEndDate', today + timedelta(days=120)))
    except:
        project_start = today - timedelta(days=60)
        project_end = today + timedelta(days=120)
    
    # Alert level
    alert_level = str(row.get('HoursBudgetAlertLevel', 'Green')).lower()
    
    # Calculate totals
    total_scheduled = sum(monthly_scheduled)
    total_actual = sum(monthly_actuals)
    total_unscheduled = max(0, total_budget - total_scheduled)
    
    # Percentages
    if total_budget > 0:
        actual_pct = (actual_revenue / total_budget) * 100
        scheduled_pct = (total_scheduled / total_budget) * 100
        unscheduled_pct = 100 - scheduled_pct
    else:
        actual_pct = scheduled_pct = unscheduled_pct = 0
    
    # Check for budget overrun
    is_over_budget = actual_revenue > total_scheduled or sum(monthly_actuals) > sum(monthly_scheduled[:len(monthly_actuals)])
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # === TITLE ===
    title_color = COLORS['red'] if is_over_budget else COLORS['text']
    ax.text(50, 11.5, f'{project_name} - Budget Health', 
            ha='center', va='top', fontsize=16, fontweight='bold', color=title_color)
    
    # Alert badge
    badge_colors = {'green': '#dcfce7', 'yellow': '#fef3c7', 'red': '#fee2e2'}
    badge_text_colors = {'green': '#166534', 'yellow': '#a16207', 'red': '#991b1b'}
    badge_bg = badge_colors.get(alert_level, badge_colors['green'])
    badge_fg = badge_text_colors.get(alert_level, badge_text_colors['green'])
    ax.text(92, 11.5, alert_level.upper(), ha='center', va='top', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=badge_bg, edgecolor='none'), color=badge_fg)
    
    # === DATE HEADER ===
    months = []
    current = project_start.replace(day=1)
    for i in range(6):
        months.append(current)
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)
    
    # Month labels
    month_width = 100 / 6
    for i, month in enumerate(months):
        x_pos = i * month_width + month_width / 2
        ax.text(x_pos, 10.2, month.strftime('%b %Y'), ha='center', va='center', 
                fontsize=9, color=COLORS['text'], fontweight='bold')
    
    # === MAIN BAR ===
    bar_y = 6
    bar_height = 2.5
    
    # Draw unscheduled portion (hatched pattern for warning)
    if unscheduled_pct > 0:
        ax.add_patch(Rectangle(
            (scheduled_pct, bar_y), unscheduled_pct, bar_height,
            facecolor=COLORS['unscheduled'], edgecolor='#d97706', linewidth=1.5,
            hatch='///', alpha=0.8
        ))
    
    # Draw scheduled amount (light green)
    if scheduled_pct > 0:
        ax.add_patch(Rectangle(
            (0, bar_y), scheduled_pct, bar_height,
            facecolor=COLORS['scheduled'], edgecolor='#16a34a', linewidth=1.5
        ))
    
    # Draw actual amount (dark green)
    if actual_pct > 0:
        ax.add_patch(Rectangle(
            (0, bar_y), min(actual_pct, 100), bar_height,
            facecolor=COLORS['actual'], edgecolor='#166534', linewidth=1.5
        ))
    
    # Over-budget indicator (red overlay if actuals exceed scheduled)
    if actual_pct > scheduled_pct:
        ax.add_patch(Rectangle(
            (scheduled_pct, bar_y), actual_pct - scheduled_pct, bar_height,
            facecolor=COLORS['red'], edgecolor='#991b1b', linewidth=2, alpha=0.7
        ))
    
    # === MONTHLY DEMARCATION LINES ===
    cumulative_scheduled = 0
    for i, amount in enumerate(monthly_scheduled):
        cumulative_scheduled += amount
        if total_budget > 0:
            x_pos = (cumulative_scheduled / total_budget) * 100
            # Vertical line
            ax.plot([x_pos, x_pos], [bar_y - 0.3, bar_y + bar_height + 0.3], 
                    color=COLORS['month_line'], linewidth=1.5, linestyle='--', alpha=0.7)
            # Amount label below
            if i < 5:  # Don't show for last month
                ax.text(x_pos, bar_y - 0.5, f'${cumulative_scheduled/1000:.0f}K', 
                        ha='center', va='top', fontsize=8, color=COLORS['text'])
    
    # === MONTHLY BREAKDOWN BARS ===
    mini_bar_y = 3.5
    mini_bar_height = 1.2
    
    ax.text(0, mini_bar_y + mini_bar_height + 0.5, 'Monthly Breakdown:', 
            ha='left', va='bottom', fontsize=10, fontweight='bold', color=COLORS['text'])
    
    for i in range(6):
        x_start = i * month_width + 1
        bar_width = month_width - 2
        
        scheduled_amt = monthly_scheduled[i]
        actual_amt = monthly_actuals[i] if i < len(monthly_actuals) else 0
        
        max_amt = max(scheduled_amt, actual_amt, 1)
        
        # Background (scheduled)
        if scheduled_amt > 0:
            ax.add_patch(Rectangle(
                (x_start, mini_bar_y), bar_width, mini_bar_height,
                facecolor=COLORS['scheduled'], edgecolor='#d1d5db', linewidth=1
            ))
        else:
            ax.add_patch(Rectangle(
                (x_start, mini_bar_y), bar_width, mini_bar_height,
                facecolor='#f3f4f6', edgecolor='#d1d5db', linewidth=1, hatch='...'
            ))
        
        # Actual overlay
        if actual_amt > 0 and scheduled_amt > 0:
            actual_width = (actual_amt / scheduled_amt) * bar_width
            actual_width = min(actual_width, bar_width * 1.2)  # Allow slight overflow for visual
            bar_color = COLORS['actual'] if actual_amt <= scheduled_amt else COLORS['red']
            ax.add_patch(Rectangle(
                (x_start, mini_bar_y), actual_width, mini_bar_height,
                facecolor=bar_color, edgecolor='none', alpha=0.9
            ))
        
        # Amount labels
        ax.text(x_start + bar_width/2, mini_bar_y - 0.2, 
                f'${scheduled_amt/1000:.0f}K' if scheduled_amt > 0 else 'Unsched',
                ha='center', va='top', fontsize=8, color=COLORS['text'])
        if actual_amt > 0:
            ax.text(x_start + bar_width/2, mini_bar_y + mini_bar_height/2,
                    f'${actual_amt/1000:.0f}K', ha='center', va='center', 
                    fontsize=8, color='white', fontweight='bold')
    
    # === LEGEND ===
    legend_y = 1.2
    
    # Legend items
    ax.add_patch(Rectangle((5, legend_y), 3, 0.6, facecolor=COLORS['actual']))
    ax.text(10, legend_y + 0.3, f'Actual: ${actual_revenue:,.0f} ({actual_pct:.1f}%)', 
            va='center', fontsize=9, color=COLORS['actual'], fontweight='bold')
    
    ax.add_patch(Rectangle((35, legend_y), 3, 0.6, facecolor=COLORS['scheduled']))
    ax.text(40, legend_y + 0.3, f'Scheduled: ${total_scheduled:,.0f} ({scheduled_pct:.1f}%)', 
            va='center', fontsize=9, color='#16a34a', fontweight='bold')
    
    ax.add_patch(Rectangle((70, legend_y), 3, 0.6, facecolor=COLORS['unscheduled'], hatch='///'))
    ax.text(75, legend_y + 0.3, f'Unscheduled: ${total_unscheduled:,.0f} ({unscheduled_pct:.1f}%)', 
            va='center', fontsize=9, color='#d97706', fontweight='bold')
    
    # === SUMMARY STATS ===
    stats_y = 0.2
    
    ax.text(0, stats_y, f"Budget: ${total_budget:,.0f}", fontsize=9, color=COLORS['text'])
    ax.text(25, stats_y, f"Remaining: ${total_budget - actual_revenue:,.0f}", fontsize=9, color=COLORS['text'])
    
    variance = total_scheduled - actual_revenue
    variance_color = COLORS['green'] if variance >= 0 else COLORS['red']
    ax.text(50, stats_y, f"Variance: ${variance:,.0f}", fontsize=9, color=variance_color, fontweight='bold')
    
    completion = (actual_revenue / total_budget) * 100 if total_budget > 0 else 0
    ax.text(75, stats_y, f"Completion: {completion:.1f}%", fontsize=9, color=COLORS['text'])
    
    plt.tight_layout()
    plt.show()
    
else:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.text(0.5, 0.5, 'No data available\nAdd project fields to the visual', 
            ha='center', va='center', fontsize=14, color='#6b7280')
    ax.axis('off')
    plt.show()
