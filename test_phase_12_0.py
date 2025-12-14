"""
Phase 12.0 - AI Producer Mode: Insight Engine Test
Validates read-only analysis with mock session data
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.AnalysisEngine.insight_engine import InsightEngine, InsightSeverity, InsightCategory


def create_mock_session_state():
    """Create realistic mock session data for testing"""
    return {
        # Script data
        "data": {
            "scenes": [
                {"heading": "INT. COFFEE SHOP - DAY", "lines": ["A: Hello", "B: Hi"], "characters": ["A", "B"]},
                {"heading": "EXT. STREET - NIGHT", "lines": ["Action line"], "characters": ["A"]},
                {"heading": "INT. APARTMENT - DAY", "lines": ["C: Dialogue"], "characters": ["C"]},
                {"heading": "INT. OFFICE - DAY", "lines": ["A: Talk", "B: More talk"], "characters": ["A", "B"]},
                {"heading": "EXT. PARK - DAY", "lines": ["Action"], "characters": ["A", "C"]},
            ],
            "characters": ["A", "B", "C"],
            "scene_count": 5
        },
        
        # Character intelligence
        "intel": {
            "A": {"scenes": 4, "dialogue_lines": 15, "estimated_screen_time_min": 25},
            "B": {"scenes": 2, "dialogue_lines": 8, "estimated_screen_time_min": 10},
            "C": {"scenes": 2, "dialogue_lines": 5, "estimated_screen_time_min": 8}
        },
        
        # Cost data
        "cost": {
            "A": {"daily_rate": 2000, "shoot_days": 4, "total": 8000},
            "B": {"daily_rate": 1500, "shoot_days": 2, "total": 3000},
            "C": {"daily_rate": 800, "shoot_days": 2, "total": 1600}
        },
        
        # Master budget
        "master_budget": {
            "crew_total": 45000,
            "cast_total": 12600,
            "equipment_total": 28000,
            "location_total": 15000,
            "post_total": 35000,
            "insurance_total": 8000,
            "total": 143600
        },
        
        # Schedule
        "schedule": {
            "shoot_days": 8,
            "day_assignments": {
                "Day 1": ["scene_1", "scene_2"],
                "Day 2": ["scene_3"],
                "Day 3": ["scene_4", "scene_5", "scene_6"],
                "Day 4": ["scene_7"],
                "Day 5": ["scene_8"],
                "Day 6": ["scene_9", "scene_10"],
                "Day 7": ["scene_11"],
                "Day 8": ["scene_12"]
            }
        },
        
        # Scene density
        "density": {
            "scene_1": {"dialogue_action_ratio": 2.5},
            "scene_2": {"dialogue_action_ratio": 0.8},
            "scene_3": {"dialogue_action_ratio": 3.0},
            "scene_4": {"dialogue_action_ratio": 2.2},
            "scene_5": {"dialogue_action_ratio": 1.5}
        },
        
        # Risks
        "risks": [
            {"scene": "scene_1", "risk_type": "weather", "risk_level": "HIGH"},
            {"scene": "scene_2", "risk_type": "complexity", "risk_level": "MEDIUM"},
            {"scene": "scene_3", "risk_type": "location", "risk_level": "HIGH"},
            {"scene": "scene_4", "risk_type": "cast", "risk_level": "LOW"},
            {"scene": "scene_5", "risk_type": "stunts", "risk_level": "HIGH"}
        ],
        
        # Monte Carlo simulation
        "monte_carlo": {
            "p10": 125000,
            "p50": 143600,
            "p90": 180000,
            "mean": 149500
        },
        
        # Talent conflicts
        "talent_overrides": {
            "A": ["Day 3", "Day 7"],
            "B": []
        }
    }


def test_insight_engine():
    """Run full Insight Engine test"""
    print("=" * 60)
    print("PHASE 12.0 - AI PRODUCER MODE: INSIGHT ENGINE TEST")
    print("=" * 60)
    print()
    
    # Create mock data
    print("📦 Creating mock session data...")
    session_state = create_mock_session_state()
    print(f"   ✓ {session_state['data']['scene_count']} scenes")
    print(f"   ✓ {len(session_state['intel'])} characters")
    print(f"   ✓ ${session_state['master_budget']['total']:,} budget")
    print(f"   ✓ {session_state['schedule']['shoot_days']} shoot days")
    print()
    
    # Initialize engine
    print("🧠 Initializing Insight Engine...")
    engine = InsightEngine()
    print("   ✓ Engine ready")
    print()
    
    # Run analysis
    print("🔍 Running analysis...")
    insights = engine.analyze_session(session_state)
    print(f"   ✓ Found {len(insights)} insights")
    print()
    
    # Get summary
    summary = engine.to_summary()
    
    # Display summary
    print("📊 INSIGHT SUMMARY")
    print("-" * 60)
    print(f"Total Insights: {summary['total_insights']}")
    print()
    
    print("By Severity:")
    for severity, count in summary['by_severity'].items():
        icon = {"critical": "🚨", "warning": "⚠️", "info": "ℹ️", "success": "✅"}.get(severity, "📌")
        print(f"  {icon} {severity.title()}: {count}")
    print()
    
    print("By Category:")
    for category, count in summary['by_category'].items():
        if count > 0:
            icon = {
                "budget": "💰",
                "schedule": "📅",
                "talent": "🎭",
                "risk": "⚠️",
                "efficiency": "⚡",
                "opportunity": "💡"
            }.get(category, "📌")
            print(f"  {icon} {category.title()}: {count}")
    print()
    
    # Display insights by severity
    print("=" * 60)
    print("DETAILED INSIGHTS")
    print("=" * 60)
    print()
    
    # Group by severity
    critical = engine.get_insights_by_severity(InsightSeverity.CRITICAL)
    warnings = engine.get_insights_by_severity(InsightSeverity.WARNING)
    info_insights = engine.get_insights_by_severity(InsightSeverity.INFO)
    success = engine.get_insights_by_severity(InsightSeverity.SUCCESS)
    
    for severity_name, insights_list in [
        ("🚨 CRITICAL ISSUES", critical),
        ("⚠️ WARNINGS", warnings),
        ("ℹ️ INFORMATION", info_insights),
        ("✅ POSITIVE INDICATORS", success)
    ]:
        if not insights_list:
            continue
        
        print(severity_name)
        print("-" * 60)
        
        for insight in insights_list:
            print(f"\n📌 {insight.title}")
            print(f"   Category: {insight.category.value.title()}")
            print(f"   {insight.description}")
            
            if insight.data_points:
                print("   Data Points:")
                for key, value in insight.data_points.items():
                    if isinstance(value, (int, float)):
                        if "pct" in key or "percentage" in key:
                            print(f"     • {key}: {value:.1f}%")
                        elif "rate" in key or "cost" in key or "total" in key or "budget" in key:
                            print(f"     • {key}: ${value:,.0f}")
                        else:
                            print(f"     • {key}: {value:.2f}")
                    else:
                        print(f"     • {key}: {value}")
            
            if insight.recommendation:
                print(f"   💡 Recommendation: {insight.recommendation}")
        
        print()
    
    # Test filtering
    print("=" * 60)
    print("TESTING FILTERS")
    print("=" * 60)
    print()
    
    budget_insights = engine.get_insights_by_category(InsightCategory.BUDGET)
    print(f"Budget Insights: {len(budget_insights)}")
    for insight in budget_insights:
        print(f"  • {insight.title}")
    print()
    
    risk_insights = engine.get_insights_by_category(InsightCategory.RISK)
    print(f"Risk Insights: {len(risk_insights)}")
    for insight in risk_insights:
        print(f"  • {insight.title}")
    print()
    
    # Test critical filter
    critical_only = engine.get_critical_insights()
    print(f"Critical Only: {len(critical_only)}")
    for insight in critical_only:
        print(f"  • {insight.title}")
    print()
    
    # Validation
    print("=" * 60)
    print("VALIDATION")
    print("=" * 60)
    print()
    
    checks = [
        ("At least one insight generated", len(insights) > 0),
        ("Budget insights present", len(budget_insights) > 0),
        ("Risk insights present", len(risk_insights) > 0),
        ("Summary totals match", summary['total_insights'] == len(insights)),
        ("All insights have titles", all(i.title for i in insights)),
        ("All insights have descriptions", all(i.description for i in insights)),
        ("All insights have categories", all(i.category for i in insights)),
        ("All insights have severities", all(i.severity for i in insights))
    ]
    
    passed = 0
    failed = 0
    
    for check_name, check_result in checks:
        if check_result:
            print(f"✅ {check_name}")
            passed += 1
        else:
            print(f"❌ {check_name}")
            failed += 1
    
    print()
    print(f"Results: {passed} passed, {failed} failed")
    print()
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED - Phase 12.0 ready for production!")
    else:
        print(f"⚠️ {failed} test(s) failed - review implementation")
    
    return failed == 0


if __name__ == "__main__":
    success = test_insight_engine()
    sys.exit(0 if success else 1)
