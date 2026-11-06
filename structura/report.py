from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def build_pdf(name, model, result):
    output = BytesIO()
    pdf = canvas.Canvas(output, pagesize=A4)
    pdf.setTitle(name)
    pdf.drawString(72, 780, f"Structura - {name}")
    pdf.drawString(72, 755, "Laporan analisis portal 2D")
    pdf.drawString(72, 730, f"Jumlah node: {len(model.get('nodes', []))}")
    pdf.drawString(72, 710, f"Jumlah elemen: {len(model.get('members', []))}")
    pdf.save()
    return output.getvalue()
