from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from entrenadores.models import Entrenador
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from io import BytesIO
from datetime import date


class Command(BaseCommand):
    help = 'Generate and assign generic certificate to all trainers without one'

    def handle(self, *args, **options):
        # Generate PDF
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)

        # Page size
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
        self.stdout.write(f'✓ PDF guardado: {path}')

        # Assign to all trainers without certificate
        entrenadores = Entrenador.objects.filter(certificado__isnull=True)
        count = 0

        for entrenador in entrenadores:
            entrenador.certificado = path
            entrenador.save()
            count += 1
            self.stdout.write(f'  ✓ {entrenador.nombre} {entrenador.apellido}')

        self.stdout.write(f'\n✓ Certificado asignado a {count} entrenadores')
