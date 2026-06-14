# Desarrollo de Cuerpo Sano

Documento que registra el proceso de construcción de la aplicación Django **Cuerpo Sano** — Sistema de gestión de gimnasio.

**Presentación:** Jueves 18 de junio de 2026  
**Status:** En construcción (Paso 4/13 completado)

---

## Decisiones Arquitectónicas

### Stack
- **Backend:** Django 5.0 + Python 3.13
- **Base de datos:** PostgreSQL (Neon.tech en prod) / SQLite (dev local)
- **Frontend:** DaisyUI (CDN) + Alpine.js + Tailwind 3 — sin build step
- **Fotos/Barcode:** Cloudinary (django-cloudinary-storage)
- **Async:** django-q2 con PostgreSQL broker
- **Testing:** pytest-django + factory-boy
- **Deploy:** Render.com con Gunicorn + Whitenoise

### Por qué NO usar
- **WeasyPrint** → riesgo de dependencias de sistema en Render
- **django-crispy-forms** → clases generadas no son DaisyUI
- **Node.js/Tailwind CLI** → CDN de DaisyUI cubre todo
- **django-guardian** → 3 roles fijos, Groups nativos suficiente
- **Almacenamiento local** → siempre Cloudinary para prod

---

## Paso 1: Proyecto + Configuración + Base Template

**Objetivo:** Estructura base con settings correcto, templates, y autenticación lista

### Qué se hizo

1. **Creación del proyecto**
   ```bash
   django-admin startproject cuerposano
   ```
   Creadas 7 apps: `miembros`, `membresias`, `asistencia`, `actividades`, `entrenadores`, `cobros`, `reportes`

2. **Configuración de `settings.py`**
   - Variables de entorno vía `python-dotenv` (DATABASE_URL, SECRET_KEY, CLOUDINARY_URL)
   - `dj_database_url` para PostgreSQL/SQLite flexible
   - Cloudinary storage para archivos (fotos, códigos de barras)
   - Whitenoise para static files en producción
   - django-q2 config con PostgreSQL broker
   - Zona horaria: América/Argentina/Buenos Aires
   - AUTH: Groups nativos (sin django-guardian)
   - LOGIN_URL y LOGIN_REDIRECT_URL configurados

3. **Base template (`templates/base.html`)**
   - DaisyUI CDN + Alpine.js CDN
   - Navbar responsive con logo
   - Navegación condicional según grupo del usuario
   - Messages/alerts integrados
   - Soporte para @media print (sin display nav, footer)
   - Footer minimalista

4. **Archivo `.env.example`**
   - Template para variables de entorno local
   - Incluye DATABASE_URL, CLOUDINARY_URL, BIOMETRIC_COLUMN_KEY

### Cómo se hizo

**Venv y dependencias:**
```bash
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt  # pytest, factory-boy, etc.
```

**Settings clave:**
```python
load_dotenv()  # Cargar .env
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'
DATABASES = dj_database_url.config(ssl_require=not DEBUG)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

**URLs raíz:**
```python
path('', views.home_redirect)  # Redirige según grupo
path('accounts/', include('django.contrib.auth.urls'))  # Login/logout nativo
path('healthz', views.healthz)  # Health check para Render
```

---

## Paso 2: Autenticación + Grupos + Redirects

**Objetivo:** Login funcional, permisos por rol, navegación según grupo

### Qué se hizo

1. **Templates de autenticación**
   - `templates/registration/login.html` — Tarjeta DaisyUI centrada
   - `templates/registration/logged_out.html` — Confirmación de logout
   - Inputs con clases DaisyUI (`input input-bordered`)
   - Manejo de errores: non_field_errors, field-specific

2. **Vista de home con redirección por grupo**
   ```python
   @login_required
   def home_redirect(request):
       if request.user.groups.filter(name='Recepcion').exists():
           return redirect('asistencia:registro')
       elif request.user.groups.filter(name='Entrenador').exists():
           return redirect('entrenadores:lista')
       else:  # Admin
           return redirect('miembros:lista')
   ```

3. **Creación automática de grupos**
   - Data migration (`miembros/migrations/0002_create_groups.py`)
   - Crea 3 grupos: Admin, Recepcion, Entrenador
   - Reversible con delete_groups

4. **Custom template filter**
   - `miembros/templatetags/custom_tags.py` → filter `has_group`
   - Uso en base.html: `{% if user|has_group:"Admin" %}`

5. **Navegación condicional en base.html**
   - Botones diferentes según rol:
     - **Admin:** Miembros, Membresías, Actividades, Cobros, Reportes
     - **Recepcion:** Asistencia, Miembros, Cobros
     - **Entrenador:** Mi Asistencia, Actividades

6. **Usuario de prueba**
   - Superusuario `admin`/`admin123` creado en shell
   - Agregado al grupo Admin

### Cómo se hizo

**Grupos en migration:**
```python
def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='Admin')
    Group.objects.get_or_create(name='Recepcion')
    Group.objects.get_or_create(name='Entrenador')
```

**Template filter:**
```python
@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
```

**En base.html:**
```html
{% load custom_tags %}
{% if user|has_group:"Admin" %}
    <a href="{% url 'miembros:lista' %}">Miembros</a>
    ...
{% endif %}
```

---

## Paso 3: App Miembros (CRUD + Carnet + Código de Barras)

**Objetivo:** Gestión completa de miembros con generación automática de carnets con código de barras

### Qué se hizo

1. **Modelos**
   - `Miembro`: nombre, apellido, DNI (unique), email, teléfono, foto (CloudinaryField), tipo_miembro (REGULAR/ESTUDIANTE/MAYOR), activo, fecha_alta
   - `Carnet`: OneToOne con Miembro, número_carnet (formato CS-00001), código_barras_imagen (CloudinaryField), fecha_emision
   - Validación de foto máx. 5MB en clean()

2. **Formulario (`forms.py`)**
   ```python
   class MiembroForm(forms.ModelForm):
       widgets = {
           'nombre': TextInput(attrs={'class': 'input input-bordered w-full'}),
           'tipo_miembro': Select(attrs={'class': 'select select-bordered w-full'}),
           ...
       }
   ```
   - Todos los campos con clases DaisyUI
   - File input para foto con accept="image/*"

3. **Vistas CRUD**
   - `lista_miembros()` — Tabla con 7 columnas, ordenada por fecha_alta descendente
   - `crear_miembro()` — POST salva, trigger signal para carnet
   - `detalle_miembro()` — Perfil con foto, carnet, membresías relacionadas
   - `editar_miembro()` — Pre-poblado con datos actuales
   - `ver_carnet()` — Template print (código de barras + foto + DNI)

4. **Signal para carnet automático**
   - `miembros/signals.py`: en `post_save` de Miembro, crea Carnet
   - Genera número: `CS-{miembro.id:05d}` (ej: CS-00001)
   - Genera barcode Code128 vía `python-barcode` + Cloudinary
   - Si no hay CLOUDINARY_URL, usa placeholder

5. **Utilidades**
   - `miembros/utils.py`: `generar_barcode_cloudinary(numero)`
   - Convierte string a barcode Code128
   - Sube BytesIO a Cloudinary con folder='carnets'
   - Retorna secure_url o None

6. **Templates**
   - `lista.html` — Tabla responsive con links a Ver/Editar/Carnet
   - `form.html` — Formulario grid 2 cols (nombre/apellido, DNI/email, etc.)
   - `detalle.html` — Card con info + foto + carnet preview
   - `carnet_print.html` — Tarjeta ISO/CE (85.6×53.98 mm) con @media print

7. **Admin**
   - Miembro registrado con list_display, list_filter, search_fields
   - Carnet read-only excepto creación vía signal

### Cómo se hizo

**Signal sin importación circular:**
- Función de barcode en `utils.py` (evita ciclo views → signals → views)
- Signal importa de utils: `from .utils import generar_barcode_cloudinary`
- En apps.py: `def ready(self): import miembros.signals`

**Carnet printable:**
```html
<style>
    .carnet {
        width: 85.6mm;
        height: 53.98mm;
        display: flex;
    }
    @media print {
        .no-print { display: none; }
        .carnet { page-break-after: avoid; }
    }
</style>
```

**Flujo de creación de miembro:**
1. Usuario POST en `/miembros/nuevo/`
2. Validación de formulario (foto < 5MB, DNI único)
3. `form.save()` crea Miembro
4. Signal `post_save` se dispara
5. Signal genera carnet con código de barras
6. Redirect a detalle del miembro

---

## Paso 4: App Membresias (Tipos + Membresías + Auto-actualización)

**Objetivo:** Gestión de tipos de membresía y membresías de miembros con actualización automática de estados

### Qué se hizo

1. **Modelos**
   - `TipoMembresia`: nombre, descripción, precio (MinValueValidator 0.01), duracion_dias
   - `Membresia`: miembro (FK), tipo (FK/PROTECT), fecha_inicio, fecha_fin (calculado en save()), estado (ACTIVA/VENCIDA/CANCELADA)
   - save() de Membresia calcula fecha_fin = fecha_inicio + tipo.duracion_dias

2. **Formulario (`forms.py`)**
   ```python
   class MembresiaForm(forms.ModelForm):
       miembro = forms.ModelChoiceField(
           queryset=Miembro.objects.filter(activo=True),
           widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
       )
       class Meta:
           model = Membresia
           fields = ['miembro', 'tipo', 'fecha_inicio']
   ```
   - Solo muestra miembros activos
   - fecha_fin se calcula automáticamente (no es editable)

3. **Vistas CRUD**
   - `lista_membresias()` — Tabla de membresías con estado badge
   - `crear_membresia()` — POST crea Membresia y calcula fecha_fin
   - `detalle_membresia()` — Card con info de miembro + tipo + fechas
   - `editar_membresia()` — Solo permite editar si estado es ACTIVA
   - `print_membresia()` — Comprobante imprimible con fechas y precio
   - `lista_tipos()` — Grid de tipos de membresía disponibles
   - `crear_tipo()` — Crea nuevo tipo de membresía
   - `editar_tipo()` — Edita tipo existente

4. **Tarea django-q2 automática**
   - `membresias/tasks.py`: `actualizar_estados_membresias()`
   - Se ejecuta diariamente (schedule: 'daily')
   - Busca membresías ACTIVA con fecha_fin < hoy y las marca como VENCIDA
   - Configurada en settings.py bajo Q_CLUSTER['scheduled']

5. **Templates**
   - `lista.html` — Tabla con 7 columnas, estado badges color-coded
   - `form.html` — Formulario para crear/editar membresía
   - `detalle.html` — Card con info de miembro + tipo + estado + fechas
   - `print.html` — Comprobante printable con DaisyUI (100% CSS, no WeasyPrint)
   - `lista_tipos.html` — Grid de tarjetas de tipos
   - `form_tipo.html` — Formulario para crear/editar tipo

6. **URLs**
   ```python
   path('', lista_membresias, name='lista'),
   path('nueva/', crear_membresia, name='crear'),
   path('<int:pk>/', detalle_membresia, name='detalle'),
   path('<int:pk>/editar/', editar_membresia, name='editar'),
   path('<int:pk>/print/', print_membresia, name='print'),
   path('tipos/', lista_tipos, name='lista_tipos'),
   path('tipos/nuevo/', crear_tipo, name='crear_tipo'),
   path('tipos/<int:pk>/editar/', editar_tipo, name='editar_tipo'),
   ```

7. **Admin**
   - TipoMembresiaAdmin: list_display (nombre, precio, duracion_dias)
   - MembresiaAdmin: list_display (miembro, tipo, fecha_inicio, fecha_fin, estado), readonly_fields (fecha_fin)

### Cómo se hizo

**Dato de prueba:**
```bash
# Crear 3 tipos de membresía
TipoMembresia.objects.create(nombre='Básica', precio=50, duracion_dias=30)
TipoMembresia.objects.create(nombre='Premium', precio=100, duracion_dias=30)
TipoMembresia.objects.create(nombre='Anual', precio=500, duracion_dias=365)
```

**Flujo de creación:**
1. Usuario accede `/membresias/nueva/`
2. Selecciona miembro (solo activos), tipo, fecha_inicio
3. Form valida y POST
4. Membresia.save() calcula fecha_fin
5. Redirect a detalle

**Auto-update de estado:**
- django-q2 task corre diariamente
- QuerySet: Membresia.objects.filter(estado='ACTIVA', fecha_fin__lt=today).update(estado='VENCIDA')
- Sin necesidad de intervención manual

**Fix pendiente:**
- Se agregó 'testserver' a ALLOWED_HOSTS para permitir tests con Client()
- Se corrigió base.html: {% url 'logout' %} en lugar de 'django.contrib.auth.logout'

---

## Estado Actual

### ✅ Completado
- Paso 1: Proyecto + settings + base.html
- Paso 2: Auth (login/logout/grupos/redirects)
- Paso 3: Miembros (CRUD + carnet + barcode)
- Paso 4: Membresias (CRUD + tipos + auto-update de estado con django-q2)

### ⏳ Próximos pasos
- Paso 5: App asistencia (registro por barcode + listado)
- Paso 6: App cobros (descuento automático + comprobante print)
- Paso 7: App actividades (CRUD + horarios + inscripciones)
- Paso 8: App entrenadores (CRUD + asistencia de entrenador)
- Paso 9: App reportes (3 vistas sin modelos)
- Paso 10: Healthz + auditlog
- Paso 11: Tests (pytest)
- Paso 12: Deploy (Render)
- Paso 13: RF-11 biométrico (stub con WebSocket)

---

## Patrones Usados

### Importación circular evitada
```python
# ❌ views.py importa generar_barcode
# ❌ signals.py importa de views
# ✅ generar_barcode va en utils.py
# ✅ views.py y signals.py importan de utils.py
```

### Señales registradas
```python
# apps.py ready()
def ready(self):
    import miembros.signals
```

### Formularios con DaisyUI
```python
# Todos los widgets tienen class='input input-bordered w-full'
# o class='select select-bordered w-full'
# Sin crispy-forms
```

### Validaciones
- Foto: máx. 5MB en model.clean()
- DNI: unique=True
- Carnet: OneToOne asegura 1:1 con Miembro
- Formulario: required en ModelForm

### Namespace URLs
```python
# urls.py: include('miembros.urls', namespace='miembros')
# Template: {% url 'miembros:lista' %}
```

---

## Estructura de carpetas actual

```
cuerposano/
├── cuerposano/
│   ├── settings.py (DATABASE_URL, CLOUDINARY, etc.)
│   ├── urls.py (home_redirect, healthz, includes)
│   ├── views.py (healthz, home_redirect)
│   └── wsgi.py
├── miembros/
│   ├── models.py (Miembro, Carnet)
│   ├── forms.py (MiembroForm)
│   ├── views.py (5 vistas CRUD)
│   ├── signals.py (crear_carnet_automatico)
│   ├── utils.py (generar_barcode_cloudinary)
│   ├── admin.py (MiembroAdmin, CarnetAdmin)
│   ├── urls.py
│   ├── apps.py (ready() registra signals)
│   ├── migrations/ (0001_initial, 0002_create_groups)
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── custom_tags.py (filter has_group)
│   └── templates/miembros/
│       ├── lista.html
│       ├── form.html
│       ├── detalle.html
│       └── carnet_print.html
├── membresias/ asistencia/ actividades/ ... (7 apps con stubs)
├── templates/
│   ├── base.html (navbar, messages, footer)
│   └── registration/
│       ├── login.html
│       └── logged_out.html
├── .env (sqlite:///, SECRET_KEY, etc.)
├── .env.example
├── requirements.txt
├── requirements-dev.txt
├── manage.py
└── db.sqlite3
```

---

## Notas para próximos pasos

### App Asistencia
- Modelo Asistencia: miembro (FK), fecha (auto_now_add), hora (auto_now_add), metodo (BARCODE/MANUAL)
- Página `/asistencia/`: input invisible + barcode.js
  - Acumula keystrokes en buffer
  - En Enter: POST JSON {numero_carnet: "CS-00001"}
  - Backend valida carnet existe + membresia activa
  - Toast con resultado (éxito o error)
- Listado con filtros por fecha

### App Cobros
- Descuento según tipo_miembro:
  - ESTUDIANTE: 20%
  - MAYOR: 15%
  - REGULAR: 0%
- Vista POST calcula descuento antes de crear Cobro
- Comprobante auto-crea con número auto-incremental
- Print con @media print similar a carnet

---

## Testing (para paso 11)

Casos mínimos en `conftest.py` / `tests.py`:
1. Crear Miembro → auto-crea Carnet
2. Validación foto < 5MB
3. DNI unique
4. Descuento ESTUDIANTE = 20%
5. Asistencia por barcode válido → HTTP 200
6. Barcode miembro inactivo → rechazado

---

## Deploy (para paso 12)

**Render.com:**
- Procfile: `web: gunicorn cuerposano.wsgi --workers 2`
- Variables de entorno: SECRET_KEY, DATABASE_URL (Neon), CLOUDINARY_URL
- Static files: Whitenoise + CompressedManifestStaticFilesStorage
- Healthz: `/healthz/` para uptime monitoring

---

**Fecha de inicio:** 2026-06-13  
**Fecha de este documento:** 2026-06-13  
**Próxima actualización:** Al completar paso 4 (membresias)
