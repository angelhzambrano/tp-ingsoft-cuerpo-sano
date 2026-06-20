from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Entrenador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='entrenador')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    certificado = models.FileField(
        upload_to='certificados/entrenadores/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text='PDF de certificación que acredita al entrenador',
        blank=False,
        null=True
    )
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
