from django.contrib import admin
from .models import Miembro, Carnet


@admin.register(Miembro)
class MiembroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni', 'tipo_miembro', 'tipo_membresia_activa', 'activo', 'fecha_alta')
    list_filter = ('tipo_miembro', 'tipo_membresia_activa', 'activo', 'fecha_alta')
    search_fields = ('nombre', 'apellido', 'dni', 'email')
    readonly_fields = ('fecha_alta',)
    fields = ('nombre', 'apellido', 'dni', 'email', 'telefono', 'foto', 'tipo_miembro', 'tipo_membresia_activa', 'activo', 'fecha_alta')


@admin.register(Carnet)
class CarnetAdmin(admin.ModelAdmin):
    list_display = ('numero_carnet', 'miembro', 'fecha_emision')
    search_fields = ('numero_carnet', 'miembro__nombre', 'miembro__apellido')
    readonly_fields = ('numero_carnet', 'fecha_emision')
