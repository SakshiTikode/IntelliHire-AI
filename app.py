import streamlit as st

st.set_page_config(
    page_title="IntelliHire AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================================================
# PROFESSIONAL SIDEBAR THEME
# ==================================================

st.markdown("""
<style>

/* Sidebar background */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0B1120 0%,
        #10182B 55%,
        #111B30 100%
    );
    border-right: 1px solid rgba(148, 163, 184, 0.14);
}

/* Sidebar padding */
section[data-testid="stSidebar"] > div {
    padding: 1.2rem 1rem 1rem;
}

/* Hide default navigation */
[data-testid="stSidebarNav"] {
    display: none !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] p {
    color: #CBD5E1;
}

/* Brand title */
section[data-testid="stSidebar"] h3 {
    color: #F8FAFC;
    font-size: 19px;
    font-weight: 750;
    letter-spacing: -0.5px;
}

/* Section title */
.sidebar-section-label {
    color: #818CF8;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.8px;
    margin: 12px 0 8px 2px;
}

/* Navigation button container */
section[data-testid="stSidebar"] .stButton {
    width: 100%;
    margin-bottom: 4px;
}

/* Navigation buttons */
section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 44px;
    padding: 0.65rem 0.8rem;

    background: rgba(255, 255, 255, 0.025);
    color: #CBD5E1;

    border: 1px solid rgba(148, 163, 184, 0.08);
    border-radius: 10px;

    font-size: 13px;
    font-weight: 500;
    text-align: left;

    box-shadow: none;
    transition: all 0.2s ease;
}

/* Button text */
section[data-testid="stSidebar"] .stButton button p {
    color: inherit !important;
    font-size: 13px;
}

/* Hover */
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(99, 102, 241, 0.17);
    color: #FFFFFF;
    border-color: rgba(129, 140, 248, 0.4);
}

/* Focus */
section[data-testid="stSidebar"] .stButton > button:focus-visible {
    outline: 2px solid #818CF8;
    outline-offset: 2px;
}

/* Footer card */
.sidebar-footer-card {
    background: linear-gradient(
        145deg,
        rgba(99, 102, 241, 0.19),
        rgba(139, 92, 246, 0.07)
    );

    border: 1px solid rgba(129, 140, 248, 0.27);
    border-radius: 14px;

    padding: 16px 10px;
    margin-top: 22px;
    text-align: center;
}

/* Footer caption */
.sidebar-footer-caption {
    color: #94A3B8;
    font-size: 10px;
    text-align: center;
    line-height: 1.8;
    padding-top: 10px;
}

/* Divider */
section[data-testid="stSidebar"] hr {
    border-color: rgba(148, 163, 184, 0.15);
}

/* Responsive layout */
@media (max-width: 768px) {
    section[data-testid="stSidebar"] > div {
        padding: 1rem 0.75rem;
    }

    section[data-testid="stSidebar"] .stButton > button {
        min-height: 42px;
        font-size: 12px;
    }
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# PAGE DEFINITIONS
# ==================================================

home_page = st.Page(
    "home_page.py",
    title="Home",
    icon="🏠",
    default=True,
)

resume_page = st.Page(
    "pages/1_Resume_Analysis.py",
    title="Resume Analysis",
    icon="📄",
)

genai_page = st.Page(
    "pages/2_GenAI_Review.py",
    title="GenAI Review",
    icon="🤖",
)

dashboard_page = st.Page(
    "pages/3_Interactive_Dashboard.py",
    title="Interactive Dashboard",
    icon="📈",
)

report_page = st.Page(
    "pages/4_Download_Report.py",
    title="Download AI Report",
    icon="📑",
)

chatbot_page = st.Page(
    "pages/5_Career_Chatbot.py",
    title="AI Career Chatbot",
    icon="💬",
)


# ==================================================
# NAVIGATION CONFIGURATION
# ==================================================

navigation = st.navigation(
    [
        home_page,
        resume_page,
        genai_page,
        dashboard_page,
        report_page,
        chatbot_page,
    ],
    position="hidden",
)


# ==================================================
# PROFESSIONAL SIDEBAR
# ==================================================

with st.sidebar:

    # Brand header using native Streamlit components
    st.markdown("## ✦ IntelliHire AI")

    st.caption("CAREER INTELLIGENCE")

    st.divider()

    st.markdown(
        '<div class="sidebar-section-label">WORKSPACE</div>',
        unsafe_allow_html=True,
    )

    # Home
    if st.button(
        "🏠   Home",
        key="nav_home",
        use_container_width=True,
    ):
        st.switch_page("home_page.py")

    # Resume Analysis
    if st.button(
        "📄   Resume Analysis",
        key="nav_resume",
        use_container_width=True,
    ):
        st.switch_page("pages/1_Resume_Analysis.py")

    # GenAI Review
    if st.button(
        "🤖   GenAI Review",
        key="nav_genai",
        use_container_width=True,
    ):
        st.switch_page("pages/2_GenAI_Review.py")

    # Interactive Dashboard
    if st.button(
        "📈   Interactive Dashboard",
        key="nav_dashboard",
        use_container_width=True,
    ):
        st.switch_page("pages/3_Interactive_Dashboard.py")

    # Download AI Report
    if st.button(
        "📑   Download AI Report",
        key="nav_report",
        use_container_width=True,
    ):
        st.switch_page("pages/4_Download_Report.py")

    # AI Career Chatbot
    if st.button(
        "💬   AI Career Chatbot",
        key="nav_chatbot",
        use_container_width=True,
    ):
        st.switch_page("pages/5_Career_Chatbot.py")

    st.markdown("---")

    # Footer branding
    st.markdown(
        """
        <div class="sidebar-footer-card">
            <div style="
                color:#F8FAFC;
                font-size:14px;
                font-weight:700;
            ">
                ✦ IntelliHire AI
            </div>
            <div style="
                color:#A5B4FC;
                font-size:9px;
                font-weight:600;
                letter-spacing:0.8px;
                margin-top:8px;
            ">
                SMARTER CAREER. BETTER FUTURE.
            </div>
        </div>

        <div class="sidebar-footer-caption">
            ✨ AI-powered career assistant<br>
            Powered by Gemini
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==================================================
# RUN SELECTED PAGE
# ==================================================

navigation.run()