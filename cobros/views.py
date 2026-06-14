from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Cobro, Comprobante
from .forms import CobroForm
from membresias.models import Membresia


def calcular_descuento(miembro):
    """Calcula descuento según tipo de miembro"""
    descuentos = {
        'ESTUDIANTE': Decimal('20.00'),
        'MAYOR': Decimal('15.00'),
        'REGULAR': Decimal('0.00'),
    }
    return descuentos.get(miembro.tipo_miembro, Decimal('0.00'))


@login_required
def lista_cobros(request):
    """Listado de cobros con filtros"""
    cobros = Cobro.objects.select_related('miembro', 'membresia', 'membresia__tipo').order_by('-fecha')

    # Filtro por forma de pago
    forma_pago = request.GET.get('forma_pago')
    if forma_pago:
        cobros = cobros.filter(forma_pago=forma_pago)

    context = {
        'cobros': cobros,
        'total': cobros.count(),
        'forma_pago_selected': forma_pago,
    }
    return render(request, 'cobros/lista.html', context)


@login_required
def registrar_cobro(request):
    """Registrar nuevo cobro con cálculo automático de descuento"""
    if request.method == 'POST':
        form = CobroForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                membresia = form.cleaned_data['membresia']
                monto_base = form.cleaned_data['monto_base']

                # Calcular descuento
                descuento_porcentaje = calcular_descuento(membresia.miembro)
                descuento_monto = monto_base * (descuento_porcentaje / Decimal('100'))
                monto_final = monto_base - descuento_monto

                # Crear cobro
                cobro = Cobro(
                    miembro=membresia.miembro,
                    membresia=membresia,
                    monto_base=monto_base,
                    descuento_porcentaje=descuento_porcentaje,
                    monto_final=monto_final,
                    forma_pago=form.cleaned_data['forma_pago'],
                    observaciones=form.cleaned_data.get('observaciones', '')
                )
                cobro.save()

                # Crear comprobante automáticamente
                Comprobante.objects.create(cobro=cobro)

                messages.success(
                    request,
                    f'Cobro registrado: ${monto_final} (descuento {descuento_porcentaje}%)'
                )
                return redirect('cobros:comprobante', pk=cobro.pk)
    else:
        form = CobroForm()

    context = {'form': form}
    return render(request, 'cobros/form.html', context)


@login_required
def detalle_cobro(request, pk):
    """Detalle de un cobro"""
    cobro = get_object_or_404(Cobro, pk=pk)
    comprobante = cobro.comprobante if hasattr(cobro, 'comprobante') else None
    context = {
        'cobro': cobro,
        'comprobante': comprobante,
    }
    return render(request, 'cobros/detalle.html', context)


@login_required
def ver_comprobante(request, pk):
    """Comprobante printable"""
    cobro = get_object_or_404(Cobro, pk=pk)
    comprobante = get_object_or_404(Comprobante, cobro=cobro)
    context = {
        'cobro': cobro,
        'comprobante': comprobante,
    }
    return render(request, 'cobros/print.html', context)
