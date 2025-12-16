"""
Storytelling Insights Dashboard
AI Producer recommendations and script health analysis
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# Page config
st.set_page_config(page_title="Storytelling Insights", page_icon="🎬", layout="wide")

# Title
st.title("🎬 Storytelling Insights Dashboard")
st.markdown(
    "**AI Producer Analysis** - Comprehensive script health and recommendations"
)

# Prerequisites check
if not st.session_state.get("data"):
    st.error("⚠️ No script loaded. Please upload a script on the Home page.")
    st.stop()

if not st.session_state.get("emotion_data"):
    st.error("⚠️ Character analysis not run. Please analyze emotions first.")
    st.stop()

# Import engines
from src.CharacterArcEngine.arc_classifier import ArcClassifier
from src.CharacterArcEngine.arc_predictor import ArcPredictor
from src.CharacterArcEngine.consistency_analyzer import ConsistencyAnalyzer
from src.CharacterArcEngine.relationship_tracker import RelationshipTracker
from src.CharacterArcEngine.storytelling_insights import StorytellingInsights

# Get character arcs
character_arcs = st.session_state.emotion_data.get("character_arcs", {})

if not character_arcs:
    st.error("⚠️ No character arcs found. Ensure script has character dialogue.")
    st.stop()

# Generate all analyses if not cached
if "insights_data" not in st.session_state:
    with st.spinner("🧠 Generating AI Producer insights..."):

        # Classification
        classifier = ArcClassifier()
        classifications = {}
        for char, arc in character_arcs.items():
            if len(arc.get("scenes", [])) >= 3:
                classifications[char] = classifier.classify_arc(char, arc)

        # Predictions
        predictor = ArcPredictor()
        predictions = {}
        for char, classification in classifications.items():
            arc = character_arcs[char]
            predictions[char] = predictor.predict_completion(
                char, arc, classification["arc_type"]
            )

        # Relationships
        tracker = RelationshipTracker()
        relationships = []
        chars = list(classifications.keys())
        for i in range(len(chars)):
            for j in range(i + 1, len(chars)):
                char1, char2 = chars[i], chars[j]
                rel = tracker.track_relationship(
                    char1, character_arcs[char1], char2, character_arcs[char2]
                )
                if rel["shared_scenes"] > 0:
                    relationships.append(rel)

        # Consistency
        analyzer = ConsistencyAnalyzer()
        consistency = {}
        for char, arc in character_arcs.items():
            if len(arc.get("scenes", [])) >= 3:
                consistency[char] = analyzer.analyze_consistency(char, arc)

        # Generate insights
        insights_engine = StorytellingInsights()
        insights = insights_engine.generate_insights(
            character_arcs=character_arcs,
            classifications=classifications,
            predictions=predictions,
            relationships=relationships,
            consistency=consistency,
        )

        st.session_state.insights_data = insights
        st.session_state.classifications = classifications
        st.session_state.predictions = predictions
        st.session_state.relationships = relationships
        st.session_state.consistency = consistency

insights = st.session_state.insights_data

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# OVERALL SCRIPT HEALTH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("📊 Overall Script Health")

health = insights["overall_health"]

# Main health score
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.metric(
        "Overall Health Score",
        f"{health['score']:.0f}/100",
        delta=health["rating"],
        help="Aggregated score from character coverage, arc diversity, completion, and consistency",
    )

with col2:
    st.markdown(f"### {health['emoji']}")
    st.markdown(f"**{health['rating']}**")

with col3:
    st.metric("Characters Analyzed", insights["analyzed_arcs"])

# Health breakdown
st.subheader("🔍 Score Breakdown")

breakdown_data = []
for key, data in health["breakdown"].items():
    breakdown_data.append(
        {
            "Category": key.replace("_", " ").title(),
            "Score": f"{data['score']:.0f}/100",
            "Score_Value": data["score"],
        }
    )

df_breakdown = pd.DataFrame(breakdown_data)

# Horizontal bar chart
fig_breakdown = go.Figure(
    go.Bar(
        x=df_breakdown["Score_Value"],
        y=df_breakdown["Category"],
        orientation="h",
        marker=dict(
            color=df_breakdown["Score_Value"],
            colorscale="RdYlGn",
            cmin=0,
            cmax=100,
            showscale=False,
        ),
        text=df_breakdown["Score"],
        textposition="auto",
    )
)

fig_breakdown.update_layout(
    title="Health Score Breakdown",
    xaxis_title="Score (0-100)",
    height=300,
    xaxis=dict(range=[0, 100]),
)

st.plotly_chart(fig_breakdown, use_container_width=True)

# Strengths & Weaknesses
col1, col2 = st.columns(2)

with col1:
    st.success("**✅ Strengths**")
    for strength in health["strengths"]:
        st.write(f"• {strength}")

with col2:
    st.warning("**⚠️ Areas for Improvement**")
    for weakness in health["weaknesses"]:
        st.write(f"• {weakness}")

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PRIORITY RECOMMENDATIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("🎯 Priority Recommendations")

recommendations = insights["recommendations"]

# Group by priority
high_priority = [r for r in recommendations if r["priority"] == "HIGH"]
medium_priority = [r for r in recommendations if r["priority"] == "MEDIUM"]
low_priority = [r for r in recommendations if r["priority"] == "LOW"]

# Display by priority
if high_priority:
    st.error(f"**🚨 HIGH PRIORITY ({len(high_priority)})**")
    for rec in high_priority:
        with st.expander(f"{rec['character']} - {rec['category']}"):
            st.write(f"**Issue:** {rec['issue']}")
            st.write(f"**Action:** {rec['suggestion']}")

if medium_priority:
    st.warning(f"**⚠️ MEDIUM PRIORITY ({len(medium_priority)})**")
    for rec in medium_priority:
        with st.expander(f"{rec['character']} - {rec['category']}"):
            st.write(f"**Issue:** {rec['issue']}")
            st.write(f"**Action:** {rec['suggestion']}")

if low_priority:
    st.info(f"**ℹ️ LOW PRIORITY ({len(low_priority)})**")
    for rec in low_priority:
        with st.expander(f"{rec['character']} - {rec['category']}"):
            st.write(f"**Issue:** {rec['issue']}")
            st.write(f"**Action:** {rec['suggestion']}")

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PACING ANALYSIS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("⏱️ Pacing Analysis")

pacing = insights["pacing_analysis"]

col1, col2 = st.columns([1, 2])

with col1:
    st.metric(
        "Average Scenes/Character", f"{pacing['average_scenes_per_character']:.1f}"
    )
    st.markdown(f"### {pacing['emoji']}")
    st.write(pacing["overall_assessment"])

with col2:
    # Scene distribution chart
    dist = pacing["scene_distribution"]

    fig_dist = go.Figure(
        go.Bar(
            x=["Minimum", "Average", "Maximum"],
            y=[dist["min"], dist["avg"], dist["max"]],
            marker=dict(color=["#ff4444", "#4488ff", "#44ff44"]),
            text=[f"{dist['min']:.0f}", f"{dist['avg']:.1f}", f"{dist['max']:.0f}"],
            textposition="auto",
        )
    )

    fig_dist.update_layout(
        title="Scene Distribution Across Characters",
        yaxis_title="Number of Scenes",
        height=300,
    )

    st.plotly_chart(fig_dist, use_container_width=True)

# Pacing issues
if pacing["pacing_issues"]:
    st.subheader("⚠️ Pacing Issues Detected")
    for issue in pacing["pacing_issues"]:
        st.warning(issue)
else:
    st.success("✅ No significant pacing issues detected")

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EMOTIONAL ARC OPTIMIZATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("�� Emotional Arc Optimization")

optimizations = insights["arc_optimization"]

if optimizations:
    for opt in optimizations:
        with st.expander(
            f"{opt['character']} - {opt['current_completion']:.0f}% Complete"
        ):
            for suggestion in opt["suggestions"]:
                impact_color = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
                st.write(
                    f"{impact_color[suggestion['impact']]} **{suggestion['type']}**: {suggestion['description']}"
                )
else:
    st.success("✅ All character arcs are well-optimized")

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INDUSTRY BENCHMARKS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("📈 Industry Benchmark Comparison")

benchmarks = insights["benchmarks"]

# Overall alignment
alignment = benchmarks["overall_alignment"]
st.metric("Industry Alignment", f"{alignment['score']:.0f}%", delta=alignment["rating"])
st.markdown(f"### {alignment['emoji']} {alignment['rating']}")

# Detailed comparisons
st.subheader("📊 Metric Comparisons")

for comp in benchmarks["comparisons"]:
    status_color = {
        "Meets Industry Standard": "success",
        "Above Industry Standard": "info",
        "Below Industry Standard": "warning",
        "Limited": "warning",
        "Strong": "success",
    }

    with st.expander(f"{comp['metric']}: {comp['status']}"):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Current", comp["current"])
        with col2:
            st.metric("Benchmark", comp["benchmark"])

        method = getattr(st, status_color.get(comp["status"], "info"))
        method(f"**Recommendation:** {comp['recommendation']}")

st.info(f"ℹ️ {benchmarks['industry_note']}")

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXPORT SUMMARY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("📄 Executive Summary")

summary = insights["export_summary"]

st.subheader("📋 Quick Stats")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Characters", summary["quick_stats"]["characters_analyzed"])
with col2:
    st.metric("Arc Completion", f"{summary['quick_stats']['arc_completion_avg']:.0f}%")
with col3:
    st.metric("Consistency", f"{summary['quick_stats']['consistency_avg']:.0f}%")
with col4:
    st.metric("Priority Actions", summary["executive_summary"]["priority_actions"])

# Top priorities
st.subheader("🎯 Top 5 Action Items")
for i, priority in enumerate(summary["top_priorities"], 1):
    st.write(f"**{i}. {priority['character']}**")
    st.write(f"   Issue: {priority['issue']}")
    st.write(f"   Action: {priority['action']}")
    st.write("")

# Download button (future implementation)
st.download_button(
    label="📥 Download Full Report (Coming Soon)",
    data="Report generation in progress...",
    file_name="storytelling_insights.txt",
    mime="text/plain",
    disabled=True,
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXPORT CENTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.divider()
st.header("📥 Export Analysis Data")

import io
import tempfile
import zipfile

from src.ExportEngine.character_analysis_exporter import CharacterAnalysisExporter

# Export options
st.subheader("🎯 Select Export Formats")

col1, col2, col3 = st.columns(3)

with col1:
    export_csv = st.checkbox(
        "CSV Files", value=True, help="Individual CSV files for each analysis type"
    )
with col2:
    export_excel = st.checkbox(
        "Excel Workbook", value=True, help="Multi-sheet Excel file with all data"
    )
with col3:
    export_json = st.checkbox("JSON Data", value=False, help="Raw data in JSON format")

# Export button
if st.button("🚀 Generate Export Package", type="primary"):
    with st.spinner("📦 Preparing export package..."):

        # Create temporary directory for exports
        temp_dir = tempfile.mkdtemp()

        try:
            exporter = CharacterAnalysisExporter(output_dir=temp_dir)

            # Get all data from session state
            character_arcs = st.session_state.emotion_data.get("character_arcs", {})
            classifications = st.session_state.get("classifications", {})
            predictions = st.session_state.get("predictions", {})
            relationships = st.session_state.get("relationships", [])
            consistency = st.session_state.get("consistency", {})
            insights = st.session_state.get("insights_data", {})

            # Track exported files
            exported_files = []

            # CSV Exports
            if export_csv:
                st.text("Exporting CSV files...")

                # Arc progressions
                csv_path = exporter.export_arc_progression_csv(
                    character_arcs, classifications, "arc_progressions.csv"
                )
                exported_files.append(("arc_progressions.csv", csv_path))

                # Relationships
                if relationships:
                    csv_path = exporter.export_relationship_matrix_csv(
                        relationships, "relationship_matrix.csv"
                    )
                    exported_files.append(("relationship_matrix.csv", csv_path))

                # Consistency
                if consistency:
                    csv_path = exporter.export_consistency_reports_csv(
                        consistency, "consistency_reports.csv"
                    )
                    exported_files.append(("consistency_reports.csv", csv_path))

                # Insights summary
                if insights:
                    csv_path = exporter.export_insights_summary_csv(
                        insights, "storytelling_insights.csv"
                    )
                    exported_files.append(("storytelling_insights.csv", csv_path))

            # Excel Export
            if export_excel:
                st.text("Generating Excel workbook...")
                excel_path = exporter.export_all_to_excel(
                    character_arcs,
                    classifications,
                    predictions=predictions,
                    relationships=relationships,
                    consistency=consistency,
                    insights=insights,
                    filename="character_analysis_full.xlsx",
                )
                exported_files.append(("character_analysis_full.xlsx", excel_path))

            # JSON Export
            if export_json:
                st.text("Preparing JSON data...")
                import json

                json_data = {
                    "character_arcs": {
                        char: {
                            "scenes": arc.get("scenes", []),
                            "emotions_by_scene": {
                                str(k): v
                                for k, v in arc.get("emotions_by_scene", {}).items()
                            },
                        }
                        for char, arc in character_arcs.items()
                    },
                    "classifications": classifications,
                    "predictions": predictions,
                    "relationships": [
                        {k: v for k, v in rel.items() if k not in ["network_data"]}
                        for rel in relationships
                    ],
                    "consistency": consistency,
                    "insights": {
                        "overall_health": insights.get("overall_health", {}),
                        "recommendations": insights.get("recommendations", []),
                        "pacing_analysis": insights.get("pacing_analysis", {}),
                        "benchmarks": insights.get("benchmarks", {}),
                    },
                }

                json_path = os.path.join(temp_dir, "character_analysis.json")
                with open(json_path, "w") as f:
                    json.dump(json_data, f, indent=2, default=str)
                exported_files.append(("character_analysis.json", json_path))

            # Create ZIP package
            st.text("Creating download package...")
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
                for filename, filepath in exported_files:
                    zipf.write(filepath, filename)

            zip_buffer.seek(0)

            # Offer download
            st.success(f"✅ Export package ready! ({len(exported_files)} files)")

            st.download_button(
                label="📥 Download Export Package (ZIP)",
                data=zip_buffer,
                file_name=f"character_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                mime="application/zip",
                type="primary",
            )

            # Show file list
            with st.expander("📋 Included Files"):
                for filename, _ in exported_files:
                    st.write(f"• {filename}")

        except Exception as e:
            st.error(f"❌ Export failed: {str(e)}")

        finally:
            # Cleanup temp directory
            import shutil

            try:
                shutil.rmtree(temp_dir)
            except:
                pass

# Individual downloads
st.subheader("📄 Individual Downloads")

col1, col2 = st.columns(2)

with col1:
    if st.button("Download Arc Progressions (CSV)"):
        temp_dir = tempfile.mkdtemp()
        try:
            exporter = CharacterAnalysisExporter(output_dir=temp_dir)
            csv_path = exporter.export_arc_progression_csv(
                st.session_state.emotion_data.get("character_arcs", {}),
                st.session_state.get("classifications", {}),
                "arc_progressions.csv",
            )
            with open(csv_path, "r") as f:
                st.download_button(
                    label="💾 Save Arc Progressions CSV",
                    data=f.read(),
                    file_name="arc_progressions.csv",
                    mime="text/csv",
                )
        finally:
            import shutil

            try:
                shutil.rmtree(temp_dir)
            except:
                pass

with col2:
    if st.button("Download Full Analysis (Excel)"):
        temp_dir = tempfile.mkdtemp()
        try:
            exporter = CharacterAnalysisExporter(output_dir=temp_dir)
            excel_path = exporter.export_all_to_excel(
                st.session_state.emotion_data.get("character_arcs", {}),
                st.session_state.get("classifications", {}),
                predictions=st.session_state.get("predictions", {}),
                relationships=st.session_state.get("relationships", []),
                consistency=st.session_state.get("consistency", {}),
                insights=st.session_state.get("insights_data", {}),
                filename="character_analysis_full.xlsx",
            )
            with open(excel_path, "rb") as f:
                st.download_button(
                    label="💾 Save Excel Workbook",
                    data=f.read(),
                    file_name=f"character_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
        finally:
            import shutil

            try:
                shutil.rmtree(temp_dir)
            except:
                pass

st.info(
    "💡 **Tip:** Use the ZIP package for complete analysis exports, or individual downloads for specific data sets."
)

st.success("✅ Storytelling Insights Dashboard Complete - Phase 13.2 Week 2 Days 2-3")
