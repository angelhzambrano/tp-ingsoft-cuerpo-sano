from django import forms
from .models import Cobro
from membresias.models import Membresia


class CobroForm(forms.ModelForm):
    membresia = forms.ModelChoiceField(
        queryset=Membresia.objects.filter(estado='ACTIVA'),
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'}),
        help_text='Se cobrará automáticamente el precio de la membresía seleccionada'
    )

    monto_base = forms.DecimalField(
        disabled=True,
        widget=forms.NumberInput(attrs={
            'class': 'input input-bordered w-full',
            'readonly': True
        }),
        help_text='Se calcula automáticamente del precio de la membresía'
    )

    class Meta:
        model = Cobro
        fields = ['membresia', 'monto_base', 'forma_pago', 'observaciones']
        widgets = {
            'forma_pago': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'observaciones': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar membresías activas
        self.fields['membresia'].queryset = Membresia.objects.filter(
            estado='ACTIVA'
        ).select_related('miembro', 'tipo')
