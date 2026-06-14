from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('asistencias/', views.reporte_asistencias, name='asistencias'),
    path('cobros/', views.reporte_cobros, name='cobros'),
    path('membresias-vencidas/', views.membresias_vencidas, name='membresias_vencidas'),
]
