from django.db import migrations
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from io import BytesIO
from datetime import date


def generate_and_assign_certificates(apps, schema_editor):
    Entrenador = apps.get_model('entrenadores', 'Entrenador')

    # Generate PDF
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width / 2, height - 1.5 * inch, "CERTIFICADO")

    # Subtitle
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2, height - 2.2 * inch, "de Entrenador")

    # Decorative line
    c.setLineWidth(2)
    c.line(1.5 * inch, height - 2.5 * inch, width - 1.5 * inch, height - 2.5 * inch)

    # Body text
    c.setFont("Helvetica", 12)
    text_y = height - 3.5 * inch
    c.drawCentredString(width / 2, text_y, "Este certificado acredita que el portador")
    c.drawCentredString(width / 2, text_y - 0.3 * inch, "está autorizado para impartir clases de fitness")
    c.drawCentredString(width / 2, text_y - 0.6 * inch, "en Cuerpo Sano.")

    # Date
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - 6 * inch, f"Emitido: {date.today().strftime('%d/%m/%Y')}")

    # Gym name
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, 1 * inch, "Cuerpo Sano")

    c.save()
    pdf_buffer.seek(0)

    # Save to storage
    filename = 'certificado_generico_entrenador.pdf'
    file_path = f'certificados/entrenadores/{filename}'

    path = default_storage.save(file_path, ContentFile(pdf_buffer.read()))

    # Assign to all trainers without certificate
    entrenadores = Entrenador.objects.filter(certificado__isnull=True)
    for entrenador in entrenadores:
        entrenador.certificado = path
        entrenador.save()


def reverse_certificates(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('entrenadores', '0004_delete_asistenciaentrenador'),
    ]

    operations = [
        migrations.RunPython(generate_and_assign_certificates, reverse_certificates),
    ]
