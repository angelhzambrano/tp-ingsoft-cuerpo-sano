from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseForbidden
from .models import Miembro, Carnet
from .forms import MiembroForm
from .utils import generar_barcode_cloudinary


def _puede_ver_miembros(user):
    """Verificar si usuario puede ver lista de miembros"""
    return user.groups.filter(name__in=['Admin', 'Recepcion']).exists()


def _puede_crear_miembro(user):
    """Verificar si usuario puede crear miembros"""
    return user.groups.filter(name__in=['Admin', 'Recepcion']).exists()


@login_required
def lista_miembros(request):
    if not _puede_ver_miembros(request.user):
        return HttpResponseForbidden('No tienes permiso para ver esta página')

    miembros = Miembro.objects.all().order_by('-fecha_alta')
    context = {
        'miembros': miembros,
        'total': miembros.count(),
    }
    return render(request, 'miembros/lista.html', context)


@login_required
def crear_miembro(request):
    if not _puede_crear_miembro(request.user):
        return HttpResponseForbidden('No tienes permiso para crear miembros')

    if request.method == 'POST':
        form = MiembroForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                miembro = form.save()
                # Carnet se crea automáticamente en post_save signal
                messages.success(request, f'Miembro {miembro} creado exitosamente')
            return redirect('miembros:detalle', pk=miembro.pk)
    else:
        form = MiembroForm()
    context = {'form': form}
    return render(request, 'miembros/form.html', context)


@login_required
def detalle_miembro(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    try:
        carnet = miembro.carnet
    except Carnet.DoesNotExist:
        carnet = None

    context = {
        'miembro': miembro,
        'carnet': carnet,
    }
    return render(request, 'miembros/detalle.html', context)


@login_required
def editar_miembro(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    if request.method == 'POST':
        form = MiembroForm(request.POST, request.FILES, instance=miembro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Miembro actualizado exitosamente')
            return redirect('miembros:detalle', pk=miembro.pk)
    else:
        form = MiembroForm(instance=miembro)
    context = {'form': form, 'miembro': miembro}
    return render(request, 'miembros/form.html', context)


@login_required
def ver_carnet(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    try:
        carnet = miembro.carnet
    except Carnet.DoesNotExist:
        messages.error(request, 'Este miembro no tiene carnet')
        return redirect('miembros:detalle', pk=miembro.pk)

    context = {
        'miembro': miembro,
        'carnet': carnet,
    }
    return render(request, 'miembros/carnet_print.html', context)
