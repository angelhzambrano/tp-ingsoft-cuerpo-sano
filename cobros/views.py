from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def lista_cobros(request):
    return HttpResponse("Lista de cobros")

@login_required
def registrar_cobro(request):
    return HttpResponse("Registrar cobro")

@login_required
def ver_comprobante(request, pk):
    return HttpResponse(f"Comprobante {pk}")
