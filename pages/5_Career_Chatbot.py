import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(
    page_title="AI Career Chatbot",
    page_icon="💬",
    layout="wide",
)

st.title("💬 IntelliHire AI Career Assistant")
st.write(
    "Ask me about careers, resume improvement, missing skills, "
    "interview preparation, and job readiness."
)

# Initialize Gemini
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error(
        "GEMINI_API_KEY was not found. Please check your .env file."
    )
    st.stop()

client = genai.Client(api_key=api_key)

# Initialize chat history
if "career_chat_history" not in st.session_state:
    st.session_state.career_chat_history = []

# Optional context from previous resume analysis
with st.expander("📄 Your Resume Analysis Context"):
    if st.session_state.get("resume_text"):
        st.success("Resume analysis data is available.")

        matched = st.session_state.get("matched_skills", [])
        missing = st.session_state.get("missing_skills", [])

        st.write("**Matched skills:**")
        st.write(", ".join(map(str, matched)) or "Not available")

        st.write("**Skills to improve:**")
        st.write(", ".join(map(str, missing)) or "Not available")
    else:
        st.info(
            "Complete Resume Analysis first to make your career "
            "guidance more personalized."
        )

# Suggested questions
st.subheader("✨ Try asking")

suggestions = [
    "How can I prepare for a job interview?",
    "Create a 30-day career learning roadmap.",
    "How can I improve my resume?",
    "Give me five technical interview questions.",
]

cols = st.columns(2)

for index, question in enumerate(suggestions):
    with cols[index % 2]:
        if st.button(question, key=f"suggestion_{index}"):
            st.session_state.career_pending_question = question

st.divider()

# Display chat history
for message in st.session_state.career_chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input(
    "Ask about careers, skills, jobs, or interviews..."
)

if (
    not prompt
    and st.session_state.get("career_pending_question")
):
    prompt = st.session_state.pop("career_pending_question")

if prompt:
    st.session_state.career_chat_history.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Add relevant resume context
    resume_text = st.session_state.get("resume_text", "")
    job_description = st.session_state.get("job_description", "")
    matched = st.session_state.get("matched_skills", [])
    missing = st.session_state.get("missing_skills", [])

    context = f"""
Resume text:
{resume_text[:6000] if resume_text else "Not provided"}

Target job description:
{job_description[:3000] if job_description else "Not provided"}

Matched skills:
{", ".join(map(str, matched)) if matched else "Not available"}

Missing skills:
{", ".join(map(str, missing)) if missing else "Not available"}
"""

    system_instruction = """
You are IntelliHire AI, a helpful career guidance assistant.

Help users with:
- Career planning and job-role exploration
- Resume improvement
- Skill development roadmaps
- Technical and HR interview preparation
- Mock interview questions and feedback
- Job search strategies

Give practical, structured, encouraging answers.
Personalize your suggestions using the provided resume context when relevant.
Do not invent qualifications, experience, or achievements.
Clearly distinguish general guidance from information actually present
in the user's resume.
If a question is unrelated to careers, politely redirect the discussion.
"""

    conversation = []

    for message in st.session_state.career_chat_history[-12:]:
        conversation.append(
            f'{message["role"].upper()}: {message["content"]}'
        )

    full_prompt = f"""
{system_instruction}

USER CAREER CONTEXT:
{context}

CONVERSATION:
{chr(10).join(conversation)}

Respond to the latest user message with useful, specific guidance.
"""

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.interactions.create(
                    model="gemini-3.8-flash",
                    input=full_prompt,
                )

                answer = getattr(response, "output_text", None)

                if not answer:
                    answer = str(response)

                st.markdown(answer)

                st.session_state.career_chat_history.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as error:
                st.error(
                    "I couldn't generate a response. Please try again."
                )
                st.caption(str(error))

# Clear conversation
if st.session_state.career_chat_history:
    if st.button("🗑️ Clear Chat"):
        st.session_state.career_chat_history = []
        st.rerun()