from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def registro_asistencia(request):
    return HttpResponse("Registro de asistencia por barcode")

@login_required
def listado_asistencia(request):
    return HttpResponse("Listado de asistencias")

@login_required
def registro_manual(request):
    return HttpResponse("Registro manual de asistencia")
