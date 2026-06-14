from django.db import models


class Entrenador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class AsistenciaEntrenador(models.Model):
    TIPO_CHOICES = [
        ('PRESENTE', 'Presente'),
        ('AUSENTE', 'Ausente')
    ]

    entrenador = models.ForeignKey(Entrenador, on_delete=models.CASCADE, related_name='asistencias')
    horario = models.ForeignKey('actividades.HorarioClase', on_delete=models.CASCADE)
    fecha = models.DateField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    justificada = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.entrenador} - {self.fecha} ({self.tipo})"

    class Meta:
        unique_together = ('entrenador', 'horario', 'fecha')
        verbose_name_plural = 'Asistencias de entrenadores'
