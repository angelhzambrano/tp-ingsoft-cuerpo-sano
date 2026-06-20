from django import forms
from .models import Entrenador


class EntrenadorForm(forms.ModelForm):
    certificado = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'file-input file-input-bordered w-full',
            'accept': '.pdf'
        }),
        help_text='Archivo PDF obligatorio'
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
