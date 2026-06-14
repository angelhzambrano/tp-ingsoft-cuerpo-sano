from django.contrib import admin
from .models import Actividad, HorarioClase, Inscripcion


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'capacidad_maxima', 'horarios_count')
    search_fields = ('nombre',)

    def horarios_count(self, obj):
        return obj.horarios.count()
    horarios_count.short_description = 'Horarios'


@admin.register(HorarioClase)
class HorarioClaseAdmin(admin.ModelAdmin):
    list_display = ('actividad', 'dia_semana', 'hora_inicio', 'hora_fin', 'entrenador', 'sala')
    list_filter = ('dia_semana', 'actividad')
    search_fields = ('actividad__nombre', 'sala')


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('miembro', 'horario', 'fecha_inscripcion', 'estado')
    list_filter = ('estado', 'fecha_inscripcion')
    search_fields = ('miembro__nombre', 'miembro__apellido', 'horario__actividad__nombre')
    readonly_fields = ('fecha_inscripcion',)
