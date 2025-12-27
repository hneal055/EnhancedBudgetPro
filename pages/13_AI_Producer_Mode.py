"""
Phase 12.0 - AI Producer Mode: Insight Engine UI
Read-only producer guidance system
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.AnalysisEngine.insight_engine import (
    InsightEngine,
    InsightSeverity,
    InsightCategory
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Page Config
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.set_page_config(
    page_title="AI Producer Mode - EnhancedBudgetPro",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Producer Mode")
st.caption("Phase 12.0 - Insight Engine • Read-Only Analysis & Guidance")

st.markdown("""
**What This Does:**
- Observes your script, budget, schedule, and risk data
- Identifies patterns, inefficiencies, and opportunities
- Provides actionable producer-level guidance
- **Zero modifications** - completely read-only

**What This Doesn't Do:**
- ❌ Auto-modify budgets or schedules
- ❌ Make decisions for you
- ❌ Change any session data
""")

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Prerequisites Check
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if "data" not in st.session_state or st.session_state.data is None:
    st.warning("⚠️ No script loaded. Upload a script on the Home page first.")
    st.stop()

if "master_budget" not in st.session_state or st.session_state.master_budget is None:
    st.info("💡 Run Production Budget calculation to get budget insights.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Run Insight Engine
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if st.button("🔍 Analyze Production", type="primary", width='stretch'):
    with st.spinner("🧠 AI Producer analyzing your production..."):
        engine = InsightEngine()
        insights = engine.analyze_session(st.session_state)
        
        # Store in session state
        st.session_state.producer_insights = insights
        st.session_state.insight_summary = engine.to_summary()
        
        st.success(f"✅ Analysis complete! Found {len(insights)} insights.")
        st.rerun()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Display Insights
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if "producer_insights" in st.session_state and st.session_state.producer_insights:
    insights = st.session_state.producer_insights
    summary = st.session_state.get("insight_summary", {})
    
    # Summary Dashboard
    st.header("📊 Insight Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    severity_counts = summary.get("by_severity", {})
    
    with col1:
        critical = severity_counts.get("critical", 0)
        st.metric(
            "🚨 Critical",
            critical,
            delta=None,
            delta_color="inverse"
        )
    
    with col2:
        warnings = severity_counts.get("warning", 0)
        st.metric(
            "⚠️ Warnings",
            warnings,
            delta=None
        )
    
    with col3:
        info = severity_counts.get("info", 0)
        st.metric(
            "ℹ️ Info",
            info,
            delta=None
        )
    
    with col4:
        success = severity_counts.get("success", 0)
        st.metric(
            "✅ Positive",
            success,
            delta=None,
            delta_color="normal"
        )
    
    st.divider()
    
    # Filter Controls
    st.subheader("🔧 Filter Insights")
    
    filter_col1, filter_col2 = st.columns(2)
    
    with filter_col1:
        severity_filter = st.multiselect(
            "Filter by Severity",
            options=["critical", "warning", "info", "success"],
            default=["critical", "warning"]
        )
    
    with filter_col2:
        category_filter = st.multiselect(
            "Filter by Category",
            options=["budget", "schedule", "talent", "risk", "efficiency", "opportunity"],
            default=["budget", "schedule", "talent", "risk", "efficiency", "opportunity"]
        )
    
    # Filter insights
    filtered = [
        i for i in insights
        if i.severity.value in severity_filter
        and i.category.value in category_filter
    ]
    
    if not filtered:
        st.info("No insights match your filters.")
        st.stop()
    
    st.divider()
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Display Filtered Insights
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    st.header(f"📋 Insights ({len(filtered)})")
    
    # Severity icons
    severity_icons = {
        "critical": "🚨",
        "warning": "⚠️",
        "info": "ℹ️",
        "success": "✅"
    }
    
    # Category icons
    category_icons = {
        "budget": "💰",
        "schedule": "📅",
        "talent": "🎭",
        "risk": "⚠️",
        "efficiency": "⚡",
        "opportunity": "💡"
    }
    
    # Group by severity (critical first)
    critical_insights = [i for i in filtered if i.severity.value == "critical"]
    warning_insights = [i for i in filtered if i.severity.value == "warning"]
    info_insights = [i for i in filtered if i.severity.value == "info"]
    success_insights = [i for i in filtered if i.severity.value == "success"]
    
    all_grouped = [
        ("🚨 Critical Issues", critical_insights, "error"),
        ("⚠️ Warnings", warning_insights, "warning"),
        ("ℹ️ Information", info_insights, "info"),
        ("✅ Positive Indicators", success_insights, "success")
    ]
    
    for group_title, group_insights, alert_type in all_grouped:
        if not group_insights:
            continue
        
        st.subheader(group_title)
        
        for insight in group_insights:
            # Create expander for each insight
            with st.expander(
                f"{category_icons.get(insight.category.value, '📌')} {insight.title}",
                expanded=(insight.severity.value == "critical")
            ):
                # Description
                st.markdown(f"**{insight.description}**")
                
                # Data points
                if insight.data_points:
                    st.markdown("**📊 Data Points:**")
                    data_col1, data_col2 = st.columns(2)
                    
                    items = list(insight.data_points.items())
                    mid = len(items) // 2
                    
                    with data_col1:
                        for key, value in items[:mid]:
                            if isinstance(value, (int, float)):
                                if "pct" in key or "percentage" in key:
                                    st.metric(key.replace("_", " ").title(), f"{value:.1f}%")
                                elif "rate" in key or "cost" in key or "total" in key or "budget" in key:
                                    st.metric(key.replace("_", " ").title(), f"${value:,.0f}")
                                else:
                                    st.metric(key.replace("_", " ").title(), f"{value:.1f}")
                            else:
                                st.markdown(f"- **{key.replace('_', ' ').title()}:** {value}")
                    
                    with data_col2:
                        for key, value in items[mid:]:
                            if isinstance(value, (int, float)):
                                if "pct" in key or "percentage" in key:
                                    st.metric(key.replace("_", " ").title(), f"{value:.1f}%")
                                elif "rate" in key or "cost" in key or "total" in key or "budget" in key:
                                    st.metric(key.replace("_", " ").title(), f"${value:,.0f}")
                                else:
                                    st.metric(key.replace("_", " ").title(), f"{value:.1f}")
                            else:
                                st.markdown(f"- **{key.replace('_', ' ').title()}:** {value}")
                
                # Recommendation
                if insight.recommendation:
                    st.markdown("---")
                    st.markdown(f"**💡 Producer Recommendation:**")
                    st.info(insight.recommendation)
        
        st.divider()
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Export Insights
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    st.header("📥 Export Insights")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        # Export as JSON
        import json
        insights_json = json.dumps(
            [i.to_dict() for i in insights],
            indent=2
        )
        
        st.download_button(
            label="💾 Download as JSON",
            data=insights_json,
            file_name="producer_insights.json",
            mime="application/json",
            width='stretch'
        )
    
    with export_col2:
        # Export as text report
        report_lines = ["=" * 60, "AI PRODUCER MODE - INSIGHT REPORT", "=" * 60, ""]
        report_lines.append(f"Total Insights: {len(insights)}\n")
        
        for severity_name, insights_list, _ in all_grouped:
            if insights_list:
                report_lines.append(f"\n{severity_name}")
                report_lines.append("-" * 60)
                
                for insight in insights_list:
                    report_lines.append(f"\n{insight.title}")
                    report_lines.append(f"Category: {insight.category.value.title()}")
                    report_lines.append(f"{insight.description}")
                    
                    if insight.recommendation:
                        report_lines.append(f"Recommendation: {insight.recommendation}")
                    
                    report_lines.append("")
        
        report_text = "\n".join(report_lines)
        
        st.download_button(
            label="📄 Download as Text Report",
            data=report_text,
            file_name="producer_insights.txt",
            mime="text/plain",
            width='stretch'
        )

else:
    st.info("👆 Click 'Analyze Production' above to generate AI producer insights.")
    
    # Show what data is available
    st.subheader("📦 Available Data for Analysis")
    
    check_col1, check_col2 = st.columns(2)
    
    with check_col1:
        st.markdown("**✅ Available:**")
        if "data" in st.session_state and st.session_state.data:
            st.markdown("- ✓ Script data")
        if "intel" in st.session_state and st.session_state.intel:
            st.markdown("- ✓ Character intelligence")
        if "master_budget" in st.session_state and st.session_state.master_budget:
            st.markdown("- ✓ Production budget")
        if "schedule" in st.session_state and st.session_state.schedule:
            st.markdown("- ✓ Shooting schedule")
    
    with check_col2:
        st.markdown("**❌ Missing:**")
        if "data" not in st.session_state or not st.session_state.data:
            st.markdown("- ✗ Script data")
        if "intel" not in st.session_state or not st.session_state.intel:
            st.markdown("- ✗ Character intelligence")
        if "master_budget" not in st.session_state or not st.session_state.master_budget:
            st.markdown("- ✗ Production budget")
        if "schedule" not in st.session_state or not st.session_state.schedule:
            st.markdown("- ✗ Shooting schedule")

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Footer
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.caption("""
**About AI Producer Mode:**
This system uses rule-based analysis (not LLM inference) to provide producer-level guidance.
All insights are derived from observable patterns in your data.
No machine learning models are involved - just seasoned production logic.

**Phase 12.0** - Read-only analysis | Zero risk | Pure observation
""")

import streamlit as st

st.title("Monte Carlo Simulation")

if "data" not in st.session_state:
    st.warning("Please upload and analyze a script first.")
    st.stop()

st.info("This page is under construction. Core logic coming soon.")
