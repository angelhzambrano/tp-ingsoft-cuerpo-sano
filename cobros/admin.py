from django.contrib import admin
from .models import Cobro, Comprobante


@admin.register(Cobro)
class CobroAdmin(admin.ModelAdmin):
    list_display = ('miembro', 'membresia', 'monto_base', 'descuento_porcentaje', 'monto_final', 'forma_pago', 'fecha')
    list_filter = ('forma_pago', 'fecha', 'miembro__tipo_miembro')
    search_fields = ('miembro__nombre', 'miembro__apellido', 'miembro__dni')
    readonly_fields = ('fecha',)


@admin.register(Comprobante)
class ComprobanteAdmin(admin.ModelAdmin):
    list_display = ('numero', 'cobro', 'fecha_emision')
    search_fields = ('numero', 'cobro__miembro__nombre', 'cobro__miembro__apellido')
    readonly_fields = ('numero', 'fecha_emision')
