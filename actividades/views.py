from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Actividad, HorarioClase, Inscripcion
from .forms import ActividadForm, HorarioClaseForm, InscripcionForm


@login_required
def lista_actividades(request):
    """Listado de actividades"""
    actividades = Actividad.objects.prefetch_related('horarios').order_by('nombre')
    context = {
        'actividades': actividades,
        'total': actividades.count(),
    }
    return render(request, 'actividades/lista.html', context)


@login_required
def crear_actividad(request):
    """Crear nueva actividad"""
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

    context = {
        'actividad': actividad,
        'horarios': horarios,
    }
    return render(request, 'actividades/detalle.html', context)


@login_required
def editar_actividad(request, pk):
    """Editar actividad"""
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
    context = {
        'horarios': horarios,
        'total': horarios.count(),
    }
    return render(request, 'actividades/lista_horarios.html', context)


@login_required
def crear_horario(request):
    """Crear nuevo horario de clase"""
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
def editar_horario(request, pk):
    """Editar horario de clase"""
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

    context = {
        'actividad': actividad,
        'horarios': horarios,
    }
    return render(request, 'actividades/horarios_actividad.html', context)


@login_required
def inscripciones_horario(request, pk):
    """Listado de miembros inscritos en un horario"""
    horario = get_object_or_404(HorarioClase, pk=pk)
    inscripciones = horario.inscripciones.filter(estado='ACTIVA').select_related('miembro')

    context = {
        'horario': horario,
        'inscripciones': inscripciones,
        'total': inscripciones.count(),
        'disponibles': horario.actividad.capacidad_maxima - inscripciones.count(),
    }
    return render(request, 'actividades/inscripciones_horario.html', context)


@login_required
def inscribir_miembro(request):
    """Crear nueva inscripción"""
    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    inscripcion = form.save()
                    messages.success(
                        request,
                        f'Inscripción de {inscripcion.miembro} exitosa'
                    )
                    return redirect('actividades:horarios_actividad', pk=inscripcion.horario.actividad.pk)
            except ValidationError as e:
                messages.error(request, str(e))
    else:
        form = InscripcionForm()

    context = {'form': form}
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
