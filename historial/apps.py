from django.apps import AppConfig


class HistorialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'historial'

    def ready(self):
        from django.db.models.signals import post_save, post_delete
        from miembros.models import Miembro
        from cobros.models import Cobro
        from .signals import (
            registrar_cambios_miembro,
            registrar_cambios_cobro,
            registrar_eliminacion_miembro,
            registrar_eliminacion_cobro
        )

        post_save.connect(registrar_cambios_miembro, sender=Miembro, dispatch_uid='audit_miembro_save')
        post_delete.connect(registrar_eliminacion_miembro, sender=Miembro, dispatch_uid='audit_miembro_delete')
        post_save.connect(registrar_cambios_cobro, sender=Cobro, dispatch_uid='audit_cobro_save')
        post_delete.connect(registrar_eliminacion_cobro, sender=Cobro, dispatch_uid='audit_cobro_delete')
