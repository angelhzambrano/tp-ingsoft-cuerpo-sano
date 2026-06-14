from django import forms
from .models import Membresia, TipoMembresia
from miembros.models import Miembro


class MembresiaForm(forms.ModelForm):
    miembro = forms.ModelChoiceField(
        queryset=Miembro.objects.filter(activo=True),
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )

    class Meta:
        model = Membresia
        fields = ['miembro', 'tipo', 'fecha_inicio']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'date'
            }),
        }
