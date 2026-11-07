from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import ListFlowable, ListItem
import os


def generate_pdf_resume(txt_path: str, pdf_path: str):
    """
    Convert a plain text resume file into a formatted PDF.
    """

    if not os.path.exists(txt_path):
        raise FileNotFoundError(f"Resume text file not found: {txt_path}")

    # Create PDF document
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    elements = []

    styles = getSampleStyleSheet()

    normal_style = styles["Normal"]
    normal_style.fontSize = 11
    normal_style.leading = 14

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontSize=14,
        spaceAfter=10,
        textColor=colors.black,
    )

    # Read text resume
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        if not line:
            elements.append(Spacer(1, 0.2 * inch))
            continue

        # Detect section headings (ALL CAPS)
        if line.isupper():
            elements.append(Paragraph(line, heading_style))
            elements.append(Spacer(1, 0.2 * inch))
        else:
            elements.append(Paragraph(line, normal_style))
            elements.append(Spacer(1, 0.1 * inch))

    # Build PDF
    doc.build(elements)

    print(f"✅ PDF generated successfully at: {pdf_path}")
