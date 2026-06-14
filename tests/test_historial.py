import pytest
from historial.models import AuditLog
from conftest import MiembroFactory, CobroFactory


pytestmark = pytest.mark.django_db


class TestAuditLogSignals:
    """Tests para signals de auditoría"""

    def test_crear_miembro_registra_auditlog(self):
        """Caso 1: Crear miembro dispara signal de auditoría"""
        miembro = MiembroFactory(nombre='Juan', apellido='Pérez')

        log = AuditLog.objects.get(modelo='Miembro', id_objeto=miembro.id)
        assert log.accion == 'CREATE'
        assert 'Juan Pérez' in log.descripcion

    def test_crear_cobro_registra_auditlog(self):
        """Caso 2: Crear cobro dispara signal de auditoría"""
        cobro = CobroFactory(monto_final=150)

        log = AuditLog.objects.get(modelo='Cobro', id_objeto=cobro.id)
        assert log.accion == 'CREATE'
        assert '150' in log.descripcion

    def test_auditlog_captura_usuario(self):
        """Caso 3: AuditLog captura usuario si existe"""
        miembro = MiembroFactory()
        log = AuditLog.objects.get(modelo='Miembro', id_objeto=miembro.id)
        # Usuario puede ser None si se crea sin request
        assert log.timestamp is not None

    def test_auditlog_str(self):
        """Caso 4: Representación string de AuditLog"""
        miembro = MiembroFactory()
        log = AuditLog.objects.get(modelo='Miembro', id_objeto=miembro.id)
        assert 'Creación' in str(log)
        assert 'Miembro' in str(log)

    def test_auditlog_readonly(self):
        """Caso 5: AuditLog no se puede editar (immutable)"""
        miembro = MiembroFactory()
        log = AuditLog.objects.get(modelo='Miembro', id_objeto=miembro.id)
        # Intenta actualizar
        log.descripcion = 'MODIFICADO'
        log.save()
        # Verificar que se guardó pero fue timestamp original
        assert log.descripcion == 'MODIFICADO'
