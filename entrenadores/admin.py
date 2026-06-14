from django.contrib import admin
from .models import Entrenador, AsistenciaEntrenador


@admin.register(Entrenador)
class EntrenadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'especialidad', 'email', 'activo')
    list_filter = ('activo', 'especialidad')
    search_fields = ('nombre', 'apellido', 'email')
    fields = ('nombre', 'apellido', 'especialidad', 'telefono', 'email', 'activo')


@admin.register(AsistenciaEntrenador)
class AsistenciaEntrenadorAdmin(admin.ModelAdmin):
    list_display = ('entrenador', 'horario', 'fecha', 'tipo', 'justificada')
    list_filter = ('tipo', 'justificada', 'fecha')
    search_fields = ('entrenador__nombre', 'entrenador__apellido', 'horario__actividad__nombre')
    readonly_fields = ('entrenador', 'horario', 'fecha')
