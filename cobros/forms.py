from django import forms
from .models import Cobro
from membresias.models import Membresia


class CobroForm(forms.ModelForm):
    membresia = forms.ModelChoiceField(
        queryset=Membresia.objects.filter(estado='ACTIVA'),
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )

    class Meta:
        model = Cobro
        fields = ['membresia', 'monto_base', 'forma_pago', 'observaciones']
        widgets = {
            'monto_base': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'step': '0.01',
                'min': '0.01'
            }),
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

    def clean_monto_base(self):
        monto = self.cleaned_data.get('monto_base')
        if monto and monto <= 0:
            raise forms.ValidationError('El monto debe ser mayor a 0')
        return monto
