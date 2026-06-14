from django.db import models
from miembros.models import Miembro


class Asistencia(models.Model):
    METODO_CHOICES = [
        ('BARCODE', 'Código de barras'),
        ('MANUAL', 'Manual')
    ]

    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE, related_name='asistencias')
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    metodo = models.CharField(max_length=10, choices=METODO_CHOICES, default='BARCODE')

    def __str__(self):
        return f"Asistencia {self.miembro} - {self.fecha} {self.hora}"

    class Meta:
        verbose_name_plural = 'Asistencias'
