import streamlit as st

st.set_page_config(
    page_title="GenAI Resume Review",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 GenAI-Powered Resume Review")
st.write("AI-generated feedback tailored to your resume and target job.")

if "ai_review" not in st.session_state:
    st.session_state.ai_review = ""

if st.session_state.ai_review:
    st.markdown(st.session_state.ai_review)
else:
    st.info(
        "No AI review available yet. "
        "Open Resume Analysis, upload your resume, "
        "enter a job description, and click Analyze My Resume."
    )