import streamlit as st
import random

st.title("💰 Budget Gamification")

if "data" not in st.session_state or "insights_data" not in st.session_state:
    st.warning("Please analyze a script and generate budget insights first.")
    st.stop()

# Budget Health Meter
def get_budget_health(score):
    if score >= 90:
        return "🏆 Excellent", "green"
    elif score >= 75:
        return "👍 Good", "blue"
    elif score >= 60:
        return "⚠️ Caution", "orange"
    else:
        return "🚨 At Risk", "red"

overall_health = st.session_state.insights_data.get("overall_health", {})
score = overall_health.get("score", 0)
rating, color = get_budget_health(score)

st.subheader("Budget Health Meter")
st.markdown(f"<h2 style='color:{color}'>{rating} ({score}%)</h2>", unsafe_allow_html=True)
st.progress(score / 100)

# What If? Scenario Generator
st.subheader("🎲 What If? Scenario Generator")
scenarios = [
    "What if you add 2 more shooting days?",
    "What if you move 3 scenes to a night shoot?",
    "What if you upgrade camera equipment?",
    "What if you reduce cast by 1 supporting role?",
    "What if you shoot 20% of scenes on location instead of studio?",
    "What if you add a stunt sequence to Scene 5?",
    "What if you cut 10 pages from the script?",
    "What if you increase the VFX budget by 25%?",
    "What if you have to reshoot 2 scenes due to weather?",
    "What if you hire a celebrity cameo?"
]
if st.button("Generate What If?"):
    st.info(random.choice(scenarios))

# Budget Achievement Badges
st.subheader("🏅 Budget Achievement Badges")
badges = []
if score >= 90:
    badges.append("🟢 Budget Master: Kept costs under control!")
if "arc_optimization" in st.session_state.insights_data and st.session_state.insights_data["arc_optimization"]:
    badges.append("🔄 Optimization Guru: Implemented arc optimizations.")
if st.session_state.insights_data.get("analyzed_arcs", 0) > 3:
    badges.append("🎭 Ensemble Expert: Managed a large cast efficiently.")
if st.session_state.insights_data.get("benchmarks", {}).get("overall_alignment", {}).get("score", 0) >= 95:
    badges.append("🏅 Industry Standard: Matched or exceeded industry benchmarks.")

if badges:
    for badge in badges:
        st.success(badge)
else:
    st.info("Complete more analyses to unlock achievement badges!")

st.caption("Gamify your budgeting process and see how your decisions impact the bottom line!")