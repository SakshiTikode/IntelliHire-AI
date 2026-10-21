import re

from skills_database import SKILLS_DATABASE


# --------------------------------------------------
# SKILL SYNONYMS
# --------------------------------------------------

SKILL_SYNONYMS = {
    # Object-oriented programming
    "oop": "object-oriented programming",
    "object oriented programming": "object-oriented programming",
    "object-oriented programming": "object-oriented programming",

    # Scikit-learn
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "scikit-learn": "scikit-learn",

    # Natural Language Processing
    "nlp": "natural language processing",
    "natural language processing": "natural language processing",

    # Generative AI
    "genai": "generative ai",
    "gen ai": "generative ai",
    "generative ai": "generative ai",

    # Large Language Models
    "llm": "large language models",
    "llms": "large language models",
    "large language model": "large language models",
    "large language models": "large language models",

    # Programming languages
    "js": "javascript",
    "javascript": "javascript",
    "py": "python",
    "python": "python",

    # Deep learning frameworks
    "tf": "tensorflow",
    "tensorflow": "tensorflow",
    "pytorch": "pytorch",

    # Web frameworks
    "fast api": "fastapi",
    "fastapi": "fastapi",

    # Databases
    "postgres": "postgresql",
    "postgresql": "postgresql",

    # Development tools
    "github": "github",
    "git": "git",

    # Text similarity
    "tf idf": "tf-idf",
    "tf-idf": "tf-idf",
    "cosine similarity": "cosine similarity",

    # NLP models
    "sentence transformer": "sentence transformers",
    "sentence transformers": "sentence transformers",
}


# --------------------------------------------------
# NORMALIZE SKILL NAME
# --------------------------------------------------

def normalize_skill(skill):
    """Convert known skill aliases to a common skill name."""

    normalized = skill.lower().strip()
    normalized = re.sub(r"\s+", " ", normalized)

    return SKILL_SYNONYMS.get(normalized, normalized)


# --------------------------------------------------
# EXTRACT SKILLS
# --------------------------------------------------

def extract_skills(text):
    """Extract unique skills from resume or job description."""

    if not text or not text.strip():
        return []

    found_skills = []
    seen_skills = set()
    text_lower = text.lower()

    for category, skills in SKILLS_DATABASE.items():
        for skill in skills:
            pattern = (
                r"(?<!\w)"
                + re.escape(skill.lower())
                + r"(?!\w)"
            )

            if re.search(pattern, text_lower):
                normalized = normalize_skill(skill)

                if normalized not in seen_skills:
                    found_skills.append(skill)
                    seen_skills.add(normalized)

    return found_skills


# --------------------------------------------------
# CATEGORIZE SKILLS
# --------------------------------------------------

def categorize_skills(text):
    """Group detected resume skills by category."""

    if not text or not text.strip():
        return {}

    categorized_skills = {}
    text_lower = text.lower()

    for category, skills in SKILLS_DATABASE.items():
        found = []
        seen = set()

        for skill in skills:
            pattern = (
                r"(?<!\w)"
                + re.escape(skill.lower())
                + r"(?!\w)"
            )

            if re.search(pattern, text_lower):
                normalized = normalize_skill(skill)

                if normalized not in seen:
                    found.append(skill)
                    seen.add(normalized)

        if found:
            categorized_skills[category] = found

    return categorized_skills


# --------------------------------------------------
# SMART SKILL COMPARISON
# --------------------------------------------------

def compare_skills(resume_skills, required_skills):
    """
    Compare resume skills with required job skills.

    Returns:
        matched_skills, missing_skills, match_percentage
    """

    resume_normalized = {
        normalize_skill(skill)
        for skill in resume_skills
    }

    unique_required = []
    seen_required = set()

    for skill in required_skills:
        normalized = normalize_skill(skill)

        if normalized not in seen_required:
            seen_required.add(normalized)
            unique_required.append(skill)

    matched_skills = []
    missing_skills = []

    for skill in unique_required:
        normalized = normalize_skill(skill)

        if normalized in resume_normalized:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    match_percentage = (
        len(matched_skills) / len(unique_required) * 100
        if unique_required
        else 0.0
    )

    return matched_skills, missing_skills, match_percentage


# --------------------------------------------------
# ALTERNATIVE SKILL MATCHING
# --------------------------------------------------

def compare_skills_with_alternatives(
    resume_skills,
    required_skills,
):
    """
    Treat TensorFlow and PyTorch as one alternative requirement
    when both appear in the detected job skills.
    """

    matched, missing, percentage = compare_skills(
        resume_skills,
        required_skills,
    )

    resume_normalized = {
        normalize_skill(skill)
        for skill in resume_skills
    }

    required_normalized = {
        normalize_skill(skill)
        for skill in required_skills
    }

    alternatives = {"tensorflow", "pytorch"}

    # Apply alternative matching only when both skills are required.
    if alternatives.issubset(required_normalized):

        has_alternative = bool(
            resume_normalized.intersection(alternatives)
        )

        # Remove the individual skills from the result lists.
        matched = [
            skill for skill in matched
            if normalize_skill(skill) not in alternatives
        ]

        missing = [
            skill for skill in missing
            if normalize_skill(skill) not in alternatives
        ]

        if has_alternative:
            matched.append("TensorFlow or PyTorch")
        else:
            missing.append("TensorFlow or PyTorch")

        # Count unique requirements, treating the alternatives as one.
        total_requirements = len(required_normalized) - 1

        percentage = (
            len(matched) / total_requirements * 100
            if total_requirements
            else 0.0
        )

    return matched, missing, percentage


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 45)
    print("       Welcome to IntelliHire AI")
    print(" Resume Analysis & Job Matching System")
    print("=" * 45)

    print("\nPaste your resume text below.")
    print("Type END on a new line when finished.")

    resume_lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        resume_lines.append(line)

    resume_text = "\n".join(resume_lines)

    print("\nPaste the Job Description below.")
    print("Type END on a new line when finished.")

    job_lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        job_lines.append(line)

    job_description = "\n".join(job_lines)

    # Extract skills
    resume_skills = extract_skills(resume_text)
    required_skills = extract_skills(job_description)

    # Categorize resume skills
    categorized_skills = categorize_skills(resume_text)

    # Compare skills, including alternative requirements
    matched_skills, missing_skills, match_percentage = (
        compare_skills_with_alternatives(
            resume_skills,
            required_skills,
        )
    )

    # Display results
    print("\n" + "=" * 45)
    print("          ANALYSIS RESULTS")
    print("=" * 45)

    print("\n--- Resume Skills by Category ---")

    for category, skills in categorized_skills.items():
        print(f"\n{category}:")

        for skill in skills:
            print(f"  - {skill}")

    print("\n--- Resume Skills ---")
    print(resume_skills)

    print("\n--- Required Job Skills ---")
    print(required_skills)

    print("\n--- Matched Skills ---")
    print(matched_skills)

    print("\n--- Missing Skills ---")
    print(missing_skills)

    print(f"\nSkill Match: {match_percentage:.2f}%")