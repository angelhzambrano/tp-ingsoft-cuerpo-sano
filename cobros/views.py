from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db import transaction
from .models import Cobro, Comprobante
from .forms import CobroForm
from membresias.models import Membresia


def require_admin_or_recepcion(view_func):
    """Decorador que requiere ser Admin o Recepción"""
    def wrapper(request, *args, **kwargs):
        is_admin = request.user.groups.filter(name='Admin').exists()
        is_recepcion = request.user.groups.filter(name='Recepcion').exists()
        if not (is_admin or is_recepcion):
            return HttpResponseForbidden('No tienes permiso para acceder a esta página')
        return view_func(request, *args, **kwargs)
    return wrapper


def calcular_descuento(miembro):
    """Calcula descuento según tipo de miembro"""
    descuentos = {
        'ESTUDIANTE': Decimal('20.00'),
        'MAYOR': Decimal('15.00'),
        'REGULAR': Decimal('0.00'),
    }
    return descuentos.get(miembro.tipo_miembro, Decimal('0.00'))


@login_required
@require_admin_or_recepcion
def lista_cobros(request):
    """Listado de cobros con filtros - Admin y Recepción"""
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
@require_admin_or_recepcion
def registrar_cobro(request):
    """Registrar nuevo cobro - Admin y Recepción"""
    if request.method == 'POST':
        form = CobroForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                membresia = form.cleaned_data['membresia']
                miembro = membresia.miembro

                # Validar que miembro tenga membresía asignada
                if not miembro.membresia_activa:
                    messages.error(
                        request,
                        f'El miembro {miembro} no tiene membresía asignada. Asignale una membresía antes de registrar cobros.'
                    )
                    return redirect('cobros:registrar')

                # Usar automáticamente el precio de la membresía
                monto_base = membresia.tipo.precio

                # Calcular descuento
                descuento_porcentaje = calcular_descuento(miembro)
                descuento_monto = monto_base * (descuento_porcentaje / Decimal('100'))
                monto_final = monto_base - descuento_monto

                # Crear cobro
                cobro = Cobro(
                    miembro=miembro,
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
@require_admin_or_recepcion
def detalle_cobro(request, pk):
    """Detalle de un cobro - Admin y Recepción"""
    cobro = get_object_or_404(Cobro, pk=pk)
    comprobante = cobro.comprobante if hasattr(cobro, 'comprobante') else None
    context = {
        'cobro': cobro,
        'comprobante': comprobante,
    }
    return render(request, 'cobros/detalle.html', context)


@login_required
@require_admin_or_recepcion
def ver_comprobante(request, pk):
    """Comprobante printable - Admin y Recepción"""
    cobro = get_object_or_404(Cobro, pk=pk)
    comprobante = get_object_or_404(Comprobante, cobro=cobro)
    context = {
        'cobro': cobro,
        'comprobante': comprobante,
    }
    return render(request, 'cobros/print.html', context)
