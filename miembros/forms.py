from django import forms
from .models import Miembro


class MiembroForm(forms.ModelForm):
    class Meta:
        model = Miembro
        fields = ['nombre', 'apellido', 'dni', 'email', 'telefono', 'foto', 'tipo_miembro', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'apellido': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'dni': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'email': forms.EmailInput(attrs={'class': 'input input-bordered w-full'}),
            'telefono': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'foto': forms.FileInput(attrs={'class': 'file-input file-input-bordered w-full', 'accept': 'image/*'}),
            'tipo_miembro': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'activo': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }
