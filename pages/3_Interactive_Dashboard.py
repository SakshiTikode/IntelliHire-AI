
import streamlit as st
import pandas as pd

from common import apply_global_style, render_sidebar


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="IntelliHire AI | Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_style()
render_sidebar()


# =========================================================
# HERO SECTION
# =========================================================

st.html(
    """
    <section class="ih-hero">
        <div class="ih-eyebrow">
            CAREER INTELLIGENCE ANALYTICS
        </div>

        <h1>
            Interactive <span class="ih-highlight">Dashboard</span>
        </h1>

        <div class="ih-hero-description">
            Explore your resume's skill coverage, keyword similarity,
            and semantic alignment with your target job.
            Use these insights to identify strengths and areas to improve.
        </div>

        <div class="ih-pill-row">
            <span class="ih-pill">📊 Performance Metrics</span>
            <span class="ih-pill">🧩 Skill Coverage</span>
            <span class="ih-pill">🧠 AI Insights</span>
        </div>
    </section>
    """
)



# =========================================================
# CHECK ANALYSIS RESULTS
# =========================================================

required_keys = [
    "skill_match_percentage",
    "similarity_score",
    "semantic_score",
]

if not all(key in st.session_state for key in required_keys):
    st.info(
        "Your dashboard is waiting for analysis results. "
        "Complete Resume Analysis to view your personalized metrics."
    )

    if st.button(
        "📄 Go to Resume Analysis",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/1_Resume_Analysis.py")

    st.stop()


# =========================================================
# LOAD RESULTS
# =========================================================

skill_score = float(st.session_state.skill_match_percentage)
tfidf_score = float(st.session_state.similarity_score)
semantic_score = float(st.session_state.semantic_score)

matched = st.session_state.get("matched_skills", [])
missing = st.session_state.get("missing_skills", [])

resume_skills = st.session_state.get("resume_skills", [])
required_skills = st.session_state.get("required_skills", [])


# =========================================================
# KPI SECTION
# =========================================================

st.markdown(
    """
    <div class="ih-section">
        <div class="ih-section-label">PERFORMANCE OVERVIEW</div>
        <div class="ih-section-title">Your Resume at a Glance</div>
        <div class="ih-section-description">
            A summary of your resume's detected skills and similarity scores.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

metric1, metric2, metric3, metric4 = st.columns(4, gap="medium")

with metric1:
    st.metric(
        label="🎯 Skill Match",
        value=f"{skill_score:.1f}%",
        help="Percentage of detected job skills matched to your resume.",
    )

with metric2:
    st.metric(
        label="🧠 TF-IDF Similarity",
        value=f"{tfidf_score:.1f}%",
        help="Textual similarity based on TF-IDF features.",
    )

with metric3:
    st.metric(
        label="🤖 Semantic Similarity",
        value=f"{semantic_score:.1f}%",
        help="Similarity based on sentence embeddings.",
    )

with metric4:
    st.metric(
        label="✅ Matched Skills",
        value=len(matched),
        delta=f"{len(missing)} missing",
        delta_color="inverse",
        help="Number of detected matching and missing skills.",
    )


# =========================================================
# SCORE COMPARISON
# =========================================================

st.markdown(
    """
    <div class="ih-section">
        <div class="ih-section-title">📊 Similarity Analysis</div>
        <div class="ih-section-description">
            Compare the three scores calculated during resume analysis.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

score_col, insight_col = st.columns([1.7, 1], gap="large")

scores_df = pd.DataFrame(
    {
        "Method": [
            "Skill Match",
            "TF-IDF Similarity",
            "Semantic Similarity",
        ],
        "Score (%)": [
            skill_score,
            tfidf_score,
            semantic_score,
        ],
    }
).set_index("Method")

with score_col:
    with st.container(border=True):
        st.markdown("#### Score Comparison")
        st.bar_chart(
            scores_df,
            y="Score (%)",
            horizontal=True,
            x_label="Score (%)",
            y_label="Analysis Method",
        )

with insight_col:
    with st.container(border=True):
        st.markdown("#### 📌 Score Summary")

        score_summary = [
            ("Skill Match", skill_score),
            ("TF-IDF Similarity", tfidf_score),
            ("Semantic Similarity", semantic_score),
        ]

        for label, score in score_summary:
            st.write(f"**{label}** — {score:.2f}%")
            st.progress(max(0, min(100, int(round(score)))))

        st.caption(
            "Each score measures a different aspect of the comparison. "
            "A higher similarity score does not guarantee job eligibility."
        )


# =========================================================
# SKILL COVERAGE
# =========================================================

st.markdown(
    """
    <div class="ih-section">
        <div class="ih-section-title">🧩 Skills Coverage</div>
        <div class="ih-section-description">
            Review the skills detected in your resume and how they
            compare with the target job requirements.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

matched_count = len(matched)
missing_count = len(missing)
total_detected = matched_count + missing_count

coverage_col, summary_col = st.columns([1.2, 1], gap="large")

with coverage_col:
    with st.container(border=True):
        st.markdown("#### Skill Match Breakdown")

        skill_counts = pd.DataFrame(
            {
                "Skill Status": ["Matched", "Missing"],
                "Count": [matched_count, missing_count],
            }
        ).set_index("Skill Status")

        st.bar_chart(
            skill_counts,
            y="Count",
            horizontal=True,
            x_label="Number of Skills",
            y_label="Skill Status",
        )

with summary_col:
    with st.container(border=True):
        st.markdown("#### 📋 Skill Summary")

        summary_metrics = st.columns(2)

        with summary_metrics[0]:
            st.metric("Matched", matched_count)

        with summary_metrics[1]:
            st.metric("Missing", missing_count)

        if total_detected:
            matched_coverage = matched_count / total_detected * 100
        else:
            matched_coverage = 0

        st.write("**Matched vs. unmatched detected skills**")
        st.progress(int(round(matched_coverage)))

        st.caption(
            "This breakdown uses the matched and missing skill lists "
            "returned by your analysis module."
        )

        if missing:
            st.warning(
                f"{missing_count} detected job skill(s) need review."
            )
        else:
            st.success("No missing skills were recorded.")


# =========================================================
# SKILL DETAILS
# =========================================================

st.markdown(
    """
    <div class="ih-section">
        <div class="ih-section-title">🔎 Detailed Skill Breakdown</div>
        <div class="ih-section-description">
            Expand each section to inspect individual skills.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

matched_col, missing_col = st.columns(2, gap="large")

with matched_col:
    with st.container(border=True):
        st.markdown("#### ✅ Matched Skills")
        st.caption(f"{matched_count} skill(s) found in both lists")

        if matched:
            for skill in matched:
                st.markdown(f"- ✓ {skill}")
        else:
            st.info("No matched skills were recorded.")

with missing_col:
    with st.container(border=True):
        st.markdown("#### 📌 Skills to Review")
        st.caption(f"{missing_count} skill(s) not detected in your resume")

        if missing:
            for skill in missing:
                st.markdown(f"- {skill}")
        else:
            st.success("No missing skills were recorded.")


# =========================================================
# ADDITIONAL ANALYSIS DETAILS
# =========================================================

with st.expander("📄 View Analysis Details"):
    detail_col1, detail_col2 = st.columns(2)

    with detail_col1:
        st.markdown("**Resume Skills Detected**")
        st.write(resume_skills if resume_skills else "No data available.")

    with detail_col2:
        st.markdown("**Required Job Skills Detected**")
        st.write(
            required_skills if required_skills else "No data available."
        )


# =========================================================
# DOWNLOAD DASHBOARD DATA
# =========================================================

st.markdown(
    """
    <div class="ih-section">
        <div class="ih-section-title">⬇️ Export Your Results</div>
        <div class="ih-section-description">
            Download your dashboard metrics and skill comparison
            for future reference.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

download_df = pd.DataFrame(
    [
        {"Category": "Score", "Metric": "Skill Match (%)", "Value": skill_score},
        {"Category": "Score", "Metric": "TF-IDF Similarity (%)", "Value": tfidf_score},
        {"Category": "Score", "Metric": "Semantic Similarity (%)", "Value": semantic_score},
        {"Category": "Skills", "Metric": "Resume Skills Found", "Value": len(resume_skills)},
        {"Category": "Skills", "Metric": "Required Skills Found", "Value": len(required_skills)},
        {"Category": "Skills", "Metric": "Matched Skills Count", "Value": matched_count},
        {"Category": "Skills", "Metric": "Missing Skills Count", "Value": missing_count},
    ]
)

skills_df = pd.DataFrame(
    [
        {"Category": "Matched", "Skill": str(skill)}
        for skill in matched
    ] + [
        {"Category": "Missing", "Skill": str(skill)}
        for skill in missing
    ]
)

download_col1, download_col2 = st.columns(2, gap="medium")

with download_col1:
    st.download_button(
        label="📊 Download Scores (CSV)",
        data=download_df.to_csv(index=False),
        file_name="intellihire_dashboard_scores.csv",
        mime="text/csv",
        use_container_width=True,
    )

with download_col2:
    st.download_button(
        label="🧩 Download Skill Details (CSV)",
        data=skills_df.to_csv(index=False),
        file_name="intellihire_skill_details.csv",
        mime="text/csv",
        use_container_width=True,
    )


# =========================================================
# NAVIGATION
# =========================================================

st.divider()

if st.button(
    "← Back to Resume Analysis",
    use_container_width=True,
):
    st.switch_page("pages/1_Resume_Analysis.py")


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="ih-footer">
        <div class="ih-footer-brand">✦ IntelliHire AI</div>
        <div class="ih-footer-copy">
            Career Analytics · Skill Matching · Resume Intelligence
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
