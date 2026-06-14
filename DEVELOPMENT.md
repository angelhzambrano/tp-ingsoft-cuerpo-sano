# Desarrollo de Cuerpo Sano

Documento que registra el proceso de construcción de la aplicación Django **Cuerpo Sano** — Sistema de gestión de gimnasio.

**Presentación:** Jueves 18 de junio de 2026  
**Status:** En construcción (Paso 11/13 completado)

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

## Paso 5: App Asistencia (Scanner de Código de Barras + Listado)

**Objetivo:** Registro rápido de asistencias por código de barras con validación de membresía

### Qué se hizo

1. **Modelo**
   - `Asistencia`: miembro (FK), fecha (auto_now_add), hora (auto_now_add), metodo (BARCODE/MANUAL)
   - Ya existía con campos correctos

2. **Vistas**
   - `registro_asistencia()` — GET: renderiza página con scanner + input manual
   - `registrar_por_barcode()` — POST AJAX JSON, valida carnet + membresía ACTIVA, crea Asistencia, retorna {success, message, miembro}
   - `listado_asistencia()` — GET con filtro por fecha (desde/hasta), renderiza tabla con todas las asistencias
   - `registro_manual()` — GET/POST, select de miembro activo, crea Asistencia con metodo=MANUAL

3. **Endpoints**
   ```python
   /asistencia/                    # Página scanner
   /asistencia/api/barcode/        # AJAX POST para procesar barcode
   /asistencia/listado/            # Listado con filtros
   /asistencia/manual/             # Registro manual
   ```

4. **Frontend**
   - `registro.html`:
     - CDN html5-qrcode (barcode.js equivalente)
     - Scanner en vivo con camera
     - Input invisible para capturar enteradas
     - Buffer de últimos escaneos con toast success/error
     - AJAX POST a `/asistencia/api/barcode/`
     - Keypress Enter en input manual también dispara el escaneo
   
   - `lista.html`:
     - Filtro por fecha (desde/hasta)
     - Tabla: miembro, DNI, fecha, hora, método (badge BARCODE/MANUAL)
     - Total de registros
   
   - `registro_manual.html`:
     - Select de miembros activos
     - POST crea Asistencia con metodo=MANUAL

5. **Validaciones en API**
   - Código de barras no vacío
   - Carnet existe (get_object_or_404)
   - Miembro está activo
   - Miembro tiene membresía ACTIVA
   - Transacción atómica en creación

6. **Admin**
   - AsistenciaAdmin: list_display (miembro, fecha, hora, metodo)
   - Filtros por metodo y fecha
   - Búsqueda por nombre/apellido/DNI de miembro
   - Readonly: fecha y hora

### Cómo se hizo

**Scanner HTML5:**
```javascript
const html5QrcodeScanner = new Html5QrcodeScanner(
    "scanner",
    { fps: 10, qrbox: { width: 250, height: 250 } },
    false
);

html5QrcodeScanner.render(onScanSuccess, onScanError);
```

**Validación de membresía:**
```python
membresia = Membresia.objects.filter(
    miembro=miembro,
    estado='ACTIVA'
).first()

if not membresia:
    return JsonResponse({'success': False, 'error': '...'})
```

**AJAX POST:**
```javascript
fetch('/asistencia/api/barcode/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token }}'
    },
    body: JSON.stringify({ numero_carnet: codigo })
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        // Toast success
        lastRegistry.innerHTML = `<p>${data.miembro}</p>`;
    } else {
        // Toast error
    }
});
```

---

## Paso 6: App Cobros (Descuento Automático + Comprobante)

**Objetivo:** Registro de cobros con descuento automático según tipo de miembro

### Qué se hizo

1. **Modelos** (ya existían)
   - `Cobro`: miembro (FK), membresia (FK), monto_base, descuento_porcentaje, monto_final, forma_pago (EFECTIVO/TARJETA/TRANSFERENCIA), fecha (auto_now_add), observaciones
   - `Comprobante`: cobro (OneToOne), numero (AutoField PK), fecha_emision (auto_now_add)

2. **Formulario (`forms.py`)**
   - `CobroForm`: membresia (select ACTIVAS), monto_base, forma_pago, observaciones
   - Validación: monto_base > 0

3. **Lógica de Descuentos**
   ```python
   def calcular_descuento(miembro):
       descuentos = {
           'ESTUDIANTE': 20.00,
           'MAYOR': 15.00,
           'REGULAR': 0.00,
       }
       return descuentos.get(miembro.tipo_miembro, 0.00)
   ```
   - Se aplica automáticamente en POST
   - monto_final = monto_base - (monto_base * descuento% / 100)

4. **Vistas**
   - `lista_cobros()` — Tabla con filtro por forma de pago
   - `registrar_cobro()` — GET: formulario, POST: calcula descuento, crea Cobro + Comprobante
   - `detalle_cobro()` — Card con info completa (miembro, membresía, montos, descuento)
   - `ver_comprobante()` — Template imprimible

5. **Templates**
   - `lista.html` — Tabla: miembro, membresía, montos, forma pago, fecha
   - `form.html` — Formulario con alerta explicando descuentos
   - `detalle.html` — Card grid con: miembro, membresía, montos, forma pago
   - `print.html` — Comprobante printable con logo, número de comprobante, detalle de descuento

6. **URLs**
   ```python
   /cobros/                    # Listado
   /cobros/nuevo/              # Crear
   /cobros/<id>/               # Detalle
   /cobros/<id>/comprobante/   # Imprimir
   ```

7. **Admin**
   - CobroAdmin: list_display (miembro, membresia, montos, forma, fecha), filtros por forma y tipo_miembro
   - ComprobanteAdmin: list_display (numero, cobro, fecha)

### Cómo se hizo

**Flujo de creación:**
1. Usuario POST en `/cobros/nuevo/` con membresia, monto_base, forma_pago
2. Vista calcula: `descuento = monto_base * (tipo_miembro_descuento / 100)`
3. Calcula: `monto_final = monto_base - descuento`
4. Crea Cobro con todos los campos
5. Signal/manual crea Comprobante asociado
6. Redirect a detalle

**Validación:**
- Solo membresías ACTIVAS disponibles en select
- monto_base > 0
- AutoField en Comprobante genera números secuenciales

---

## Paso 7: App Actividades (CRUD + Horarios + Inscripciones)

**Objetivo:** Gestión completa de actividades, horarios y inscripciones con validación de capacidad

### Qué se hizo

1. **Modelos** (ya existían)
   - `Actividad`: nombre, descripción, capacidad_maxima
   - `HorarioClase`: actividad (FK), entrenador (FK/NULL), dia_semana (LUN-SAB), hora_inicio, hora_fin, sala
   - `Inscripcion`: miembro (FK), horario (FK), fecha_inscripcion (auto_now_add), estado (ACTIVA/CANCELADA)
   - Validación en Inscripcion.save(): lanza ValidationError si clase está llena
   - unique_together (miembro, horario) previene inscripciones duplicadas

2. **Formularios (`forms.py`)**
   - `ActividadForm`: nombre, descripcion, capacidad_maxima
   - `HorarioClaseForm`: actividad, entrenador, dia_semana, hora_inicio, hora_fin, sala
     - Validación: hora_fin > hora_inicio
   - `InscripcionForm`: miembro (filtrado a activos), horario
     - Validación en save() de modelo

3. **Vistas CRUD**
   - **Actividades:**
     - `lista_actividades()` — Grid de actividades con capacidad e info rápida
     - `crear_actividad()` — Form para nueva actividad
     - `detalle_actividad()` — Card con info + horarios de esa actividad
     - `editar_actividad()` — Edit form
   
   - **Horarios:**
     - `lista_horarios()` — Tabla global de todos los horarios
     - `crear_horario()` — Form para nuevo horario
     - `editar_horario()` — Edit form
     - `horarios_actividad()` — Cards de horarios específicos con contador de inscritos
   
   - **Inscripciones:**
     - `inscripciones_horario()` — Tabla con miembros inscritos + contador
     - `inscribir_miembro()` — Form para crear inscripción (con validación de capacidad)
     - `cancelar_inscripcion()` — Confirmación + cambio de estado a CANCELADA

4. **URLs**
   ```python
   /actividades/                               # Lista actividades
   /actividades/nueva/                         # Crear actividad
   /actividades/<id>/                          # Detalle actividad
   /actividades/<id>/editar/                   # Editar actividad
   /actividades/<id>/horarios/                 # Horarios de esa actividad
   /actividades/horarios/                      # Lista global de horarios
   /actividades/horarios/nuevo/                # Crear horario
   /actividades/horarios/<id>/editar/          # Editar horario
   /actividades/horarios/<id>/inscripciones/   # Ver inscritos en horario
   /actividades/inscribir/                     # Crear inscripción
   /actividades/inscripcion/<id>/cancelar/     # Cancelar inscripción
   ```

5. **Templates**
   - `lista.html` — Grid de actividades con cards
   - `detalle.html` — Info + horarios asociados
   - `form_actividad.html` — Formulario crear/editar
   - `lista_horarios.html` — Tabla global: actividad, día, hora, entrenador, sala
   - `horarios_actividad.html` — Cards de horarios con contador inscritos/capacidad + badge de disponibilidad
   - `inscripciones_horario.html` — Tabla con miembros inscritos + botón cancelar
   - `form_inscripcion.html` — Formulario seleccionar miembro + horario
   - `confirmar_cancelar.html` — Confirmación antes de cancelar

6. **Admin**
   - ActividadAdmin: list_display (nombre, capacidad, horarios_count)
   - HorarioClaseAdmin: list_display (actividad, dia, horas, entrenador, sala), filtros
   - InscripcionAdmin: list_display (miembro, horario, fecha, estado), filtros

### Validaciones

- **Horario**: hora_fin > hora_inicio (validado en form)
- **Inscripción**: no permite si inscritos >= capacidad (validado en model.save())
- **Inscripción**: unique_together previene duplicados
- **Miembros**: solo activos en selector de inscripciones

### Cómo se hizo

**Validación de capacidad:**
```python
def save(self, *args, **kwargs):
    inscripciones_activas = self.horario.inscripciones.filter(estado='ACTIVA').count()
    if self.pk is None and inscripciones_activas >= self.horario.actividad.capacidad_maxima:
        raise ValidationError('La clase está llena')
    super().save(*args, **kwargs)
```

**Contador en UI:**
```html
<div class="text-3xl font-bold">{{ horario.inscripciones.count }}/{{ actividad.capacidad_maxima }}</div>
{% if horario.inscripciones.count == actividad.capacidad_maxima %}
    <span class="badge badge-error">Lleno</span>
{% endif %}
```

---

## Paso 8: App Entrenadores (CRUD + Asistencia de Entrenador)

**Objetivo:** Gestión de entrenadores con registro de asistencia a clases

### Qué se hizo

1. **Modelos** (ya existían)
   - `Entrenador`: nombre, apellido, especialidad, telefono, email, activo
   - `AsistenciaEntrenador`: entrenador (FK), horario (FK), fecha, tipo (PRESENTE/AUSENTE), justificada, observaciones
   - unique_together (entrenador, horario, fecha) previene duplicados

2. **Formularios (`forms.py`)**
   - `EntrenadorForm`: nombre, apellido, especialidad, telefono, email, activo
   - `AsistenciaEntrenadorForm`: entrenador, horario, fecha, tipo, justificada, observaciones

3. **Vistas CRUD**
   - `lista_entrenadores()` — Tabla de entrenadores con estado activo/inactivo
   - `crear_entrenador()` — Formulario crear entrenador
   - `detalle_entrenador()` — Card con info + últimas asistencias
   - `editar_entrenador()` — Edit form
   - `print_entrenador()` — Reporte imprimible con estadísticas
   - `registro_asistencia_entrenador()` — Form para registrar asistencia
   - `historial_asistencias_entrenador()` — Tabla con todas las asistencias + estadísticas

4. **URLs**
   ```python
   /entrenadores/                                  # Lista entrenadores
   /entrenadores/nuevo/                            # Crear entrenador
   /entrenadores/<id>/                             # Detalle entrenador
   /entrenadores/<id>/editar/                      # Editar entrenador
   /entrenadores/<id>/print/                       # Reporte imprimible
   /entrenadores/<id>/asistencias/                 # Historial asistencias
   /entrenadores/asistencia/registrar/             # Registrar asistencia
   ```

5. **Templates**
   - `lista.html` — Tabla con nombre, especialidad, email, estado, acciones
   - `form.html` — Formulario crear/editar entrenador
   - `detalle.html` — Card info personal + estadísticas + últimas asistencias
   - `print.html` — Reporte imprimible con tabla de asistencias y campos de firma
   - `form_asistencia.html` — Formulario registrar asistencia (entrenador, clase, fecha, estado)
   - `historial_asistencias.html` — Tabla completa con estadísticas (total, presentes, ausentes, justificadas)

6. **Admin**
   - EntrenadorAdmin: list_display (nombre, apellido, especialidad, email, activo), filtros, búsqueda
   - AsistenciaEntrenadorAdmin: list_display (entrenador, horario, fecha, tipo, justificada), filtros, readonly

### Validaciones

- **Asistencia**: unique_together (entrenador, horario, fecha) previene duplicados en mismo día

### Cómo se hizo

**CRUD básico:**
- lista: ORDER BY -activo, apellido (activos primero)
- detalle: muestra últimas 5 asistencias
- print: genera reporte con estadísticas y campo de firmas
- historial: tabla completa + stats (total, presentes, ausentes, justificadas)

**Estadísticas en templates:**
```python
stats = {
    'total': asistencias.count(),
    'presentes': asistencias.filter(tipo='PRESENTE').count(),
    'ausentes': asistencias.filter(tipo='AUSENTE').count(),
    'justificadas': asistencias.filter(justificada=True).count(),
}
```

---

## Paso 9: App Reportes (3 Vistas de Análisis)

**Objetivo:** Generar reportes analíticos SIN crear nuevos modelos, utilizando datos existentes

### Qué se hizo

1. **Sin modelos propios**
   - Reportes utilizan `Asistencia`, `Cobro`, `Membresia` existentes
   - NO se crearon nuevas tablas

2. **Formularios de filtro (`forms.py`)**
   - `FiltroAsistenciasForm`: fecha_inicio, fecha_fin, miembro, metodo
   - `FiltroCobrosForm`: fecha_inicio, fecha_fin, forma_pago, miembro
   - `FiltroMembresiasVencidasForm`: fecha_vencimiento, tipo_miembro

3. **Vistas (3 reportes)**
   - **`reporte_asistencias()`**
     - Filtra por: rango de fechas, miembro específico, método (BARCODE/MANUAL)
     - Stats: total asistencias, miembros únicos, breakdown por método
     - Query: `Asistencia.objects.filter(...)`
   
   - **`reporte_cobros()`**
     - Filtra por: rango de fechas, forma de pago, miembro
     - Stats: total cobros, monto total, descuentos aplicados, breakdown por forma de pago
     - Query: `Cobro.objects.filter(...)` con `Sum` aggregation
   
   - **`membresias_vencidas()`**
     - Filtra por: fecha vencimiento, tipo de miembro
     - Stats: total vencidas, monto no renovado, días promedio sin renovar, breakdown por tipo
     - Query: `Membresia.objects.filter(estado='VENCIDA').filter(...)`

4. **URLs**
   ```python
   /reportes/asistencias/          # Filtrable por fecha, miembro, método
   /reportes/cobros/               # Filtrable por fecha, forma_pago, miembro
   /reportes/membresias-vencidas/  # Filtrable por vencimiento, tipo_miembro
   ```

5. **Templates**
   - `asistencias.html` — Card filtros + stats + tabla con Fecha/Hora/Miembro/DNI/Método
   - `cobros.html` — Card filtros + stats + tabla con Monto/Descuento/Forma Pago
   - `membresias_vencidas.html` — Card filtros + stats + tabla con Fecha vencimiento/Días vencida

### Cómo se hizo

**Agregaciones:**
```python
stats = {
    'total': asistencias.count(),
    'monto_total': cobros.aggregate(Sum('monto_final'))['monto_final__sum'] or 0,
    'miembros_unicos': asistencias.values('miembro').distinct().count(),
}
```

**Filtros dinámicos:**
```python
if form.is_valid():
    if form.cleaned_data.get('fecha_inicio'):
        queryset = queryset.filter(fecha__gte=fecha_inicio)
```

**Sin paginación** — reportes muestran todos los registros (útil para export manual)

---

## Paso 10: Healthz + Auditlog

**Objetivo:** Health check para Render + Registro de auditoría para cambios en Miembro y Cobro

### Qué se hizo

1. **Healthz endpoint (ya existía, mejorado)**
   ```python
   GET /healthz/
   → {'status': 'ok', 'db': 'connected'}
   → Valida conexión a DB
   → Status 503 si falla
   ```
   Usado por Render para comprobar salud del servicio

2. **App historial**
   - Nuevo modelo `AuditLog`: modelo, id_objeto, accion (CREATE/UPDATE/DELETE), usuario, timestamp, cambios, descripcion
   - Índices en: modelo+id_objeto, timestamp, usuario

3. **Signals registrados**
   - `post_save` en Miembro → crea AuditLog con accion=CREATE o UPDATE
   - `post_delete` en Miembro → crea AuditLog con accion=DELETE
   - `post_save` en Cobro → crea AuditLog con accion=CREATE o UPDATE
   - `post_delete` en Cobro → crea AuditLog con accion=DELETE
   - Registrados en `apps.py` con `dispatch_uid` para evitar duplicados

4. **Vistas**
   - `lista_auditlog()` — Tabla filtrable por modelo y acción
   - `auditlog_miembro(id)` — Historial completo de cambios en Miembro específico
   - `auditlog_cobro(id)` — Historial completo de cambios en Cobro específico

5. **URLs**
   ```python
   /historial/auditlog/                    # Tabla general de eventos
   /historial/auditlog/miembro/<id>/       # Historial de Miembro
   /historial/auditlog/cobro/<id>/         # Historial de Cobro
   ```

6. **Templates**
   - `auditlog.html` — Tabla general con filtros (modelo, acción) + links a detalles
   - `auditlog_detalle.html` — Timeline de cambios con usuario y timestamp

7. **Admin**
   - AuditLogAdmin: list_display (timestamp, usuario, modelo, id, accion, descripcion)
   - read-only: no permitir agregar, editar, o eliminar logs (immutable)
   - date_hierarchy por timestamp para navegación rápida

### Cómo se hizo

**Signals en apps.py:**
```python
def ready(self):
    post_save.connect(registrar_cambios_miembro, sender=Miembro, dispatch_uid='audit_miembro_save')
    post_delete.connect(registrar_eliminacion_miembro, sender=Miembro, dispatch_uid='audit_miembro_delete')
```

**Creación de AuditLog:**
```python
AuditLog.objects.create(
    modelo='Miembro',
    id_objeto=instance.id,
    accion='CREATE',
    usuario=request.user,
    descripcion=f'Nuevo miembro: {instance.nombre}'
)
```

**Admin immutable:**
```python
def has_add_permission(self, request):
    return False
def has_delete_permission(self, request, obj=None):
    return False
```

### Nota de implementación

- Sin captura de "cambios específicos" (qué campo cambió de qué a qué) en v1
- Solo registra acción y descripción general
- Extensible para JSONField con diff en futuras versiones
- Apunta a objetos que pueden haber sido eliminados (FK a User solo, no a Miembro/Cobro)

---

## Paso 11: Tests (pytest-django + factory-boy)

**Objetivo:** Suite de tests para validar lógica, modelos, vistas y signals

### Qué se hizo

1. **Configuración pytest**
   - `pytest.ini`: settings Django, cobertura HTML/terminal, markers
   - `conftest.py`: factories y fixtures reutilizables

2. **Factories (conftest.py)**
   - UserFactory, MiembroFactory, CarnetFactory
   - TipoMembresiaFactory, MembresiaFactory
   - CobroFactory, ActividadFactory, HorarioClaseFactory, InscripcionFactory
   - EntrenadorFactory
   - Fixtures: admin_user, recepcion_user, miembro, membresia, cobro, etc.

3. **Test Files (33 casos)**

   **test_miembros.py (7 casos)**
   - ✅ Crear miembro con DNI único
   - ✅ DNI debe ser único (IntegrityError)
   - ✅ Representación string
   - ✅ Carnet creado automáticamente (signal)
   - ✅ Relación 1:1 Carnet-Miembro
   - ✅ Lista requiere login
   - ✅ Validación de formulario

   **test_membresias.py (5 casos)**
   - ✅ Crear membresía con fecha_fin calculada
   - ✅ Estado vencida
   - ✅ Crear tipo de membresía
   - ✅ Representación string
   - ✅ Múltiples membresías ACTIVAS por miembro (permitido)

   **test_cobros.py (5 casos)**
   - ✅ Crear cobro
   - ✅ Formas de pago válidas (EFECTIVO/TARJETA/TRANSFERENCIA)
   - ✅ Comprobante creación manual
   - ✅ Representación string
   - ✅ Número de comprobante autoincrement

   **test_actividades.py (5 casos)**
   - ✅ Crear actividad con capacidad
   - ✅ Representación string
   - ✅ Crear horario clase
   - ✅ Inscripción rechazada si clase llena (ValidationError)
   - ✅ Inscripción única por miembro-horario (unique_together)

   **test_asistencia.py (5 casos)**
   - ✅ Crear asistencia
   - ✅ Asistencia manual
   - ✅ Validar membresía ACTIVA requerida
   - ✅ Validar miembro activo requerido
   - ✅ Representación string

   **test_historial.py (5 casos)**
   - ✅ Crear miembro dispara AuditLog
   - ✅ Crear cobro dispara AuditLog
   - ✅ AuditLog captura usuario
   - ✅ Representación string AuditLog
   - ✅ AuditLog read-only (immutable)

4. **Cobertura**
   - 71% total de código
   - 100% en test files
   - Models: 92-97% (solo validaciones complejas sin cobertura)
   - Views: 28-45% (requeriría más test de integración)

### Cómo se hizo

**Factory con relaciones:**
```python
class MembresiaFactory(DjangoModelFactory):
    miembro = SubFactory(MiembroFactory)
    tipo = SubFactory(TipoMembresiaFactory)
```

**Fixture reutilizable:**
```python
@pytest.fixture
def miembro(db):
    return MiembroFactory()
```

**Test con validación:**
```python
def test_inscripcion_capacidad_maxima(self):
    # Setup
    actividad = ActividadFactory(capacidad_maxima=2)
    horario = HorarioClaseFactory(actividad=actividad)
    miembro1, miembro2, miembro3 = MiembroFactory(), MiembroFactory(), MiembroFactory()
    
    InscripcionFactory(miembro=miembro1, horario=horario)
    InscripcionFactory(miembro=miembro2, horario=horario)
    
    # Assert validation
    with pytest.raises(ValidationError):
        inscripcion = Inscripcion(miembro=miembro3, horario=horario)
        inscripcion.save()
```

### Ejecución

```bash
pytest tests/ -v                    # Todos los tests
pytest tests/test_miembros.py -v    # Un archivo
pytest -k "capacidad"               # Por keyword
pytest --cov=. --html=htmlcov       # Con cobertura HTML
```

---

## Estado Actual

### ✅ Completado
- Paso 1: Proyecto + settings + base.html
- Paso 2: Auth (login/logout/grupos/redirects)
- Paso 3: Miembros (CRUD + carnet + barcode)
- Paso 4: Membresias (CRUD + tipos + auto-update de estado con django-q2)
- Paso 5: Asistencia (Scanner HTML5 + registro por barcode + listado + validación de membresía)
- Paso 6: Cobros (Descuento automático por tipo_miembro + comprobante printable)
- Paso 7: Actividades (CRUD actividades + horarios + inscripciones con validación de capacidad)
- Paso 8: Entrenadores (CRUD + asistencia de entrenador + reporte imprimible)
- Paso 9: Reportes (3 vistas: asistencias, cobros, membresías vencidas con filtros)
- Paso 10: Healthz (health check para Render) + Auditlog (historial de cambios en Miembro y Cobro)
- Paso 11: Tests (pytest-django + factory-boy, 33 casos, 71% cobertura)

### ⏳ Próximos pasos
- Paso 12: Deploy (Render, Procfile, env vars)
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
