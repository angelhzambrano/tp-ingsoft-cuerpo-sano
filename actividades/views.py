from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def lista_actividades(request):
    return HttpResponse("Lista de actividades")

@login_required
def crear_actividad(request):
    return HttpResponse("Crear actividad")

@login_required
def editar_actividad(request, pk):
    return HttpResponse(f"Editar actividad {pk}")

@login_required
def print_actividad(request, pk):
    return HttpResponse(f"Print actividad {pk}")

@login_required
def lista_horarios(request):
    return HttpResponse("Lista de horarios")

@login_required
def crear_horario(request):
    return HttpResponse("Crear horario")

@login_required
def editar_horario(request, pk):
    return HttpResponse(f"Editar horario {pk}")

@login_required
def print_horario(request, pk):
    return HttpResponse(f"Print horario {pk}")

@login_required
def inscripciones_horario(request, pk):
    return HttpResponse(f"Inscripciones horario {pk}")

@login_required
def inscribir_miembro(request):
    return HttpResponse("Inscribir miembro")
