from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError


class Miembro(models.Model):
    TIPO_CHOICES = [
        ('REGULAR', 'Regular'),
        ('ESTUDIANTE', 'Estudiante'),
        ('MAYOR', 'Persona Mayor'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='miembro')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    foto = CloudinaryField('foto', folder='miembros', blank=True, null=True)
    tipo_miembro = models.CharField(max_length=20, choices=TIPO_CHOICES, default='REGULAR')
    activo = models.BooleanField(default=True)
    fecha_alta = models.DateField(auto_now_add=True)

    def clean(self):
        if self.foto and self.foto.size > 5 * 1024 * 1024:
            raise ValidationError('La foto no debe exceder 5MB')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Carnet(models.Model):
    miembro = models.OneToOneField(Miembro, on_delete=models.CASCADE, related_name='carnet')
    numero_carnet = models.CharField(max_length=10, unique=True)
    codigo_barras_imagen = CloudinaryField('barcode', folder='carnets')
    fecha_emision = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Carnet {self.numero_carnet}"
