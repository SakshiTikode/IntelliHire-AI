
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

from common import apply_global_style, render_sidebar


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Career Assistant | IntelliHire AI",
    page_icon="💬",
    layout="wide",
)

load_dotenv()

apply_global_style()
render_sidebar()


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------
st.markdown(
    """
    <div class="ih-hero">
        <div class="ih-eyebrow">INTELLIHIRE AI • CAREER SUPPORT</div>
        <h1>AI Career Assistant</h1>
        <p>
            Get personalized career guidance, improve your resume,
            prepare for interviews, and build a practical learning roadmap.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")


# --------------------------------------------------
# GEMINI CONFIGURATION
# --------------------------------------------------
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error(
        "GEMINI_API_KEY was not found. "
        "Please check your .env file and restart the application."
    )
    st.stop()

try:
    client = genai.Client(api_key=api_key)
except Exception as error:
    st.error("Could not initialize the Gemini client.")
    st.caption(str(error))
    st.stop()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "career_chat_history" not in st.session_state:
    st.session_state.career_chat_history = []

if "career_pending_question" not in st.session_state:
    st.session_state.career_pending_question = None

if "career_clear_confirmation" not in st.session_state:
    st.session_state.career_clear_confirmation = False


# --------------------------------------------------
# RESUME CONTEXT
# --------------------------------------------------
resume_text = st.session_state.get("resume_text", "")
job_description = st.session_state.get("job_description", "")
matched_skills = st.session_state.get("matched_skills", [])
missing_skills = st.session_state.get("missing_skills", [])

with st.expander("📄 Your Resume Analysis Context", expanded=False):
    if resume_text:
        st.success("Resume analysis data is available.")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**✅ Matched Skills**")

            if matched_skills:
                st.write(", ".join(map(str, matched_skills)))
            else:
                st.caption("No matched skills recorded.")

        with col2:
            st.markdown("**🎯 Skills to Improve**")

            if missing_skills:
                st.write(", ".join(map(str, missing_skills)))
            else:
                st.caption("No missing skills recorded.")

        if job_description:
            st.markdown("**Target Job Description**")
            st.write(
                job_description[:1200]
                + ("..." if len(job_description) > 1200 else "")
            )
    else:
        st.info(
            "Complete Resume Analysis first to receive more personalized "
            "career guidance. You can still ask general career questions."
        )


# --------------------------------------------------
# SUGGESTED QUESTIONS
# --------------------------------------------------
st.markdown("### ✨ What would you like help with?")

suggestions = [
    "How can I prepare for a job interview?",
    "Create a 30-day career learning roadmap.",
    "How can I improve my resume?",
    "Give me five technical interview questions.",
]

suggestion_cols = st.columns(2)

for index, question in enumerate(suggestions):
    with suggestion_cols[index % 2]:
        if st.button(
            question,
            key=f"career_suggestion_{index}",
            use_container_width=True,
        ):
            st.session_state.career_pending_question = question
            st.rerun()


st.divider()


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------
st.markdown("### 💬 Your Conversation")

if not st.session_state.career_chat_history:
    st.caption(
        "Your conversation will appear here. Choose a suggested question "
        "above or type your own question below."
    )

for message in st.session_state.career_chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# GEMINI SYSTEM INSTRUCTION
# --------------------------------------------------
system_instruction = """
You are IntelliHire AI, a helpful and professional career guidance assistant.

Your responsibilities include:
- Career planning and job-role exploration
- Resume improvement and ATS-friendly writing advice
- Skill development roadmaps
- Technical and HR interview preparation
- Mock interview questions and feedback
- Job search strategies and professional development

Guidelines:
1. Give practical, structured, encouraging answers.
2. Personalize recommendations using the supplied resume context when relevant.
3. Never invent qualifications, experience, skills, or achievements.
4. Distinguish information explicitly present in the resume from your suggestions.
5. If resume context is unavailable, explain that your advice is general.
6. Break learning roadmaps into manageable steps when appropriate.
7. Use examples where they help the user understand your advice.
8. For unrelated questions, politely guide the conversation back to careers.
9. Do not claim to have submitted applications, contacted employers,
   or performed actions outside this conversation.
"""


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------
prompt = st.chat_input(
    "Ask about careers, resumes, skills, jobs, or interviews..."
)

if not prompt and st.session_state.career_pending_question:
    prompt = st.session_state.career_pending_question
    st.session_state.career_pending_question = None


# --------------------------------------------------
# PROCESS USER MESSAGE
# --------------------------------------------------
if prompt:
    st.session_state.career_chat_history.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    context = f"""
USER RESUME CONTEXT

Resume text:
{resume_text[:6000] if resume_text else "Not provided"}

Target job description:
{job_description[:3000] if job_description else "Not provided"}

Matched skills:
{", ".join(map(str, matched_skills)) if matched_skills else "Not available"}

Skills to improve:
{", ".join(map(str, missing_skills)) if missing_skills else "Not available"}
"""

    # Keep a limited amount of conversation history.
    # The latest user message is already included in the history.
    recent_messages = st.session_state.career_chat_history[-12:]

    conversation = "\n\n".join(
        f'{message["role"].upper()}: {message["content"]}'
        for message in recent_messages
    )

    full_prompt = f"""
{system_instruction}

{context}

CONVERSATION HISTORY:
{conversation}

Respond to the latest user message with specific, useful career guidance.
"""

    with st.chat_message("assistant"):
        with st.spinner("Thinking about your question..."):
            try:
                response = client.interactions.create(
                    model="gemini-3.8-flash",
                    input=full_prompt,
                )

                answer = getattr(response, "output_text", None)

                if not answer:
                    answer = str(response)

                answer = answer.strip()

                if not answer:
                    answer = (
                        "I couldn't generate a useful response. "
                        "Please try asking your question another way."
                    )

                st.markdown(answer)

                st.session_state.career_chat_history.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            except Exception:
                # Remove the unanswered user message so that a retry
                # doesn't retain a failed request in the conversation.
                if (
                    st.session_state.career_chat_history
                    and st.session_state.career_chat_history[-1]["role"]
                    == "user"
                ):
                    st.session_state.career_chat_history.pop()

                st.error(
                    "I couldn't generate a response. Please try again."
                )

                st.info(
                    "Check your internet connection, Gemini API key, "
                    "model availability, and installed Google GenAI SDK."
                )


# --------------------------------------------------
# CLEAR CHAT
# --------------------------------------------------
if st.session_state.career_chat_history:
    st.divider()

    if not st.session_state.career_clear_confirmation:
        if st.button(
            "🗑️ Clear Conversation",
            use_container_width=False,
        ):
            st.session_state.career_clear_confirmation = True
            st.rerun()

    else:
        st.warning(
            "Are you sure you want to delete this conversation? "
            "This action cannot be undone."
        )

        confirm_col, cancel_col = st.columns(2)

        with confirm_col:
            if st.button(
                "Yes, clear chat",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.career_chat_history = []
                st.session_state.career_pending_question = None
                st.session_state.career_clear_confirmation = False
                st.rerun()

        with cancel_col:
            if st.button(
                "Cancel",
                use_container_width=True,
            ):
                st.session_state.career_clear_confirmation = False
                st.rerun()


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    <div class="ih-footer">
        <p>
            <strong>IntelliHire AI Career Assistant</strong><br>
            Your partner in resume improvement, skill development,
            and career preparation.
        </p>
        <p>
            AI-generated advice is intended for guidance.
            Review important career decisions carefully.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
