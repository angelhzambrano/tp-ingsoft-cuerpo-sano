from django.db import models
from django.core.exceptions import ValidationError
from miembros.models import Miembro


class Actividad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    capacidad_maxima = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Actividades'


class HorarioClase(models.Model):
    DIA_CHOICES = [
        ('LUN', 'Lunes'),
        ('MAR', 'Martes'),
        ('MIE', 'Miércoles'),
        ('JUE', 'Jueves'),
        ('VIE', 'Viernes'),
        ('SAB', 'Sábado'),
    ]

    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name='horarios')
    entrenador = models.ForeignKey(
        'entrenadores.Entrenador',
        on_delete=models.SET_NULL,
        null=True,
        related_name='clases'
    )
    dia_semana = models.CharField(max_length=3, choices=DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    sala = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.actividad} - {self.get_dia_semana_display()} {self.hora_inicio}"

    class Meta:
        verbose_name_plural = 'Horarios de clase'


class Inscripcion(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVA', 'Activa'),
        ('CANCELADA', 'Cancelada')
    ]

    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE, related_name='inscripciones')
    horario = models.ForeignKey(HorarioClase, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVA')

    def save(self, *args, **kwargs):
        inscripciones_activas = self.horario.inscripciones.filter(estado='ACTIVA').count()
        if self.pk is None and inscripciones_activas >= self.horario.actividad.capacidad_maxima:
            raise ValidationError('La clase está llena')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.miembro} - {self.horario.actividad}"

    class Meta:
        unique_together = ('miembro', 'horario')
        verbose_name_plural = 'Inscripciones'
