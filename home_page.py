import streamlit as st

from common import apply_global_style, render_sidebar


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="IntelliHire AI | Home",
    page_icon="📄",
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


# =========================================================
# HERO SECTION
# =========================================================

st.html(
    """
    <section class="ih-hero">
        <div class="ih-eyebrow">
            ✦ &nbsp; AI-POWERED CAREER INTELLIGENCE
        </div>

        <h1>
            Make your next career move<br>
            with <span class="ih-highlight">IntelliHire AI.</span>
        </h1>

        <div class="ih-hero-description">
            Turn your resume into a smarter career strategy.
            Analyze your skills, understand job compatibility,
            uncover skill gaps, and get AI-powered recommendations
            to prepare for your next opportunity.
        </div>

        <div class="ih-pill-row">
            <span class="ih-pill">◈ Machine Learning</span>
            <span class="ih-pill">◈ Semantic AI</span>
            <span class="ih-pill">◈ Generative AI</span>
        </div>
    </section>
    """
)


# =========================================================
# FEATURE EXPLORER
# =========================================================

st.html(
    """
    <div class="ih-section">
        <div class="ih-section-label">EXPLORE THE PLATFORM</div>
        <div class="ih-section-title">From Resume to Opportunity</div>
        <div class="ih-section-description">
            Start with your resume, discover where you stand,
            and get actionable insights to move forward.
        </div>
    </div>
    """
)

feature1, feature2 = st.columns(2, gap="large")


with feature1:
    st.html(
        """
        <div class="ih-feature-card primary">
            <div class="ih-feature-title">
                📄 Resume Analysis
            </div>

            <div class="ih-feature-tag">ANALYZE &amp; MATCH</div>

            <div class="ih-feature-description">
                Evaluate your resume against a target job description.
                Explore keyword and semantic similarity, identify
                missing skills, and understand areas that need attention.
            </div>

            <div class="ih-feature-points">
                <span class="ih-feature-point">Resume Parsing</span>
                <span class="ih-feature-point">Skill Gap Analysis</span>
                <span class="ih-feature-point">Job Matching</span>
            </div>
        </div>
        """
    )

    if st.button(
        "Open Resume Analysis →",
        key="home_resume_analysis",
        use_container_width=True,
        type="primary",
    ):
        st.switch_page("pages/1_Resume_Analysis.py")


with feature2:
    st.html(
        """
        <div class="ih-feature-card secondary">
            <div class="ih-feature-title">
                ✨ GenAI Resume Review
            </div>

            <div class="ih-feature-tag">REVIEW &amp; IMPROVE</div>

            <div class="ih-feature-description">
                Get personalized resume feedback and practical
                improvement suggestions. Explore recommendations
                and a learning roadmap aligned with your target role.
            </div>

            <div class="ih-feature-points">
                <span class="ih-feature-point">AI Feedback</span>
                <span class="ih-feature-point">Resume Improvements</span>
                <span class="ih-feature-point">Learning Roadmap</span>
            </div>
        </div>
        """
    )

    if st.button(
        "Open GenAI Review →",
        key="home_genai_review",
        use_container_width=True,
        type="secondary",
    ):
        st.switch_page("pages/2_GenAI_Review.py")


# =========================================================
# WORKFLOW
# =========================================================

st.html(
    """
    <div class="ih-section">
        <div class="ih-section-label">SIMPLE FOUR-STEP WORKFLOW</div>
        <div class="ih-section-title">How IntelliHire AI Works</div>
        <div class="ih-section-description">
            A guided process that turns your resume into useful,
            job-focused insights.
        </div>
    </div>
    """
)

steps = [
    ("01", "Upload", "Provide your resume in PDF or DOCX format."),
    ("02", "Match", "Compare your resume with target job requirements."),
    ("03", "Analyze", "Explore keyword and semantic similarity insights."),
    ("04", "Improve", "Use AI feedback to plan your next career steps."),
]

workflow_columns = st.columns(4, gap="medium")

for column, (number, title, description) in zip(
    workflow_columns,
    steps,
):
    with column:
        st.html(
            f"""
            <div class="ih-step-card">
                <div class="ih-step-number">{number}</div>
                <div class="ih-step-title">{title}</div>
                <div class="ih-step-description">{description}</div>
            </div>
            """
        )


# =========================================================
# TECHNOLOGY EXPLAINERS
# =========================================================

st.html(
    """
    <div class="ih-section">
        <div class="ih-section-label">BEHIND THE TECHNOLOGY</div>
        <div class="ih-section-title">Understand the Intelligence</div>
        <div class="ih-section-description">
            Learn how each technology contributes to the analysis.
        </div>
    </div>
    """
)

with st.expander("📊 Machine Learning — TF-IDF Similarity"):
    st.write(
        "TF-IDF and cosine similarity estimate how closely the "
        "words and terms in your resume match the job description. "
        "This helps identify keyword-level overlap between the two."
    )

with st.expander("🧠 Deep Learning — Semantic Similarity"):
    st.write(
        "A pretrained Sentence Transformer converts text into "
        "embeddings to estimate similarity in meaning, even when "
        "the exact words differ."
    )

with st.expander("✨ Generative AI — Gemini"):
    st.write(
        "Gemini generates contextual resume feedback, improvement "
        "suggestions, and a learning roadmap using the resume and "
        "target job description as context."
    )


# =========================================================
# FOOTER
# =========================================================

st.html(
    """
    <div class="ih-footer">
        <div class="ih-footer-brand">✦ IntelliHire AI</div>
        <div class="ih-footer-copy">
            Resume Intelligence · Job Matching · Semantic Analysis ·
            Generative AI
        </div>
    </div>
    """
)
