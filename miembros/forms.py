from django import forms
from django.core.exceptions import ValidationError
from .models import Miembro
from membresias.models import Membresia


class MiembroForm(forms.ModelForm):
    membresia_activa = forms.ModelChoiceField(
        queryset=Membresia.objects.filter(estado='ACTIVA'),
        required=True,
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'}),
        help_text='Membresía activa asignada al miembro - requerida para registrar cobros'
    )

    class Meta:
        model = Miembro
        fields = ['nombre', 'apellido', 'dni', 'email', 'telefono', 'foto', 'tipo_miembro', 'membresia_activa', 'activo']
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

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if dni:
            # Verificar que el DNI sea único, pero permitir el mismo DNI en edición
            existing = Miembro.objects.filter(dni=dni).exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError('Este DNI ya existe en el sistema.')
        return dni
