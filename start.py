#!/usr/bin/env python
import os
import sys
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=" * 50, file=sys.stderr)
print("🔄 Running migrations...", file=sys.stderr)
print("=" * 50, file=sys.stderr)
result = subprocess.run([sys.executable, "manage.py", "migrate"])
if result.returncode != 0:
    print("❌ Migrations FAILED!", file=sys.stderr)
    sys.exit(1)

print("\n" + "=" * 50, file=sys.stderr)
print("👤 Creating default user...", file=sys.stderr)
print("=" * 50, file=sys.stderr)
subprocess.run([sys.executable, "manage.py", "create_default_user"])

print("\n" + "=" * 50, file=sys.stderr)
print("📦 Collecting static files...", file=sys.stderr)
print("=" * 50, file=sys.stderr)
subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"])

print("\n" + "=" * 50, file=sys.stderr)
print("🚀 Starting gunicorn...", file=sys.stderr)
print("=" * 50, file=sys.stderr)
subprocess.run(["gunicorn", "cuerposano.wsgi:application"])
