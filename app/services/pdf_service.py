from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io
from datetime import datetime


def generate_pdf(pa_data: dict) -> bytes:
    """
    Generates Prior Authorization PDF.
    REQUIREMENT: pa_data["status"] must be APPROVED
    """

    # Safety check (Human-in-the-loop enforcement)
    if pa_data.get("status") != "APPROVED":
        raise ValueError("PDF can only be generated for APPROVED requests")

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=LETTER)
    width, height = LETTER

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, height - 50, "Prior Authorization Request")

    # Metadata header
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, height - 75, f"PA ID: {pa_data.get('id', 'N/A')}")
    pdf.drawString(300, height - 75, f"Date: {datetime.utcnow().strftime('%Y-%m-%d')}")
    pdf.drawString(50, height - 90, f"Approved By: {pa_data.get('approved_by', 'Reviewer')}")

    # Divider
    pdf.line(50, height - 100, width - 50, height - 100)

    y = height - 130
    pdf.setFont("Helvetica", 11)

    #  Main content
    fields_to_render = [
        "diagnosis",
        "procedure",
        "medical_necessity",
        "clinical_note"
    ]

    for field in fields_to_render:
        value = pa_data.get(field)
        if not value:
            continue

        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(50, y, field.replace("_", " ").title())
        y -= 14

        pdf.setFont("Helvetica", 11)
        text = pdf.beginText(70, y)
        for line in value.split("\n"):
            text.textLine(line)
            y -= 14

            # Page break protection
            if y < 100:
                pdf.drawText(text)
                pdf.showPage()
                pdf.setFont("Helvetica", 11)
                y = height - 80
                text = pdf.beginText(70, y)

        pdf.drawText(text)
        y -= 20

    #  Legal disclaimer (healthcare-safe)
    pdf.setFont("Helvetica-Oblique", 9)
    pdf.line(50, 110, width - 50, 110)
    pdf.drawString(
        50,
        90,
        "Disclaimer: This document was generated using AI assistance and reviewed by a licensed professional."
    )
    pdf.drawString(
        50,
        75,
        "Final authorization decisions rest with the payer."
    )

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer.read()
