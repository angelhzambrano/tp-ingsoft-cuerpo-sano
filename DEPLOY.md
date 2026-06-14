# 🚀 Deploy a Render - Cuerpo Sano

## Paso 1: Preparar el repositorio

Asegúrate de que todos los cambios estén committed:

```bash
git status
git add .
git commit -m "Paso 12: Preparar deploy a Render"
git push origin main
```

## Paso 2: Crear cuenta en Render

1. Ir a https://render.com
2. Sign Up con GitHub (recomendado)
3. Autorizar acceso a tus repositorios

## Paso 3: Crear Web Service

### Opción A: Manual (interfaz Render)

1. En dashboard de Render → **+ New**
2. Seleccionar **Web Service**
3. Buscar y conectar tu repositorio `cuerposano`
4. Configurar:
   - **Name**: `cuerpo-sano`
   - **Region**: `New Jersey (USA)` o más cercano a ti
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn cuerposano.wsgi:application`
   - **Plan**: Free (o Starter si necesitas uptime)

### Opción B: Automática (render.yaml)

```bash
git push origin main
# Render auto-detectará render.yaml en el repo
```

## Paso 4: Configurar variables de entorno

En dashboard Render → tu Web Service → **Environment**:

```
SECRET_KEY=          # Generar: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
DEBUG=False
DATABASE_URL=        # postgresql://user:pass@host/database (desde Neon.tech)
CLOUDINARY_URL=      # cloudinary://key:secret@cloud_name
```

### Obtener DATABASE_URL de Neon.tech:

1. Ir a https://console.neon.tech
2. Crear proyecto PostgreSQL
3. Copiar "Connection string" (incluye usuario/contraseña)
4. Pegarla en DATABASE_URL

## Paso 5: Crear base de datos PostgreSQL (Neon.tech)

Si no tienes base de datos:

1. Ir a https://console.neon.tech
2. Create Project → PostgreSQL
3. Esperar a que se cree (~2 min)
4. Copiar connection string:
   ```
   postgresql://user:password@host/database
   ```
5. Agregar a Render como DATABASE_URL

## Paso 6: Deploy automático

Una vez que has configurado todo:

```bash
git push origin main
# Render auto-detecta cambios y redeploy automático
```

## Paso 7: Ejecutar migrations

El **Procfile** ejecuta automáticamente:
```
python manage.py migrate && python manage.py collectstatic --noinput
```

Esto ocurre durante el **Release Phase** de Render.

## Verificar logs

En Render dashboard → Web Service → **Logs**:

```
# Buscar:
✓ "Running migrations"
✓ "Collecting static files"
✓ "Listening on 0.0.0.0:PORT"
```

## Probar la aplicación

1. Copiar URL del Web Service desde dashboard Render
2. Visitar: `https://cuerpo-sano.onrender.com`
3. Ir a `/admin` con usuario superuser:
   ```bash
   # Ejecutar en Render shell:
   python manage.py createsuperuser
   ```

## Troubleshooting

### Error: "Module not found"
```bash
# Verificar requirements.txt contiene todos los paquetes
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Error: "Static files not found"
```
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

Render ejecuta `collectstatic` automáticamente.

### Error: "Database connection refused"
- Verificar DATABASE_URL es correcto
- Verificar PostgreSQL está corriendo en Neon.tech
- Probar connection local primero

### Error: "SECRET_KEY not set"
- Asegurar que SECRET_KEY está en Render environment variables
- No debe estar en .env (por seguridad)

## Monitoreo en producción

### Health check
```
curl https://cuerpo-sano.onrender.com/healthz
# Respuesta: {"status": "ok"}
```

### Ver logs en tiempo real
```bash
# Render dashboard → Logs
# O conectar terminal SSH (plan Starter+)
```

## Próximos pasos

- Configurar dominio personalizado en Render
- Agregar Sentry para error tracking
- Configurar backups automáticos en Neon.tech
- Paso 13: Integración biométrica (RF-11)

---

**Fecha deployment**: 2026-06-14  
**Deadline presentación**: 2026-06-18
