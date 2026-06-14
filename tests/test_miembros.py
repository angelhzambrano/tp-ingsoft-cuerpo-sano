import pytest
from django.test import Client
from django.urls import reverse
from miembros.models import Miembro, Carnet
from conftest import MiembroFactory, UserFactory


pytestmark = pytest.mark.django_db


class TestMiembroModels:
    """Tests para modelo Miembro"""

    def test_crear_miembro(self):
        """Caso 1: Crear miembro con DNI único"""
        miembro = MiembroFactory(dni='12345678901')
        assert miembro.id is not None
        assert miembro.activo is True
        assert miembro.tipo_miembro == 'REGULAR'

    def test_dni_unico(self):
        """Caso 2: DNI debe ser único"""
        MiembroFactory(dni='11111111111')
        with pytest.raises(Exception):  # IntegrityError
            MiembroFactory(dni='11111111111')

    def test_miembro_str(self):
        """Caso 3: Representación string de Miembro"""
        miembro = MiembroFactory(nombre='Juan', apellido='Pérez')
        assert str(miembro) == 'Juan Pérez'


class TestCarnetSignal:
    """Tests para creación automática de Carnet"""

    def test_carnet_creado_automaticamente(self):
        """Caso 4: Carnet se crea automáticamente al crear Miembro"""
        miembro = MiembroFactory()
        carnet = Carnet.objects.get(miembro=miembro)
        assert carnet is not None
        assert carnet.numero_carnet is not None

    def test_carnet_relacion_uno_a_uno(self):
        """Caso 5: Carnet tiene relación 1:1 con Miembro"""
        miembro = MiembroFactory()
        carnet1 = Carnet.objects.get(miembro=miembro)
        assert carnet1.miembro == miembro


class TestMiembroViews:
    """Tests para vistas de Miembro"""

    def test_lista_miembros_requiere_login(self, client):
        """Test: Vista lista requiere autenticación"""
        response = client.get(reverse('miembros:lista'))
        assert response.status_code == 302  # Redirect a login

    def test_lista_miembros_autenticado(self, client, user):
        """Test: Lista muestra miembros si autenticado"""
        client.force_login(user)
        MiembroFactory()
        response = client.get(reverse('miembros:lista'))
        assert response.status_code == 200
        assert 'miembros' in response.context

    def test_crear_miembro_valida_form(self, client, user):
        """Test: Crear miembro valida campos requeridos"""
        client.force_login(user)
        response = client.post(reverse('miembros:crear'), {
            'nombre': '',  # Requerido
            'apellido': 'Pérez',
        })
        assert response.status_code == 200
        assert 'form' in response.context
