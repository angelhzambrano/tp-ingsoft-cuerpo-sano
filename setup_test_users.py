#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cuerposano.settings')
django.setup()

from django.contrib.auth.models import User, Group

users_data = [
    ('admin', 'admin123', 'Admin', 'admin@test.com'),
    ('recepcion', '123456', 'Recepcion', 'recepcion@test.com'),
    ('entrenador', '123456', 'Entrenador', 'entrenador@test.com'),
    ('juan_miembro', '123456', 'Miembro', 'juan.miembro@test.com'),
]

# Crear grupos si no existen
group_names = set(g[2] for g in users_data)
for group_name in group_names:
    Group.objects.get_or_create(name=group_name)
    print(f"✅ Grupo '{group_name}' creado/verificado")

print()

# Crear usuarios y asignar a grupos
for username, password, group_name, email in users_data:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email, 'first_name': username}
    )
    if created:
        user.set_password(password)
        user.save()
        print(f"✅ Usuario '{username}' creado")
    else:
        print(f"⚠️  Usuario '{username}' ya existe")

    group = Group.objects.get(name=group_name)
    user.groups.add(group)

print("\n=== USUARIOS DISPONIBLES ===")
for user in User.objects.all():
    groups = list(user.groups.values_list('name', flat=True))
    password = 'admin123' if user.username == 'admin' else '123456'
    print(f"👤 {user.username:15} | Pass: {password:8} | Groups: {groups}")
