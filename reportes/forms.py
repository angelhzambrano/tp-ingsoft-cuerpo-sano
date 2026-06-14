from django import forms
from miembros.models import Miembro
from datetime import date, timedelta


class FiltroAsistenciasForm(forms.Form):
    fecha_inicio = forms.DateField(
        required=False,
        initial=date.today() - timedelta(days=30),
        widget=forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'})
    )
    fecha_fin = forms.DateField(
        required=False,
        initial=date.today(),
        widget=forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'})
    )
    miembro = forms.ModelChoiceField(
        queryset=Miembro.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )
    metodo = forms.ChoiceField(
        required=False,
        choices=[('', '-- Todos --'), ('BARCODE', 'Por Código'), ('MANUAL', 'Manual')],
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )


class FiltroCobrosForm(forms.Form):
    fecha_inicio = forms.DateField(
        required=False,
        initial=date.today() - timedelta(days=30),
        widget=forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'})
    )
    fecha_fin = forms.DateField(
        required=False,
        initial=date.today(),
        widget=forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'})
    )
    forma_pago = forms.ChoiceField(
        required=False,
        choices=[
            ('', '-- Todas --'),
            ('EFECTIVO', 'Efectivo'),
            ('TRANSFERENCIA', 'Transferencia'),
            ('TARJETA', 'Tarjeta')
        ],
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )
    miembro = forms.ModelChoiceField(
        queryset=Miembro.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )


class FiltroMembresiasVencidasForm(forms.Form):
    fecha_vencimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'})
    )
    tipo_miembro = forms.ChoiceField(
        required=False,
        choices=[('', '-- Todos --'), ('ESTUDIANTE', 'Estudiante'), ('MAYOR', 'Mayor'), ('REGULAR', 'Regular')],
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )
