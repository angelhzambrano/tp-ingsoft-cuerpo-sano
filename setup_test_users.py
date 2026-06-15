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

for username, password, group_name, email in users_data:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email, 'first_name': username}
    )
    if created:
        user.set_password(password)
        user.save()

    try:
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        print(f"✅ {username} -> {group_name}")
    except Group.DoesNotExist:
        print(f"⚠️  Grupo {group_name} no existe para {username}")

print("✅ Setup completado")
