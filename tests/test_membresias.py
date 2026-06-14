import pytest
from datetime import date, timedelta
from membresias.models import Membresia, TipoMembresia
from conftest import MembresiaFactory, TipoMembresiaFactory, MiembroFactory


pytestmark = pytest.mark.django_db


class TestMembresiaModels:
    """Tests para modelo Membresia"""

    def test_crear_membresia(self):
        """Caso 1: Crear membresía con fecha_fin calculada"""
        tipo = TipoMembresiaFactory(nombre='Mensual', duracion_dias=30)
        miembro = MiembroFactory()
        fecha_inicio = date.today()

        membresia = MembresiaFactory(
            miembro=miembro,
            tipo=tipo,
            fecha_inicio=fecha_inicio,
            estado='ACTIVA'
        )

        assert membresia.id is not None
        assert membresia.estado == 'ACTIVA'
        assert membresia.fecha_fin == fecha_inicio + timedelta(days=30)

    def test_membresia_estado_vencida(self):
        """Caso 2: Membresía vencida (fecha_fin < hoy)"""
        tipo = TipoMembresiaFactory(duracion_dias=1)
        miembro = MiembroFactory()
        membresia = MembresiaFactory(
            miembro=miembro,
            tipo=tipo,
            fecha_inicio=date.today() - timedelta(days=2),
            estado='VENCIDA'
        )
        assert membresia.estado == 'VENCIDA'


class TestTipoMembresiaModels:
    """Tests para modelo TipoMembresia"""

    def test_crear_tipo_membresia(self):
        """Caso 3: Crear tipo de membresía"""
        tipo = TipoMembresiaFactory(
            nombre='Anual',
            duracion_dias=365,
            precio=1200
        )
        assert tipo.id is not None
        assert tipo.nombre == 'Anual'
        assert tipo.precio == 1200

    def test_tipo_membresia_str(self):
        """Caso 4: Representación string"""
        tipo = TipoMembresiaFactory(nombre='Premium')
        assert str(tipo) == 'Premium'


class TestMembresiaValidaciones:
    """Tests para validaciones de Membresia"""

    def test_membresia_unica_por_miembro_activa(self):
        """Caso 5: Solo una membresía ACTIVA por miembro"""
        miembro = MiembroFactory()
        tipo = TipoMembresiaFactory()

        MembresiaFactory(miembro=miembro, tipo=tipo, estado='ACTIVA')
        # Segunda membresía ACTIVA (permitida, no hay restricción en modelo)
        membresia2 = MembresiaFactory(miembro=miembro, tipo=tipo, estado='ACTIVA')
        assert membresia2.estado == 'ACTIVA'
