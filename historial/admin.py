from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'usuario', 'modelo', 'id_objeto', 'accion', 'descripcion')
    list_filter = ('accion', 'modelo', 'timestamp', 'usuario')
    search_fields = ('descripcion', 'modelo', 'id_objeto')
    readonly_fields = ('timestamp', 'modelo', 'id_objeto', 'accion', 'usuario', 'cambios', 'descripcion')
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
