def generate_suggestions(missing_skills, matched_skills, similarity_score):
    """
    Generate personalized suggestions to improve a resume
    based on missing skills, matched skills, and similarity score.
    """

    suggestions = []

    # Suggest learning missing skills
    if missing_skills:
        suggestions.append(
            "Consider learning or highlighting these skills required "
            "for the job: " + ", ".join(missing_skills[:5]) + "."
        )
    else:
        suggestions.append(
            "Great! All detected job-description skills are present "
            "in your resume."
        )

    # Suggest highlighting matched skills
    if matched_skills:
        suggestions.append(
            "Highlight your relevant skills in the resume's Skills "
            "section and connect them to specific projects or work experience."
        )

    # Suggest improving resume-job description alignment
    if similarity_score < 40:
        suggestions.append(
            "Your resume has relatively low text similarity with the job "
            "description. Tailor your resume summary and experience to "
            "accurately reflect the role's requirements."
        )
    elif similarity_score < 70:
        suggestions.append(
            "Your resume has moderate text similarity. Improve alignment "
            "by using relevant terminology from the job description where "
            "it truthfully describes your experience."
        )
    else:
        suggestions.append(
            "Your resume has good text similarity with the job description. "
            "Keep your experience and achievements specific and relevant."
        )

    # Suggest adding measurable achievements
    suggestions.append(
        "Include measurable achievements wherever possible, such as "
        "project results, time saved, accuracy improved, or performance gains."
    )

    # Suggest adding projects
    suggestions.append(
        "Add relevant projects that demonstrate your technical skills, "
        "tools, and practical problem-solving ability."
    )

    return suggestions