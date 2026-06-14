from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from miembros.models import Miembro
from cobros.models import Cobro
from .models import AuditLog


def registrar_cambios_miembro(sender, instance, created, request=None, **kwargs):
    usuario = None
    if hasattr(instance, '_request_user'):
        usuario = instance._request_user
    elif request:
        usuario = request.user if request.user.is_authenticated else None

    if created:
        AuditLog.objects.create(
            modelo='Miembro',
            id_objeto=instance.id,
            accion='CREATE',
            usuario=usuario,
            descripcion=f'Nuevo miembro: {instance.nombre} {instance.apellido}'
        )
    else:
        AuditLog.objects.create(
            modelo='Miembro',
            id_objeto=instance.id,
            accion='UPDATE',
            usuario=usuario,
            descripcion=f'Actualizado: {instance.nombre} {instance.apellido}'
        )


def registrar_cambios_cobro(sender, instance, created, request=None, **kwargs):
    usuario = None
    if hasattr(instance, '_request_user'):
        usuario = instance._request_user
    elif request:
        usuario = request.user if request.user.is_authenticated else None

    if created:
        AuditLog.objects.create(
            modelo='Cobro',
            id_objeto=instance.id,
            accion='CREATE',
            usuario=usuario,
            descripcion=f'Nuevo cobro: {instance.miembro} - ${instance.monto_final}'
        )
    else:
        AuditLog.objects.create(
            modelo='Cobro',
            id_objeto=instance.id,
            accion='UPDATE',
            usuario=usuario,
            descripcion=f'Actualizado: {instance.miembro} - ${instance.monto_final}'
        )


def registrar_eliminacion_miembro(sender, instance, **kwargs):
    AuditLog.objects.create(
        modelo='Miembro',
        id_objeto=instance.id,
        accion='DELETE',
        descripcion=f'Eliminado: {instance.nombre} {instance.apellido}'
    )


def registrar_eliminacion_cobro(sender, instance, **kwargs):
    AuditLog.objects.create(
        modelo='Cobro',
        id_objeto=instance.id,
        accion='DELETE',
        descripcion=f'Eliminado: Cobro #{instance.id}'
    )
