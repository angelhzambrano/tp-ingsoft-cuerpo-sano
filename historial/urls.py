from django.urls import path
from . import views

app_name = 'historial'

urlpatterns = [
    path('auditlog/', views.lista_auditlog, name='auditlog'),
    path('auditlog/miembro/<int:miembro_id>/', views.auditlog_miembro, name='auditlog_miembro'),
    path('auditlog/cobro/<int:cobro_id>/', views.auditlog_cobro, name='auditlog_cobro'),
]
