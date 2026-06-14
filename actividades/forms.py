from django import forms
from .models import Actividad, HorarioClase, Inscripcion


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'descripcion', 'capacidad_maxima']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 3
            }),
            'capacidad_maxima': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'min': '1'
            }),
        }


class HorarioClaseForm(forms.ModelForm):
    class Meta:
        model = HorarioClase
        fields = ['actividad', 'entrenador', 'dia_semana', 'hora_inicio', 'hora_fin', 'sala']
        widgets = {
            'actividad': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'entrenador': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'dia_semana': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'hora_inicio': forms.TimeInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'time'
            }),
            'hora_fin': forms.TimeInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'time'
            }),
            'sala': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise forms.ValidationError('La hora de fin debe ser posterior a la de inicio')

        return cleaned_data


class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['miembro', 'horario']
        widgets = {
            'miembro': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'horario': forms.Select(attrs={'class': 'select select-bordered w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar miembros activos
        from miembros.models import Miembro
        self.fields['miembro'].queryset = Miembro.objects.filter(activo=True)
