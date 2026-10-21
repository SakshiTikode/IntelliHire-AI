import streamlit as st

st.set_page_config(
    page_title="IntelliHire AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* Sidebar background */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #111827 0%,
        #1E293B 55%,
        #0F172A 100%
    ) !important;
}

/* Hide default Streamlit navigation */
[data-testid="stSidebarNav"] {
    display: none !important;
}

/* Sidebar padding */
section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

/* Custom navigation buttons */
section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    text-align: left;
    background-color: transparent !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: 1px solid transparent !important;
    border-radius: 8px !important;
    padding: 0.65rem 0.8rem !important;
    font-size: 15px !important;
    font-weight: 500 !important;
}

/* Force all button text white */
section[data-testid="stSidebar"] .stButton > button p,
section[data-testid="stSidebar"] .stButton > button span {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Hover */
section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #374151 !important;
    border: 1px solid #64748B !important;
}

/* Brand card */
.sidebar-brand {
    background: linear-gradient(120deg, #2563EB, #7C3AED);
    padding: 28px 12px;
    border-radius: 18px;
    text-align: center;
    color: white !important;
    margin: 30px 0;
    border: 1px solid #818CF8;
}

.sidebar-brand h2,
.sidebar-brand p {
    color: white !important;
}

/* Gemini card */
.ai-badge {
    background: rgba(255,255,255,0.06);
    border: 1px solid #475569;
    padding: 20px 10px;
    border-radius: 16px;
    text-align: center;
    color: white !important;
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.markdown("## 🧭 Navigation")

    # Custom navigation
    if st.button("🏠  Home", key="nav_home"):
        st.switch_page("home_page.py")

    if st.button("📄  Resume Analysis", key="nav_resume"):
        st.switch_page("pages/1_Resume_Analysis.py")

    if st.button("🤖  GenAI Review", key="nav_genai"):
        st.switch_page("pages/2_GenAI_Review.py")

    if st.button("📈  Interactive Dashboard", key="nav_dashboard"):
        st.switch_page("pages/3_Interactive_Dashboard.py")

    if st.button("📑  Download AI Report", key="nav_report"):
        st.switch_page("pages/4_Download_Report.py")

    if st.button("💬  AI Career Chatbot", key="nav_chatbot"):
        st.switch_page("pages/5_Career_Chatbot.py")

    st.markdown("---")

    st.markdown("""
    <div class="sidebar-brand">
        <h2>📄 IntelliHire AI</h2>
        <p style="font-size:11px; letter-spacing:1px;">
            SMARTER CAREER. BETTER FUTURE.
        </p>
    </div>

    <div class="ai-badge">
        <p>✨ AI-POWERED CAREER ASSISTANT</p>
        <br>
        <p>Powered by Gemini</p>
    </div>
    """, unsafe_allow_html=True)


# ---------------- PAGE NAVIGATION ----------------
home_page = st.Page(
    "home_page.py",
    title="Home",
    icon="🏠",
    default=True
)

resume_page = st.Page(
    "pages/1_Resume_Analysis.py",
    title="Resume Analysis",
    icon="📄"
)

genai_page = st.Page(
    "pages/2_GenAI_Review.py",
    title="GenAI Review",
    icon="🤖"
)

dashboard_page = st.Page(
    "pages/3_Interactive_Dashboard.py",
    title="Interactive Dashboard",
    icon="📈"
)

report_page = st.Page(
    "pages/4_Download_Report.py",
    title="Download AI Report",
    icon="📑"
)

chatbot_page = st.Page(
    "pages/5_Career_Chatbot.py",
    title="AI Career Chatbot",
    icon="💬"
)

navigation = st.navigation(
    [
        home_page,
        resume_page,
        genai_page,
        dashboard_page,
        report_page,
        chatbot_page
    ],
    position="hidden"
)

navigation.run()