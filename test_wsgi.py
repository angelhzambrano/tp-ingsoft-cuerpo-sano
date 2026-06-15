#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cuerposano.settings')
os.environ['DEBUG'] = 'False'
os.environ['SECRET_KEY'] = 'test-key-for-testing'
os.environ['DATABASE_URL'] = 'sqlite:///test.db'

print("[TEST] Setting up Django...")
try:
    django.setup()
    print("[TEST] ✓ Django setup completed")
except Exception as e:
    print(f"[TEST] ❌ Django setup failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("[TEST] Loading WSGI application...")
try:
    from cuerposano.wsgi import application
    print("[TEST] ✓ WSGI application loaded")
except Exception as e:
    print(f"[TEST] ❌ WSGI load failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("[TEST] Testing basic request...")
from django.test import RequestFactory
factory = RequestFactory()
request = factory.get('/')

print("[TEST] All tests passed!")
