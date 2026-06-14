from django.urls import path
from . import views

app_name = 'membresias'

urlpatterns = [
    path('', views.lista_membresias, name='lista'),
    path('nueva/', views.crear_membresia, name='crear'),
    path('<int:pk>/', views.detalle_membresia, name='detalle'),
    path('<int:pk>/editar/', views.editar_membresia, name='editar'),
    path('<int:pk>/print/', views.print_membresia, name='print'),
    path('tipos/', views.lista_tipos, name='lista_tipos'),
    path('tipos/nuevo/', views.crear_tipo, name='crear_tipo'),
    path('tipos/<int:pk>/editar/', views.editar_tipo, name='editar_tipo'),
]
