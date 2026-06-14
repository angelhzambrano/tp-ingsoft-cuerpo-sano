from django.urls import path
from . import views

app_name = 'actividades'

urlpatterns = [
    path('', views.lista_actividades, name='lista'),
    path('nueva/', views.crear_actividad, name='crear'),
    path('<int:pk>/', views.detalle_actividad, name='detalle'),
    path('<int:pk>/editar/', views.editar_actividad, name='editar'),
    path('<int:pk>/horarios/', views.horarios_actividad, name='horarios_actividad'),
    path('horarios/', views.lista_horarios, name='lista_horarios'),
    path('horarios/nuevo/', views.crear_horario, name='crear_horario'),
    path('horarios/<int:pk>/editar/', views.editar_horario, name='editar_horario'),
    path('horarios/<int:pk>/inscripciones/', views.inscripciones_horario, name='inscripciones_horario'),
    path('inscribir/', views.inscribir_miembro, name='inscribir'),
    path('inscripcion/<int:pk>/cancelar/', views.cancelar_inscripcion, name='cancelar_inscripcion'),
]
