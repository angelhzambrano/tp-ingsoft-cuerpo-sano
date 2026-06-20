from django import forms
from .models import Cobro
from miembros.models import Miembro


class CobroForm(forms.ModelForm):
    miembro = forms.ModelChoiceField(
        queryset=Miembro.objects.filter(activo=True),
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'}),
        help_text='Selecciona el miembro para cobrar'
    )

    monto_base = forms.DecimalField(
        disabled=True,
        widget=forms.NumberInput(attrs={
            'class': 'input input-bordered w-full',
            'readonly': True
        }),
        help_text='Se calcula automáticamente del tipo de membresía del miembro'
    )

    class Meta:
        model = Cobro
        fields = ['miembro', 'monto_base', 'forma_pago', 'observaciones']
        exclude = ['membresia']
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
