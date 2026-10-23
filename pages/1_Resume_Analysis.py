
import sys
import tempfile
from pathlib import Path
from html import escape

import streamlit as st

# =========================================================
# PATH CONFIGURATION
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# =========================================================
# PROJECT MODULES
# =========================================================

from common import apply_global_style, render_sidebar

from resume_parser import extract_resume_text
from resume_analyzer import (
    extract_skills,
    categorize_skills,
    compare_skills_with_alternatives,
)
from similarity_matcher import calculate_similarity
from resume_suggestions import generate_suggestions
from semantic_matcher import calculate_semantic_similarity
from genai_assistant import generate_resume_review


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="IntelliHire AI | Resume Analysis",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_style()
render_sidebar()


# =========================================================
# SESSION STATE
# =========================================================

DEFAULT_STATE = {
    "ai_review": "",
    "resume_text": "",
    "job_description": "",
    "resume_skills": [],
    "required_skills": [],
    "matched_skills": [],
    "missing_skills": [],
    "skill_match_percentage": 0.0,
    "similarity_score": 0.0,
    "semantic_score": 0.0,
}

for key, default_value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = default_value


# =========================================================
# HERO HEADER
# =========================================================


st.html(
    """
    <section class="ih-hero">
        <div class="ih-eyebrow">
            ✦ &nbsp; AI-POWERED CAREER INTELLIGENCE
        </div>

        <h1>
            Resume <span class="ih-highlight">Analysis</span>
        </h1>

        <div class="ih-hero-description">
            Compare your resume with a target job description.
            Discover matching skills, identify skill gaps, and
            understand how closely your experience aligns with
            the opportunity.
        </div>

        <div class="ih-pill-row">
            <span class="ih-pill">📄 Resume Parsing</span>
            <span class="ih-pill">🧠 Text Similarity</span>
            <span class="ih-pill">✨ AI Recommendations</span>
        </div>
    </section>
    """
)



# =========================================================
# RESUME INPUT
# =========================================================

st.markdown(
    """
    <div class="ih-section">
        <div class="ih-section-label">STEP 1</div>
        <div class="ih-section-title">Upload Your Resume</div>
        <div class="ih-section-description">
            Upload a PDF or DOCX file to extract your skills and experience.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx"],
    help="Supported formats: PDF and DOCX.",
    key="resume_upload",
)


# =========================================================
# JOB DESCRIPTION INPUT
# =========================================================

st.markdown(
    """
    <div class="ih-section">
        <div class="ih-section-label">STEP 2</div>
        <div class="ih-section-title">Target Job Description</div>
        <div class="ih-section-description">
            Paste the job description to compare its requirements
            against the skills found in your resume.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

job_description = st.text_area(
    "Job description",
    value=st.session_state.job_description,
    height=220,
    placeholder=(
        "Paste the job title, required skills, responsibilities "
        "and qualifications here..."
    ),
    label_visibility="collapsed",
    key="job_description_input",
)


# =========================================================
# ANALYSIS ACTION
# =========================================================

analyze_button = st.button(
    "✨ Analyze My Resume",
    type="primary",
    use_container_width=True,
    key="analyze_resume_button",
)


# =========================================================
# RESUME ANALYSIS PROCESS
# =========================================================

if analyze_button:

    if uploaded_file is None:
        st.warning("Please upload a PDF or DOCX resume.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        temp_path = None

        try:
            with st.spinner("Analyzing your resume..."):

                # -------------------------------------------------
                # Extract resume text
                # -------------------------------------------------

                suffix = Path(uploaded_file.name).suffix.lower()

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix,
                ) as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                    temp_path = Path(temp_file.name)

                try:
                    resume_text = extract_resume_text(temp_path)
                finally:
                    temp_path.unlink(missing_ok=True)
                    temp_path = None

                if not resume_text or not resume_text.strip():
                    st.error(
                        "No readable text was found in your resume. "
                        "If this is a scanned PDF, OCR may be required."
                    )
                    st.stop()

                # -------------------------------------------------
                # Extract and categorize skills
                # -------------------------------------------------

                resume_skills = extract_skills(resume_text)
                required_skills = extract_skills(job_description)
                categorized_skills = categorize_skills(resume_text)

                # -------------------------------------------------
                # Compare skills
                # -------------------------------------------------

                matched, missing, percentage = (
                    compare_skills_with_alternatives(
                        resume_skills,
                        required_skills,
                    )
                )

                # -------------------------------------------------
                # Calculate similarity scores
                # -------------------------------------------------

                similarity_score = calculate_similarity(
                    resume_text,
                    job_description,
                )

                semantic_score = calculate_semantic_similarity(
                    resume_text,
                    job_description,
                )

                # -------------------------------------------------
                # Generate AI review
                # -------------------------------------------------

                ai_review = generate_resume_review(
                    resume_text,
                    job_description,
                )

                # -------------------------------------------------
                # Save results for other pages
                # -------------------------------------------------

                st.session_state.resume_text = resume_text
                st.session_state.job_description = job_description

                st.session_state.resume_skills = resume_skills
                st.session_state.required_skills = required_skills
                st.session_state.matched_skills = matched
                st.session_state.missing_skills = missing
                st.session_state.skill_match_percentage = percentage

                st.session_state.similarity_score = similarity_score
                st.session_state.semantic_score = semantic_score
                st.session_state.ai_review = ai_review

                st.session_state.categorized_skills = categorized_skills

            st.success("Resume analysis completed successfully!")

        except Exception:
            st.error("An error occurred during resume analysis.")
            st.exception(Exception)

        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)


# =========================================================
# DISPLAY SAVED RESULTS
# =========================================================

if st.session_state.resume_text:

    resume_text = st.session_state.resume_text
    required_skills = st.session_state.required_skills
    resume_skills = st.session_state.resume_skills
    matched = st.session_state.matched_skills
    missing = st.session_state.missing_skills
    percentage = st.session_state.skill_match_percentage
    similarity_score = st.session_state.similarity_score
    semantic_score = st.session_state.semantic_score
    categorized_skills = st.session_state.get(
        "categorized_skills", {}
    )

    st.divider()

    st.markdown(
        """
        <div class="ih-section">
            <div class="ih-section-label">YOUR RESULTS</div>
            <div class="ih-section-title">Analysis Dashboard</div>
            <div class="ih-section-description">
                Review your skill coverage, textual similarity,
                semantic similarity, and recommended next steps.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =====================================================
    # METRIC CARDS
    # =====================================================

    col1, col2, col3 = st.columns(3, gap="medium")

    metrics = [
        (col1, "📄 Resume Skills Found", len(resume_skills)),
        (col2, "✅ Matched Skills", len(matched)),
        (col3, "📌 Missing Skills", len(missing)),
    ]

    for column, label, value in metrics:
        with column:
            st.metric(label=label, value=value)

    # =====================================================
    # SKILL MATCH SCORE
    # =====================================================

    st.markdown(
        """
        <div class="ih-section">
            <div class="ih-section-title">🎯 Skill Match Score</div>
            <div class="ih-section-description">
                The percentage of detected job skills matched
                against your resume.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    score_col1, score_col2 = st.columns([1, 3])

    with score_col1:
        st.metric("Skill Match", f"{percentage:.2f}%")

    with score_col2:
        st.write("**Required skills coverage**")
        st.progress(
            max(0, min(100, int(round(percentage))))
        )
        st.caption(
            "This score reflects detected skill overlap. "
            "It does not guarantee job eligibility."
        )

    # =====================================================
    # TEXT SIMILARITY
    # =====================================================

    st.markdown(
        """
        <div class="ih-section">
            <div class="ih-section-title">
                🧠 Text Similarity (TF-IDF)
            </div>
            <div class="ih-section-description">
                Estimates textual overlap between your resume
                and the target job description.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    similarity_col1, similarity_col2 = st.columns([1, 3])

    with similarity_col1:
        st.metric(
            "TF-IDF Similarity",
            f"{similarity_score:.2f}%",
        )

    with similarity_col2:
        st.write("**Resume and job description similarity**")
        st.progress(
            max(0, min(100, int(round(similarity_score))))
        )
        st.caption(
            "TF-IDF measures textual overlap. It is not a hiring "
            "probability or a guarantee of job eligibility."
        )

    # =====================================================
    # SEMANTIC SIMILARITY
    # =====================================================

    st.markdown(
        """
        <div class="ih-section">
            <div class="ih-section-title">
                🤖 Semantic Similarity
            </div>
            <div class="ih-section-description">
                Uses a Sentence Transformer model to estimate
                similarity in meaning between the two texts.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    semantic_col1, semantic_col2 = st.columns([1, 3])

    with semantic_col1:
        st.metric(
            "Semantic Similarity",
            f"{semantic_score:.2f}%",
        )

    with semantic_col2:
        st.write("**Meaning-based similarity**")
        st.progress(
            max(0, min(100, int(round(semantic_score))))
        )
        st.caption(
            "Semantic similarity estimates how closely the texts "
            "align in meaning. It is not a hiring probability."
        )

    # =====================================================
    # SKILLS COMPARISON
    # =====================================================

    st.markdown(
        """
        <div class="ih-section">
            <div class="ih-section-title">🧩 Skills Comparison</div>
            <div class="ih-section-description">
                Skills found in both texts and skills to review.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    matched_col, missing_col = st.columns(2, gap="large")

    with matched_col:
        matched_chips = "".join(
            (
                '<span class="skill-chip matched-chip">'
                f'✓ &nbsp; {escape(str(skill))}'
                '</span>'
            )
            for skill in matched
        )

        if not matched:
            matched_chips = (
                '<div class="empty-state">'
                'No matching skills detected yet.'
                '</div>'
            )

        st.markdown(
            f"""
            <div class="skill-panel matched-panel">
                <div class="panel-title">
                    ✅ Matched Skills
                    <span class="count-matched">({len(matched)})</span>
                </div>
                <div class="panel-subtitle">
                    Skills found in your resume and job description.
                </div>
                <div class="skills-container">
                    {matched_chips}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with missing_col:
        missing_chips = "".join(
            (
                '<span class="skill-chip missing-chip">'
                f'+ &nbsp; {escape(str(skill))}'
                '</span>'
            )
            for skill in missing
        )

        if not missing:
            missing_chips = (
                '<div class="empty-state">'
                'All detected job skills were matched.'
                '</div>'
            )

        st.markdown(
            f"""
            <div class="skill-panel missing-panel">
                <div class="panel-title">
                    📌 Skills to Review
                    <span class="count-missing">({len(missing)})</span>
                </div>
                <div class="panel-subtitle">
                    Required skills not detected in your resume.
                </div>
                <div class="skills-container">
                    {missing_chips}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # =====================================================
    # RESUME IMPROVEMENT SUGGESTIONS
    # =====================================================

    st.markdown(
        """
        <div class="ih-section">
            <div class="ih-section-title">
                💡 Resume Improvement Suggestions
            </div>
            <div class="ih-section-description">
                Practical recommendations based on your analysis.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    suggestions = generate_suggestions(
        missing_skills=missing,
        matched_skills=matched,
        similarity_score=similarity_score,
    )

    with st.container(border=True):
        st.markdown("### 🚀 Your Action Plan")

        if suggestions:
            for index, suggestion in enumerate(suggestions, start=1):
                st.markdown(f"**{index}.** {suggestion}")
        else:
            st.info("No improvement suggestions are available.")

    if missing:
        st.info(
            "Add a missing skill to your resume only if you genuinely "
            "have that skill. Otherwise, consider learning it and "
            "building a relevant project."
        )

    # =====================================================
    # CATEGORY-WISE SKILLS
    # =====================================================

    st.markdown(
        """
        <div class="ih-section">
            <div class="ih-section-title">🧩 Skills by Category</div>
            <div class="ih-section-description">
                Explore the skills detected in your resume by category.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if categorized_skills:
        category_columns = st.columns(2)

        for index, (category, skills) in enumerate(
            categorized_skills.items()
        ):
            with category_columns[index % 2]:
                with st.container(border=True):
                    st.markdown(f"**{escape(str(category))}**")
                    st.write(" · ".join(map(str, skills)))
    else:
        st.info(
            "No skills from the current skills database were "
            "found in this resume."
        )

    # =====================================================
    # AI REVIEW
    # =====================================================

    st.markdown(
        """
        <div class="ih-section">
            <div class="ih-section-title">
                ✨ AI-Powered Resume Review
            </div>
            <div class="ih-section-description">
                Personalized feedback generated using your resume
                and the target job description.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.ai_review:
        st.markdown(st.session_state.ai_review)
    else:
        st.info(
            "AI feedback is not available for this analysis."
        )

    # =====================================================
    # EXPANDABLE DETAILS
    # =====================================================

    with st.expander("🔎 View Extracted Resume Text"):
        st.text(resume_text)

    with st.expander("📋 View Detected Job Skills"):
        st.write(required_skills)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="ih-footer">
        <div class="ih-footer-brand">✦ IntelliHire AI</div>
        <div class="ih-footer-copy">
            Resume Analysis · Skill Matching · Semantic Analysis ·
            Generative AI
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)