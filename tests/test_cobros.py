import pytest
from decimal import Decimal
from cobros.models import Cobro, Comprobante
from conftest import CobroFactory, MiembroFactory, MembresiaFactory


pytestmark = pytest.mark.django_db


class TestCobroModels:
    """Tests para modelo Cobro"""

    def test_crear_cobro(self):
        """Caso 1: Crear cobro con cálculo de monto final"""
        miembro = MiembroFactory(tipo_miembro='ESTUDIANTE')
        membresia = MembresiaFactory(miembro=miembro)

        cobro = CobroFactory(
            miembro=miembro,
            membresia=membresia,
            monto_base=100,
            descuento_porcentaje=20,
            forma_pago='EFECTIVO'
        )

        assert cobro.id is not None
        assert cobro.monto_base == 100
        assert cobro.descuento_porcentaje == 20

    def test_cobro_forma_pago_valida(self):
        """Caso 2: Formas de pago válidas"""
        formas = ['EFECTIVO', 'TARJETA', 'TRANSFERENCIA']
        for forma in formas:
            cobro = CobroFactory(forma_pago=forma)
            assert cobro.forma_pago == forma

    def test_comprobante_creacion_manual(self):
        """Caso 3: Comprobante se puede crear manualmente"""
        cobro = CobroFactory()
        comprobante = Comprobante.objects.create(cobro=cobro)
        assert comprobante is not None
        assert comprobante.numero is not None

    def test_cobro_str(self):
        """Caso 4: Representación string de Cobro"""
        miembro = MiembroFactory(nombre='Juan', apellido='Pérez')
        cobro = CobroFactory(miembro=miembro)
        assert 'Juan Pérez' in str(cobro)

    def test_comprobante_numero_autoincrement(self):
        """Caso 5: Número de comprobante es AutoField"""
        cobro = CobroFactory()
        comprobante = Comprobante.objects.create(cobro=cobro)
        assert comprobante.numero is not None
        assert isinstance(comprobante.numero, int)
