from django.urls import path
from . import views

app_name = 'cobros'

urlpatterns = [
    path('', views.lista_cobros, name='lista'),
    path('nuevo/', views.registrar_cobro, name='crear'),
    path('<int:pk>/comprobante/', views.ver_comprobante, name='comprobante'),
]
