from django.core.management.base import BaseCommand
from miembros.models import Miembro, Carnet
from membresias.models import Membresia, PlanMembresia
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Crea datos de prueba para demostración'

    def handle(self, *args, **options):
        # Crear plan si no existe
        plan, created = PlanMembresia.objects.get_or_create(
            nombre="Plan Mensual",
            defaults={'precio': 50000, 'duracion_dias': 30}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Plan creado'))

        # Crear miembros de prueba
        miembros_data = [
            ('Juan', 'Pérez', '12345679', 'juan@test.com'),
            ('María', 'García', '12345680', 'maria@test.com'),
            ('Carlos', 'Martinez', '12345681', 'carlos@test.com'),
            ('Ana', 'López', '12345682', 'ana@test.com'),
        ]

        for i, (nombre, apellido, dni, email) in enumerate(miembros_data, 1):
            miembro, created = Miembro.objects.get_or_create(
                dni=dni,
                defaults={
                    'nombre': nombre,
                    'apellido': apellido,
                    'email': email,
                    'telefono': '1111111111',
                    'tipo_miembro': 'REGULAR',
                    'activo': True
                }
            )
            
            # Crear carnet
            carnet, _ = Carnet.objects.get_or_create(
                miembro=miembro,
                defaults={'numero_carnet': f'CS-000{i}'}
            )
            
            # Crear membresía
            Membresia.objects.get_or_create(
                miembro=miembro,
                defaults={
                    'plan': plan,
                    'fecha_inicio': datetime.now().date(),
                    'fecha_fin': datetime.now().date() + timedelta(days=30),
                    'estado': 'ACTIVA'
                }
            )
            
            if created:
                self.stdout.write(f'✓ {miembro} (carnet: {carnet.numero_carnet})')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Datos de prueba creados'))
