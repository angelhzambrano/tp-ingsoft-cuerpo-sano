from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', RedirectView.as_view(url='asistencias/', permanent=False), name='index'),
    path('asistencias/', views.reporte_asistencias, name='asistencias'),
    path('cobros/', views.reporte_cobros, name='cobros'),
    path('membresias-vencidas/', views.membresias_vencidas, name='membresias_vencidas'),
]
