from django import forms
from django.core.exceptions import ValidationError
from .models import Entrenador, AsistenciaEntrenador


def validar_pdf(file):
    """Validador personalizado para PDFs"""
    if not file:
        raise ValidationError('Por favor carga un archivo PDF.')

    # Verificar extensión
    if not file.name.lower().endswith('.pdf'):
        raise ValidationError(f'El archivo debe ser PDF. Recibido: {file.name}')

    # Verificar tamaño (máximo 50MB)
    if file.size > 50 * 1024 * 1024:
        raise ValidationError('El PDF no debe exceder 50MB.')

    # Verificar que empiece con PDF magic number
    file.seek(0)
    header = file.read(4)
    if not header.startswith(b'%PDF'):
        raise ValidationError('El archivo no es un PDF válido (no tiene encabezado PDF correcto).')

    file.seek(0)  # Resetear posición para que Django lo pueda leer


class EntrenadorForm(forms.ModelForm):
    certificado = forms.FileField(
        required=True,
        validators=[validar_pdf],
        widget=forms.FileInput(attrs={
            'class': 'file-input file-input-bordered w-full',
            'accept': '.pdf'
        }),
        help_text='PDF válido, máximo 50MB'
    )

    class Meta:
        model = Entrenador
        fields = ['nombre', 'apellido', 'especialidad', 'telefono', 'email', 'certificado', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'apellido': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'especialidad': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'telefono': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'email': forms.EmailInput(attrs={'class': 'input input-bordered w-full'}),
            'activo': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }


class AsistenciaEntrenadorForm(forms.ModelForm):
    class Meta:
        model = AsistenciaEntrenador
        fields = ['entrenador', 'horario', 'fecha', 'tipo', 'justificada', 'observaciones']
        widgets = {
            'entrenador': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'horario': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'fecha': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
            'tipo': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'justificada': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'observaciones': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3}),
        }
