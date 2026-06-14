from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def lista_entrenadores(request):
    return HttpResponse("Lista de entrenadores")

@login_required
def crear_entrenador(request):
    return HttpResponse("Crear entrenador")

@login_required
def editar_entrenador(request, pk):
    return HttpResponse(f"Editar entrenador {pk}")

@login_required
def print_entrenador(request, pk):
    return HttpResponse(f"Print entrenador {pk}")

@login_required
def registro_asistencia_entrenador(request):
    return HttpResponse("Registro de asistencia de entrenador")
