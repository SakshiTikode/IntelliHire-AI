"""
IntelliHire AI
Resume and Job Description Similarity Matcher

Uses TF-IDF and Cosine Similarity to calculate
textual similarity between a resume and a job description.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_description):
    """
    Calculate textual similarity between a resume
    and a job description.

    Args:
        resume_text (str): Extracted resume text.
        job_description (str): Target job description.

    Returns:
        float: Similarity percentage between 0 and 100.
    """

    if not resume_text or not job_description:
        return 0.0

    resume_text = resume_text.strip()
    job_description = job_description.strip()

    if not resume_text or not job_description:
        return 0.0

    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(documents)

        similarity = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )[0][0]

        return round(float(similarity) * 100, 2)

    except ValueError:
        # Handles text that produces no usable TF-IDF features.
        return 0.0


if __name__ == "__main__":
    sample_resume = """
    Python developer with experience in machine learning,
    pandas, numpy, scikit-learn, and natural language processing.
    """

    sample_job_description = """
    We need a Python developer skilled in machine learning,
    pandas, numpy, scikit-learn, and NLP.
    """

    score = calculate_similarity(
        sample_resume,
        sample_job_description
    )

    print("=" * 45)
    print("       IntelliHire AI Similarity Test")
    print("=" * 45)
    print(f"Text Similarity Score: {score}%")