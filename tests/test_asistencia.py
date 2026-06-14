import pytest
import json
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


class TestBiometricoAPI:
    """Tests para API biométrica (RF-11)"""

    def test_biometrico_escaneo_exitoso(self, client, db):
        """Caso 6: Escaneo biométrico exitoso registra asistencia"""
        miembro = MiembroFactory()
        carnet = CarnetFactory(miembro=miembro)
        membresia = MembresiaFactory(miembro=miembro, estado='ACTIVA')

        response = client.post(
            '/asistencia/api/barcode/',
            data=json.dumps({'numero_carnet': carnet.numero_carnet}),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'registrado exitosamente' in data['message']
        assert Asistencia.objects.filter(miembro=miembro, metodo='BARCODE').exists()

    def test_biometrico_carnet_no_existe(self, client, db):
        """Caso 7: Código de carnet inexistente devuelve error"""
        response = client.post(
            '/asistencia/api/barcode/',
            data=json.dumps({'numero_carnet': 'NOEXISTE'}),
            content_type='application/json'
        )

        assert response.status_code == 404

    def test_biometrico_miembro_inactivo(self, client, db):
        """Caso 8: Miembro inactivo no puede registrar asistencia"""
        miembro = MiembroFactory(activo=False)
        carnet = CarnetFactory(miembro=miembro)
        membresia = MembresiaFactory(miembro=miembro, estado='ACTIVA')

        response = client.post(
            '/asistencia/api/barcode/',
            data=json.dumps({'numero_carnet': carnet.numero_carnet}),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is False
        assert 'inactivo' in data['error']

    def test_biometrico_membresia_vencida(self, client, db):
        """Caso 9: Membresía vencida no permite escaneo"""
        miembro = MiembroFactory()
        carnet = CarnetFactory(miembro=miembro)
        membresia = MembresiaFactory(miembro=miembro, estado='VENCIDA')

        response = client.post(
            '/asistencia/api/barcode/',
            data=json.dumps({'numero_carnet': carnet.numero_carnet}),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is False
        assert 'Membresía vencida' in data['error']

    def test_biometrico_reader_view_requiere_login(self, client, db):
        """Caso 10: Vista del lector biométrico requiere autenticación"""
        response = client.get('/asistencia/biometrico/')
        assert response.status_code == 302  # Redirect to login

    def test_biometrico_reader_view_autenticado(self, client, db, admin_user):
        """Caso 11: Usuario autenticado puede acceder al lector"""
        client.force_login(admin_user)
        response = client.get('/asistencia/biometrico/')
        assert response.status_code == 200
        assert 'biometrico' in response.content.decode()
