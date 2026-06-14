import pytest
from django.core.exceptions import ValidationError
from actividades.models import Actividad, HorarioClase, Inscripcion
from conftest import (
    ActividadFactory,
    HorarioClaseFactory,
    InscripcionFactory,
    MiembroFactory
)


pytestmark = pytest.mark.django_db


class TestActividadModels:
    """Tests para modelo Actividad"""

    def test_crear_actividad(self):
        """Caso 1: Crear actividad con capacidad"""
        actividad = ActividadFactory(nombre='Yoga', capacidad_maxima=20)
        assert actividad.id is not None
        assert actividad.nombre == 'Yoga'
        assert actividad.capacidad_maxima == 20

    def test_actividad_str(self):
        """Caso 2: Representación string"""
        actividad = ActividadFactory(nombre='Pilates')
        assert str(actividad) == 'Pilates'


class TestHorarioClaseModels:
    """Tests para modelo HorarioClase"""

    def test_crear_horario_clase(self):
        """Caso 3: Crear horario con actividad y día"""
        horario = HorarioClaseFactory(
            dia_semana='LUN',
            hora_inicio='09:00:00',
            hora_fin='10:00:00'
        )
        assert horario.id is not None
        assert horario.dia_semana == 'LUN'


class TestInscripcionValidaciones:
    """Tests para validaciones de Inscripción"""

    def test_inscripcion_capacidad_maxima(self):
        """Caso 4: No permitir inscripción si clase está llena"""
        actividad = ActividadFactory(capacidad_maxima=2)
        horario = HorarioClaseFactory(actividad=actividad)

        # Inscribir 2 miembros (capacidad máxima)
        miembro1 = MiembroFactory()
        miembro2 = MiembroFactory()
        InscripcionFactory(miembro=miembro1, horario=horario)
        InscripcionFactory(miembro=miembro2, horario=horario)

        # Intentar inscribir un tercero debe fallar
        miembro3 = MiembroFactory()
        with pytest.raises(ValidationError):
            inscripcion = Inscripcion(miembro=miembro3, horario=horario)
            inscripcion.save()

    def test_inscripcion_unica_por_miembro_horario(self):
        """Caso 5: No duplicar inscripciones de mismo miembro en mismo horario"""
        miembro = MiembroFactory()
        horario = HorarioClaseFactory()

        InscripcionFactory(miembro=miembro, horario=horario, estado='ACTIVA')

        # Intentar inscribir de nuevo con unique_together constraint
        with pytest.raises(Exception):  # IntegrityError
            InscripcionFactory(miembro=miembro, horario=horario, estado='ACTIVA')
