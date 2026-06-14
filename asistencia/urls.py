from django.urls import path
from . import views

app_name = 'asistencia'

urlpatterns = [
    path('', views.registro_asistencia, name='registro'),
    path('listado/', views.listado_asistencia, name='listado'),
    path('manual/', views.registro_manual, name='manual'),
]
