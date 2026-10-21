import streamlit as st
import sys
from pathlib import Path

# Add project src directory to Python path
SRC_PATH = Path(__file__).resolve().parent.parent / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))
import tempfile
import sys
from pathlib import Path
from html import escape

# --------------------------------------------------
# IMPORT PROJECT MODULES
# --------------------------------------------------

SRC_PATH = Path(__file__).parent / "src"
sys.path.insert(0, str(SRC_PATH))

from resume_parser import extract_resume_text
from resume_analyzer import (
    extract_skills,
    categorize_skills,
    compare_skills,
    compare_skills_with_alternatives,
)
from similarity_matcher import calculate_similarity
from resume_suggestions import generate_suggestions
from semantic_matcher import calculate_semantic_similarity
from genai_assistant import generate_resume_review


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="IntelliHire AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "ai_review" not in st.session_state:
    st.session_state.ai_review = ""

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    .stApp {
        background: linear-gradient(
            135deg,
            #f7f8ff 0%,
            #eef2ff 100%
        );
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1350px;
    }

    .hero {
        padding: 32px;
        border-radius: 24px;
        background: linear-gradient(
            120deg,
            #171b4d,
            #4838a8,
            #7654d6
        );
        color: white;
        margin-bottom: 28px;
        box-shadow: 0 12px 35px rgba(48, 44, 130, 0.18);
    }

    .hero h1 {
        color: white;
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .hero p {
        color: #e2e7ff;
        font-size: 16px;
        margin-bottom: 0;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 30px;
        padding: 7px 14px;
        margin-bottom: 15px;
        font-size: 12px;
        font-weight: 600;
    }

    .section-heading {
        color: #202451;
        font-size: 23px;
        font-weight: 750;
        margin-top: 20px;
        margin-bottom: 6px;
    }

    .section-description {
        color: #6b7280;
        font-size: 14px;
        margin-bottom: 18px;
    }

    .metric-card {
        background: white;
        padding: 23px;
        border-radius: 18px;
        border: 1px solid #e5e7f5;
        box-shadow: 0 5px 20px rgba(35, 39, 90, 0.05);
        min-height: 135px;
        box-sizing: border-box;
    }

    .metric-label {
        color: #6b7280;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 12px;
    }

    .metric-value {
        color: #25265e;
        font-size: 34px;
        font-weight: 800;
        line-height: 1.2;
        overflow-wrap: anywhere;
    }

    .metric-note {
        color: #8b91a7;
        font-size: 12px;
        margin-top: 8px;
    }

    /* SKILLS PANELS */

    .skill-panel {
        background: #ffffff;
        border-radius: 20px;
        padding: 22px;
        min-height: 230px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 8px 25px rgba(40, 50, 100, 0.06);
        box-sizing: border-box;
        width: 100%;
        overflow-wrap: anywhere;
    }

    .matched-panel {
        border-top: 5px solid #10b981;
    }

    .missing-panel {
        border-top: 5px solid #f43f5e;
    }

    .panel-title {
        font-size: 22px;
        font-weight: 750;
        color: #202451;
        margin-bottom: 10px;
    }

    .panel-subtitle {
        font-size: 13px;
        line-height: 1.6;
        color: #778096;
        margin-bottom: 18px;
    }

    .count-matched {
        color: #059669;
        font-size: 15px;
        font-weight: 600;
    }

    .count-missing {
        color: #e11d48;
        font-size: 15px;
        font-weight: 600;
    }

    /* HORIZONTAL SKILLS LAYOUT */

    .skills-container {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        justify-content: flex-start;
        align-items: flex-start;
        gap: 10px;
        width: 100%;
    }

    .skill-chip {
        display: inline-flex !important;
        flex: 0 0 auto !important;
        align-items: center;
        width: auto !important;
        max-width: 100%;
        padding: 8px 12px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 600;
        line-height: 1.4;
        white-space: normal;
        overflow-wrap: anywhere;
        box-sizing: border-box;
    }

    .matched-chip {
        background: #e7fbf1;
        color: #087f5b;
        border: 1px solid #c4f1dc;
    }

    .missing-chip {
        background: #fff0f2;
        color: #be123c;
        border: 1px solid #ffd9df;
    }

    .empty-state {
        color: #8790a5;
        padding: 15px 0;
        font-size: 14px;
    }

    div[data-testid="stFileUploader"] {
        background: white;
        border: 1px dashed #9ca3e8;
        border-radius: 15px;
        padding: 15px;
    }

    div[data-testid="stTextArea"] textarea {
        background: white;
        border: 1px solid #dfe3f0;
        border-radius: 12px;
    }

    div.stButton > button {
        background: linear-gradient(
            100deg,
            #5145cd,
            #7957df
        );
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 700;
        min-height: 48px;
        transition: 0.2s ease;
    }

    div.stButton > button:hover {
        color: white;
        border: none;
        box-shadow: 0 5px 18px rgba(81, 69, 205, 0.25);
        transform: translateY(-1px);
    }

    section[data-testid="stSidebar"] {
        background: #171b3f;
    }

    section[data-testid="stSidebar"] * {
        color: #f4f5ff;
    }

    .footer {
        text-align: center;
        color: #8b91a7;
        font-size: 12px;
        padding-top: 28px;
        padding-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("# 📄 IntelliHire")
    st.markdown("### AI Resume Intelligence")

    st.divider()

    st.markdown("**YOUR WORKSPACE**")
    st.markdown("📄 Resume Analysis")
    st.markdown("🎯 Job Matching")
    st.markdown("🧩 Skills Overview")
    st.markdown("🧠 Text Similarity")
    st.markdown("🤖 Semantic Matching")

    st.divider()

    st.markdown("**SUPPORTED FORMATS**")
    st.markdown("📕 PDF")
    st.markdown("📘 DOCX")

    st.info(
        "Compare resume skills with job requirements "
        "and discover areas for improvement."
    )


# --------------------------------------------------
# HERO HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">
            ✨ AI-POWERED CAREER INTELLIGENCE
        </div>
        <h1>IntelliHire AI</h1>
        <p>
            Understand your skills. Discover skill gaps.
            Prepare for your next opportunity.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">📄 Resume Upload</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Upload your resume in PDF or DOCX format.'
    '</div>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx"],
    help="Supported formats: PDF and DOCX.",
)


# --------------------------------------------------
# JOB DESCRIPTION
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">🎯 Target Job Description</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Paste the job description to compare required skills.'
    '</div>',
    unsafe_allow_html=True,
)

job_description = st.text_area(
    "Job description",
    height=220,
    placeholder=(
        "Paste the job title, required skills, "
        "responsibilities and qualifications here..."
    ),
    label_visibility="collapsed",
)


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

analyze_button = st.button(
    "✨  Analyze My Resume",
    type="primary",
    use_container_width=True,
)


# --------------------------------------------------
# RESUME ANALYSIS
# --------------------------------------------------

if analyze_button:

    if uploaded_file is None:
        st.warning("Please upload a PDF or DOCX resume.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:

        try:

            with st.spinner(
                "Analyzing resume and comparing skills..."
            ):

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

                if not resume_text or not resume_text.strip():
                    st.error(
                        "No readable text was found. "
                        "A scanned PDF may require OCR."
                    )
                    st.stop()

                # Extract skills
                resume_skills = extract_skills(resume_text)
                required_skills = extract_skills(job_description)
                
                categorized_skills = categorize_skills(resume_text)

                # Save inputs for other pages
                st.session_state.resume_text = resume_text
                st.session_state.job_description = job_description

                # Compare skills
                matched, missing, percentage = compare_skills_with_alternatives(
                    resume_skills,
                    required_skills,
                )

                # Save analysis results for dashboard and report pages
                st.session_state.resume_skills = resume_skills
                st.session_state.required_skills = required_skills
                st.session_state.matched_skills = matched
                st.session_state.missing_skills = missing
                st.session_state.skill_match_percentage = percentage

                # Generate AI-powered resume review
                st.subheader("🤖 AI-Powered Resume Review")
                with st.spinner("Gemini AI is analyzing your resume..."):
                     ai_review = generate_resume_review(
                           resume_text,
                           job_description,
                     )

                st.session_state.ai_review = ai_review
                # ML: TF-IDF and Cosine Similarity
                similarity_score = calculate_similarity(
                    resume_text,
                    job_description,
                )

                # DL: Sentence Transformer Semantic Similarity
                semantic_score = calculate_semantic_similarity(
                    resume_text,
                    job_description,
                )

                # Save ML and DL scores for dashboard
                st.session_state.similarity_score = similarity_score
                st.session_state.semantic_score = semantic_score

            # --------------------------------------------------
            # RESULTS HEADER
            # --------------------------------------------------

            st.success(
                "Resume analysis completed successfully!"
            )

            st.divider()

            st.markdown(
                '<div class="section-heading">'
                '📊 Your Analysis Dashboard'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="section-description">'
                'Review your detected skills, required skills, '
                'and text similarity with the target job.'
                '</div>',
                unsafe_allow_html=True,
            )

            # --------------------------------------------------
            # TOP METRIC CARDS
            # --------------------------------------------------

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            📄 Resume Skills Found
                        </div>
                        <div class="metric-value">
                            {len(resume_skills)}
                        </div>
                        <div class="metric-note">
                            Skills detected in your resume
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            ✅ Matched Skills
                        </div>
                        <div class="metric-value">
                            {len(matched)}
                        </div>
                        <div class="metric-note">
                            Skills also found in job requirements
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col3:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            📌 Missing Skills
                        </div>
                        <div class="metric-value">
                            {len(missing)}
                        </div>
                        <div class="metric-note">
                            Required skills not detected in resume
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # --------------------------------------------------
            # SKILL MATCH SCORE
            # --------------------------------------------------

            st.markdown(
                '<div class="section-heading">'
                '🎯 Skill Match Score'
                '</div>',
                unsafe_allow_html=True,
            )

            score_col1, score_col2 = st.columns([1, 3])

            with score_col1:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-value">
                            {percentage:.2f}%
                        </div>
                        <div class="metric-note">
                            Keyword skill overlap
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with score_col2:
                st.write("**Required skills coverage**")
                st.progress(
                    max(0, min(100, int(round(percentage))))
                )

                st.caption(
                    "This score measures the percentage of detected "
                    "job skills that were also found in your resume. "
                    "It does not guarantee job eligibility."
                )

            # --------------------------------------------------
            # ML: TF-IDF TEXT SIMILARITY SCORE
            # --------------------------------------------------

            st.markdown(
                '<div class="section-heading">'
                '🧠 Text Similarity Score (ML)'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="section-description">'
                'Measures textual similarity between your resume '
                'and the target job description using TF-IDF '
                'and Cosine Similarity.'
                '</div>',
                unsafe_allow_html=True,
            )

            similarity_col1, similarity_col2 = st.columns([1, 3])

            with similarity_col1:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            🧠 TF-IDF Similarity
                        </div>
                        <div class="metric-value">
                            {similarity_score:.2f}%
                        </div>
                        <div class="metric-note">
                            Keyword-based text similarity
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with similarity_col2:
                st.write("**Resume and Job Description Similarity**")

                st.progress(
                    max(
                        0,
                        min(100, int(round(similarity_score))),
                    )
                )

                st.caption(
                    "TF-IDF measures textual overlap and does not "
                    "fully understand sentence meaning. This is "
                    "not a hiring probability."
                )

            # --------------------------------------------------
            # DL: SEMANTIC SIMILARITY SCORE
            # --------------------------------------------------

            st.markdown(
                '<div class="section-heading">'
                '🤖 Semantic Similarity Score (Deep Learning)'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="section-description">'
                'Uses a pretrained Sentence Transformer model '
                'to compare the meaning of the resume and '
                'the target job description.'
                '</div>',
                unsafe_allow_html=True,
            )

            semantic_col1, semantic_col2 = st.columns([1, 3])

            with semantic_col1:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">
                            🤖 Semantic Similarity
                        </div>
                        <div class="metric-value">
                            {semantic_score:.2f}%
                        </div>
                        <div class="metric-note">
                            Sentence Transformer score
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with semantic_col2:
                st.write("**Meaning-based Resume and Job Similarity**")

                st.progress(
                    max(
                        0,
                        min(100, int(round(semantic_score))),
                    )
                )

                st.caption(
                    "Uses the pretrained all-MiniLM-L6-v2 model. "
                    "This score estimates semantic similarity; "
                    "it is not a hiring probability or guarantee "
                    "of job eligibility."
                )

            # --------------------------------------------------
            # SKILLS COMPARISON
            # --------------------------------------------------

            st.markdown(
                '<div class="section-heading">'
                '🧩 Skills Comparison'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="section-description">'
                'See which required skills were found '
                'and which ones were not detected.'
                '</div>',
                unsafe_allow_html=True,
            )

            matched_col, missing_col = st.columns(2, gap="large")

            # MATCHED SKILLS

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

                matched_html = (
                    '<div class="skill-panel matched-panel">'
                    '<div class="panel-title">'
                    '✅ Matched Skills '
                    f'<span class="count-matched">'
                    f'({len(matched)} found)'
                    '</span>'
                    '</div>'
                    '<div class="panel-subtitle">'
                    'Skills found in both your resume '
                    'and the job description.'
                    '</div>'
                    '<div class="skills-container">'
                    f'{matched_chips}'
                    '</div>'
                    '</div>'
                )

                st.markdown(
                    matched_html,
                    unsafe_allow_html=True,
                )

            # MISSING SKILLS

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

                missing_html = (
                    '<div class="skill-panel missing-panel">'
                    '<div class="panel-title">'
                    '📌 Missing Skills '
                    f'<span class="count-missing">'
                    f'({len(missing)} to review)'
                    '</span>'
                    '</div>'
                    '<div class="panel-subtitle">'
                    'Required skills not detected in resume.'
                    '</div>'
                    '<div class="skills-container">'
                    f'{missing_chips}'
                    '</div>'
                    '</div>'
                )

                st.markdown(
                    missing_html,
                    unsafe_allow_html=True,
                )

            # --------------------------------------------------
            # RESUME IMPROVEMENT SUGGESTIONS
            # --------------------------------------------------

            st.markdown(
                '<div class="section-heading">'
                '💡 Resume Improvement Suggestions'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="section-description">'
                'Recommendations to help improve your resume '
                'for the target job.'
                '</div>',
                unsafe_allow_html=True,
            )

            suggestions = generate_suggestions(
                missing_skills=missing,
                matched_skills=matched,
                similarity_score=similarity_score,
            )

            with st.container(border=True):

                st.markdown("### 🚀 Your Action Plan")

                for index, suggestion in enumerate(
                    suggestions,
                    start=1,
                ):
                    st.markdown(
                        f"**{index}.** {suggestion}"
                    )

            if missing:
                st.info(
                    "💡 Tip: Add a missing skill to your resume "
                    "only if you genuinely have that skill. "
                    "Otherwise, consider learning it and building "
                    "a relevant project."
                )

            # --------------------------------------------------
            # CATEGORY-WISE SKILLS
            # --------------------------------------------------

            st.markdown(
                '<div class="section-heading">'
                '🧩 Skills by Category'
                '</div>',
                unsafe_allow_html=True,
            )

            if categorized_skills:

                categories = list(categorized_skills.items())
                category_columns = st.columns(2)

                for index, (category, skills) in enumerate(categories):

                    with category_columns[index % 2]:

                        with st.container(border=True):

                            st.markdown(
                                f"**{escape(str(category))}**"
                            )

                            st.write(" · ".join(map(str, skills)))

            else:
                st.info(
                    "No skills from the current skills database "
                    "were found in this resume."
                )

            # --------------------------------------------------
            # EXTRACTED RESUME TEXT
            # --------------------------------------------------

            with st.expander("🔎 View Extracted Resume Text"):
                st.text(resume_text)

            # --------------------------------------------------
            # DETECTED JOB SKILLS
            # --------------------------------------------------

            with st.expander("📋 View Detected Job Skills"):
                st.write(required_skills)

        except Exception as error:
            st.error("An error occurred during resume analysis.")
            st.exception(error)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        IntelliHire AI · Resume Analysis & Job Matching
        <br>
        Built with Python, Streamlit and Sentence Transformers
    </div>
    """,
    unsafe_allow_html=True,
)