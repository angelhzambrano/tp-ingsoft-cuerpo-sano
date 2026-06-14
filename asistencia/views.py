import json
from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from miembros.models import Carnet, Miembro
from membresias.models import Membresia
from .models import Asistencia


@login_required
def registro_asistencia(request):
    """Página de registro de asistencia por código de barras con barcode.js"""
    context = {}
    return render(request, 'asistencia/registro.html', context)


@login_required
@require_http_methods(["POST"])
def registrar_por_barcode(request):
    """AJAX endpoint para procesar escaneo de código de barras"""
    try:
        data = json.loads(request.body)
        numero_carnet = data.get('numero_carnet', '').strip()

        if not numero_carnet:
            return JsonResponse({'success': False, 'error': 'Código de barras vacío'})

        # Buscar el carnet
        carnet = get_object_or_404(Carnet, numero_carnet=numero_carnet)
        miembro = carnet.miembro

        # Validar que miembro esté activo
        if not miembro.activo:
            return JsonResponse({'success': False, 'error': f'Miembro {miembro} inactivo'})

        # Validar que tenga membresía activa
        membresia = Membresia.objects.filter(
            miembro=miembro,
            estado='ACTIVA'
        ).first()

        if not membresia:
            return JsonResponse({'success': False, 'error': f'Membresía vencida o inexistente para {miembro}'})

        # Crear asistencia
        with transaction.atomic():
            asistencia = Asistencia.objects.create(
                miembro=miembro,
                metodo='BARCODE'
            )

        return JsonResponse({
            'success': True,
            'message': f'✓ {miembro} registrado exitosamente',
            'miembro': str(miembro),
            'tipo_miembro': miembro.get_tipo_miembro_display()
        })

    except Carnet.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Código de barras no encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Error: {str(e)}'})


@login_required
def listado_asistencia(request):
    """Listado de asistencias con filtros por fecha"""
    fecha_inicio = request.GET.get('fecha_inicio', str(date.today()))
    fecha_fin = request.GET.get('fecha_fin', str(date.today()))

    try:
        fecha_inicio = date.fromisoformat(fecha_inicio)
        fecha_fin = date.fromisoformat(fecha_fin)
    except ValueError:
        fecha_inicio = date.today()
        fecha_fin = date.today()

    asistencias = Asistencia.objects.filter(
        fecha__gte=fecha_inicio,
        fecha__lte=fecha_fin
    ).select_related('miembro').order_by('-fecha', '-hora')

    context = {
        'asistencias': asistencias,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'total': asistencias.count(),
    }
    return render(request, 'asistencia/lista.html', context)


@login_required
def registro_manual(request):
    """Registro manual de asistencia"""
    if request.method == 'POST':
        miembro_id = request.POST.get('miembro_id')
        miembro = get_object_or_404(Miembro, pk=miembro_id)

        # Validar membresía activa
        membresia = Membresia.objects.filter(
            miembro=miembro,
            estado='ACTIVA'
        ).first()

        if not membresia:
            messages.error(request, f'Membresía vencida o inexistente para {miembro}')
            return render(request, 'asistencia/registro_manual.html')

        # Crear asistencia
        with transaction.atomic():
            asistencia = Asistencia.objects.create(
                miembro=miembro,
                metodo='MANUAL'
            )
            messages.success(request, f'Asistencia de {miembro} registrada exitosamente')

    miembros = Miembro.objects.filter(activo=True)
    context = {'miembros': miembros}
    return render(request, 'asistencia/registro_manual.html', context)
