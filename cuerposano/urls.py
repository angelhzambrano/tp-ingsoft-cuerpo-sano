from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_redirect),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('miembros/', include('miembros.urls', namespace='miembros')),
    path('membresias/', include('membresias.urls', namespace='membresias')),
    path('asistencia/', include('asistencia.urls', namespace='asistencia')),
    path('actividades/', include('actividades.urls', namespace='actividades')),
    path('entrenadores/', include('entrenadores.urls', namespace='entrenadores')),
    path('cobros/', include('cobros.urls', namespace='cobros')),
    path('reportes/', include('reportes.urls', namespace='reportes')),
    path('healthz/', views.healthz),
]
