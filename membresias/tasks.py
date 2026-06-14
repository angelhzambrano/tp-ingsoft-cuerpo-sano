from datetime import date
from .models import Membresia


def actualizar_estados_membresias():
    """Tarea diaria que marca membresías como vencidas si fecha_fin < hoy"""
    hoy = date.today()
    membresias_vencidas = Membresia.objects.filter(
        estado='ACTIVA',
        fecha_fin__lt=hoy
    )
    count = membresias_vencidas.update(estado='VENCIDA')
    return f"Actualizadas {count} membresías a estado VENCIDA"
