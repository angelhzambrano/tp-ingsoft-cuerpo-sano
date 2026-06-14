from django.urls import path
from . import views

app_name = 'asistencia'

urlpatterns = [
    path('', views.registro_asistencia, name='registro'),
    path('api/barcode/', views.registrar_por_barcode, name='api_barcode'),
    path('listado/', views.listado_asistencia, name='listado'),
    path('manual/', views.registro_manual, name='manual'),
    path('biometrico/', views.biometrico_reader, name='biometrico'),
]
