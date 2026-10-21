import streamlit as st

st.set_page_config(
    page_title="IntelliHire AI | Home",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- SESSION STATE ----------------

if "ai_review" not in st.session_state:
    st.session_state.ai_review = ""

# ---------------- CUSTOM CSS ----------------

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    .hero {
        padding: 42px 36px;
        border-radius: 24px;
        color: white;
        background: linear-gradient(
            120deg,
            #171b4d,
            #4838a8,
            #7654d6
        );
        box-shadow: 0 12px 32px rgba(48, 44, 130, 0.18);
        margin-bottom: 28px;
    }

    .hero h1 {
        color: white;
        font-size: 42px;
        margin-bottom: 12px;
    }

    .hero p {
        color: #f1efff;
        font-size: 17px;
        line-height: 1.7;
    }

    .badge {
        display: inline-block;
        padding: 7px 13px;
        border-radius: 20px;
        background: rgba(255,255,255,0.16);
        font-size: 13px;
        margin-bottom: 15px;
    }

    .feature-card {
        padding: 23px;
        border: 1px solid #e3e6f0;
        border-radius: 18px;
        background: white;
        min-height: 195px;
        margin-bottom: 12px;
    }

    .feature-card h3 {
        color: #252858;
        margin-bottom: 12px;
    }

    .feature-card p {
        color: #555b70;
        line-height: 1.65;
    }

    .section-title {
        color: #252858;
        font-size: 26px;
        font-weight: 700;
        margin-top: 24px;
        margin-bottom: 15px;
    }

    .step-card {
        padding: 18px;
        border-radius: 14px;
        background: #f2f4ff;
        border: 1px solid #e3e6ff;
        min-height: 125px;
    }

    .step-card h4 {
        color: #343b8b;
        margin-bottom: 8px;
    }

    div.stButton > button {
        border-radius: 10px;
        min-height: 45px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- HERO SECTION ----------------

st.markdown(
    """
    <div class="hero">
        <div class="badge">✨ AI-POWERED CAREER INTELLIGENCE</div>
        <h1>Welcome to IntelliHire AI</h1>
        <p>
            Your intelligent career companion.<br>
            Analyze your resume, discover skill gaps, and prepare
            yourself for your next career opportunity using
            Machine Learning, Deep Learning and Generative AI.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- QUICK STATS ----------------

st.markdown('<div class="section-title">Your AI Career Toolkit</div>',
            unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Core Technology", "Machine Learning", "TF-IDF")

with col2:
    st.metric("Semantic Engine", "Deep Learning", "Sentence Transformers")

with col3:
    st.metric("AI Career Advisor", "Generative AI", "Gemini")

# ---------------- FEATURE CARDS ----------------

st.markdown('<div class="section-title">Explore Features</div>',
            unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    st.markdown(
        """
        <div class="feature-card">
            <h3>📊 Resume Analysis</h3>
            <p>
                Upload a PDF or DOCX resume, compare your skills
                with a target job, identify skill gaps, and explore
                keyword-based and semantic similarity scores.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "📄 Open Resume Analysis",
        use_container_width=True,
        type="primary",
    ):
        st.switch_page("pages/1_Resume_Analysis.py")

with right:
    st.markdown(
        """
        <div class="feature-card">
            <h3>🤖 GenAI Resume Review</h3>
            <p>
                Get personalized resume feedback, identify areas
                for improvement, and explore a recommended
                learning roadmap tailored to your target job.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "✨ Open GenAI Review",
        use_container_width=True,
    ):
        st.switch_page("pages/2_GenAI_Review.py")

# ---------------- HOW IT WORKS ----------------

st.markdown('<div class="section-title">How It Works</div>',
            unsafe_allow_html=True)

step1, step2, step3, step4 = st.columns(4)

with step1:
    st.markdown(
        """
        <div class="step-card">
            <h4>1. Upload</h4>
            <p>Provide your PDF or DOCX resume.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with step2:
    st.markdown(
        """
        <div class="step-card">
            <h4>2. Match</h4>
            <p>Compare resume skills with job requirements.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with step3:
    st.markdown(
        """
        <div class="step-card">
            <h4>3. Analyze</h4>
            <p>Review ML and semantic similarity results.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with step4:
    st.markdown(
        """
        <div class="step-card">
            <h4>4. Improve</h4>
            <p>Use Gemini feedback to plan your next steps.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------- INTERACTIVE EXPANDER ----------------

st.markdown('<div class="section-title">Understand the Technology</div>',
            unsafe_allow_html=True)

with st.expander("🧠 Machine Learning — TF-IDF Similarity"):
    st.write(
        "TF-IDF and cosine similarity estimate how closely the "
        "words and terms in your resume match the job description."
    )

with st.expander("🔬 Deep Learning — Semantic Similarity"):
    st.write(
        "A pretrained Sentence Transformer converts text into "
        "embeddings to estimate similarity in meaning, even when "
        "the exact words differ."
    )

with st.expander("✨ Generative AI — Gemini"):
    st.write(
        "Gemini generates contextual resume feedback, improvement "
        "suggestions, and a learning roadmap from your resume and "
        "the target job description."
    )

# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "IntelliHire AI | Resume Analysis • Job Matching • "
    "Machine Learning • Deep Learning • Generative AI"
)