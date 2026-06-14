from django.urls import path
from . import views

app_name = 'entrenadores'

urlpatterns = [
    path('', views.lista_entrenadores, name='lista'),
    path('nuevo/', views.crear_entrenador, name='crear'),
    path('<int:pk>/editar/', views.editar_entrenador, name='editar'),
    path('<int:pk>/print/', views.print_entrenador, name='print'),
    path('asistencia/', views.registro_asistencia_entrenador, name='asistencia'),
]
