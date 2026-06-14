from django.db import models
from django.contrib.auth.models import User
import json


class AuditLog(models.Model):
    ACCION_CHOICES = [
        ('CREATE', 'Creación'),
        ('UPDATE', 'Actualización'),
        ('DELETE', 'Eliminación'),
    ]

    modelo = models.CharField(max_length=50)  # Ej: 'Miembro', 'Cobro'
    id_objeto = models.IntegerField()  # ID del objeto auditado
    accion = models.CharField(max_length=10, choices=ACCION_CHOICES)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    cambios = models.JSONField(default=dict, blank=True)  # {campo: {anterior: X, nuevo: Y}}
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Auditoría'
        indexes = [
            models.Index(fields=['modelo', 'id_objeto']),
            models.Index(fields=['-timestamp']),
            models.Index(fields=['usuario']),
        ]

    def __str__(self):
        return f"{self.get_accion_display()} {self.modelo}#{self.id_objeto} - {self.timestamp.strftime('%d/%m/%Y %H:%M')}"
