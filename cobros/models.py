from django.db import models
from miembros.models import Miembro
from membresias.models import Membresia


class Cobro(models.Model):
    FORMA_PAGO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia'),
    ]

    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE, related_name='cobros')
    membresia = models.ForeignKey(Membresia, on_delete=models.CASCADE)
    monto_base = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    monto_final = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pago = models.CharField(max_length=20, choices=FORMA_PAGO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Cobro {self.miembro} - {self.fecha.date()}"

    class Meta:
        verbose_name_plural = 'Cobros'


class Comprobante(models.Model):
    cobro = models.OneToOneField(Cobro, on_delete=models.CASCADE, related_name='comprobante')
    numero = models.AutoField(primary_key=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comprobante #{self.numero}"

    class Meta:
        verbose_name_plural = 'Comprobantes'
