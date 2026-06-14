from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def reporte_asistencias(request):
    return HttpResponse("Reporte de asistencias")

@login_required
def reporte_cobros(request):
    return HttpResponse("Reporte de cobros")

@login_required
def membresias_vencidas(request):
    return HttpResponse("Membresías vencidas")
