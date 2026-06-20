from django import forms
from .models import Cobro
from miembros.models import Miembro


class CobroForm(forms.ModelForm):
    miembro = forms.ModelChoiceField(
        queryset=Miembro.objects.filter(activo=True),
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'}),
        help_text='Selecciona el miembro para cobrar su membresía activa'
    )

    class Meta:
        model = Cobro
        fields = ['miembro', 'forma_pago', 'observaciones']
        exclude = ['membresia', 'monto_base', 'descuento_porcentaje', 'monto_final']
        widgets = {
            'forma_pago': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'observaciones': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar solo miembros activos
        self.fields['miembro'].queryset = Miembro.objects.filter(
            activo=True
        ).select_related('tipo_membresia_activa')
