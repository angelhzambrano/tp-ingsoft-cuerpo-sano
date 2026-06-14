import pytest
from django.contrib.auth.models import User, Group
from factory.django import DjangoModelFactory
from factory import Faker, SubFactory, django
from miembros.models import Miembro, Carnet
from membresias.models import TipoMembresia, Membresia
from cobros.models import Cobro
from actividades.models import Actividad, HorarioClase, Inscripcion
from entrenadores.models import Entrenador
from datetime import date, timedelta


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('user_name')
    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')


class MiembroFactory(DjangoModelFactory):
    class Meta:
        model = Miembro

    nombre = Faker('first_name')
    apellido = Faker('last_name')
    dni = Faker('numerify', text='##########')
    email = Faker('email')
    telefono = Faker('numerify', text='1#########')
    tipo_miembro = 'REGULAR'
    activo = True


class CarnetFactory(DjangoModelFactory):
    class Meta:
        model = Carnet

    miembro = SubFactory(MiembroFactory)
    numero_carnet = Faker('numerify', text='##########')


class TipoMembresiaFactory(DjangoModelFactory):
    class Meta:
        model = TipoMembresia

    nombre = Faker('word')
    duracion_dias = 30
    precio = 100


class MembresiaFactory(DjangoModelFactory):
    class Meta:
        model = Membresia

    miembro = SubFactory(MiembroFactory)
    tipo = SubFactory(TipoMembresiaFactory)
    fecha_inicio = Faker('date_object')
    estado = 'ACTIVA'


class CobroFactory(DjangoModelFactory):
    class Meta:
        model = Cobro

    miembro = SubFactory(MiembroFactory)
    membresia = SubFactory(MembresiaFactory)
    monto_base = 100
    descuento_porcentaje = 0
    monto_final = 100
    forma_pago = 'EFECTIVO'


class ActividadFactory(DjangoModelFactory):
    class Meta:
        model = Actividad

    nombre = Faker('word')
    descripcion = Faker('text', max_nb_chars=100)
    capacidad_maxima = 20


class HorarioClaseFactory(DjangoModelFactory):
    class Meta:
        model = HorarioClase

    actividad = SubFactory(ActividadFactory)
    dia_semana = 'LUN'
    hora_inicio = '09:00:00'
    hora_fin = '10:00:00'
    sala = 'Sala 1'


class InscripcionFactory(DjangoModelFactory):
    class Meta:
        model = Inscripcion

    miembro = SubFactory(MiembroFactory)
    horario = SubFactory(HorarioClaseFactory)
    estado = 'ACTIVA'


class EntrenadorFactory(DjangoModelFactory):
    class Meta:
        model = Entrenador

    nombre = Faker('first_name')
    apellido = Faker('last_name')
    especialidad = Faker('word')
    email = Faker('email')
    telefono = Faker('numerify', text='1#########')
    activo = True


# Fixtures
@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def admin_user(db):
    user = UserFactory(username='admin')
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    user.groups.add(admin_group)
    return user


@pytest.fixture
def recepcion_user(db):
    user = UserFactory(username='recepcion')
    recepcion_group, _ = Group.objects.get_or_create(name='Recepcion')
    user.groups.add(recepcion_group)
    return user


@pytest.fixture
def miembro(db):
    return MiembroFactory()


@pytest.fixture
def carnet(db):
    return CarnetFactory()


@pytest.fixture
def tipo_membresia(db):
    return TipoMembresiaFactory()


@pytest.fixture
def membresia(db, miembro, tipo_membresia):
    return MembresiaFactory(miembro=miembro, tipo=tipo_membresia)


@pytest.fixture
def cobro(db, miembro, membresia):
    return CobroFactory(miembro=miembro, membresia=membresia)


@pytest.fixture
def actividad(db):
    return ActividadFactory()


@pytest.fixture
def horario(db, actividad):
    return HorarioClaseFactory(actividad=actividad)


@pytest.fixture
def inscripcion(db, miembro, horario):
    return InscripcionFactory(miembro=miembro, horario=horario)


@pytest.fixture
def entrenador(db):
    return EntrenadorFactory()


@pytest.fixture
def client():
    from django.test import Client
    return Client()
