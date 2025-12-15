def test_scenario_comparison_selection():
    scenarios = {
        "A": {"new_cast_total": 1000, "compressed_days": 3, "config": {"volatility": 0.02}, "mc": {"mean": 1100, "p90": 1300}},
        "B": {"new_cast_total": 1200, "compressed_days": 2, "config": {"volatility": 0.05}, "mc": {"mean": 1250, "p90": 1500}},
    }
    selected = ["A", "B"]
    rows = []
    for name in selected:
        s = scenarios[name]
        rows.append({
            "Scenario": name,
            "Cast Cost": s["new_cast_total"],
            "Shoot Days": s["compressed_days"],
            "Volatility": s["config"].get("volatility", 0),
            "MC Mean Cost": s["mc"]["mean"],
            "MC P95 Cost": s["mc"]["p90"],
        })
    assert rows[0]["Scenario"] == "A"
    assert rows[1]["Scenario"] == "B"
    assert rows[0]["Cast Cost"] == 1000
    assert rows[1]["MC P95 Cost"] == 1500
    print("Scenario comparison selection logic test passed.")

if __name__ == "__main__":
    test_scenario_comparison_selection()
