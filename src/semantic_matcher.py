from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# LOAD PRETRAINED SEMANTIC SIMILARITY MODEL
# --------------------------------------------------

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


# --------------------------------------------------
# CALCULATE SEMANTIC SIMILARITY
# --------------------------------------------------

def calculate_semantic_similarity(resume_text, job_description):
    """
    Calculate semantic similarity between resume text
    and a job description using a pretrained model.

    Returns:
        Similarity score as a percentage.
    """

    if not resume_text or not resume_text.strip():
        return 0.0

    if not job_description or not job_description.strip():
        return 0.0

    # Generate semantic embeddings
    embeddings = model.encode(
        [resume_text, job_description],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    resume_embedding = embeddings[0].reshape(1, -1)
    job_embedding = embeddings[1].reshape(1, -1)

    # Calculate cosine similarity
    similarity = cosine_similarity(
        resume_embedding,
        job_embedding,
    )[0][0]

    # Convert to percentage
    semantic_score = float(similarity * 100)

    return round(semantic_score, 2)