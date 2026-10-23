
import streamlit as st

from common import apply_global_style, render_sidebar


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="IntelliHire AI | GenAI Resume Review",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_style()
render_sidebar()


# =========================================================
# SESSION STATE
# =========================================================

if "ai_review" not in st.session_state:
    st.session_state.ai_review = ""

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "job_description" not in st.session_state:
    st.session_state.job_description = ""


# =========================================================
# HERO SECTION
# =========================================================

st.html(
    """
    <section class="ih-hero">
        <div class="ih-eyebrow">
            ✦ &nbsp; GENERATIVE AI CAREER ASSISTANT
        </div>

        <h1>
            GenAI Resume <span class="ih-highlight">Review</span>
        </h1>

        <div class="ih-hero-description">
            Get personalized feedback on your resume, discover
            opportunities for improvement, and receive practical
            recommendations tailored to your target job.
        </div>

        <div class="ih-pill-row">
            <span class="ih-pill">🤖 AI Feedback</span>
            <span class="ih-pill">💡 Improvement Tips</span>
            <span class="ih-pill">🎯 Career Guidance</span>
        </div>
    </section>
    """
)

# =========================================================
# REVIEW CONTENT
# =========================================================

st.markdown(
    """
    <div class="ih-section">
        <div class="ih-section-label">PERSONALIZED INSIGHTS</div>
        <div class="ih-section-title">Your Resume Review</div>
        <div class="ih-section-description">
            Review the AI-generated feedback based on your resume
            and target job description.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


if st.session_state.ai_review:

    with st.container(border=True):
        st.markdown("### ✨ AI-Generated Feedback")
        st.markdown(st.session_state.ai_review)

    st.success("Your AI resume review is ready.")

    with st.expander("📄 View Resume and Job Details"):

        if st.session_state.resume_text:
            st.markdown("**Resume text**")
            st.text(st.session_state.resume_text)
        else:
            st.info("No resume text is available.")

        if st.session_state.job_description:
            st.markdown("**Target job description**")
            st.text(st.session_state.job_description)
        else:
            st.info("No job description is available.")

else:

    st.info(
        "No AI review is available yet. "
        "Open Resume Analysis, upload your resume, enter a job "
        "description, and click Analyze My Resume to generate "
        "your personalized feedback."
    )

    if st.button(
        "📄 Go to Resume Analysis",
        type="primary",
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
            Generative AI · Resume Feedback · Personalized Recommendations
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
