# Excel Data Contracts Specification
**Version:** 1.0.0  
**Phase:** 11.1 - Studio Excel Export Standardization  
**Last Updated:** December 14, 2025

---

## Core Principles

### 1. Fundamental Rule
**ONE ROW = ONE REAL-WORLD LINE ITEM**

Every row in every sheet must represent a single, discrete business entity:
- One crew member role
- One equipment rental
- One cast member
- One scene
- One risk item

### 2. Prohibited Structures
❌ **NEVER ALLOWED:**
- Nested dictionaries in cells
- JSON strings in cells
- Lists/arrays in cells (except comma-separated strings for display)
- Multi-line text in single cells (except Notes fields)
- Merged cells (except headers)
- Formulas that reference other sheets

### 3. Data Type Standards
| Type | Format | Example | Notes |
|------|--------|---------|-------|
| Currency | Float/Integer | `25000` | NO dollar signs, NO commas |
| Date | ISO-8601 | `2025-12-14` | YYYY-MM-DD format |
| Shoot Day | Integer | `15` | 1-based day number |
| Percentage | Float | `0.12` | Decimal format, not "12%" |
| String | UTF-8 Text | `John Smith` | No special encoding |
| Boolean | String | `TRUE` / `FALSE` | All caps |

---

## File 1: EBP_Master_Budget.xlsx

### Input Data Contract
```python
{
    "master_budget": {
        "cast_total": float,              # Required
        "crew_total": float,              # Required
        "equipment_total": float,         # Required
        "location_total": float,          # Required
        "post_total": float,              # Required
        "insurance_total": float,         # Required
        "total": float,                   # Required
        "subtotal_before_insurance": float,  # Required
        
        # Optional: If not provided, generates defaults
        "crew_breakdown": List[{
            "Department": str,            # Required
            "Role": str,                  # Required
            "Rate": float,                # Required (no $)
            "Units": int,                 # Required
            "Unit_Type": str,             # "days" | "weeks" | "flat"
            "Notes": str                  # Optional
        }],
        
        "equipment_breakdown": List[{
            "Package": str,               # Required
            "Item": str,                  # Required
            "Rate": float,                # Required
            "Units": int,                 # Required
            "Unit_Type": str,             # "days" | "weeks"
            "Notes": str                  # Optional
        }],
        
        "post_breakdown": List[{
            "Category": str,              # Required
            "Item": str,                  # Required
            "Rate": float,                # Required
            "Units": int,                 # Required
            "Unit_Type": str,             # "weeks" | "flat" | "shots"
            "Notes": str                  # Optional
        }]
    },
    
    "intel": {
        "<character_name>": {
            "scenes": int,                    # Required
            "dialogue_lines": int,            # Required
            "estimated_screen_time_min": int  # Required
        }
    },
    
    "cost": {
        "<character_name>": {
            "daily_rate": float,          # Required
            "total_cost": float           # Required
        }
    },
    
    "data": {
        "scenes": List[{
            "heading": str,               # Required
            "characters": List[str],      # Required
            "dialogue_lines": int,        # Optional
            "action_lines": int           # Optional
        }]
    },
    
    "schedule": {
        "shoot_days": int                 # Required for defaults
    }
}
```

### Sheet 1: Summary
**Purpose:** High-level budget totals

| Column | Type | Required | Validation |
|--------|------|----------|------------|
| Category | string | Yes | Fixed values: "Above-The-Line", "Crew", "Equipment", "Locations", "Post-Production", "Insurance & Contingency", "GRAND TOTAL" |
| Total Cost | float | Yes | Must be >= 0 |

**Row Count:** Exactly 7 rows  
**Validation:** Sum of first 6 rows must equal GRAND TOTAL

### Sheet 2: Crew
**Purpose:** Per-role crew costs

| Column | Type | Required | Validation |
|--------|------|----------|------------|
| Department | string | Yes | Non-empty |
| Role | string | Yes | Non-empty |
| Rate | float | Yes | Must be >= 0 |
| Units | integer | Yes | Must be >= 1 |
| Unit Type | string | Yes | "days" \| "weeks" \| "flat" |
| Total Cost | float | Yes | Must equal Rate × Units |
| Notes | string | No | Max 500 chars |

**Minimum Rows:** 1  
**Validation:** Total Cost must be calculated, not user-provided

### Sheet 3: Cast
**Purpose:** Per-character talent costs

| Column | Type | Required | Validation |
|--------|------|----------|------------|
| Character | string | Yes | Must exist in intel dict |
| Scenes | integer | Yes | Must be >= 1 |
| Dialogue Lines | integer | Yes | Must be >= 0 |
| Screen Time (min) | integer | Yes | Must be >= 0 |
| Daily Rate | float | Yes | Must be >= 0 |
| Days Needed | integer | Yes | Must be >= 1 |
| Total Cost | float | Yes | Should equal Daily Rate × Days Needed |
| Notes | string | No | Max 500 chars |

**Minimum Rows:** 1  
**Validation:** Character names must be unique

### Sheet 4: Equipment
**Purpose:** Rental package line items

| Column | Type | Required | Validation |
|--------|------|----------|------------|
| Package | string | Yes | Non-empty |
| Item | string | Yes | Non-empty |
| Rate | float | Yes | Must be >= 0 |
| Units | integer | Yes | Must be >= 1 |
| Unit Type | string | Yes | "days" \| "weeks" |
| Total Cost | float | Yes | Must equal Rate × Units |
| Notes | string | No | Max 500 chars |

**Minimum Rows:** 1

### Sheet 5: Locations
**Purpose:** Per-location costs

| Column | Type | Required | Validation |
|--------|------|----------|------------|
| Location | string | Yes | Non-empty, unique |
| Scenes | integer | Yes | Must be >= 1 |
| Scout Cost | float | Yes | Must be >= 0 |
| Permit Cost | float | Yes | Must be >= 0 |
| Location Fee | float | Yes | Must be >= 0 |
| Total Cost | float | Yes | Must equal Scout + Permit + Location Fee |
| Notes | string | No | Max 500 chars |

**Minimum Rows:** 1  
**Validation:** Location names should come from scene headings

### Sheet 6: Post
**Purpose:** Post-production line items

| Column | Type | Required | Validation |
|--------|------|----------|------------|
| Category | string | Yes | "Editing" \| "Color" \| "Sound" \| "VFX" \| "Music" |
| Item | string | Yes | Non-empty |
| Rate | float | Yes | Must be >= 0 |
| Units | integer | Yes | Must be >= 1 |
| Unit Type | string | Yes | "weeks" \| "flat" \| "shots" |
| Total Cost | float | Yes | Must equal Rate × Units |
| Notes | string | No | Max 500 chars |

**Minimum Rows:** 1

### Sheet 7: Insurance
**Purpose:** Insurance and contingency

| Column | Type | Required | Validation |
|--------|------|----------|------------|
| Category | string | Yes | Non-empty |
| Coverage | string | Yes | Non-empty |
| Rate | float | Yes | Must be >= 0 |
| Notes | string | No | Max 500 chars |

**Minimum Rows:** 1  
**Standard Categories:** "General Liability", "E&O Insurance", "Equipment Insurance", "Contingency (10%)"

### Sheet 8: __METADATA (Hidden)
**Purpose:** Audit trail

| Column | Type | Required | Validation |
|--------|------|----------|------------|
| Key | string | Yes | Fixed values |
| Value | string/boolean | Yes | Varies by key |

**Required Rows:**
- Project Name (string)
- Export Timestamp (ISO-8601 datetime)
- EBP Version (semver string)
- Budget Locked (TRUE/FALSE)
- Schedule Locked (TRUE/FALSE)

---

## File 2: EBP_Shooting_Schedule.xlsx

### Input Data Contract
```python
{
    "schedule": {
        "shoot_days": int,               # Required
        "day_assignments": {             # Optional
            <day_num: int>: List[int]    # Scene IDs
        }
    },
    
    "data": {
        "scenes": List[{
            "heading": str,               # Required
            "characters": List[str],      # Required
            "dialogue_lines": int,        # Optional
            "action_lines": int           # Optional
        }]
    }
}
```

### Sheet 1: Daily Schedule
**Purpose:** Stripboard-style day-by-day schedule

| Column | Type | Required | Validation |
|--------|------|----------|------------|
| Shoot Day | integer | Yes | 1-based, sequential |
| Scene | string | Yes | "Scene N" format |
| Location | string | Yes | From scene heading |
| Characters | string | Yes | Comma-separated list |
| Estimated Cost | float | Yes | Must be >= 0 |
| Risk Level | string | Yes | "HIGH" \| "MEDIUM" \| "LOW" |
| Notes | string | No | Max 500 chars |

**Minimum Rows:** 1  
**Validation:** Shoot Days must be sequential within tolerance

### Sheet 2: Scene Breakdown
**Purpose:** Scene metadata

| Column | Type | Required | Validation |
|--------|------|----------|------------|
| Scene # | integer | Yes | 1-based, sequential |
| Heading | string | Yes | Non-empty |
| Characters | string | Yes | Comma-separated |
| Dialogue Lines | integer | Yes | Must be >= 0 |
| Action Lines | integer | Yes | Must be >= 0 |
| Page Est | float | Yes | (Dialogue + Action) / 55 |
| Notes | string | No | Max 500 chars |

**Minimum Rows:** 1  
**Validation:** Page Est must be calculated

---

## File 3: EBP_Talent_Availability.xlsx

### Input Data Contract
```python
{
    "intel": {
        "<character_name>": {
            # Character data
        }
    },
    
    "schedule": {
        "shoot_days": int                # Required
    },
    
    "talent_overrides": {                # Optional
        "<character_name>": {
            "Day <N>": str               # Conflict description
        }
    }
}
```

### Sheet 1: Talent Availability
**Purpose:** Character × Day availability matrix

| Column | Type | Required | Validation |
|--------|------|----------|------------|
| Character | string | Yes | Must exist in intel |
| Shoot Day | integer | Yes | 1 to shoot_days |
| Availability | string | Yes | "Available" \| "Conflict" |
| Conflict | string | No | Non-empty if Availability = "Conflict" |
| Notes | string | No | Max 500 chars |

**Minimum Rows:** characters × shoot_days  
**Critical:** ONE ROW PER CHARACTER PER DAY

**Validation Rules:**
- Total rows must equal len(intel) × shoot_days
- Each (Character, Shoot Day) pair must be unique
- If Availability = "Conflict", Conflict column must not be empty

---

## File 4: EBP_Risk_Forecast.xlsx

### Input Data Contract
```python
{
    "risks": List[{
        "scene": str,                    # Required
        "risk_type": str,                # Required
        "risk_level": str,               # Required: "HIGH" | "MEDIUM" | "LOW"
        "mitigation": str                # Required
    }],
    
    "monte_carlo": {                     # Optional
        "p10": float,
        "p50": float,
        "p90": float
    }
}
```

### Sheet 1: Risk Summary
**Purpose:** Aggregate risk statistics

| Column | Type | Required | Validation |
|--------|------|----------|------------|
| Metric | string | Yes | Fixed values |
| Count | integer | Yes | Must be >= 0 |

**Required Rows:**
- "High Risk Scenes"
- "Medium Risk Scenes"
- "Low Risk Scenes"
- "Total Scenes"

**Validation:** Sum of first 3 must equal Total Scenes

### Sheet 2: Scene Risk
**Purpose:** Per-scene risk breakdown

| Column | Type | Required | Validation |
|--------|------|----------|------------|
| Scene | string | Yes | Non-empty |
| Risk Type | string | Yes | Non-empty |
| Risk Level | string | Yes | "HIGH" \| "MEDIUM" \| "LOW" |
| Mitigation | string | Yes | Non-empty |
| Notes | string | No | Max 500 chars |

**Minimum Rows:** 1  
**Validation:** Risk Level must be uppercase

### Sheet 3: Monte Carlo
**Purpose:** Budget simulation results

| Column | Type | Required | Validation |
|--------|------|----------|------------|
| Percentile | string | Yes | Fixed format |
| Budget | float | Yes | Must be >= 0 |

**Required Rows:**
- "P10 (Best Case)"
- "P50 (Most Likely)"
- "P90 (Worst Case)"

**Validation:** P10 <= P50 <= P90

---

## Global Validation Rules

### 1. File-Level Validation
- All files must be valid .xlsx format
- All files must open without errors in Excel, Numbers, Google Sheets
- Sheet names must be ASCII-compatible
- No external links or references
- File size < 50MB

### 2. Cell-Level Validation
- No empty cells in required columns
- No NULL or NaN values
- No infinity values
- Strings max 65,535 characters
- No control characters (except newlines in Notes)

### 3. Type Coercion Rules
```python
# Currency: Always float
"$25,000" → 25000.0  # Remove $ and commas
"25000" → 25000.0

# Dates: Always ISO-8601 string
"12/14/2025" → "2025-12-14"
datetime(2025, 12, 14) → "2025-12-14"

# Booleans: Always uppercase string
True → "TRUE"
1 → "TRUE"
0 → "FALSE"

# Lists: Comma-separated string
["John", "Mary"] → "John, Mary"
```

### 4. Error Handling
If validation fails:
1. Raise `ValueError` with specific error message
2. Include row/column number in error
3. Include expected vs actual values
4. Do NOT attempt to auto-correct
5. Do NOT export partial files

---

## Validation Test Suite

### Required Tests
```python
def test_master_budget_contract():
    """Validate Master Budget data contract"""
    # Test all 7 sheets exist
    # Test row counts
    # Test column names
    # Test data types
    # Test calculations
    pass

def test_shooting_schedule_contract():
    """Validate Shooting Schedule data contract"""
    # Test scene sequence
    # Test shoot day continuity
    # Test page calculations
    pass

def test_talent_availability_contract():
    """Validate Talent Availability matrix"""
    # Test rows = characters × days
    # Test no duplicate (character, day) pairs
    # Test conflict logic
    pass

def test_risk_forecast_contract():
    """Validate Risk Forecast data contract"""
    # Test risk level enum
    # Test summary calculations
    # Test Monte Carlo ordering
    pass

def test_no_nested_structures():
    """Ensure no nested dicts/lists in cells"""
    # Scan all cells
    # Reject any dict/list types
    pass

def test_studio_compatibility():
    """Ensure files open cleanly"""
    # Open in openpyxl
    # Verify no errors
    # Check formatting preserved
    pass
```

---

## Changelog

### Version 1.0.0 (2025-12-14)
- Initial specification
- 4 export files defined
- Data contracts formalized
- Validation rules established

---

## Contact & Support

For questions about data contracts:
- **GitHub Issues:** https://github.com/hneal055/EnhancedBudgetPro/issues
- **Label:** `data-contract`
- **Documentation:** See `docs/` directory

---

**END OF SPECIFICATION**
