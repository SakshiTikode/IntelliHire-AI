from src.genai_assistant import generate_resume_review

resume_text = """
B.Tech in Artificial Intelligence and Data Science.
Skills: Python, Pandas, NumPy, Machine Learning.
Project: Smart Agriculture using Machine Learning.
"""

job_description = """
Looking for a Data Scientist with Python, Pandas,
SQL, Machine Learning and data visualization skills.
"""

result = generate_resume_review(
    resume_text,
    job_description
)

print("\n===== GEMINI AI RESUME REVIEW =====\n")
print(result)