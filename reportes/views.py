from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Sum, Count
from datetime import date, timedelta
from asistencia.models import Asistencia
from cobros.models import Cobro
from membresias.models import Membresia
from .forms import FiltroAsistenciasForm, FiltroCobrosForm, FiltroMembresiasVencidasForm


@login_required
@require_http_methods(["GET", "POST"])
def reporte_asistencias(request):
    form = FiltroAsistenciasForm(request.GET or None)
    asistencias = Asistencia.objects.all().order_by('-fecha', '-hora')

    if form.is_valid():
        if form.cleaned_data.get('fecha_inicio'):
            asistencias = asistencias.filter(fecha__gte=form.cleaned_data['fecha_inicio'])
        if form.cleaned_data.get('fecha_fin'):
            asistencias = asistencias.filter(fecha__lte=form.cleaned_data['fecha_fin'])
        if form.cleaned_data.get('miembro'):
            asistencias = asistencias.filter(miembro=form.cleaned_data['miembro'])
        if form.cleaned_data.get('metodo'):
            asistencias = asistencias.filter(metodo=form.cleaned_data['metodo'])

    stats = {
        'total': asistencias.count(),
        'por_metodo': {
            'BARCODE': asistencias.filter(metodo='BARCODE').count(),
            'MANUAL': asistencias.filter(metodo='MANUAL').count(),
        },
        'miembros_unicos': asistencias.values('miembro').distinct().count(),
    }

    return render(request, 'reportes/asistencias.html', {
        'form': form,
        'asistencias': asistencias,
        'stats': stats
    })


@login_required
@require_http_methods(["GET", "POST"])
def reporte_cobros(request):
    form = FiltroCobrosForm(request.GET or None)
    cobros = Cobro.objects.all().order_by('-fecha_cobro')

    if form.is_valid():
        if form.cleaned_data.get('fecha_inicio'):
            cobros = cobros.filter(fecha_cobro__gte=form.cleaned_data['fecha_inicio'])
        if form.cleaned_data.get('fecha_fin'):
            cobros = cobros.filter(fecha_cobro__lte=form.cleaned_data['fecha_fin'])
        if form.cleaned_data.get('forma_pago'):
            cobros = cobros.filter(forma_pago=form.cleaned_data['forma_pago'])
        if form.cleaned_data.get('miembro'):
            cobros = cobros.filter(miembro=form.cleaned_data['miembro'])

    stats = {
        'total_cobros': cobros.count(),
        'monto_total': cobros.aggregate(Sum('monto_final'))['monto_final__sum'] or 0,
        'descuento_total': cobros.aggregate(Sum('descuento_monto'))['descuento_monto__sum'] or 0,
        'por_forma': {
            'EFECTIVO': cobros.filter(forma_pago='EFECTIVO').count(),
            'TRANSFERENCIA': cobros.filter(forma_pago='TRANSFERENCIA').count(),
            'TARJETA': cobros.filter(forma_pago='TARJETA').count(),
        },
    }

    return render(request, 'reportes/cobros.html', {
        'form': form,
        'cobros': cobros,
        'stats': stats
    })


@login_required
@require_http_methods(["GET", "POST"])
def membresias_vencidas(request):
    form = FiltroMembresiasVencidasForm(request.GET or None)
    membresias = Membresia.objects.filter(estado='VENCIDA').order_by('-fecha_fin')

    if form.is_valid():
        if form.cleaned_data.get('fecha_vencimiento'):
            membresias = membresias.filter(fecha_fin=form.cleaned_data['fecha_vencimiento'])
        if form.cleaned_data.get('tipo_miembro'):
            membresias = membresias.filter(miembro__tipo_miembro=form.cleaned_data['tipo_miembro'])

    stats = {
        'total_vencidas': membresias.count(),
        'monto_total_no_renovado': membresias.aggregate(
            total=Sum('tipo__precio')
        )['total'] or 0,
        'por_tipo_miembro': dict(
            membresias.values('miembro__tipo_miembro')
            .annotate(count=Count('id'))
            .values_list('miembro__tipo_miembro', 'count')
        ),
        'dias_promedio_sin_renovar': (date.today() - membresias.aggregate(
            fecha_promedio=Sum('fecha_fin')
        )['fecha_promedio']).days if membresias.exists() else 0,
    }

    return render(request, 'reportes/membresias_vencidas.html', {
        'form': form,
        'membresias': membresias,
        'stats': stats
    })
