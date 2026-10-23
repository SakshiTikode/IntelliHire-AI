
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
CSS_FILE = BASE_DIR / "style.css"


# ============================================================
# GLOBAL CSS STYLING
# ============================================================

def apply_global_style():
    """Apply the shared CSS theme safely."""

    if not CSS_FILE.exists():
        st.warning(
            f"CSS file not found: {CSS_FILE.name}. "
            "Please ensure style.css exists in the project folder."
        )
        return

    try:
        css = CSS_FILE.read_text(encoding="utf-8")

        st.markdown(
            f"<style>\n{css}\n</style>",
            unsafe_allow_html=True,
        )

    except OSError as error:
        st.warning(f"Unable to load the global stylesheet: {error}")


# ============================================================
# SHARED SIDEBAR
# ============================================================

def render_sidebar():
    """
    Render shared IntelliHire AI branding and information.

    Navigation is managed by app.py using st.navigation.
    Do not create additional navigation buttons here, as doing
    so can cause duplicate widget-key errors.
    """

    with st.sidebar:

        # Application branding
        st.markdown(
            """
            <div style="padding: 12px 0 20px 0;">
                <h2 style="margin-bottom: 4px;">
                    🧠 IntelliHire AI
                </h2>

                <p style="
                    color: #8A94A6;
                    font-size: 13px;
                    margin-top: 0;
                ">
                    Resume Analysis &amp; Job Matching
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # Available platform features
        st.caption("AI-POWERED CAREER TOOLS")

        st.markdown(
            """
            - 📄 Resume Analysis
            - 🤖 GenAI Resume Review
            - 📊 Interactive Dashboard
            - 📥 Download Report
            - 💬 Career Assistant
            """
        )

        st.divider()

        # Footer
        st.markdown(
            """
            <div style="
                color: #8A94A6;
                font-size: 12px;
                line-height: 1.6;
            ">
                <strong>Analyze. Improve. Get Hired.</strong><br>
                Your AI-powered career companion.
            </div>
            """,
            unsafe_allow_html=True,
        )
