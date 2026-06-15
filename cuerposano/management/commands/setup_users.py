from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    help = 'Crear usuarios de prueba para todos los roles'

    def handle(self, *args, **options):
        users_data = [
            {
                'username': 'admin',
                'password': 'admin123',
                'email': 'admin@test.com',
                'first_name': 'Administrador',
                'last_name': 'Principal',
                'group': 'Admin'
            },
            {
                'username': 'recepcion',
                'password': '123456',
                'email': 'recepcion@test.com',
                'first_name': 'Recepción',
                'last_name': 'Staff',
                'group': 'Recepcion'
            },
            {
                'username': 'entrenador',
                'password': '123456',
                'email': 'entrenador@test.com',
                'first_name': 'Entrenador',
                'last_name': 'Principal',
                'group': 'Entrenador'
            },
            {
                'username': 'juan_miembro',
                'password': '123456',
                'email': 'juan.miembro@test.com',
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'group': 'Miembro'
            },
        ]

        for user_data in users_data:
            username = user_data['username']
            group_name = user_data.pop('group')

            if User.objects.filter(username=username).exists():
                self.stdout.write(f"⚠️  Usuario '{username}' ya existe")
            else:
                user = User.objects.create_user(**user_data)
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ Usuario '{username}' creado en grupo '{group_name}'"
                    )
                )

        self.stdout.write(self.style.SUCCESS('\n=== USUARIOS DISPONIBLES ==='))
        for user in User.objects.all():
            groups = list(user.groups.values_list('name', flat=True))
            password = 'admin123' if user.username == 'admin' else '123456'
            self.stdout.write(f"👤 {user.username:15} | Pass: {password:8} | {groups}")
