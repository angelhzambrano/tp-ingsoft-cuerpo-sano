from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Actividad, HorarioClase, Inscripcion
from .forms import ActividadForm, HorarioClaseForm, InscripcionForm


def require_group(group_name):
    """Decorador para requerir pertenencia a un grupo"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.groups.filter(name=group_name).exists():
                return HttpResponseForbidden('No tienes permiso para acceder a esta página')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


@login_required
def lista_actividades(request):
    """Listado de actividades"""
    actividades = Actividad.objects.prefetch_related('horarios').order_by('nombre')
    is_admin = request.user.groups.filter(name='Admin').exists()
    context = {
        'actividades': actividades,
        'total': actividades.count(),
        'is_admin': is_admin,
    }
    return render(request, 'actividades/lista.html', context)


@login_required
@require_group('Admin')
def crear_actividad(request):
    """Crear nueva actividad - Solo Admin"""
    if request.method == 'POST':
        form = ActividadForm(request.POST)
        if form.is_valid():
            actividad = form.save()
            messages.success(request, f'Actividad "{actividad}" creada exitosamente')
            return redirect('actividades:detalle', pk=actividad.pk)
    else:
        form = ActividadForm()

    context = {'form': form}
    return render(request, 'actividades/form_actividad.html', context)


@login_required
def detalle_actividad(request, pk):
    """Detalle de una actividad con sus horarios"""
    actividad = get_object_or_404(Actividad, pk=pk)
    horarios = actividad.horarios.all()
    is_admin = request.user.groups.filter(name='Admin').exists()

    context = {
        'actividad': actividad,
        'horarios': horarios,
        'is_admin': is_admin,
    }
    return render(request, 'actividades/detalle.html', context)


@login_required
@require_group('Admin')
def editar_actividad(request, pk):
    """Editar actividad - Solo Admin"""
    actividad = get_object_or_404(Actividad, pk=pk)

    if request.method == 'POST':
        form = ActividadForm(request.POST, instance=actividad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Actividad actualizada exitosamente')
            return redirect('actividades:detalle', pk=actividad.pk)
    else:
        form = ActividadForm(instance=actividad)

    context = {'form': form, 'actividad': actividad}
    return render(request, 'actividades/form_actividad.html', context)


@login_required
def lista_horarios(request):
    """Listado de horarios de clase"""
    horarios = HorarioClase.objects.select_related('actividad', 'entrenador').order_by('dia_semana', 'hora_inicio')
    is_admin = request.user.groups.filter(name='Admin').exists()
    context = {
        'horarios': horarios,
        'total': horarios.count(),
        'is_admin': is_admin,
    }
    return render(request, 'actividades/lista_horarios.html', context)


@login_required
@require_group('Admin')
def crear_horario(request):
    """Crear nuevo horario de clase - Solo Admin"""
    if request.method == 'POST':
        form = HorarioClaseForm(request.POST)
        if form.is_valid():
            horario = form.save()
            messages.success(request, f'Horario "{horario}" creado exitosamente')
            return redirect('actividades:horarios_actividad', pk=horario.actividad.pk)
    else:
        form = HorarioClaseForm()

    context = {'form': form}
    return render(request, 'actividades/form_horario.html', context)


@login_required
@require_group('Admin')
def editar_horario(request, pk):
    """Editar horario de clase - Solo Admin"""
    horario = get_object_or_404(HorarioClase, pk=pk)

    if request.method == 'POST':
        form = HorarioClaseForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horario actualizado exitosamente')
            return redirect('actividades:horarios_actividad', pk=horario.actividad.pk)
    else:
        form = HorarioClaseForm(instance=horario)

    context = {'form': form, 'horario': horario}
    return render(request, 'actividades/form_horario.html', context)


@login_required
def horarios_actividad(request, pk):
    """Horarios de una actividad con inscripciones"""
    actividad = get_object_or_404(Actividad, pk=pk)
    horarios = actividad.horarios.prefetch_related('inscripciones').order_by('dia_semana', 'hora_inicio')

    # Información de permisos
    is_admin = request.user.groups.filter(name='Admin').exists()
    is_miembro = request.user.groups.filter(name='Miembro').exists()
    miembro_usuario = None
    if is_miembro:
        try:
            miembro_usuario = request.user.miembro
        except Exception:
            pass

    context = {
        'actividad': actividad,
        'horarios': horarios,
        'is_admin': is_admin,
        'is_miembro': is_miembro,
        'miembro_usuario': miembro_usuario,
    }
    return render(request, 'actividades/horarios_actividad.html', context)


@login_required
def inscripciones_horario(request, pk):
    """Listado de miembros inscritos en un horario - Admin/Entrenador de la clase"""
    horario = get_object_or_404(HorarioClase, pk=pk)
    is_admin = request.user.groups.filter(name='Admin').exists()
    is_entrenador_clase = horario.entrenador and request.user.entrenador == horario.entrenador if hasattr(request.user, 'entrenador') else False

    if not (is_admin or is_entrenador_clase):
        return HttpResponseForbidden('No tienes permiso para ver los inscritos en esta clase')

    inscripciones = horario.inscripciones.filter(estado='ACTIVA').select_related('miembro')

    context = {
        'horario': horario,
        'inscripciones': inscripciones,
        'total': inscripciones.count(),
        'disponibles': horario.actividad.capacidad_maxima - inscripciones.count(),
    }
    return render(request, 'actividades/inscripciones_horario.html', context)


@login_required
@require_group('Miembro')
def inscribir_miembro(request):
    """Crear nueva inscripción - Solo Miembros"""
    try:
        miembro = request.user.miembro
    except Exception:
        return HttpResponseForbidden('Tu usuario no está vinculado a un registro de miembro')

    # Pre-llenar desde query params
    horario_pk = request.GET.get('horario')
    horario = None
    initial_data = {'miembro': miembro}

    if horario_pk:
        try:
            horario = HorarioClase.objects.get(pk=horario_pk)
            initial_data['horario'] = horario
        except HorarioClase.DoesNotExist:
            pass

    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            # Verificar que solo pueda inscribirse a sí mismo
            if form.cleaned_data['miembro'] != miembro:
                messages.error(request, 'Solo puedes inscribirte a ti mismo')
                return render(request, 'actividades/form_inscripcion.html', {'form': form})

            try:
                with transaction.atomic():
                    inscripcion = form.save()
                    entrenador_info = f" con {inscripcion.horario.entrenador}" if inscripcion.horario.entrenador else ""
                    messages.success(
                        request,
                        f'¡Te inscribiste exitosamente en {inscripcion.horario.actividad}!{entrenador_info}'
                    )
                    return redirect('actividades:horarios_actividad', pk=inscripcion.horario.actividad.pk)
            except ValidationError as e:
                messages.error(request, str(e))
    else:
        form = InscripcionForm(initial=initial_data)
        # Filtrar solo el miembro autenticado
        form.fields['miembro'].queryset = form.fields['miembro'].queryset.filter(pk=miembro.pk)

    context = {'form': form, 'miembro': miembro, 'horario': horario}
    return render(request, 'actividades/form_inscripcion.html', context)


@login_required
def cancelar_inscripcion(request, pk):
    """Cancelar inscripción"""
    inscripcion = get_object_or_404(Inscripcion, pk=pk)
    actividad_pk = inscripcion.horario.actividad.pk

    if request.method == 'POST':
        inscripcion.estado = 'CANCELADA'
        inscripcion.save()
        messages.success(
            request,
            f'Inscripción de {inscripcion.miembro} cancelada'
        )
        return redirect('actividades:horarios_actividad', pk=actividad_pk)

    context = {'inscripcion': inscripcion}
    return render(request, 'actividades/confirmar_cancelar.html', context)
