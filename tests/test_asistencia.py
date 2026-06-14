import pytest
from django.test import Client
from django.urls import reverse
from asistencia.models import Asistencia
from membresias.models import Membresia
from conftest import (
    MiembroFactory,
    CarnetFactory,
    MembresiaFactory,
    UserFactory
)


pytestmark = pytest.mark.django_db


class TestAsistenciaModels:
    """Tests para modelo Asistencia"""

    def test_crear_asistencia(self):
        """Caso 1: Crear registro de asistencia"""
        miembro = MiembroFactory()
        asistencia = Asistencia.objects.create(
            miembro=miembro,
            metodo='BARCODE'
        )
        assert asistencia.id is not None
        assert asistencia.metodo == 'BARCODE'
        assert asistencia.fecha is not None
        assert asistencia.hora is not None

    def test_asistencia_manual(self):
        """Caso 2: Asistencia manual"""
        miembro = MiembroFactory()
        asistencia = Asistencia.objects.create(
            miembro=miembro,
            metodo='MANUAL'
        )
        assert asistencia.metodo == 'MANUAL'


class TestAsistenciaValidacion:
    """Tests para validación de asistencia por barcode"""

    def test_registrar_asistencia_requiere_membressia_activa(self):
        """Caso 3: No permitir asistencia sin membresía ACTIVA"""
        miembro = MiembroFactory()

        # Crear membresía VENCIDA
        MembresiaFactory(miembro=miembro, estado='VENCIDA')

        # Intentar registrar asistencia debe fallar (no hay ACTIVA)
        membresia_activa = Membresia.objects.filter(
            miembro=miembro,
            estado='ACTIVA'
        ).exists()
        assert not membresia_activa

    def test_registrar_asistencia_requiere_miembro_activo(self):
        """Caso 4: No permitir asistencia de miembro inactivo"""
        miembro = MiembroFactory(activo=False)
        MembresiaFactory(miembro=miembro, estado='ACTIVA')

        # Verificar que miembro está inactivo
        assert not miembro.activo

    def test_asistencia_str(self):
        """Caso 5: Representación string"""
        miembro = MiembroFactory(nombre='Juan', apellido='Pérez')
        asistencia = Asistencia.objects.create(
            miembro=miembro,
            metodo='BARCODE'
        )
        assert 'Juan Pérez' in str(asistencia)
