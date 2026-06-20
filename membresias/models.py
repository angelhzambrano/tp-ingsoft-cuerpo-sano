from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from datetime import timedelta
from miembros.models import Miembro


class TipoMembresia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    duracion_dias = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Tipos de membresía'


class Membresia(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVA', 'Activa'),
        ('VENCIDA', 'Vencida'),
        ('CANCELADA', 'Cancelada')
    ]

    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE, related_name='membresias')
    tipo = models.ForeignKey(TipoMembresia, on_delete=models.PROTECT)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVA')

    def save(self, *args, **kwargs):
        if not self.fecha_fin:
            self.fecha_fin = self.fecha_inicio + timedelta(days=self.tipo.duracion_dias)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo.nombre}"

    class Meta:
        verbose_name_plural = 'Membresías'
