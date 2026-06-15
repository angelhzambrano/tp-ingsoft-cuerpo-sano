from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import timedelta, time
from miembros.models import Miembro
from entrenadores.models import Entrenador
from actividades.models import Actividad, HorarioClase
from membresias.models import TipoMembresia, Membresia


class Command(BaseCommand):
    help = 'Crear datos de prueba para desarrollo (idempotente y seguro)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Forzar recreación de datos',
        )

    def handle(self, *args, **options):
        force = options['force']

        # 1. Crear grupos
        self.stdout.write('📋 Creando grupos...')
        groups_data = ['Admin', 'Recepcion', 'Entrenador', 'Miembro']
        groups = {}
        for name in groups_data:
            group, created = Group.objects.get_or_create(name=name)
            groups[name] = group
            status = '✓ nuevo' if created else '→ existe'
            self.stdout.write(f'  {status}: {name}')

        # 2. Crear usuarios
        self.stdout.write('\n👤 Creando usuarios...')
        users_data = [
            ('admin', 'admin123', 'Admin', 'admin@test.com'),
            ('recepcion', '123456', 'Recepcion', 'recepcion@test.com'),
            ('entrenador', '123456', 'Entrenador', 'entrenador@test.com'),
            ('juan_miembro', '123456', 'Miembro', 'juan.miembro@test.com'),
        ]

        users = {}
        for username, password, group_name, email in users_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )

            if created or force:
                user.set_password(password)
                user.save()
                status = '✓ nuevo'
            else:
                status = '→ existe'

            # Agregar al grupo
            user.groups.clear()
            user.groups.add(groups[group_name])
            users[username] = user

            self.stdout.write(f'  {status}: {username} ({group_name})')

        # 3. Crear Miembro para juan_miembro
        self.stdout.write('\n👥 Creando registros de miembros...')
        miembro, created = Miembro.objects.get_or_create(
            dni='12345679',
            defaults={
                'nombre': 'Juan',
                'apellido': 'Pérez',
                'email': 'juan.miembro@test.com',
                'tipo_miembro': 'REGULAR',
                'activo': True,
            }
        )

        # Vincular usuario
        if miembro.usuario_id != users['juan_miembro'].id:
            miembro.usuario = users['juan_miembro']
            miembro.save()
            status = '✓ vinculado'
        else:
            status = '→ vinculado'

        self.stdout.write(f'  {status}: Juan Pérez → juan_miembro')

        # 4. Crear Entrenador
        self.stdout.write('\n🏋️  Creando entrenadores...')
        entrenador, created = Entrenador.objects.get_or_create(
            email='entrenador@test.com',
            defaults={
                'nombre': 'Entrenador',
                'apellido': 'Principal',
                'especialidad': 'Entrenamiento General',
                'telefono': '555-0001',
                'activo': True,
            }
        )

        # Vincular usuario
        if entrenador.usuario_id != users['entrenador'].id:
            entrenador.usuario = users['entrenador']
            entrenador.save()
            status = '✓ vinculado'
        else:
            status = '→ vinculado'

        self.stdout.write(f'  {status}: Entrenador Principal → entrenador')

        # 5. Crear actividades
        self.stdout.write('\n🏃 Creando actividades...')
        actividades_data = [
            ('Spinning', 'Clases de ciclismo indoor de alta intensidad', 20),
            ('Yoga', 'Clases de yoga para relajación y flexibilidad', 15),
            ('Pilates', 'Ejercicios de pilates para core y postura', 12),
            ('Pesas', 'Entrenamiento con pesas y resistencia', 25),
        ]

        actividades = {}
        for nombre, desc, capacidad in actividades_data:
            act, created = Actividad.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': desc, 'capacidad_maxima': capacidad}
            )
            actividades[nombre] = act
            status = '✓ nueva' if created else '→ existe'
            self.stdout.write(f'  {status}: {nombre}')

        # 6. Crear horarios de clases
        self.stdout.write('\n📅 Creando horarios...')
        horarios_data = [
            ('Spinning', 'LUN', '07:00', '08:00'),
            ('Spinning', 'MIE', '18:30', '19:30'),
            ('Yoga', 'MAR', '09:00', '10:30'),
            ('Yoga', 'JUE', '18:00', '19:30'),
            ('Pilates', 'LUN', '10:00', '11:00'),
            ('Pilates', 'VIE', '15:00', '16:00'),
            ('Pesas', 'MAR', '06:00', '07:00'),
            ('Pesas', 'SAB', '10:00', '11:30'),
        ]

        horarios_count = 0
        for actividad_name, dia, h_inicio_str, h_fin_str in horarios_data:
            actividad = actividades[actividad_name]
            # Convertir strings a objetos time
            h_inicio = time(*map(int, h_inicio_str.split(':')))
            h_fin = time(*map(int, h_fin_str.split(':')))

            horario, created = HorarioClase.objects.get_or_create(
                actividad=actividad,
                dia_semana=dia,
                hora_inicio=h_inicio,
                hora_fin=h_fin,
                defaults={
                    'entrenador': entrenador,
                    'sala': f'Sala {actividad_name}',
                }
            )
            if created:
                horarios_count += 1
                self.stdout.write(f'    ✓ {actividad_name} - {dia} {h_inicio_str}-{h_fin_str}')

        self.stdout.write(f'  Total: {horarios_count} horarios nuevos')

        # 7. Crear tipos de membresía
        self.stdout.write('\n💳 Creando tipos de membresía...')
        tipos_data = [
            ('Plan Mensual', 'Acceso ilimitado por 30 días', 29.99, 30),
            ('Plan Trimestral', 'Acceso ilimitado por 90 días', 79.99, 90),
            ('Plan Anual', 'Acceso ilimitado por 365 días', 249.99, 365),
            ('Plan Estudiante', 'Descuento para estudiantes - 30 días', 14.99, 30),
        ]

        tipos_membresia = {}
        for nombre, desc, precio, duracion in tipos_data:
            tipo, created = TipoMembresia.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': desc, 'precio': precio, 'duracion_dias': duracion}
            )
            tipos_membresia[nombre] = tipo
            status = '✓ nuevo' if created else '→ existe'
            self.stdout.write(f'  {status}: {nombre}')

        # 8. Asignar membresía activa a juan_miembro
        self.stdout.write('\n📋 Asignando membresías...')
        membresia, created = Membresia.objects.get_or_create(
            miembro=miembro,
            defaults={
                'tipo': tipos_membresia['Plan Mensual'],
                'fecha_inicio': timezone.now().date(),
                'fecha_fin': timezone.now().date() + timedelta(days=30),
                'estado': 'ACTIVA'
            }
        )
        status = '✓ nueva' if created else '→ existe'
        self.stdout.write(f'  {status}: Plan Mensual → Juan Pérez')

        self.stdout.write('\n✅ Setup completado exitosamente!\n')
        self.stdout.write(self.style.SUCCESS('Credenciales de prueba:'))
        self.stdout.write('  admin / admin123')
        self.stdout.write('  recepcion / 123456')
        self.stdout.write('  entrenador / 123456')
        self.stdout.write('  juan_miembro / 123456')
