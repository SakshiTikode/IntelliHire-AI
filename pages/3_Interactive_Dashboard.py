import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Interactive Dashboard",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Interactive Resume Dashboard")
st.write(
    "Explore your resume's skill match, machine-learning score, "
    "and semantic similarity with your target job."
)

# Check whether resume analysis has been completed
required_keys = [
    "skill_match_percentage",
    "similarity_score",
    "semantic_score",
]

if not all(key in st.session_state for key in required_keys):
    st.info(
        "Please open Resume Analysis, upload your resume, enter a job "
        "description, and complete the analysis first."
    )
    if st.button("📄 Go to Resume Analysis"):
        st.switch_page("pages/1_Resume_Analysis.py")
    st.stop()

# Read actual analysis results
skill_score = float(st.session_state.skill_match_percentage)
tfidf_score = float(st.session_state.similarity_score)
semantic_score = float(st.session_state.semantic_score)

matched = st.session_state.get("matched_skills", [])
missing = st.session_state.get("missing_skills", [])

# Summary metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🎯 Skill Match", f"{skill_score:.2f}%")

with col2:
    st.metric("🤖 TF-IDF / ML", f"{tfidf_score:.2f}%")

with col3:
    st.metric("🧠 Semantic / DL", f"{semantic_score:.2f}%")

st.divider()

# Score comparison chart
st.subheader("📊 Score Comparison")

scores_df = pd.DataFrame(
    {
        "Method": [
            "Skill Match",
            "TF-IDF / ML",
            "Semantic / DL",
        ],
        "Score (%)": [
            skill_score,
            tfidf_score,
            semantic_score,
        ],
    }
).set_index("Method")

st.bar_chart(scores_df, y="Score (%)")

st.caption(
    "Scores are taken from your completed resume analysis. "
    "Different methods measure different aspects of job suitability."
)

st.divider()

# Skill match details
left, right = st.columns(2)

with left:
    st.subheader("✅ Matched Skills")
    if matched:
        st.write(f"**Total: {len(matched)}**")
        for skill in matched:
            st.write(f"✓ {skill}")
    else:
        st.info("No matched skills were recorded.")

with right:
    st.subheader("❌ Missing Skills")
    if missing:
        st.write(f"**Total: {len(missing)}")
        for skill in missing:
            st.write(f"• {skill}")
    else:
        st.success("No missing skills were recorded.")

st.divider()

# Skill counts chart
st.subheader("📈 Skill Coverage")

skill_counts = pd.DataFrame(
    {
        "Category": ["Matched Skills", "Missing Skills"],
        "Count": [len(matched), len(missing)],
    }
).set_index("Category")

st.bar_chart(skill_counts, y="Count")

# Download results as CSV
download_df = pd.DataFrame(
    {
        "Metric": [
            "Skill Match (%)",
            "TF-IDF / ML (%)",
            "Semantic / DL (%)",
            "Matched Skills Count",
            "Missing Skills Count",
        ],
        "Value": [
            skill_score,
            tfidf_score,
            semantic_score,
            len(matched),
            len(missing),
        ],
    }
)

st.download_button(
    label="⬇️ Download Dashboard Scores (CSV)",
    data=download_df.to_csv(index=False),
    file_name="intellihire_dashboard.csv",
    mime="text/csv",
)

if st.button("📄 Back to Resume Analysis"):
    st.switch_page("pages/1_Resume_Analysis.py")