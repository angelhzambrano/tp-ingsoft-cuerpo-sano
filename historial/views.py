from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from miembros.models import Miembro
from cobros.models import Cobro
from .models import AuditLog


@login_required
def lista_auditlog(request):
    logs = AuditLog.objects.all().order_by('-timestamp')

    filtro_modelo = request.GET.get('modelo', '')
    filtro_accion = request.GET.get('accion', '')

    if filtro_modelo:
        logs = logs.filter(modelo=filtro_modelo)
    if filtro_accion:
        logs = logs.filter(accion=filtro_accion)

    modelos_unicos = AuditLog.objects.values_list('modelo', flat=True).distinct()

    return render(request, 'historial/auditlog.html', {
        'logs': logs,
        'modelos': modelos_unicos,
        'filtro_modelo': filtro_modelo,
        'filtro_accion': filtro_accion,
    })


@login_required
def auditlog_miembro(request, miembro_id):
    miembro = get_object_or_404(Miembro, pk=miembro_id)
    logs = AuditLog.objects.filter(modelo='Miembro', id_objeto=miembro_id).order_by('-timestamp')

    return render(request, 'historial/auditlog_detalle.html', {
        'objeto': miembro,
        'logs': logs,
        'tipo': 'Miembro'
    })


@login_required
def auditlog_cobro(request, cobro_id):
    cobro = get_object_or_404(Cobro, pk=cobro_id)
    logs = AuditLog.objects.filter(modelo='Cobro', id_objeto=cobro_id).order_by('-timestamp')

    return render(request, 'historial/auditlog_detalle.html', {
        'objeto': cobro,
        'logs': logs,
        'tipo': 'Cobro'
    })
