"""
Projector PSA API Data Connector for Power BI
==============================================
Fetches budget, revenue, and project data from Projector PSA Web Services API 2.0
and exports to CSV for Power BI consumption.

Usage:
    1. Set environment variables or update config below
    2. Run: python projector_api_connector.py
    3. Import generated CSV files into Power BI

API Documentation: https://help.projectorpsa.com/WebServices
"""

import os
import json
import csv
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
import urllib.request
import urllib.error
import base64

# ============================================================================
# CONFIGURATION - Update these values or use environment variables
# ============================================================================

CONFIG = {
    # Projector API Base URL (your instance)
    "base_url": os.environ.get("PROJECTOR_API_URL", "https://api.projectorpsa.com"),
    
    # Authentication - Use environment variables for security
    "username": os.environ.get("PROJECTOR_USERNAME", ""),
    "password": os.environ.get("PROJECTOR_PASSWORD", ""),
    
    # Alternative: API Key authentication
    "api_key": os.environ.get("PROJECTOR_API_KEY", ""),
    
    # Output directory for CSV files
    "output_dir": os.environ.get("PROJECTOR_OUTPUT_DIR", "../../data/projector_exports"),
    
    # Date range for data fetch (adjust as needed)
    "lookback_months": 3,  # How far back to fetch actuals
    "forecast_months": 6,  # How far ahead to fetch projections
}

# ============================================================================
# API CLIENT
# ============================================================================

class ProjectorAPIClient:
    """Client for Projector PSA Web Services API 2.0"""
    
    def __init__(self, base_url: str, username: str = "", password: str = "", api_key: str = ""):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.api_key = api_key
        self.session_token = None
        
    def _get_auth_header(self) -> Dict[str, str]:
        """Generate authentication header"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        elif self.session_token:
            headers["Authorization"] = f"Bearer {self.session_token}"
        elif self.username and self.password:
            # Basic auth fallback
            credentials = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
            headers["Authorization"] = f"Basic {credentials}"
            
        return headers
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make HTTP request to Projector API"""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_auth_header()
        
        try:
            if data:
                request_data = json.dumps(data).encode("utf-8")
            else:
                request_data = None
                
            req = urllib.request.Request(url, data=request_data, headers=headers, method=method)
            
            with urllib.request.urlopen(req, timeout=60) as response:
                response_data = response.read().decode("utf-8")
                return json.loads(response_data) if response_data else {}
                
        except urllib.error.HTTPError as e:
            print(f"HTTP Error {e.code}: {e.reason}")
            print(f"URL: {url}")
            if e.code == 401:
                raise Exception("Authentication failed. Check your credentials.")
            raise
        except urllib.error.URLError as e:
            print(f"URL Error: {e.reason}")
            raise
    
    def login(self) -> bool:
        """Authenticate and get session token"""
        if self.api_key:
            print("Using API key authentication")
            return True
            
        try:
            response = self._make_request("POST", "/api/v2/auth/login", {
                "username": self.username,
                "password": self.password
            })
            self.session_token = response.get("token")
            print("Login successful")
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    
    def get_projects(self, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Fetch projects from DIM Project
        
        API Endpoint: /api/v2/projects
        Key fields: ProjectUID, ProjectName, ProjectStartDate, ProjectEndDate,
                   ClientName, ProjectManager, ProjectStatus
        """
        params = filters or {}
        # Include active projects by default
        if "status" not in params:
            params["status"] = "active,pipeline"
            
        response = self._make_request("GET", "/api/v2/projects")
        return response.get("projects", [])
    
    def get_portfolio_performance(self, project_uids: Optional[List[str]] = None) -> List[Dict]:
        """
        Fetch FACT Portfolio Performance data
        
        API Endpoint: /api/v2/reports/portfolio-performance
        Key fields: ActualBillingAdjustedRevenueToDate, BudgetedBillingAdjustedRevenueAtCompletion,
                   HoursBudgetAlertLevelAtCompletion, ActualHoursToDate, etc.
        """
        params = {}
        if project_uids:
            params["projectUIDs"] = ",".join(project_uids)
            
        response = self._make_request("GET", "/api/v2/reports/portfolio-performance")
        return response.get("data", [])
    
    def get_ops_data_by_week(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Fetch FACT Ops Data by Week
        
        API Endpoint: /api/v2/reports/ops-data-weekly
        Key fields: BudgetedHours, PersonHours, ChargeableHours, StandardRevenue,
                   ContractRevenue, BillingAdjustedRevenue, ResourceDirectCost
        """
        response = self._make_request("GET", f"/api/v2/reports/ops-data-weekly?startDate={start_date}&endDate={end_date}")
        return response.get("data", [])
    
    def get_financial_data_by_month(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Fetch FACT Financial Data by Month
        
        API Endpoint: /api/v2/reports/financial-data-monthly
        Key fields: TotalRevenue, SystemRevenue, ResourceDirectCost, ProjectProfit
        """
        response = self._make_request("GET", f"/api/v2/reports/financial-data-monthly?startDate={start_date}&endDate={end_date}")
        return response.get("data", [])
    
    def get_project_roles(self, project_uid: str) -> List[Dict]:
        """
        Fetch project roles/resource assignments
        
        API Endpoint: /api/v2/projects/{uid}/roles
        Key fields: RoleStartDate, RoleEndDate, TotalScheduledMinutes, RoleStatus
        """
        response = self._make_request("GET", f"/api/v2/projects/{project_uid}/roles")
        return response.get("roles", [])
    
    def get_milestones(self, project_uid: Optional[str] = None) -> List[Dict]:
        """
        Fetch FACT Milestones data
        
        API Endpoint: /api/v2/milestones
        Key fields: MilestoneName, MilestoneStatus, MilestoneForecastDate, MilestoneAmount
        """
        endpoint = f"/api/v2/projects/{project_uid}/milestones" if project_uid else "/api/v2/milestones"
        response = self._make_request("GET", endpoint)
        return response.get("milestones", [])


# ============================================================================
# DATA TRANSFORMERS
# ============================================================================

def transform_for_budget_health(portfolio_data: List[Dict], financial_data: List[Dict]) -> List[Dict]:
    """
    Transform raw API data into the format needed for Budget Health Visual
    
    Output columns match BudgetForecast table structure:
    - ProjectName, TotalBudget, ActualBillingAdjustedRevenueToDate
    - ScheduledRevenue_Month1-6, ActualRevenue_Month1-3
    - HoursBudgetAlertLevel
    """
    # Group financial data by project and month
    monthly_by_project = {}
    for record in financial_data:
        project_name = record.get("ProjectName", "Unknown")
        month_key = record.get("Month", record.get("PeriodStart", ""))[:7]  # YYYY-MM
        
        if project_name not in monthly_by_project:
            monthly_by_project[project_name] = {}
        monthly_by_project[project_name][month_key] = record
    
    # Build output records
    results = []
    for project in portfolio_data:
        project_name = project.get("ProjectName", "Unknown")
        
        # Get monthly data for this project
        monthly = monthly_by_project.get(project_name, {})
        sorted_months = sorted(monthly.keys())
        
        record = {
            "ProjectName": project_name,
            "TotalBudget": project.get("BudgetedBillingAdjustedRevenueAtCompletion", 0),
            "ActualBillingAdjustedRevenueToDate": project.get("ActualBillingAdjustedRevenueToDate", 0),
            "HoursBudgetAlertLevel": _map_alert_level(project.get("HoursBudgetAlertLevelAtCompletion", "G")),
        }
        
        # Map monthly scheduled/actual revenue
        # Month 1 = current month, Month 2 = next month, etc.
        for i in range(6):
            month_idx = i  # 0-5 for scheduled (forecast months)
            if month_idx < len(sorted_months):
                month_data = monthly.get(sorted_months[month_idx], {})
                record[f"ScheduledRevenue_Month{i+1}"] = month_data.get("SystemRevenue", 0)
            else:
                record[f"ScheduledRevenue_Month{i+1}"] = 0
        
        # Actual revenue for completed months (Month1-3 = past 3 months)
        for i in range(3):
            month_idx = i
            if month_idx < len(sorted_months):
                month_data = monthly.get(sorted_months[month_idx], {})
                record[f"ActualRevenue_Month{i+1}"] = month_data.get("BillingAdjustedRevenue", 0)
            else:
                record[f"ActualRevenue_Month{i+1}"] = 0
        
        results.append(record)
    
    return results


def _map_alert_level(api_value: str) -> str:
    """Map Projector alert level codes to display values"""
    mapping = {
        "G": "Green",
        "Y": "Yellow", 
        "R": "Red",
        "Green": "Green",
        "Yellow": "Yellow",
        "Red": "Red",
        "0": "Green",
        "1": "Yellow",
        "2": "Red"
    }
    return mapping.get(str(api_value), "Green")


def transform_for_kpi_summary(portfolio_data: List[Dict]) -> Dict:
    """
    Calculate KPI summary metrics
    
    Output:
    - TotalProjects, GreenCount, YellowCount, RedCount
    - TotalBudget, TotalActual, BudgetUtilization%
    """
    summary = {
        "TotalProjects": len(portfolio_data),
        "GreenCount": 0,
        "YellowCount": 0,
        "RedCount": 0,
        "TotalBudget": 0,
        "TotalActual": 0,
        "AsOfDate": datetime.now().strftime("%Y-%m-%d")
    }
    
    for project in portfolio_data:
        alert_level = _map_alert_level(project.get("HoursBudgetAlertLevelAtCompletion", "G"))
        
        if alert_level == "Green":
            summary["GreenCount"] += 1
        elif alert_level == "Yellow":
            summary["YellowCount"] += 1
        else:
            summary["RedCount"] += 1
            
        summary["TotalBudget"] += project.get("BudgetedBillingAdjustedRevenueAtCompletion", 0)
        summary["TotalActual"] += project.get("ActualBillingAdjustedRevenueToDate", 0)
    
    # Calculate utilization percentage
    if summary["TotalBudget"] > 0:
        summary["BudgetUtilization"] = round(summary["TotalActual"] / summary["TotalBudget"] * 100, 1)
    else:
        summary["BudgetUtilization"] = 0
        
    return summary


# ============================================================================
# CSV EXPORT
# ============================================================================

def export_to_csv(data: List[Dict], filename: str, output_dir: str):
    """Export data to CSV file"""
    if not data:
        print(f"No data to export for {filename}")
        return
        
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, filename)
    
    # Get all unique keys across all records
    all_keys = set()
    for record in data:
        all_keys.update(record.keys())
    fieldnames = sorted(all_keys)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Exported {len(data)} records to {filepath}")


def export_summary_to_csv(summary: Dict, filename: str, output_dir: str):
    """Export single summary record to CSV"""
    export_to_csv([summary], filename, output_dir)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def fetch_and_export_all():
    """Main function to fetch all data and export to CSV files"""
    
    print("=" * 60)
    print("Projector PSA Data Export")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Validate configuration
    if not CONFIG["api_key"] and not (CONFIG["username"] and CONFIG["password"]):
        print("\n⚠️  No credentials configured!")
        print("Set environment variables:")
        print("  PROJECTOR_API_KEY=your_api_key")
        print("  or")
        print("  PROJECTOR_USERNAME=your_username")
        print("  PROJECTOR_PASSWORD=your_password")
        print("\nGenerating sample data for testing instead...")
        _generate_sample_data()
        return
    
    # Initialize client
    client = ProjectorAPIClient(
        base_url=CONFIG["base_url"],
        username=CONFIG["username"],
        password=CONFIG["password"],
        api_key=CONFIG["api_key"]
    )
    
    # Authenticate
    if not client.login():
        print("Authentication failed. Exiting.")
        return
    
    # Calculate date range
    today = datetime.now()
    start_date = (today - timedelta(days=CONFIG["lookback_months"] * 30)).strftime("%Y-%m-%d")
    end_date = (today + timedelta(days=CONFIG["forecast_months"] * 30)).strftime("%Y-%m-%d")
    
    print(f"\nDate range: {start_date} to {end_date}")
    
    # Fetch data
    print("\nFetching projects...")
    projects = client.get_projects()
    print(f"  Found {len(projects)} projects")
    
    print("Fetching portfolio performance...")
    portfolio = client.get_portfolio_performance()
    print(f"  Found {len(portfolio)} portfolio records")
    
    print("Fetching financial data by month...")
    financial = client.get_financial_data_by_month(start_date, end_date)
    print(f"  Found {len(financial)} financial records")
    
    # Transform and export
    output_dir = os.path.join(os.path.dirname(__file__), CONFIG["output_dir"])
    
    print("\nTransforming data...")
    budget_health_data = transform_for_budget_health(portfolio, financial)
    kpi_summary = transform_for_kpi_summary(portfolio)
    
    print("\nExporting to CSV...")
    export_to_csv(projects, "projector_projects.csv", output_dir)
    export_to_csv(portfolio, "projector_portfolio_performance.csv", output_dir)
    export_to_csv(financial, "projector_financial_monthly.csv", output_dir)
    export_to_csv(budget_health_data, "budget_health_data.csv", output_dir)
    export_summary_to_csv(kpi_summary, "kpi_summary.csv", output_dir)
    
    print("\n" + "=" * 60)
    print("Export complete!")
    print(f"Files saved to: {os.path.abspath(output_dir)}")
    print("=" * 60)


def _generate_sample_data():
    """Generate sample data for testing when no API credentials available"""
    
    output_dir = os.path.join(os.path.dirname(__file__), CONFIG["output_dir"])
    
    # Sample budget health data matching our BudgetForecast table structure
    sample_data = [
        {"ProjectName": "Website Redesign", "TotalBudget": 120000, "ActualBillingAdjustedRevenueToDate": 45000,
         "ScheduledRevenue_Month1": 20000, "ScheduledRevenue_Month2": 20000, "ScheduledRevenue_Month3": 20000,
         "ScheduledRevenue_Month4": 20000, "ScheduledRevenue_Month5": 10000, "ScheduledRevenue_Month6": 0,
         "ActualRevenue_Month1": 20000, "ActualRevenue_Month2": 20000, "ActualRevenue_Month3": 5000,
         "HoursBudgetAlertLevel": "Green"},
        {"ProjectName": "Mobile App Development", "TotalBudget": 250000, "ActualBillingAdjustedRevenueToDate": 180000,
         "ScheduledRevenue_Month1": 40000, "ScheduledRevenue_Month2": 40000, "ScheduledRevenue_Month3": 50000,
         "ScheduledRevenue_Month4": 50000, "ScheduledRevenue_Month5": 40000, "ScheduledRevenue_Month6": 30000,
         "ActualRevenue_Month1": 45000, "ActualRevenue_Month2": 50000, "ActualRevenue_Month3": 55000,
         "HoursBudgetAlertLevel": "Green"},
        {"ProjectName": "Data Migration", "TotalBudget": 80000, "ActualBillingAdjustedRevenueToDate": 15000,
         "ScheduledRevenue_Month1": 0, "ScheduledRevenue_Month2": 15000, "ScheduledRevenue_Month3": 15000,
         "ScheduledRevenue_Month4": 15000, "ScheduledRevenue_Month5": 15000, "ScheduledRevenue_Month6": 10000,
         "ActualRevenue_Month1": 0, "ActualRevenue_Month2": 15000, "ActualRevenue_Month3": 0,
         "HoursBudgetAlertLevel": "Yellow"},
        {"ProjectName": "Cloud Infrastructure", "TotalBudget": 300000, "ActualBillingAdjustedRevenueToDate": 275000,
         "ScheduledRevenue_Month1": 50000, "ScheduledRevenue_Month2": 50000, "ScheduledRevenue_Month3": 50000,
         "ScheduledRevenue_Month4": 50000, "ScheduledRevenue_Month5": 50000, "ScheduledRevenue_Month6": 50000,
         "ActualRevenue_Month1": 55000, "ActualRevenue_Month2": 60000, "ActualRevenue_Month3": 80000,
         "HoursBudgetAlertLevel": "Red"},
        {"ProjectName": "ERP Implementation", "TotalBudget": 500000, "ActualBillingAdjustedRevenueToDate": 85000,
         "ScheduledRevenue_Month1": 50000, "ScheduledRevenue_Month2": 60000, "ScheduledRevenue_Month3": 70000,
         "ScheduledRevenue_Month4": 80000, "ScheduledRevenue_Month5": 90000, "ScheduledRevenue_Month6": 100000,
         "ActualRevenue_Month1": 45000, "ActualRevenue_Month2": 40000, "ActualRevenue_Month3": 0,
         "HoursBudgetAlertLevel": "Yellow"},
        {"ProjectName": "Security Audit", "TotalBudget": 45000, "ActualBillingAdjustedRevenueToDate": 0,
         "ScheduledRevenue_Month1": 0, "ScheduledRevenue_Month2": 0, "ScheduledRevenue_Month3": 15000,
         "ScheduledRevenue_Month4": 15000, "ScheduledRevenue_Month5": 15000, "ScheduledRevenue_Month6": 0,
         "ActualRevenue_Month1": 0, "ActualRevenue_Month2": 0, "ActualRevenue_Month3": 0,
         "HoursBudgetAlertLevel": "Green"},
        {"ProjectName": "API Gateway", "TotalBudget": 180000, "ActualBillingAdjustedRevenueToDate": 165000,
         "ScheduledRevenue_Month1": 30000, "ScheduledRevenue_Month2": 30000, "ScheduledRevenue_Month3": 30000,
         "ScheduledRevenue_Month4": 30000, "ScheduledRevenue_Month5": 30000, "ScheduledRevenue_Month6": 30000,
         "ActualRevenue_Month1": 35000, "ActualRevenue_Month2": 40000, "ActualRevenue_Month3": 45000,
         "HoursBudgetAlertLevel": "Red"},
        {"ProjectName": "Analytics Dashboard", "TotalBudget": 95000, "ActualBillingAdjustedRevenueToDate": 8000,
         "ScheduledRevenue_Month1": 0, "ScheduledRevenue_Month2": 10000, "ScheduledRevenue_Month3": 15000,
         "ScheduledRevenue_Month4": 20000, "ScheduledRevenue_Month5": 20000, "ScheduledRevenue_Month6": 20000,
         "ActualRevenue_Month1": 0, "ActualRevenue_Month2": 8000, "ActualRevenue_Month3": 0,
         "HoursBudgetAlertLevel": "Green"},
        {"ProjectName": "Customer Portal", "TotalBudget": 200000, "ActualBillingAdjustedRevenueToDate": 195000,
         "ScheduledRevenue_Month1": 35000, "ScheduledRevenue_Month2": 35000, "ScheduledRevenue_Month3": 35000,
         "ScheduledRevenue_Month4": 35000, "ScheduledRevenue_Month5": 30000, "ScheduledRevenue_Month6": 30000,
         "ActualRevenue_Month1": 40000, "ActualRevenue_Month2": 42000, "ActualRevenue_Month3": 48000,
         "HoursBudgetAlertLevel": "Yellow"},
        {"ProjectName": "DevOps Pipeline", "TotalBudget": 60000, "ActualBillingAdjustedRevenueToDate": 22000,
         "ScheduledRevenue_Month1": 15000, "ScheduledRevenue_Month2": 15000, "ScheduledRevenue_Month3": 15000,
         "ScheduledRevenue_Month4": 15000, "ScheduledRevenue_Month5": 0, "ScheduledRevenue_Month6": 0,
         "ActualRevenue_Month1": 12000, "ActualRevenue_Month2": 10000, "ActualRevenue_Month3": 0,
         "HoursBudgetAlertLevel": "Yellow"},
    ]
    
    # Calculate summary
    summary = {
        "TotalProjects": len(sample_data),
        "GreenCount": sum(1 for p in sample_data if p["HoursBudgetAlertLevel"] == "Green"),
        "YellowCount": sum(1 for p in sample_data if p["HoursBudgetAlertLevel"] == "Yellow"),
        "RedCount": sum(1 for p in sample_data if p["HoursBudgetAlertLevel"] == "Red"),
        "TotalBudget": sum(p["TotalBudget"] for p in sample_data),
        "TotalActual": sum(p["ActualBillingAdjustedRevenueToDate"] for p in sample_data),
        "AsOfDate": datetime.now().strftime("%Y-%m-%d")
    }
    summary["BudgetUtilization"] = round(summary["TotalActual"] / summary["TotalBudget"] * 100, 1)
    
    print("\nExporting sample data...")
    export_to_csv(sample_data, "budget_health_data.csv", output_dir)
    export_summary_to_csv(summary, "kpi_summary.csv", output_dir)
    
    print("\n" + "=" * 60)
    print("Sample data export complete!")
    print(f"Files saved to: {os.path.abspath(output_dir)}")
    print("\nTo use with real Projector data, set environment variables:")
    print("  set PROJECTOR_API_KEY=your_api_key")
    print("  set PROJECTOR_API_URL=https://your-instance.projectorpsa.com")
    print("=" * 60)


# ============================================================================
# POWER BI POWER QUERY SCRIPT (for reference)
# ============================================================================

POWER_QUERY_TEMPLATE = '''
// Power Query M script to fetch from Projector API
// Paste this into Power BI: Get Data > Blank Query > Advanced Editor

let
    // Configuration
    ApiUrl = "https://api.projectorpsa.com/api/v2",
    ApiKey = "YOUR_API_KEY_HERE",
    
    // Headers
    Headers = [
        #"Authorization" = "Bearer " & ApiKey,
        #"Content-Type" = "application/json"
    ],
    
    // Fetch Portfolio Performance
    Source = Json.Document(Web.Contents(
        ApiUrl & "/reports/portfolio-performance",
        [Headers = Headers]
    )),
    
    // Convert to table
    Data = Source[data],
    Table = Table.FromList(Data, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    ExpandedTable = Table.ExpandRecordColumn(Table, "Column1", 
        {"ProjectName", "ActualBillingAdjustedRevenueToDate", 
         "BudgetedBillingAdjustedRevenueAtCompletion", "HoursBudgetAlertLevelAtCompletion"})
in
    ExpandedTable
'''


if __name__ == "__main__":
    fetch_and_export_all()
