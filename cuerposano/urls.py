from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', views.custom_logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('miembros/', include('miembros.urls', namespace='miembros')),
    path('membresias/', include('membresias.urls', namespace='membresias')),
    path('asistencia/', include('asistencia.urls', namespace='asistencia')),
    path('actividades/', include('actividades.urls', namespace='actividades')),
    path('entrenadores/', include('entrenadores.urls', namespace='entrenadores')),
    path('cobros/', include('cobros.urls', namespace='cobros')),
    path('reportes/', include('reportes.urls', namespace='reportes')),
    path('historial/', include('historial.urls', namespace='historial')),
    path('healthz/', views.healthz),
]
