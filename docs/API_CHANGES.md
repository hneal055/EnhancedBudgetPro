# API Documentation - EnhancedBudgetPro

## Recent Changes

### MonteCarloBudgetEngine - v1.1 (2025-12-13)

**New Parameter: `risk_factor`**

The `simulate_budget()` method now accepts an optional `risk_factor` parameter as an alias for `volatility`.

#### Signatures

```python
def simulate_budget(
    self,
    simulations: int,
    base_cost: float,
    volatility: float = 10,
    risk_factor: float = None
) -> dict:
```

#### Parameters

- `simulations` (int): Number of Monte Carlo simulation runs (100-10000 recommended)
- `base_cost` (float): Base budget amount to simulate variations on
- `volatility` (float, optional): Percentage volatility (±%). Default: 10
- `risk_factor` (float, optional): Alternative to `volatility`. If provided, overrides volatility.
  - Values < 1.0 treated as decimal (e.g., 0.10 = 10%)
  - Values >= 1.0 treated as percentage (e.g., 10 = 10%)

#### Returns

Dictionary with:
- `simulations` (list): All simulated cost values
- `mean` (float): Average simulated cost
- `p10` (float): 10th percentile (downside scenario)
- `p90` (float): 90th percentile (upside scenario)

#### Example Usage

```python
from AnalysisEngine.monte_carlo_engine import MonteCarloBudgetEngine

mc = MonteCarloBudgetEngine()

# Option 1: Using volatility parameter (existing)
result = mc.simulate_budget(
    simulations=1000,
    base_cost=100000,
    volatility=15  # ±15% variation
)

# Option 2: Using risk_factor (new) - decimal
result = mc.simulate_budget(
    simulations=1000,
    base_cost=100000,
    risk_factor=0.15  # ±15% variation
)

# Option 3: Using risk_factor - percentage
result = mc.simulate_budget(
    simulations=1000,
    base_cost=100000,
    risk_factor=15  # ±15% variation
)

print(f"Mean: ${result['mean']:,.2f}")
print(f"Range: ${result['p10']:,.2f} - ${result['p90']:,.2f}")
```

#### Backward Compatibility

✅ **Fully backward compatible** - existing code using `volatility` continues to work without changes.

---

## Loader Schema Contract

All script loaders (`load_fdx`, `load_fountain`, `load_celtx`, `load_pdf`, `load_text`) return:

```python
{
    "scenes": [
        {
            "heading": str,        # Scene heading (e.g., "INT. CAFE - DAY")
            "lines": [str],        # All dialogue and action lines
            "characters": [str],   # Character names in this scene
            "dialogue_lines": int, # Count of dialogue lines
            "action_lines": int    # Count of action/description lines
        }
    ],
    "characters": [str],  # All unique characters in script
    "scene_count": int    # Total number of scenes
}
```

### Schema Validation

Use `src.validation.validate_parsed_script()` to ensure loader output conforms to contract.

```python
from src.validation import validate_parsed_script

data = load_fdx('script.fdx')
validate_parsed_script(data)  # Raises ParseError if invalid
```

---

## Scene Schema Update (2025-12-13)

**Breaking Change (Mitigated)**

Scene objects now use `heading` instead of `header`:

```python
# OLD (deprecated)
scene["header"]  # May raise KeyError

# NEW (recommended)
scene.get("heading", scene.get("header", "<unknown>"))  # Safe fallback
```

All engines and pages have been updated to use the safe `.get()` pattern for backward compatibility.

