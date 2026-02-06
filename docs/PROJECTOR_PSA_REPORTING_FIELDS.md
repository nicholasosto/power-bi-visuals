# Projector PSA Reporting Fields & Data Model Reference

## Overview
Projector PSA (now part of BigTime Enterprise) provides comprehensive project financial tracking through:
- **FACT Tables**: Transactional/aggregated data for reporting
- **DIMension Tables**: Reference/master data attributes
- **Web Services API 2.0**: Programmatic access to all data

---

## 1. Budget Fields

### Time Budget Fields
| Field Name | API Field | Description | Report Usage |
|------------|-----------|-------------|---------------|
| WorkMinutesTimeBudgetAmount | `WorkMinutesTimeBudgetAmount` | Time budget amount in work minutes (when TimeBudgetMetric is "H") | Portfolio, Budget Reports |
| ChargeableMinutesTimeBudgetAmount | `ChargeableMinutesTimeBudgetAmount` | Chargeable minutes time budget | Portfolio Performance |
| BillingAdjustedRevenueTimeBudgetAmount | `BillingAdjustedRevenueTimeBudgetAmount` | Billing adjusted time revenue budget | Portfolio, Budget vs Actual |
| ContractRevenueTimeBudgetAmount | `ContractRevenueTimeBudgetAmount` | Contract revenue time budget amount | Contract Reports |
| ResourceDirectCostTimeBudgetAmount | `ResourceDirectCostTimeBudgetAmount` | Resource direct cost time budget | Cost Analysis |
| BudgetedHours | `BudgetedHours` | Total budgeted hours | FACT Ops Data by Wk |
| BudgetedChargeableHours | `BudgetedChargeableHours` | Budgeted chargeable hours | FACT Ops Data by Wk |
| BudgetedHoursAtCompletion | `BudgetedHoursAtCompletion` | Budget hours at project completion | FACT Portfolio Perf |
| BudgetedChargeableHoursAtCompletion | `BudgetedChargeableHoursAtCompletion` | Budgeted chargeable hours at completion | FACT Portfolio Perf |

### Cost Budget Fields
| Field Name | API Field | Description | Report Usage |
|------------|-----------|-------------|---------------|
| ClientAmountCostBudgetAmount | `ClientAmountCostBudgetAmount` | Client amount cost budget (when CostBudgetMetric is "C") | Portfolio Reports |
| DisbursedAmountCostBudgetAmount | `DisbursedAmountCostBudgetAmount` | Disbursed amount cost budget (when CostBudgetMetric is "D") | Expense Analysis |
| ExpenseAmountCostBudgetAmount | `ExpenseAmountCostBudgetAmount` | Expense amount cost budget (when CostBudgetMetric is "E") | Expense Reports |
| BudgetedBillingAdjustedRevenue | `BudgetedBillingAdjustedRevenue` | Budgeted billing adjusted revenue | FACT Ops Data by Wk |
| BudgetedContractRevenue | `BudgetedContractRevenue` | Budgeted contract revenue | FACT Ops Data by Wk |
| BudgetedResourceDirectCost | `BudgetedResourceDirectCost` | Budgeted resource direct cost | FACT Ops Data by Wk |
| BudgetedOtherDirectCostsClient | `BudgetedOtherDirectCostsClient` | Budgeted ODCs - client amount | FACT Ops Data by Wk |

### Budget Metrics Configuration
| Field | Values | Description |
|-------|--------|-------------|
| TimeBudgetMetric | B = Billing Adjusted Revenue<br>C = Contract Revenue<br>R = Resource Direct Cost<br>H = Working Hours | Determines which time budget metric is primary |
| CostBudgetMetric | C = Client Amount<br>D = Disbursed Amount<br>E = Expense Amount | Determines which cost budget metric is primary |
| TimeAlertsBasisType | A = Actuals to Date<br>E = Estimate at Completion | How time alerts are calculated |
| CostAlertsBasisType | A = Actuals to Date<br>E = Estimate at Completion | How cost alerts are calculated |

---

## 2. Revenue Fields

### Standard Revenue Fields
| Field Name | API Field | Description | Report Usage |
|------------|-----------|-------------|---------------|
| StandardRevenue | `StandardRevenue` | Revenue at standard rates | FACT Ops Data by Wk |
| ContractRevenue | `ContractRevenue` | Revenue per contract terms | FACT Ops Data by Wk |
| BillingAdjustedRevenue | `BillingAdjustedRevenue` | Revenue after billing adjustments | FACT Ops Data by Wk |
| SystemRevenue | `SystemRevenue` | System-calculated revenue | FACT Ops Data by Wk, FACT Fin Data by Month |
| RecognizedRevenue | `RecognizedRevenue` | Revenue recognized | FACT Ops Data by Wk |
| TotalRevenue | `TotalRevenue` | Total revenue (time + ODCs) | FACT Ops Data by Wk, FACT Fin Data by Month |
| TotalRecognizedRevenue | `TotalRecognizedRevenue` | Total recognized revenue | FACT Ops Data by Wk |
| PotentialStandardRevenue | `PotentialStandardRevenue` | Potential revenue at standard rates | FACT Ops Data by Wk, FACT Fin Data by Month |

### Revenue Analysis - Actual/Projected
| Field Name | API Field | Description | Report Usage |
|------------|-----------|-------------|---------------|
| ActualBillingAdjustedRevenueToDate | `ActualBillingAdjustedRevenueToDate` | Actual billing adjusted revenue to date | FACT Portfolio Perf |
| ProjectedBillingAdjustedRevenueToComplete | `ProjectedBillingAdjustedRevenueToComplete` | Projected billing adjusted revenue to complete | FACT Portfolio Perf |
| BudgetedBillingAdjustedRevenueAtCompletion | `BudgetedBillingAdjustedRevenueAtCompletion` | Budget at completion | FACT Portfolio Perf |
| ActualContractRevenueToDate | `ActualContractRevenueToDate` | Actual contract revenue to date | FACT Portfolio Perf |
| ProjectedContractRevenueToComplete | `ProjectedContractRevenueToComplete` | Projected contract revenue remaining | FACT Portfolio Perf |
| BudgetedContractRevenueAtCompletion | `BudgetedContractRevenueAtCompletion` | Contract budget at completion | FACT Portfolio Perf |
| BudgetedContractRevenueRemaining | `BudgetedContractRevenueRemaining` | Contract revenue remaining | FACT Portfolio Perf |
| ActualSystemRevenueToDate | `ActualSystemRevenueToDate` | Actual system revenue to date | FACT Portfolio Perf |
| ProjectedSystemRevenueToComplete | `ProjectedSystemRevenueToComplete` | Projected system revenue to complete | FACT Portfolio Perf |
| SystemRevenueAtCompletion | `SystemRevenueAtCompletion` | System revenue at completion | FACT Portfolio Perf |

### Billing Status Fields
| Field Name | API Field | Description | Report Usage |
|------------|-----------|-------------|---------------|
| UnbilledBillingAdjustedRevenue | `UnbilledBillingAdjustedRevenue` | Unbilled billing adjusted revenue | FACT Portfolio Perf |
| UnbilledClientAmount | `UnbilledClientAmount` | Unbilled client amount | FACT Portfolio Perf |
| UnbilledMilestoneAmount | `UnbilledMilestoneAmount` | Unbilled milestone amount | FACT Portfolio Perf |
| BilledBillingAdjustedRevenue | `BilledBillingAdjustedRevenue` | Billed billing adjusted revenue | FACT Portfolio Perf |
| BilledClientAmount | `BilledClientAmount` | Billed client amount | FACT Portfolio Perf |
| BilledMilestoneAmount | `BilledMilestoneAmount` | Billed milestone amount | FACT Portfolio Perf |
| BillingStatus | `BillingStatus` | Current billing status | FACT Ops Data by Wk |

### Revenue Loss Analysis
| Field Name | API Field | Description | Report Usage |
|------------|-----------|-------------|---------------|
| RevenueLossDueToDiscounting | `RevenueLossDueToDiscounting` | Revenue loss from discounting | FACT Ops Data by Wk |
| RevenueLossDueToContractTerms | `RevenueLossDueToContractTerms` | Revenue loss from contract terms | FACT Ops Data by Wk |
| RevenueLossDueToWriteDowns | `RevenueLossDueToWriteDowns` | Revenue loss from write-downs | FACT Ops Data by Wk |
| RevenueLossDueToContractTermsAtCompletion | `RevenueLossDueToContractTermsAtCompletion` | Loss at completion | FACT Portfolio Perf |
| RevenueLossDueToDiscountingAtCompletion | `RevenueLossDueToDiscountingAtCompletion` | Discount loss at completion | FACT Portfolio Perf |
| RevenueLossDueToWriteDownsAtCompletion | `RevenueLossDueToWriteDownsAtCompletion` | Write-down loss at completion | FACT Portfolio Perf |

---

## 3. Time/Schedule Fields

### Project Date Fields
| Field Name | API Field | Description | Report Usage |
|------------|-----------|-------------|---------------|
| ProjectStartDate | `ProjectStartDate` | Project start date | DIM Project, FACT Portfolio Perf |
| ProjectEndDate | `ProjectEndDate` | Project end date | DIM Project, FACT Portfolio Perf |
| ProjectedHoursStartDate | `ProjectedHoursStartDate` | Start date of projected hours | FACT Portfolio Perf |
| ProjectedHoursEndDate | `ProjectedHoursEndDate` | End date of projected hours | FACT Portfolio Perf |
| ActualHoursStartDate | `ActualHoursStartDate` | First recorded actual hours date | FACT Portfolio Perf |
| ActualHoursEndDate | `ActualHoursEndDate` | Last recorded actual hours date | FACT Portfolio Perf |
| ProjectedCostStartDate | `ProjectedCostStartDate` | Start date of projected costs | FACT Portfolio Perf |
| ProjectedCostEndDate | `ProjectedCostEndDate` | End date of projected costs | FACT Portfolio Perf |
| ACOD (Actuals Cut Off Date) | `ACOD` | Cutoff date for actuals vs projections | FACT Portfolio Perf, FACT Ops Data |

### Hours Fields - Actual/Projected
| Field Name | API Field | Description | Report Usage |
|------------|-----------|-------------|---------------|
| PersonHours | `PersonHours` | Total person hours | FACT Ops Data by Wk, FACT Fin Data |
| ChargeableHours | `ChargeableHours` | Chargeable hours worked | FACT Ops Data by Wk, FACT Fin Data |
| ActualHoursToDate | `ActualHoursToDate` | Actual hours recorded to date | FACT Portfolio Perf |
| ProjectedHoursToComplete | `ProjectedHoursToComplete` | Hours projected to complete | FACT Portfolio Perf |
| HoursAtCompletion | `HoursAtCompletion` | Total hours at completion | FACT Portfolio Perf |
| ActualChargeableHoursToDate | `ActualChargeableHoursToDate` | Actual chargeable hours to date | FACT Portfolio Perf |
| ProjectedChargeableHoursToComplete | `ProjectedChargeableHoursToComplete` | Chargeable hours to complete | FACT Portfolio Perf |

### Resource Scheduling Fields
| Field Name | API Field | Description | Report Usage |
|------------|-----------|-------------|---------------|
| RequestedHours | `RequestedHours` | Hours requested (not yet booked) | FACT Hiring Needs |
| BookedHours | `BookedHours` | Hours booked/allocated | FACT Hiring Needs |
| TotalScheduledMinutes | `TotalScheduledMinutes` | Total minutes scheduled for role | Project Roles API |
| RoleStartDate | `RoleStartDate` | Role start date | Project Roles |
| RoleEndDate | `RoleEndDate` | Role end date | Project Roles |
| Projected Hours Start Date | `Projected Hours Start Date` | Start of projected hours | FACT Hiring Needs |
| Projected Hours End Date | `Projected Hours End Date` | End of projected hours | FACT Hiring Needs |

### Role Status Values
| Status Code | Meaning |
|-------------|---------|
| S | Staffed - Role has assigned resource |
| N | Not Staffed - Role created, no resource |
| R | Requested - Hours requested |
| C | Complete - Role scheduling complete |
| D | Deleted - Role marked deleted |

---

## 4. Resource Allocation & Cost Fields

### Resource Cost Fields
| Field Name | API Field | Description | Report Usage |
|------------|-----------|-------------|---------------|
| ResourceDirectCost | `ResourceDirectCost` | Direct cost of resource | FACT Ops Data by Wk, FACT Fin Data |
| ActualResourceDirectCostToDate | `ActualResourceDirectCostToDate` | Actual resource cost to date | FACT Portfolio Perf |
| ProjectedResourceDirectCostToComplete | `ProjectedResourceDirectCostToComplete` | Projected cost to complete | FACT Portfolio Perf |
| BudgetedResourceDirectCostAtCompletion | `BudgetedResourceDirectCostAtCompletion` | Budgeted cost at completion | FACT Portfolio Perf |
| ResourceDirectCostAtCompletion | `ResourceDirectCostAtCompletion` | Cost at completion | FACT Portfolio Perf |

### Other Direct Costs (ODCs)
| Field Name | API Field | Description | Report Usage |
|------------|-----------|-------------|---------------|
| OtherDirectCostsRevenue | `OtherDirectCostsRevenue` | ODC revenue | FACT Ops Data by Wk |
| OtherDirectCostsClient | `OtherDirectCostsClient` | ODC client amount | FACT Ops Data by Wk |
| OdcUnreimbursed | `OdcUnreimbursed` | Unreimbursed ODCs | FACT Ops Data by Wk |
| ActualClientAmountToDate | `ActualClientAmountToDate` | Actual ODC to date | FACT Portfolio Perf |
| ProjectedClientAmountToComplete | `ProjectedClientAmountToComplete` | Projected ODC to complete | FACT Portfolio Perf |
| BudgetedClientAmountAtCompletion | `BudgetedClientAmountAtCompletion` | Budgeted ODC at completion | FACT Portfolio Perf |

### Profit/Margin Fields
| Field Name | API Field | Description | Report Usage |
|------------|-----------|-------------|---------------|
| ProjectMargin | `ProjectMargin` | Project margin | FACT Ops Data by Wk |
| ResourceMargin | `ResourceMargin` | Resource margin | FACT Ops Data by Wk |
| ResourceProfit | `Resource Profit` | Resource profit | FACT Fin Data by Month |
| ProjectProfit | `ProjectProfit` | Project profit | FACT Fin Data by Month |
| ResourceProfitAtCompletion | `ResourceProfitAtCompletion` | Profit at completion | FACT Portfolio Perf |

### Utilization Fields
| Field Name | API Field | Description | Report Usage |
|------------|-----------|-------------|---------------|
| UtilizationBasisHours | `UtilizationBasisHours` | Hours used for utilization calculation | FACT Ops Data by Wk |
| NormalWorkingHours | `NormalWorkingHours` | Normal working hours | FACT Ops Data by Wk |
| WorkingHours | `WorkingHours` | Working hours | FACT Ops Data by Wk |
| BillableUtilizationMinTargetHours | `BillableUtilizationMinTargetHours` | Billable utilization min target | FACT Ops Data by Wk |
| BillableUtilizationMaxTargetHours | `BillableUtilizationMaxTargetHours` | Billable utilization max target | FACT Ops Data by Wk |
| ChargeableUtilizationMinTargetHours | `ChargeableUtilizationMinTargetHours` | Chargeable utilization min target | FACT Ops Data by Wk |
| ChargeableUtilizationMaxTargetHours | `ChargeableUtilizationMaxTargetHours` | Chargeable utilization max target | FACT Ops Data by Wk |
| ProductiveUtilizationMinTargetHours | `ProductiveUtilizationMinTargetHours` | Productive utilization min target | FACT Ops Data by Wk |
| ProductiveUtilizationMaxTargetHours | `ProductiveUtilizationMaxTargetHours` | Productive utilization max target | FACT Ops Data by Wk |
| Headcount | `Headcount` | Headcount FTE | FACT Ops Data, FACT Fin Data |
| ResourceEquivalents | `ResourceEquivalents` | Resource equivalents | FACT Ops Data by Wk |

---

## 5. Budget Alert/Variance Fields (Key for Overrun Detection)

### Budget Alert Level Fields
| Field Name | API Field | Description | Report Usage |
|------------|-----------|-------------|---------------|
| HoursBudgetAlertLevelAtCompletion | `HoursBudgetAlertLevelAtCompletion` | Hours budget alert at completion | FACT Portfolio Perf |
| HoursBudgetAlertLevelToDate | `HoursBudgetAlertLevelToDate` | Hours budget alert to date | FACT Portfolio Perf |
| ChargeableHoursBudgetAlertLevelAtCompletion | `ChargeableHoursBudgetAlertLevelAtCompletion` | Chargeable hours alert at completion | FACT Portfolio Perf |
| ChargeableHoursBudgetAlertLevelToDate | `ChargeableHoursBudgetAlertLevelToDate` | Chargeable hours alert to date | FACT Portfolio Perf |
| BillingAdjustedRevenueBudgetAlertLevelAtCompletion | `BillingAdjustedRevenueBudgetAlertLevelAtCompletion` | Revenue alert at completion | FACT Portfolio Perf |
| BillingAdjustedRevenueBudgetAlertLevelToDate | `BillingAdjustedRevenueBudgetAlertLevelToDate` | Revenue alert to date | FACT Portfolio Perf |
| ResourceDirectCostBudgetAlertLevelAtCompletion | `ResourceDirectCostBudgetAlertLevelAtCompletion` | Cost alert at completion | FACT Portfolio Perf |
| ResourceDirectCostBudgetAlertLevelToDate | `ResourceDirectCostBudgetAlertLevelToDate` | Cost alert to date | FACT Portfolio Perf |
| ContractRevenueBudgetAlertLevelAtCompletion | `ContractRevenueBudgetAlertLevelAtCompletion` | Contract revenue alert at completion | FACT Portfolio Perf |
| ContractRevenueBudgetAlertLevelToDate | `ContractRevenueBudgetAlertLevelToDate` | Contract revenue alert to date | FACT Portfolio Perf |
| ClientAmountBudgetAlertLevelAtCompletion | `ClientAmountBudgetAlertLevelAtCompletion` | Client amount alert at completion | FACT Portfolio Perf |
| ClientAmountBudgetAlertLevelToDate | `ClientAmountBudgetAlertLevelToDate` | Client amount alert to date | FACT Portfolio Perf |
| TaskHoursBudgetAlertLevelAtCompletion | `TaskHoursBudgetAlertLevelAtCompletion` | Task hours alert at completion | FACT Portfolio Perf |
| TaskHoursBudgetAlertLevelToDate | `TaskHoursBudgetAlertLevelToDate` | Task hours alert to date | FACT Portfolio Perf |

---

## 6. Earned Value Management (EVM) Fields

| Field Name | API Field | Description | Report Usage |
|------------|-----------|-------------|---------------|
| ActualCost (ACWP) | `ActualCost(ACWP)` | Actual Cost of Work Performed | FACT Portfolio Perf |
| EarnedValue (BCWP) | `EarnedValue(BCWP)` | Budgeted Cost of Work Performed | FACT Portfolio Perf |
| PlannedValue (BCWS) | `PlannedValue(BCWS)` | Budgeted Cost of Work Scheduled | FACT Portfolio Perf |

### Task-Level EVM
| Field Name | API Field | Description | Report Usage |
|------------|-----------|-------------|---------------|
| TaskEarnedValue | `TaskEarnedValue` | Task earned value | DIM Task |
| TaskPlannedValue | `TaskPlannedValue` | Task planned value | DIM Task |
| TaskActualCost | `TaskActualCost` | Task actual cost | DIM Task |
| TaskPctElapsed | `TaskPctElapsed` | Task percent elapsed | DIM Task |
| TaskBudgetStatus | `TaskBudgetStatus` | Task budget status indicator | DIM Task |
| TaskScheduleStatus | `TaskScheduleStatus` | Task schedule status indicator | DIM Task |

---

## 7. Task & Milestone Fields

### Task Fields
| Field Name | API Field | Description | Report Usage |
|------------|-----------|-------------|---------------|
| TaskHoursToDate | `TaskHoursToDate` | Task hours worked to date | DIM Task |
| TaskHoursRemaining | `TaskHoursRemaining` | Task hours remaining | DIM Task |
| TaskBudgetedHours | `TaskBudgetedHours` | Task budgeted hours | DIM Task |
| TaskPlannedStartDate | `TaskPlannedStartDate` | Planned start date | DIM Task |
| TaskPlannedEndDate | `TaskPlannedEndDate` | Planned end date | DIM Task |
| TaskBaselineStartDate | `TaskBaselineStartDate` | Baseline start date | DIM Task |
| TaskBaselineEndDate | `TaskBaselineEndDate` | Baseline end date | DIM Task |
| TaskActualStartDate | `TaskActualStartDate` | Actual start date | DIM Task |
| TaskActualEndDate | `TaskActualEndDate` | Actual end date | DIM Task |
| TaskPlannedDays | `TaskPlannedDays` | Planned duration in days | DIM Task |
| TaskBaselineDays | `TaskBaselineDays` | Baseline duration in days | DIM Task |
| TaskStatus | `TaskStatus` | Task status | DIM Task |
| ActualTaskHoursToDate | `ActualTaskHoursToDate` | Actual task hours to date | FACT Portfolio Perf |
| ProjectedTaskHoursToComplete | `ProjectedTaskHoursToComplete` | Projected task hours to complete | FACT Portfolio Perf |
| BudgetedTaskHoursAtCompletion | `BudgetedTaskHoursAtCompletion` | Budgeted task hours at completion | FACT Portfolio Perf |
| TasksToDate | `TasksToDate` | Number of tasks to date | FACT Portfolio Perf |
| IncompleteTasksToDate | `IncompleteTasksToDate` | Incomplete tasks count | FACT Portfolio Perf |
| LateTasksToDate | `LateTasksToDate` | Late tasks count | FACT Portfolio Perf |
| OverbudgetTasksToDate | `OverbudgetTasksToDate` | Over budget tasks count | FACT Portfolio Perf |
| TasksAtCompletion | `TasksAtCompletion` | Total tasks at completion | FACT Portfolio Perf |
| TaskPlanStartDate | `TaskPlanStartDate` | Task plan start date | FACT Portfolio Perf |
| TaskPlanEndDate | `TaskPlanEndDate` | Task plan end date | FACT Portfolio Perf |

### Milestone Fields
| Field Name | API Field | Description | Report Usage |
|------------|-----------|-------------|---------------|
| MilestoneName | `MilestoneName` | Milestone name | FACT Milestones |
| MilestoneStatus | `MilestoneStatus` | Current status | FACT Milestones |
| MilestoneForecastDate | `MilestoneForecastDate` | Forecast completion date | FACT Milestones |
| MilestoneAmount | `MilestoneAmount` | Milestone value | FACT Milestones |
| MilestoneAchievedDate | `MilestoneAchievedDate` | Date achieved | FACT Milestones |
| MilestonePlannedDate | `MilestonePlannedDate` | Planned date | FACT Milestones |
| DeliveryMilestonesToDate | `DeliveryMilestonesToDate` | Delivery milestones to date | FACT Portfolio Perf |
| IncompleteDeliveryMilestonesToDate | `IncompleteDeliveryMilestonesToDate` | Incomplete milestones count | FACT Portfolio Perf |
| LateDeliveryMilestonesToDate | `LateDeliveryMilestonesToDate` | Late milestones count | FACT Portfolio Perf |
| DeliveryMilestonesAtCompletion | `DeliveryMilestonesAtCompletion` | Total milestones at completion | FACT Portfolio Perf |
| AchievedMilestonesToDate | `AchievedMilestonesToDate` | Achieved milestones count | FACT Portfolio Perf |
| UnachievedMilestonesToDate | `UnachievedMilestonesToDate` | Unachieved milestones count | FACT Portfolio Perf |
| ForegoneMilestonesToDate | `ForegoneMilestonesToDate` | Foregone milestones count | FACT Portfolio Perf |

---

## 8. Common Report Types in Projector PSA

### Budget vs Actual Reports
| Report | Key Fields Used |
|--------|-----------------|
| FACT Portfolio Perf | BudgetedXAtCompletion vs ActualXToDate fields |
| FACT Ops Data by Wk | Budgeted fields vs actual time-based metrics |
| Budget Alert Reports | All BudgetAlertLevel fields |

### Project Health/Status Reports
| Report | Key Fields Used |
|--------|-----------------|
| FACT Portfolio Perf | Alert levels, issue counts, milestone statuses |
| DIM Issues | Issue counts, priorities, overdue status |
| DIM Task | Task statuses, budget status, schedule status |

### Revenue Forecasting Reports
| Report | Key Fields Used |
|--------|-----------------|
| FACT Portfolio Perf | Projected revenue fields, SystemRevenueAtCompletion |
| FACT Ops Data by Wk | TotalRevenue, TotalRecognizedRevenue |
| Revenue Recognition fields | SystemRevenueRecognized, ActualSystemRevenueToBeRecognizedToDate |

### Resource Utilization Reports
| Report | Key Fields Used |
|--------|-----------------|
| FACT Ops Data by Wk | UtilizationBasisHours, target hours, ChargeableHours |
| FACT Missing Time | Missing Hours, Working Hours, Time Off Hours |
| FACT Hiring Needs | RequestedHours, BookedHours |

---

## 9. Key Metrics for Budget Overrun Detection

### Burn Rate Calculations
```
Burn Rate = ActualHoursToDate / (ProjectEndDate - ProjectStartDate) * 100
Projected Burn = ProjectedHoursToComplete / Remaining Days

# Key fields:
- ActualHoursToDate / BudgetedHoursAtCompletion
- ActualResourceDirectCostToDate / BudgetedResourceDirectCostAtCompletion  
- ActualBillingAdjustedRevenueToDate / BudgetedBillingAdjustedRevenueAtCompletion
```

### Variance Metrics
```
Hours Variance = BudgetedHours - ActualHours
Hours Variance % = (BudgetedHours - ActualHours) / BudgetedHours * 100

Cost Variance = BudgetedResourceDirectCost - ActualResourceDirectCost
Cost Variance % = (Budgeted - Actual) / Budgeted * 100

Revenue Variance = BudgetedContractRevenue - ActualContractRevenue
```

### Schedule Performance Indicators
```
Schedule Variance (SV) = EarnedValue(BCWP) - PlannedValue(BCWS)
Schedule Performance Index (SPI) = EarnedValue(BCWP) / PlannedValue(BCWS)

Cost Variance (CV) = EarnedValue(BCWP) - ActualCost(ACWP)  
Cost Performance Index (CPI) = EarnedValue(BCWP) / ActualCost(ACWP)
```

---

## 10. Identifying Projects with Unscheduled Time/Revenue

### Key Fields for Unscheduled Detection
| Indicator | Fields to Use | Logic |
|-----------|---------------|-------|
| Unscheduled Hours | `RequestedHours` vs `BookedHours` | RequestedHours > 0 with no BookedHours |
| Unstaffed Roles | `RoleStatus` = 'N' or 'R' | Roles exist without resource |
| Unrecognized Revenue | `SystemRevenueToBeRecognized` | Revenue generated but not recognized |
| Unbilled Work | `UnbilledBillingAdjustedRevenue`, `UnbilledClientAmount` | Work complete but not invoiced |

### Query Pattern for Unscheduled Work
```
WHERE RequestedHours > BookedHours
   OR (ActualHoursToDate > 0 AND ProjectedHoursToComplete = 0)
   OR RoleStatus IN ('N', 'R')
```

---

## 11. API Methods for Data Access

### Project/Engagement Financial Data
| Method | Description |
|--------|-------------|
| `PwsGetProject` | Get project details including budget fields |
| `PwsGetEngagement` | Get engagement with budget/contract info |
| `PwsGetContractLineItem` | Contract terms, milestones, revenue |
| `PwsGetProjectList` | List projects with filtering |
| `PwsGetEngagementList` | List engagements with filtering |

### Scheduling/Resource Data
| Method | Description |
|--------|-------------|
| `PwsGetProjectRoles` | Get role assignments, hours (A=booked, R=requested) |
| `PwsGetResourceSchedule` | Resource schedule and availability |
| `PwsGetResourceUtilizationSummary` | Utilization metrics |
| `PwsRequestOrBookRoleHours` | Schedule hours |

### Time/Cost Tracking
| Method | Description |
|--------|-------------|
| `PwsGetTimeCards` | Time card entries |
| `PwsGetResourceCostCards` | Cost/expense cards |
| `PwsGetProjectCostBaseline` | Cost baselines |
| `PwsGetProjectTimeBaseline` | Time baselines |

### Reporting
| Method | Description |
|--------|-------------|
| `PwsGetReportOutput` | Get report data via web services |
| `PwsGetDashboardParameters` | Dashboard configuration |

---

## 12. Projector BI Integration

### Base FACT Tables
- **FACT Portfolio Perf** - Primary for budget monitoring, EVM, project health
- **FACT Ops Data by Wk** - Weekly operational data, utilization, revenue
- **FACT Fin Data by Month** - Monthly financial summary
- **FACT Hiring Needs** - Resource scheduling, booked vs requested
- **FACT Milestones** - Milestone tracking
- **FACT Missing Time** - Time entry compliance

### Base DIM Tables  
- **DIM Project** - Project master data
- **DIM Engagement** - Engagement/contract details
- **DIM Contract Line Item** - Contract terms
- **DIM Resource** - Resource master data
- **DIM Task** - Task details with EVM
- **DIM Invoice** - Invoice details

---

## Notes

1. **Actuals Cut Off Date (ACOD)**: Critical field that separates actual historical data from projected future data in reports.

2. **Budget Metrics**: Pay attention to `TimeBudgetMetric` and `CostBudgetMetric` settings as they determine which budget fields are active.

3. **Alert Basis**: `TimeAlertsBasisType` and `CostAlertsBasisType` can be set to Actuals to Date (A) or Estimate at Completion (E).

4. **Revenue Types**:
   - Standard Revenue = At rate card rates
   - Contract Revenue = Per contract terms
   - Billing Adjusted Revenue = After adjustments/write-offs
   - System Revenue = Projector calculated

5. **Role Modes**: When querying role hours via API:
   - A = Allocated/Booked data
   - R = Requested data
   - E = Effective (booked if exists, else requested)
