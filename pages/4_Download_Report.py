
import streamlit as st
from io import BytesIO
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

from common import apply_global_style, render_sidebar


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Download AI Report | IntelliHire AI",
    page_icon="📄",
    layout="wide",
)

apply_global_style()
render_sidebar()


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------
st.markdown(
    """
    <div class="ih-hero">
        <div class="ih-eyebrow">INTELLIHIRE AI • REPORT CENTER</div>
        <h1>Download Your AI Resume Report</h1>
        <p>
            Export your resume analysis, job-matching scores,
            matched skills, missing skills, and AI review
            into a professional PDF report.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")


# --------------------------------------------------
# CHECK ANALYSIS AVAILABILITY
# --------------------------------------------------
required_keys = [
    "resume_text",
    "job_description",
    "skill_match_percentage",
    "similarity_score",
    "semantic_score",
]

if not all(
    key in st.session_state and st.session_state[key] is not None
    for key in required_keys
):
    st.info(
        "Your analysis results are not available yet. "
        "Complete Resume Analysis before generating your report."
    )

    if st.button(
        "📄 Go to Resume Analysis",
        use_container_width=True,
        type="primary",
    ):
        st.switch_page("pages/1_Resume_Analysis.py")

    st.stop()


# --------------------------------------------------
# PDF GENERATION
# --------------------------------------------------
def make_pdf():
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45,
        title="IntelliHire AI Resume Analysis Report",
        author="IntelliHire AI",
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=24,
            leading=30,
            textColor=colors.HexColor("#2457A7"),
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ReportSubtitle",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontSize=11,
            leading=16,
            textColor=colors.HexColor("#526078"),
            spaceAfter=18,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading1"],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#2457A7"),
            spaceBefore=10,
            spaceAfter=9,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ReportBody",
            parent=styles["BodyText"],
            fontSize=9.5,
            leading=14,
            spaceAfter=5,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SmallNote",
            parent=styles["Italic"],
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#64748B"),
        )
    )

    story = []

    # --------------------------------------------------
    # REPORT TITLE
    # --------------------------------------------------
    story.append(Spacer(1, 15))
    story.append(Paragraph("IntelliHire AI", styles["ReportTitle"]))
    story.append(
        Paragraph(
            "Resume Analysis &amp; Job Matching Report",
            styles["ReportSubtitle"],
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor("#D7E3F5"),
            spaceAfter=15,
        )
    )

    generated_time = datetime.now().strftime(
        "%d %B %Y, %I:%M %p"
    )

    story.append(
        Paragraph(
            f"<b>Report generated:</b> {escape(generated_time)}",
            styles["ReportBody"],
        )
    )

    story.append(Spacer(1, 12))

    # --------------------------------------------------
    # ANALYSIS SCORES
    # --------------------------------------------------
    story.append(
        Paragraph("1. Analysis Scores", styles["SectionHeading"])
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
        colWidths=[330, 120],
        repeatRows=1,
        hAlign="LEFT",
    )

    score_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#2457A7"),
                ),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D8E0EA")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                    colors.white,
                    colors.HexColor("#F3F7FC"),
                ]),
                ("PADDING", (0, 0), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )

    story.append(score_table)
    story.append(Spacer(1, 15))

    # --------------------------------------------------
    # MATCHED SKILLS
    # --------------------------------------------------
    matched = st.session_state.get("matched_skills", [])

    story.append(
        Paragraph("2. Matched Skills", styles["SectionHeading"])
    )

    if matched:
        matched_text = escape(", ".join(map(str, matched)))
        story.append(
            Paragraph(matched_text, styles["ReportBody"])
        )
    else:
        story.append(
            Paragraph(
                "No matched skills were recorded.",
                styles["ReportBody"],
            )
        )

    story.append(Spacer(1, 8))

    # --------------------------------------------------
    # MISSING SKILLS
    # --------------------------------------------------
    missing = st.session_state.get("missing_skills", [])

    story.append(
        Paragraph("3. Missing Skills", styles["SectionHeading"])
    )

    if missing:
        missing_text = escape(", ".join(map(str, missing)))
        story.append(
            Paragraph(missing_text, styles["ReportBody"])
        )
    else:
        story.append(
            Paragraph(
                "No missing skills were recorded.",
                styles["ReportBody"],
            )
        )

    story.append(Spacer(1, 8))

    # --------------------------------------------------
    # GEMINI AI REVIEW
    # --------------------------------------------------
    story.append(
        Paragraph(
            "4. Gemini AI Resume Review",
            styles["SectionHeading"],
        )
    )

    review = st.session_state.get("ai_review", "")

    if review:
        for line in str(review).splitlines():
            clean_line = line.strip()

            if not clean_line:
                story.append(Spacer(1, 4))
                continue

            # Basic Markdown cleanup for PDF readability.
            clean_line = clean_line.replace("**", "")
            clean_line = clean_line.replace("### ", "")
            clean_line = clean_line.replace("## ", "")
            clean_line = clean_line.replace("# ", "")

            if clean_line.startswith("- ") or clean_line.startswith("* "):
                clean_line = "• " + clean_line[2:]

            story.append(
                Paragraph(
                    escape(clean_line),
                    styles["ReportBody"],
                )
            )
    else:
        story.append(
            Paragraph(
                "No AI review is available. "
                "Complete the AI review step to include feedback in this report.",
                styles["ReportBody"],
            )
        )

    story.append(Spacer(1, 18))

    # --------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------
    story.append(
        HRFlowable(
            width="100%",
            thickness=0.5,
            color=colors.HexColor("#D8E0EA"),
            spaceBefore=5,
            spaceAfter=10,
        )
    )

    story.append(
        Paragraph(
            "<b>Disclaimer:</b> Similarity scores are algorithmic estimates "
            "and do not guarantee job selection. Review all recommendations "
            "carefully before updating your resume.",
            styles["SmallNote"],
        )
    )

    # Add a page number to every page.
    def add_page_number(canvas, document):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#64748B"))
        canvas.drawRightString(
            A4[0] - 45,
            22,
            f"IntelliHire AI | Page {document.page}",
        )
        canvas.restoreState()

    doc.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    buffer.seek(0)
    return buffer.getvalue()


# --------------------------------------------------
# REPORT PREVIEW AND DOWNLOAD
# --------------------------------------------------
st.markdown("### 📊 Report Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Skill Match",
        f"{float(st.session_state.skill_match_percentage):.2f}%",
    )

with col2:
    st.metric(
        "TF-IDF / ML Similarity",
        f"{float(st.session_state.similarity_score):.2f}%",
    )

with col3:
    st.metric(
        "Semantic Similarity",
        f"{float(st.session_state.semantic_score):.2f}%",
    )

st.write("")

try:
    pdf_data = make_pdf()

    st.success("Your PDF report is ready to download.")

    st.download_button(
        label="⬇️ Download Resume Analysis Report (PDF)",
        data=pdf_data,
        file_name="IntelliHire_AI_Resume_Report.pdf",
        mime="application/pdf",
        use_container_width=True,
        type="primary",
    )

except Exception as error:
    st.error("Could not generate the PDF report.")
    st.exception(error)
