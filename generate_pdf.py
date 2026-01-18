from fpdf import FPDF
from io import BytesIO
import textwrap
import os

def create_pdf(itinerary_text):
    pdf = FPDF(format='A4', unit='mm')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Fonts (ensure DejaVu fonts are in the same folder as this file)
    font_dir = os.path.dirname(__file__)
    pdf.add_font('DejaVu', '', os.path.join(font_dir, 'DejaVuSans.ttf'), uni=True)
    pdf.add_font('DejaVu', 'B', os.path.join(font_dir, 'DejaVuSans-Bold.ttf'), uni=True)

    # Title
    pdf.set_font('DejaVu', 'B', 16)
    pdf.cell(0, 10, "AI Travel Planner - Your Itinerary", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font('DejaVu', '', 12)

    # Wrap the text so very long lines don’t get cut off
    paragraphs = itinerary_text.split("\n\n")
    for para in paragraphs:
        para = para.strip()
        if not para:
            pdf.ln(5)
            continue
        wrapped_lines = textwrap.wrap(para, width=100)
        for line in wrapped_lines:
            pdf.multi_cell(160, 8, line)
        pdf.ln(5)

    # Output PDF to bytes (works on both local and Streamlit Cloud)
    pdf_bytes = pdf.output(dest='S')
    if isinstance(pdf_bytes, str):
        pdf_bytes = pdf_bytes.encode('latin1')  # encode only if it is a string

    pdf_buffer = BytesIO(pdf_bytes)
    pdf_buffer.seek(0)
    return pdf_buffer
