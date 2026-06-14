from django.urls import path
from . import views

app_name = 'miembros'

urlpatterns = [
    path('', views.lista_miembros, name='lista'),
    path('nuevo/', views.crear_miembro, name='crear'),
    path('<int:pk>/', views.detalle_miembro, name='detalle'),
    path('<int:pk>/editar/', views.editar_miembro, name='editar'),
    path('<int:pk>/carnet/', views.ver_carnet, name='carnet'),
]
