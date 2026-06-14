from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Membresia, TipoMembresia
from .forms import MembresiaForm
from miembros.models import Miembro


@login_required
def lista_membresias(request):
    membresias = Membresia.objects.select_related('miembro', 'tipo').order_by('-fecha_inicio')
    context = {
        'membresias': membresias,
        'total': membresias.count(),
    }
    return render(request, 'membresias/lista.html', context)


@login_required
def crear_membresia(request):
    if request.method == 'POST':
        form = MembresiaForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                membresia = form.save()
                messages.success(request, f'Membresía creada exitosamente')
            return redirect('membresias:detalle', pk=membresia.pk)
    else:
        form = MembresiaForm()
    context = {'form': form}
    return render(request, 'membresias/form.html', context)


@login_required
def detalle_membresia(request, pk):
    membresia = get_object_or_404(Membresia, pk=pk)
    context = {'membresia': membresia}
    return render(request, 'membresias/detalle.html', context)


@login_required
def editar_membresia(request, pk):
    membresia = get_object_or_404(Membresia, pk=pk)
    if membresia.estado != 'ACTIVA':
        messages.error(request, 'Solo se pueden editar membresías activas')
        return redirect('membresias:detalle', pk=membresia.pk)

    if request.method == 'POST':
        form = MembresiaForm(request.POST, instance=membresia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membresía actualizada exitosamente')
            return redirect('membresias:detalle', pk=membresia.pk)
    else:
        form = MembresiaForm(instance=membresia)
    context = {'form': form, 'membresia': membresia}
    return render(request, 'membresias/form.html', context)


@login_required
def print_membresia(request, pk):
    membresia = get_object_or_404(Membresia, pk=pk)
    context = {'membresia': membresia}
    return render(request, 'membresias/print.html', context)


@login_required
def lista_tipos(request):
    tipos = TipoMembresia.objects.all()
    context = {'tipos': tipos, 'total': tipos.count()}
    return render(request, 'membresias/lista_tipos.html', context)


@login_required
def crear_tipo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion', '')
        precio = request.POST.get('precio')
        duracion_dias = request.POST.get('duracion_dias')

        try:
            tipo = TipoMembresia.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                duracion_dias=duracion_dias
            )
            messages.success(request, f'Tipo de membresía "{tipo}" creado exitosamente')
            return redirect('membresias:lista_tipos')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'membresias/form_tipo.html')


@login_required
def editar_tipo(request, pk):
    tipo = get_object_or_404(TipoMembresia, pk=pk)
    if request.method == 'POST':
        tipo.nombre = request.POST.get('nombre', tipo.nombre)
        tipo.descripcion = request.POST.get('descripcion', tipo.descripcion)
        tipo.precio = request.POST.get('precio', tipo.precio)
        tipo.duracion_dias = request.POST.get('duracion_dias', tipo.duracion_dias)
        tipo.save()
        messages.success(request, 'Tipo actualizado exitosamente')
        return redirect('membresias:lista_tipos')

    context = {'tipo': tipo}
    return render(request, 'membresias/form_tipo.html', context)
