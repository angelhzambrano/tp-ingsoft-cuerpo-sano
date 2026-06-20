from django.contrib import admin
from .models import Entrenador


@admin.register(Entrenador)
class EntrenadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'especialidad', 'email', 'activo')
    list_filter = ('activo', 'especialidad')
    search_fields = ('nombre', 'apellido', 'email')
    fields = ('nombre', 'apellido', 'especialidad', 'telefono', 'email', 'activo')
