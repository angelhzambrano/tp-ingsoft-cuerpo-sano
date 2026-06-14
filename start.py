#!/usr/bin/env python
import os
import sys
import subprocess

print("\n[START] Initializing startup script - v2", file=sys.stderr)
print(f"[START] Python: {sys.executable}", file=sys.stderr)
print(f"[START] Initial CWD: {os.getcwd()}", file=sys.stderr)

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print(f"[START] Changed CWD to: {os.getcwd()}", file=sys.stderr)
print(f"[START] manage.py exists: {os.path.exists('manage.py')}", file=sys.stderr)
print(f"[START] Procfile exists: {os.path.exists('Procfile')}", file=sys.stderr)

print("\n" + "=" * 60, file=sys.stderr)
print("🔄 RUNNING MIGRATIONS", file=sys.stderr)
print("=" * 60, file=sys.stderr)

result = subprocess.run(
    [sys.executable, "manage.py", "migrate", "--verbosity=2"],
    capture_output=True,
    text=True
)

print(f"[MIGRATE] Return code: {result.returncode}", file=sys.stderr)
print(f"[MIGRATE] STDOUT:\n{result.stdout}", file=sys.stderr)
if result.stderr:
    print(f"[MIGRATE] STDERR:\n{result.stderr}", file=sys.stderr)

if result.returncode != 0:
    print("\n❌ MIGRATIONS FAILED - SEE OUTPUT ABOVE", file=sys.stderr)
    print(f"[DEBUG] Last stdout line: {result.stdout.splitlines()[-1] if result.stdout else 'N/A'}", file=sys.stderr)
    sys.exit(1)

print("\n" + "=" * 60, file=sys.stderr)
print("👤 CREATING DEFAULT USER", file=sys.stderr)
print("=" * 60, file=sys.stderr)

result = subprocess.run(
    [sys.executable, "manage.py", "create_default_user"],
    capture_output=True,
    text=True
)
print(f"[USER] Return code: {result.returncode}", file=sys.stderr)
print(f"[USER] Output: {result.stdout}", file=sys.stderr)
if result.stderr:
    print(f"[USER] Errors: {result.stderr}", file=sys.stderr)

print("\n" + "=" * 60, file=sys.stderr)
print("📦 COLLECTING STATIC FILES", file=sys.stderr)
print("=" * 60, file=sys.stderr)

result = subprocess.run(
    [sys.executable, "manage.py", "collectstatic", "--noinput", "--verbosity=1"],
    capture_output=True,
    text=True
)
print(f"[STATIC] Return code: {result.returncode}", file=sys.stderr)
print(f"[STATIC] Output: {result.stdout}", file=sys.stderr)

print("\n" + "=" * 60, file=sys.stderr)
print("🚀 STARTING GUNICORN", file=sys.stderr)
print("=" * 60, file=sys.stderr)

subprocess.run(["gunicorn", "cuerposano.wsgi:application"])
