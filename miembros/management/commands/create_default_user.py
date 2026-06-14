from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Crea un usuario admin por defecto si no existe'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@cuerposano.local',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('✓ Usuario admin creado'))
            self.stdout.write('  Usuario: admin')
            self.stdout.write('  Contraseña: admin123')
        else:
            self.stdout.write('✓ Usuario admin ya existe')
