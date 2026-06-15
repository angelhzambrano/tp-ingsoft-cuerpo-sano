from django.urls import path
from . import views

app_name = 'entrenadores'

urlpatterns = [
    path('', views.lista_entrenadores, name='lista'),
    path('asistencia/', views.mi_asistencia_entrenador, name='asistencia'),
    path('nuevo/', views.crear_entrenador, name='crear'),
    path('<int:pk>/', views.detalle_entrenador, name='detalle'),
    path('<int:pk>/editar/', views.editar_entrenador, name='editar'),
    path('<int:pk>/print/', views.print_entrenador, name='print'),
    path('<int:pk>/asistencias/', views.historial_asistencias_entrenador, name='historial_asistencias'),
    path('asistencia/registrar/', views.registro_asistencia_entrenador, name='registrar_asistencia'),
]
