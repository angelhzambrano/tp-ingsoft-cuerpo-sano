from django.contrib import admin
from .models import Asistencia


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('miembro', 'fecha', 'hora', 'metodo')
    list_filter = ('metodo', 'fecha')
    search_fields = ('miembro__nombre', 'miembro__apellido', 'miembro__dni')
    readonly_fields = ('fecha', 'hora')
