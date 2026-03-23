#!/usr/bin/env python3
"""Generate 3 new dark-themed PBIR pages for Invoice Review Dashboard."""
import json, sys

# --- Color Palette ---
BG_PAGE = "#0F1419"
BG_CARD = "#1B2028"
BG_HEADER = "#161B22"
BORDER = "#2D333B"
TEXT_PRIMARY = "#E6EDF3"
TEXT_SECONDARY = "#8B949E"
TEXT_MUTED = "#6E7681"
ACCENT = "#2F81F7"
POSITIVE = "#3FB950"
WARNING = "#D29922"
ALERT = "#F85149"

# Entity shorthand
PE = "Portfolio - API Invoicing Review"
IE = "Invoice Review - Invoice Report"
TC = "Invoice Review - Time Cards"

def cs(obj):
    return json.dumps(obj, separators=(',', ':'))

def vc(cfg, x, y, z, w, h, flt=None):
    return {
        "config": cs(cfg),
        "filters": cs(flt if flt else []),
        "height": round(h, 2),
        "width": round(w, 2),
        "x": round(x, 2),
        "y": round(y, 2),
        "z": round(z, 2)
    }

def dark_vc(title=False, text="", border=True):
    d = {
        "background": [{"properties": {
            "show": {"expr": {"Literal": {"Value": "true"}}},
            "color": {"solid": {"color": BG_CARD}},
            "transparency": {"expr": {"Literal": {"Value": "0D"}}}
        }}],
        "title": [{"properties": {
            "show": {"expr": {"Literal": {"Value": "true" if title else "false"}}}
        }}]
    }
    if title and text:
        d["title"][0]["properties"]["text"] = {"expr": {"Literal": {"Value": f"'{text}'"}}}
        d["title"][0]["properties"]["fontColor"] = {"solid": {"color": TEXT_SECONDARY}}
    if border:
        d["border"] = [{"properties": {
            "show": {"expr": {"Literal": {"Value": "true"}}},
            "color": {"solid": {"color": BORDER}}
        }}]
    return d

dark_table_objs = {
    "columnHeaders": [{"properties": {"fontColor": {"solid": {"color": TEXT_SECONDARY}}, "backColor": {"solid": {"color": BG_HEADER}}}}],
    "values": [{"properties": {"fontColor": {"solid": {"color": TEXT_PRIMARY}}, "backColor": {"solid": {"color": BG_CARD}}}}],
    "grid": [{"properties": {"gridVertical": {"expr": {"Literal": {"Value": "false"}}}, "gridHorizontal": {"expr": {"Literal": {"Value": "true"}}}, "gridHorizontalColor": {"solid": {"color": BORDER}}}}]
}

def textbox(name, x, y, z, w, h, tab, text, font_size="18px", color=TEXT_PRIMARY, font="DIN", weight="bold"):
    return vc({
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": tab}}],
        "singleVisual": {
            "visualType": "textbox",
            "drillFilterOtherVisuals": True,
            "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": [{"value": text, "textStyle": {"fontFamily": font, "fontSize": font_size, "fontWeight": weight, "color": color}}], "horizontalTextAlignment": "left"}]}}]},
            "vcObjects": {"background": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}], "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}]}
        }
    }, x, y, z, w, h)

def slicer(name, x, y, z, w, h, tab, entity, prop, alias, ref_name, title):
    return vc({
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": tab}}],
        "singleVisual": {
            "visualType": "slicer",
            "projections": {"Values": [{"queryRef": f"{entity}.{prop}", "active": True}]},
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": alias, "Entity": entity, "Type": 0}],
                "Select": [{"Column": {"Expression": {"SourceRef": {"Source": alias}}, "Property": prop}, "Name": f"{entity}.{prop}", "NativeReferenceName": ref_name}]
            },
            "drillFilterOtherVisuals": True,
            "objects": {
                "data": [{"properties": {"mode": {"expr": {"Literal": {"Value": "'Dropdown'"}}}}}],
                "general": [{"properties": {"selfFilterEnabled": {"expr": {"Literal": {"Value": "true"}}}}}]
            },
            "vcObjects": dark_vc(True, title)
        }
    }, x, y, z, w, h)

def card(name, x, y, z, w, h, tab, entity, alias, prop, ref_name, title, label_color=TEXT_PRIMARY):
    return vc({
        "name": name,
        "layouts": [{"id": 0, "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": tab}}],
        "singleVisual": {
            "visualType": "card",
            "projections": {"Values": [{"queryRef": f"Sum({entity}.{prop})"}]},
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": alias, "Entity": entity, "Type": 0}],
                "Select": [{"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Source": alias}}, "Property": prop}}, "Function": 0}, "Name": f"Sum({entity}.{prop})", "NativeReferenceName": ref_name}]
            },
            "drillFilterOtherVisuals": True,
            "objects": {
                "labels": [{"properties": {"color": {"solid": {"color": label_color}}}}],
                "categoryLabels": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": TEXT_SECONDARY}}}}]
            },
            "vcObjects": dark_vc(True, title)
        }
    }, x, y, z, w, h)

dark_page_cfg = cs({"objects": {"background": [{"properties": {"color": {"solid": {"color": BG_PAGE}}, "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}]}})

# ============================================================
# OVERVIEW PAGE
# ============================================================
ov = []
ov.append(textbox("ov01a1b2c3d4e5f6a7b8", 20, 4, 0, 400, 40, 0, "Invoice Review Dashboard"))
ov.append(textbox("ov02a1b2c3d4e5f6a7b8", 440, 10, 1, 300, 30, 1, "Projector PSA  \u00b7  Astrix Inc", "11px", TEXT_MUTED, "Segoe UI", "normal"))
ov.append(slicer("ov03a1b2c3d4e5f6a7b8", 20, 52, 100, 370, 38, 100, PE, "Project Manager Display Name", "p", "Project Manager", "Project Manager"))
ov.append(slicer("ov05a1b2c3d4e5f6a7b8", 400, 52, 102, 370, 38, 102, PE, "PO Status", "p", "PO Status", "PO Status"))
ov.append(card("ov06a1b2c3d4e5f6a7b8", 20, 98, 200, 295, 104, 200, IE, "i", "Time Card Billing Adjusted Amount", "Total Invoiced", "Total Invoiced"))
ov.append(card("ov07a1b2c3d4e5f6a7b8", 325, 98, 201, 295, 104, 201, PE, "p", "Budgeted Billing Adjusted Revenue Remaining", "Remaining Budget", "Remaining Budget"))
ov.append(card("ov08a1b2c3d4e5f6a7b8", 630, 98, 202, 295, 104, 202, TC, "t", "Person Hours", "Total Hours", "Total Hours"))
ov.append(card("ov09a1b2c3d4e5f6a7b8", 935, 98, 203, 325, 104, 203, IE, "i", "Count Email", "Email Follow-ups", "Email Follow-ups", ALERT))

# Main Table
ov.append(vc({
    "name": "ov10a1b2c3d4e5f6a7b8",
    "layouts": [{"id": 0, "position": {"x": 20, "y": 212, "z": 300, "width": 905, "height": 488, "tabOrder": 300}}],
    "singleVisual": {
        "visualType": "tableEx",
        "projections": {"Values": [
            {"queryRef": f"{PE}.Project Name"}, {"queryRef": f"{PE}.Primary Client Name"},
            {"queryRef": f"{PE}.Project Manager Display Name"}, {"queryRef": f"{IE}.Invoice Number"},
            {"queryRef": f"Sum({PE}.Budgeted Billing Adjusted Revenue Remaining)"},
            {"queryRef": f"Sum({IE}.Time Card Billing Adjusted Amount)"},
            {"queryRef": f"Sum({IE}.Milestone Amount)"}, {"queryRef": f"Sum({IE}.Count Email)"}
        ]},
        "prototypeQuery": {
            "Version": 2,
            "From": [{"Name": "p", "Entity": PE, "Type": 0}, {"Name": "i", "Entity": IE, "Type": 0}],
            "Select": [
                {"Column": {"Expression": {"SourceRef": {"Source": "p"}}, "Property": "Project Name"}, "Name": f"{PE}.Project Name", "NativeReferenceName": "Project"},
                {"Column": {"Expression": {"SourceRef": {"Source": "p"}}, "Property": "Primary Client Name"}, "Name": f"{PE}.Primary Client Name", "NativeReferenceName": "Client"},
                {"Column": {"Expression": {"SourceRef": {"Source": "p"}}, "Property": "Project Manager Display Name"}, "Name": f"{PE}.Project Manager Display Name", "NativeReferenceName": "PM"},
                {"Column": {"Expression": {"SourceRef": {"Source": "i"}}, "Property": "Invoice Number"}, "Name": f"{IE}.Invoice Number", "NativeReferenceName": "Invoice #"},
                {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Source": "p"}}, "Property": "Budgeted Billing Adjusted Revenue Remaining"}}, "Function": 0}, "Name": f"Sum({PE}.Budgeted Billing Adjusted Revenue Remaining)", "NativeReferenceName": "Budget Remaining"},
                {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Source": "i"}}, "Property": "Time Card Billing Adjusted Amount"}}, "Function": 0}, "Name": f"Sum({IE}.Time Card Billing Adjusted Amount)", "NativeReferenceName": "Invoiced"},
                {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Source": "i"}}, "Property": "Milestone Amount"}}, "Function": 0}, "Name": f"Sum({IE}.Milestone Amount)", "NativeReferenceName": "Milestones"},
                {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Source": "i"}}, "Property": "Count Email"}}, "Function": 0}, "Name": f"Sum({IE}.Count Email)", "NativeReferenceName": "Emails"}
            ]
        },
        "drillFilterOtherVisuals": True,
        "objects": {
            **dark_table_objs,
            "values": [
                dark_table_objs["values"][0],
                {
                    "properties": {
                        "fontColor": {
                            "expr": {
                                "Conditional": {
                                    "Cases": [{
                                        "Condition": {
                                            "Comparison": {
                                                "ComparisonKind": 2,
                                                "Left": {
                                                    "Aggregation": {
                                                        "Expression": {
                                                            "Column": {
                                                                "Expression": {"SourceRef": {"Source": "i"}},
                                                                "Property": "Count Email"
                                                            }
                                                        },
                                                        "Function": 0
                                                    }
                                                },
                                                "Right": {"Literal": {"Value": "1L"}}
                                            }
                                        },
                                        "Value": {"Literal": {"Value": f"'{ALERT}'"}}
                                    }],
                                    "Else": {"Literal": {"Value": f"'{TEXT_PRIMARY}'"}}
                                }
                            }
                        }
                    },
                    "selector": {
                        "metadata": f"Sum({IE}.Count Email)"
                    }
                }
            ]
        },
        "vcObjects": dark_vc(True, "Project Budget & Invoice Status")
    }
}, 20, 212, 300, 905, 488))

# TC Alerts sidebar — multi-row card (name-based alert cards per design)
ov.append(vc({
    "name": "ov11a1b2c3d4e5f6a7b8",
    "layouts": [{"id": 0, "position": {"x": 935, "y": 212, "z": 400, "width": 325, "height": 275, "tabOrder": 400}}],
    "singleVisual": {
        "visualType": "multiRowCard",
        "projections": {"Values": [
            {"queryRef": f"{TC}.Resource Display Name"},
            {"queryRef": f"{TC}.Billing Status"},
            {"queryRef": f"Sum({TC}.Person Hours)"}
        ]},
        "prototypeQuery": {
            "Version": 2,
            "From": [{"Name": "t", "Entity": TC, "Type": 0}],
            "Select": [
                {"Column": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": "Resource Display Name"}, "Name": f"{TC}.Resource Display Name", "NativeReferenceName": "Name"},
                {"Column": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": "Billing Status"}, "Name": f"{TC}.Billing Status", "NativeReferenceName": "Status"},
                {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": "Person Hours"}}, "Function": 0}, "Name": f"Sum({TC}.Person Hours)", "NativeReferenceName": "Hours"}
            ]
        },
        "drillFilterOtherVisuals": True,
        "objects": {
            "dataLabels": [{"properties": {"color": {"solid": {"color": TEXT_PRIMARY}}}}],
            "categoryLabels": [{"properties": {"color": {"solid": {"color": TEXT_SECONDARY}}}}],
            "card": [{"properties": {
                "cardPadding": {"expr": {"Literal": {"Value": "4L"}}},
                "barShow": {"expr": {"Literal": {"Value": "false"}}}
            }}],
            "outline": [{"properties": {
                "show": {"expr": {"Literal": {"Value": "true"}}},
                "color": {"solid": {"color": BORDER}}
            }}]
        },
        "vcObjects": dark_vc(True, "Timecard Alerts")
    }
}, 935, 212, 400, 325, 275))

# Missing PO Numbers alert — filtered to rows where PO Status != "GOOD"
missing_po_filter = [{
    "type": "Categorical",
    "filter": {
        "Version": 2,
        "From": [{"Name": "p", "Entity": PE, "Type": 0}],
        "Where": [{
            "Condition": {
                "Not": {
                    "Expression": {
                        "Comparison": {
                            "ComparisonKind": 0,
                            "Left": {"Column": {"Expression": {"SourceRef": {"Source": "p"}}, "Property": "PO Status"}},
                            "Right": {"Literal": {"Value": "'GOOD'"}}
                        }
                    }
                }
            }
        }]
    },
    "isHiddenInViewMode": True
}]
ov.append(vc({
    "name": "ov12a1b2c3d4e5f6a7b8",
    "layouts": [{"id": 0, "position": {"x": 935, "y": 497, "z": 500, "width": 325, "height": 203, "tabOrder": 500}}],
    "singleVisual": {
        "visualType": "tableEx",
        "projections": {"Values": [
            {"queryRef": f"{PE}.Project Name"}, {"queryRef": f"{PE}.Primary Client Name"},
            {"queryRef": f"{PE}.Client PO Number"}
        ]},
        "prototypeQuery": {
            "Version": 2,
            "From": [{"Name": "p", "Entity": PE, "Type": 0}],
            "Select": [
                {"Column": {"Expression": {"SourceRef": {"Source": "p"}}, "Property": "Project Name"}, "Name": f"{PE}.Project Name", "NativeReferenceName": "Project"},
                {"Column": {"Expression": {"SourceRef": {"Source": "p"}}, "Property": "Primary Client Name"}, "Name": f"{PE}.Primary Client Name", "NativeReferenceName": "Client"},
                {"Column": {"Expression": {"SourceRef": {"Source": "p"}}, "Property": "Client PO Number"}, "Name": f"{PE}.Client PO Number", "NativeReferenceName": "PO #"}
            ]
        },
        "drillFilterOtherVisuals": True,
        "objects": {
            "columnHeaders": [{"properties": {"fontColor": {"solid": {"color": ALERT}}, "backColor": {"solid": {"color": BG_HEADER}}}}],
            "values": [{"properties": {"fontColor": {"solid": {"color": TEXT_PRIMARY}}, "backColor": {"solid": {"color": BG_CARD}}}}]
        },
        "vcObjects": dark_vc(True, "\u26a0 Missing PO Numbers")
    }
}, 935, 497, 500, 325, 203, missing_po_filter))

overview_section = {
    "config": dark_page_cfg,
    "displayName": "Overview",
    "displayOption": 1,
    "filters": "[]",
    "height": 720.0,
    "name": "b1c2d3e4f5a6b7c8d9e0",
    "ordinal": 0,
    "visualContainers": ov,
    "width": 1280.0
}

# ============================================================
# INVOICE DETAIL PAGE
# ============================================================
iv = []
iv.append(textbox("id01a1b2c3d4e5f6a7b8", 20, 4, 0, 400, 40, 0, "Invoice Email"))
iv.append(slicer("id02a1b2c3d4e5f6a7b8", 20, 52, 100, 300, 38, 100, PE, "Engagement Manager Display Name", "p", "Engagement Manager", "Engagement Manager"))
iv.append(slicer("id03a1b2c3d4e5f6a7b8", 330, 52, 101, 300, 38, 101, PE, "Engagement Primary Cost Center Name", "p", "Cost Center", "Cost Center"))
iv.append(vc({
    "name": "id04a1b2c3d4e5f6a7b8",
    "layouts": [{"id": 0, "position": {"x": 20, "y": 100, "z": 200, "width": 1240, "height": 600, "tabOrder": 200}}],
    "singleVisual": {
        "visualType": "tableEx",
        "projections": {"Values": [
            {"queryRef": f"{IE}.Invoice Number"}, {"queryRef": f"{PE}.Project Code"},
            {"queryRef": f"{PE}.Project Name"}, {"queryRef": f"{PE}.Primary Client Name"},
            {"queryRef": f"{PE}.Engagement Primary Cost Center Name"}, {"queryRef": f"{PE}.Invoice Template"},
            {"queryRef": f"{IE}.Count Email"},
            {"queryRef": f"Sum({IE}.Time Card Billing Adjusted Amount)"},
            {"queryRef": f"Sum({IE}.Milestone Amount)"}
        ]},
        "prototypeQuery": {
            "Version": 2,
            "From": [{"Name": "i", "Entity": IE, "Type": 0}, {"Name": "p", "Entity": PE, "Type": 0}],
            "Select": [
                {"Column": {"Expression": {"SourceRef": {"Source": "i"}}, "Property": "Invoice Number"}, "Name": f"{IE}.Invoice Number", "NativeReferenceName": "Invoice #"},
                {"Column": {"Expression": {"SourceRef": {"Source": "p"}}, "Property": "Project Code"}, "Name": f"{PE}.Project Code", "NativeReferenceName": "Project Code"},
                {"Column": {"Expression": {"SourceRef": {"Source": "p"}}, "Property": "Project Name"}, "Name": f"{PE}.Project Name", "NativeReferenceName": "Project"},
                {"Column": {"Expression": {"SourceRef": {"Source": "p"}}, "Property": "Primary Client Name"}, "Name": f"{PE}.Primary Client Name", "NativeReferenceName": "Client"},
                {"Column": {"Expression": {"SourceRef": {"Source": "p"}}, "Property": "Engagement Primary Cost Center Name"}, "Name": f"{PE}.Engagement Primary Cost Center Name", "NativeReferenceName": "Cost Center"},
                {"Column": {"Expression": {"SourceRef": {"Source": "p"}}, "Property": "Invoice Template"}, "Name": f"{PE}.Invoice Template", "NativeReferenceName": "Template"},
                {"Column": {"Expression": {"SourceRef": {"Source": "i"}}, "Property": "Count Email"}, "Name": f"{IE}.Count Email", "NativeReferenceName": "Emails"},
                {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Source": "i"}}, "Property": "Time Card Billing Adjusted Amount"}}, "Function": 0}, "Name": f"Sum({IE}.Time Card Billing Adjusted Amount)", "NativeReferenceName": "TC Amount"},
                {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Source": "i"}}, "Property": "Milestone Amount"}}, "Function": 0}, "Name": f"Sum({IE}.Milestone Amount)", "NativeReferenceName": "Milestone Amt"}
            ]
        },
        "drillFilterOtherVisuals": True,
        "objects": dark_table_objs,
        "vcObjects": dark_vc(True, "Invoice Email")
    }
}, 20, 100, 200, 1240, 600))

invoice_section = {
    "config": dark_page_cfg,
    "displayName": "Invoice Email",
    "displayOption": 1,
    "filters": "[]",
    "height": 720.0,
    "name": "c2d3e4f5a6b7c8d9e0f1",
    "ordinal": 1,
    "visualContainers": iv,
    "width": 1280.0
}

# ============================================================
# TIMECARD ALERTS PAGE
# ============================================================
tc = []
tc.append(textbox("tc01a1b2c3d4e5f6a7b8", 20, 4, 0, 400, 40, 0, "Timecard Alerts"))
tc.append(slicer("tc02a1b2c3d4e5f6a7b8", 20, 52, 100, 300, 38, 100, PE, "Engagement Manager Display Name", "p", "Engagement Manager", "Engagement Manager"))
tc.append(slicer("tc03a1b2c3d4e5f6a7b8", 330, 52, 101, 300, 38, 101, TC, "Billing Status", "t", "Billing Status", "Billing Status"))
tc.append(vc({
    "name": "tc04a1b2c3d4e5f6a7b8",
    "layouts": [{"id": 0, "position": {"x": 20, "y": 100, "z": 200, "width": 800, "height": 600, "tabOrder": 200}}],
    "singleVisual": {
        "visualType": "tableEx",
        "projections": {"Values": [
            {"queryRef": f"{PE}.Project Name"}, {"queryRef": f"{TC}.Billing Status"},
            {"queryRef": f"{TC}.Time Contract Terms"}, {"queryRef": f"Sum({TC}.Person Hours)"}
        ]},
        "prototypeQuery": {
            "Version": 2,
            "From": [{"Name": "p", "Entity": PE, "Type": 0}, {"Name": "t", "Entity": TC, "Type": 0}],
            "Select": [
                {"Column": {"Expression": {"SourceRef": {"Source": "p"}}, "Property": "Project Name"}, "Name": f"{PE}.Project Name", "NativeReferenceName": "Project"},
                {"Column": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": "Billing Status"}, "Name": f"{TC}.Billing Status", "NativeReferenceName": "Status"},
                {"Column": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": "Time Contract Terms"}, "Name": f"{TC}.Time Contract Terms", "NativeReferenceName": "Contract"},
                {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": "Person Hours"}}, "Function": 0}, "Name": f"Sum({TC}.Person Hours)", "NativeReferenceName": "Hours"}
            ]
        },
        "drillFilterOtherVisuals": True,
        "objects": dark_table_objs,
        "vcObjects": dark_vc(True, "Timecard Details")
    }
}, 20, 100, 200, 800, 600))

tc.append(vc({
    "name": "tc05a1b2c3d4e5f6a7b8",
    "layouts": [{"id": 0, "position": {"x": 830, "y": 100, "z": 300, "width": 430, "height": 600, "tabOrder": 300}}],
    "singleVisual": {
        "visualType": "clusteredBarChart",
        "projections": {
            "Category": [{"queryRef": f"{TC}.Billing Status", "active": True}],
            "Y": [{"queryRef": f"Sum({TC}.Person Hours)"}]
        },
        "prototypeQuery": {
            "Version": 2,
            "From": [{"Name": "t", "Entity": TC, "Type": 0}],
            "Select": [
                {"Column": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": "Billing Status"}, "Name": f"{TC}.Billing Status", "NativeReferenceName": "Billing Status"},
                {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": "Person Hours"}}, "Function": 0}, "Name": f"Sum({TC}.Person Hours)", "NativeReferenceName": "Total Hours"}
            ]
        },
        "drillFilterOtherVisuals": True,
        "objects": {
            "categoryAxis": [{"properties": {"labelColor": {"solid": {"color": TEXT_SECONDARY}}}}],
            "valueAxis": [{"properties": {"labelColor": {"solid": {"color": TEXT_SECONDARY}}}}],
            "dataPoint": [{"properties": {"fill": {"solid": {"color": ACCENT}}}}],
            "labels": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": TEXT_PRIMARY}}}}]
        },
        "vcObjects": dark_vc(True, "Hours by Billing Status")
    }
}, 830, 100, 300, 430, 600))

timecard_section = {
    "config": dark_page_cfg,
    "displayName": "Timecard Alerts",
    "displayOption": 1,
    "filters": "[]",
    "height": 720.0,
    "name": "d3e4f5a6b7c8d9e0f1a2",
    "ordinal": 2,
    "visualContainers": tc,
    "width": 1280.0
}

# ============================================================
# OUTPUT
# ============================================================
sections = [overview_section, invoice_section, timecard_section]
# Output each section indented at the level expected inside `"sections": [ ... ]`
# The existing file uses 2-space indent, sections are at depth 2 (4 spaces)
for i, section in enumerate(sections):
    formatted = json.dumps(section, indent=2)
    # Re-indent: add 4 spaces to each line to match sections array depth
    lines = formatted.split('\n')
    indented_lines = []
    for j, line in enumerate(lines):
        if j == 0:
            indented_lines.append('    ' + line)
        else:
            indented_lines.append('    ' + line)
    result = '\n'.join(indented_lines)
    print(result + ',')
