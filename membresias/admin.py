from django.contrib import admin
from .models import TipoMembresia, Membresia


@admin.register(TipoMembresia)
class TipoMembresiaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'duracion_dias')
    search_fields = ('nombre',)


@admin.register(Membresia)
class MembresiaAdmin(admin.ModelAdmin):
    list_display = ('miembro', 'tipo', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('estado', 'tipo', 'fecha_inicio')
    search_fields = ('miembro__nombre', 'miembro__apellido', 'miembro__dni')
    readonly_fields = ('fecha_fin',)
