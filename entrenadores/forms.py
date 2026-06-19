from django import forms
from .models import Entrenador, AsistenciaEntrenador


class EntrenadorForm(forms.ModelForm):
    class Meta:
        model = Entrenador
        fields = ['nombre', 'apellido', 'especialidad', 'telefono', 'email', 'certificado', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'apellido': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'especialidad': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'telefono': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'email': forms.EmailInput(attrs={'class': 'input input-bordered w-full'}),
            'certificado': forms.FileInput(attrs={'class': 'file-input file-input-bordered w-full', 'accept': '.pdf'}),
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
