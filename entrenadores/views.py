from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.http import HttpResponseForbidden
from django.contrib import messages
from datetime import date
import logging
from .models import Entrenador, AsistenciaEntrenador
from .forms import EntrenadorForm, AsistenciaEntrenadorForm
from actividades.models import HorarioClase

logger = logging.getLogger(__name__)


def _puede_ver_entrenadores(user):
    """Solo Admin puede ver lista de entrenadores"""
    return user.groups.filter(name='Admin').exists()


def _puede_crear_entrenador(user):
    """Solo Admin puede crear entrenadores"""
    return user.groups.filter(name='Admin').exists()


@login_required
def lista_entrenadores(request):
    if not _puede_ver_entrenadores(request.user):
        return HttpResponseForbidden('No tienes permiso para ver esta página')

    entrenadores = Entrenador.objects.all().order_by('-activo', 'apellido')
    return render(request, 'entrenadores/lista.html', {'entrenadores': entrenadores})


@login_required
@require_http_methods(["GET", "POST"])
def crear_entrenador(request):
    if not _puede_crear_entrenador(request.user):
        return HttpResponseForbidden('No tienes permiso para crear entrenadores')

    if request.method == 'POST':
        form = EntrenadorForm(request.POST, request.FILES)

        # Debug: loguear archivos recibidos
        if 'certificado' in request.FILES:
            file = request.FILES['certificado']
            logger.info(f"PDF cargado: {file.name} ({file.size} bytes)")
        else:
            logger.warning("No se recibió certificado PDF")

        if form.is_valid():
            try:
                entrenador = form.save()
                messages.success(request, f'Entrenador {entrenador} creado exitosamente')
                return redirect('entrenadores:detalle', pk=entrenador.pk)
            except Exception as e:
                logger.error(f"Error al guardar entrenador: {type(e).__name__}: {e}")
                messages.error(request, f'Error al crear entrenador: {str(e)}')
        else:
            # Loguear errores del formulario
            logger.warning(f"Errores del formulario: {form.errors}")
            for field, errors in form.errors.items():
                messages.error(request, f"{field}: {', '.join(errors)}")
    else:
        form = EntrenadorForm()
    return render(request, 'entrenadores/form.html', {'form': form, 'title': 'Crear Entrenador'})


@login_required
def detalle_entrenador(request, pk):
    entrenador = get_object_or_404(Entrenador, pk=pk)
    asistencias = entrenador.asistencias.all().order_by('-fecha')
    return render(request, 'entrenadores/detalle.html', {
        'entrenador': entrenador,
        'asistencias': asistencias
    })


@login_required
@require_http_methods(["GET", "POST"])
def editar_entrenador(request, pk):
    entrenador = get_object_or_404(Entrenador, pk=pk)
    if request.method == 'POST':
        form = EntrenadorForm(request.POST, request.FILES, instance=entrenador)
        if form.is_valid():
            form.save()
            return redirect('entrenadores:detalle', pk=entrenador.pk)
    else:
        form = EntrenadorForm(instance=entrenador)
    return render(request, 'entrenadores/form.html', {
        'form': form,
        'title': 'Editar Entrenador',
        'entrenador': entrenador
    })


@login_required
@require_http_methods(["GET"])
def print_entrenador(request, pk):
    entrenador = get_object_or_404(Entrenador, pk=pk)
    asistencias = entrenador.asistencias.all().order_by('-fecha')
    stats = {
        'total': asistencias.count(),
        'presentes': asistencias.filter(tipo='PRESENTE').count(),
        'ausentes': asistencias.filter(tipo='AUSENTE').count(),
        'justificadas': asistencias.filter(justificada=True).count(),
    }
    return render(request, 'entrenadores/print.html', {
        'entrenador': entrenador,
        'asistencias': asistencias,
        'stats': stats
    })


@login_required
@require_http_methods(["GET", "POST"])
def registro_asistencia_entrenador(request):
    if request.method == 'POST':
        form = AsistenciaEntrenadorForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            return redirect('entrenadores:lista')
    else:
        form = AsistenciaEntrenadorForm()
    return render(request, 'entrenadores/form_asistencia.html', {
        'form': form,
        'title': 'Registrar Asistencia de Entrenador'
    })


@login_required
def mi_asistencia_entrenador(request):
    """Vista personal de asistencia del entrenador logueado"""
    try:
        entrenador = Entrenador.objects.get(email=request.user.email)
    except Entrenador.DoesNotExist:
        return render(request, 'entrenadores/sin_asignacion.html', {
            'mensaje': 'No estás registrado como entrenador en el sistema'
        })

    asistencias = entrenador.asistencias.all().order_by('-fecha')

    stats = {
        'total': asistencias.count(),
        'presentes': asistencias.filter(tipo='PRESENTE').count(),
        'ausentes': asistencias.filter(tipo='AUSENTE').count(),
        'justificadas': asistencias.filter(justificada=True).count(),
    }

    return render(request, 'entrenadores/mi_asistencia.html', {
        'entrenador': entrenador,
        'asistencias': asistencias,
        'stats': stats
    })


@login_required
def historial_asistencias_entrenador(request, pk):
    entrenador = get_object_or_404(Entrenador, pk=pk)
    asistencias = entrenador.asistencias.all().order_by('-fecha')

    stats = {
        'total': asistencias.count(),
        'presentes': asistencias.filter(tipo='PRESENTE').count(),
        'ausentes': asistencias.filter(tipo='AUSENTE').count(),
        'justificadas': asistencias.filter(justificada=True).count(),
    }

    return render(request, 'entrenadores/historial_asistencias.html', {
        'entrenador': entrenador,
        'asistencias': asistencias,
        'stats': stats
    })
