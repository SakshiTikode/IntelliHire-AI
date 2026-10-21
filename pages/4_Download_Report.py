import streamlit as st
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from xml.sax.saxutils import escape

st.set_page_config(
    page_title="Download AI Report",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Download Your AI Resume Report")
st.write(
    "Generate a PDF containing your resume analysis scores, "
    "matched skills, missing skills, and Gemini AI review."
)

# Check analysis availability
required_keys = [
    "resume_text",
    "job_description",
    "skill_match_percentage",
    "similarity_score",
    "semantic_score",
]

if not all(
    key in st.session_state and st.session_state[key]
    for key in required_keys
):
    st.info(
        "Please complete Resume Analysis first. "
        "Your results will then be available here."
    )

    if st.button("📄 Go to Resume Analysis"):
        st.switch_page("pages/1_Resume_Analysis.py")

    st.stop()


def make_pdf():
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45,
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            textColor=colors.HexColor("#2457A7"),
            spaceAfter=18,
        )
    )

    story = []

    # Report heading
    story.append(
        Paragraph("IntelliHire AI", styles["ReportTitle"])
    )
    story.append(
        Paragraph(
            "Resume Analysis &amp; Job Matching Report",
            styles["Heading2"],
        )
    )
    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 18))

    # Score summary
    story.append(
        Paragraph("1. Analysis Scores", styles["Heading1"])
    )

    scores_data = [
        ["Metric", "Score"],
        [
            "Skill Match",
            f"{float(st.session_state.skill_match_percentage):.2f}%",
        ],
        [
            "TF-IDF / ML Similarity",
            f"{float(st.session_state.similarity_score):.2f}%",
        ],
        [
            "Semantic / DL Similarity",
            f"{float(st.session_state.semantic_score):.2f}%",
        ],
    ]

    score_table = Table(
        scores_data,
        colWidths=[280, 150],
        repeatRows=1,
    )

    score_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2457A7")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )

    story.append(score_table)
    story.append(Spacer(1, 18))

    # Matched and missing skills
    matched = st.session_state.get("matched_skills", [])
    missing = st.session_state.get("missing_skills", [])

    story.append(
        Paragraph("2. Matched Skills", styles["Heading1"])
    )

    if matched:
        story.append(
            Paragraph(
                escape(", ".join(map(str, matched))),
                styles["BodyText"],
            )
        )
    else:
        story.append(
            Paragraph("No matched skills recorded.", styles["BodyText"])
        )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph("3. Missing Skills", styles["Heading1"])
    )

    if missing:
        story.append(
            Paragraph(
                escape(", ".join(map(str, missing))),
                styles["BodyText"],
            )
        )
    else:
        story.append(
            Paragraph("No missing skills recorded.", styles["BodyText"])
        )

    story.append(Spacer(1, 18))

    # Gemini AI review
    story.append(
        Paragraph("4. Gemini AI Resume Review", styles["Heading1"])
    )

    review = st.session_state.get("ai_review", "")

    if review:
        for line in review.splitlines():
            clean_line = line.strip()

            if not clean_line:
                story.append(Spacer(1, 5))
                continue

            # Remove basic Markdown markers for a readable PDF.
            clean_line = clean_line.replace("**", "")
            clean_line = clean_line.replace("### ", "")
            clean_line = clean_line.replace("## ", "")
            clean_line = clean_line.replace("# ", "")
            clean_line = clean_line.replace("- ", "• ")

            story.append(
                Paragraph(
                    escape(clean_line),
                    styles["BodyText"],
                )
            )
            story.append(Spacer(1, 5))
    else:
        story.append(
            Paragraph(
                "No AI review is available. Complete Resume Analysis first.",
                styles["BodyText"],
            )
        )

    story.append(Spacer(1, 18))

    # Disclaimer
    story.append(
        Paragraph(
            "Note: Similarity scores are algorithmic estimates and do not "
            "guarantee job selection. Review all recommendations before "
            "updating your resume.",
            styles["Italic"],
        )
    )

    doc.build(story)
    buffer.seek(0)

    return buffer.getvalue()


try:
    st.success("Your analysis results are ready to export.")

    st.download_button(
        label="⬇️ Download Resume Analysis Report (PDF)",
        data=make_pdf(),
        file_name="IntelliHire_AI_Resume_Report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

except Exception as error:
    st.error("Could not generate the PDF report.")
    st.exception(error)