from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


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
    foto = models.ImageField(
        upload_to='miembros/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        help_text='Máximo 5MB. Formatos: JPG, PNG, GIF'
    )
    tipo_miembro = models.CharField(max_length=20, choices=TIPO_CHOICES, default='REGULAR')
    activo = models.BooleanField(default=True)
    fecha_alta = models.DateField(auto_now_add=True)
    membresia_activa = models.ForeignKey(
        'membresias.Membresia',
        on_delete=models.PROTECT,
        related_name='miembro_activo',
        help_text='Membresía activa del miembro - requerida para registrar cobros'
    )

    def clean(self):
        if self.foto:
            # Validar tamaño máximo
            max_size = 5 * 1024 * 1024  # 5MB
            if self.foto.size > max_size:
                raise ValidationError(f'La foto no debe exceder 5MB (actual: {self.foto.size / 1024 / 1024:.1f}MB)')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Carnet(models.Model):
    miembro = models.OneToOneField(Miembro, on_delete=models.CASCADE, related_name='carnet')
    numero_carnet = models.CharField(max_length=10, unique=True)
    codigo_barras_imagen = models.ImageField(upload_to='carnets/', help_text='Código de barras generado automáticamente')
    fecha_emision = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Carnet {self.numero_carnet}"
