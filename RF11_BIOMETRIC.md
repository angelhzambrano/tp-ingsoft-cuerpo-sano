# RF-11: Biometric Reader Integration

## Descripción

Integración de un lector biométrico para registrar asistencia automática mediante escaneo de códigos de carnet. Cuando un miembro acerca su carnet al dispositivo biométrico, se registra automáticamente su asistencia en el sistema.

## Arquitectura

```
┌─────────────────────┐
│ Dispositivo         │
│ Biométrico          │  (Lector código QR/barras)
│ (RFC-11)            │
└──────────┬──────────┘
           │ POST /api/barcode/
           ▼
┌─────────────────────────────────────┐
│ Django API Endpoint                 │
│ POST /asistencia/api/barcode/       │ ◄── Valida carnet + membresía
└──────────┬──────────────────────────┘
           │ JSON: { numero_carnet }
           ▼
┌─────────────────────────────────────┐
│ Vista Biometrico Reader             │
│ GET /asistencia/biometrico/         │ ◄── Interfaz visual
└─────────────────────────────────────┘

```

## Componentes

### 1. API Endpoint

**Ruta:** `POST /asistencia/api/barcode/`

**Request:**
```json
{
  "numero_carnet": "C001"
}
```

**Response (exitoso):**
```json
{
  "success": true,
  "message": "✓ Juan Pérez registrado exitosamente",
  "miembro": "Juan Pérez",
  "tipo_miembro": "REGULAR"
}
```

**Response (error):**
```json
{
  "success": false,
  "error": "Membresía vencida o inexistente para Juan Pérez"
}
```

**Validaciones:**
- ✓ Carnet existe en DB
- ✓ Miembro está ACTIVO
- ✓ Miembro tiene membresía ACTIVA
- ✓ Crea registro Asistencia automáticamente

### 2. Interfaz Visual

**Ruta:** `GET /asistencia/biometrico/`

**Características:**
- Input invisible enfocado (ideal para scanners)
- Estado visual en tiempo real (🟢 esperando, ✓ éxito, ✗ error)
- Último escaneo registrado
- Listado de registros del día
- Botones de fallback (registro manual)

**Flujo:**
```
Usuario abre: /asistencia/biometrico/
       ↓
Input invisible captura el código
       ↓
Se envía al endpoint /api/barcode/
       ↓
Se muestra confirmación visual
       ↓
Se actualiza listado en tiempo real
```

### 3. Simulador de Dispositivo

**Script:** `biometric_simulator.py`

**Uso - Modo Interactivo:**
```bash
python biometric_simulator.py
# Ingresa códigos manualmente:
# 📱 Código: C001
# ✓ Juan Pérez registrado exitosamente
```

**Uso - Modo Batch:**
```bash
python biometric_simulator.py C001 http://localhost:8000
python biometric_simulator.py C002
```

## Flujo de Uso

### Escenario 1: Escaneo Exitoso

```
1. Recepcionista abre /asistencia/biometrico/ en su PC
2. Input esperando códigos (invisible, enfocado)
3. Miembro acerca carnet al scanner
4. Scanner envía código "C001" via USB/conexión
5. Input captura el código automáticamente
6. JavaScript envía POST a /api/barcode/
7. Django valida:
   - Carnet C001 existe ✓
   - Miembro está activo ✓
   - Membresía está activa ✓
8. Crea registro: Asistencia(miembro=Juan, metodo='BARCODE')
9. Responde con JSON exitoso
10. JavaScript muestra: "✓ Juan Pérez registrado"
11. Input se limpia y queda listo para siguiente escaneo
```

### Escenario 2: Error - Membresía Vencida

```
1. Miembro acerca carnet al scanner
2. Código "C005" es enviado
3. API valida pero membresía está VENCIDA
4. Responde con error
5. Interfaz muestra: "✗ Membresía vencida para María López"
6. NO se crea asistencia
7. Recepcionista debe renovar membresía primero
```

### Escenario 3: Fallback Manual

```
1. Scanner no funciona
2. Recepcionista clickea "Registro Manual"
3. Selecciona miembro de dropdown
4. Registra manualmente
5. Se crea: Asistencia(miembro=X, metodo='MANUAL')
```

## Validaciones y Seguridad

| Validación | Status | Acción |
|---|---|---|
| Carnet válido | ✓ Requerido | Crear asistencia |
| Carnet no existe | ✗ Error | Rechazar |
| Miembro activo | ✓ Requerido | Crear asistencia |
| Miembro inactivo | ✗ Error | Rechazar |
| Membresía activa | ✓ Requerido | Crear asistencia |
| Membresía vencida | ✗ Error | Rechazar |
| Login requerido | ✓ Requerido | Redirect a /accounts/login/ |
| Uso principal: Recepción | ✓ Recomendado | Grupo 'Recepcion' |

## Tests Incluidos

```python
# test_asistencia.py - TestBiometricoAPI

1. test_biometrico_escaneo_exitoso()
   → Valida que escaneo crea Asistencia

2. test_biometrico_carnet_no_existe()
   → Valida error 404 si código no existe

3. test_biometrico_miembro_inactivo()
   → Rechaza si miembro está inactivo

4. test_biometrico_membresia_vencida()
   → Rechaza si membresía expiró

5. test_biometrico_reader_view_requiere_login()
   → Redirige si no autenticado

6. test_biometrico_reader_view_autenticado()
   → Carga interfaz si autenticado
```

## Deployment

### Local (desarrollo):

```bash
# Terminal 1: Django
python manage.py runserver

# Terminal 2: Simulador
python biometric_simulator.py

# Terminal 3: Navegador
# Abre http://localhost:8000/asistencia/biometrico/
```

### Producción (Render):

```
- Endpoint: https://cuerpo-sano.onrender.com/asistencia/api/barcode/
- Interface: https://cuerpo-sano.onrender.com/asistencia/biometrico/

- Dispositivo biométrico real enviará requests HTTPS
- Certificado SSL/TLS se maneja automáticamente en Render
```

## Integraciones Futuras

Para integrar con un dispositivo biométrico real:

1. **Scanner USB (Barcode/QR):**
   - Actúa como teclado HID
   - Envía código al input enfocado
   - No requiere cambios en código Django

2. **Dispositivo WiFi/API:**
   - Configurar dispositivo para POST a `/asistencia/api/barcode/`
   - Usar HTTPS en producción
   - Autenticación vía API key (opcional)

3. **Reconocimiento Biométrico Real:**
   - Agregar librería OpenCV o TensorFlow
   - Capturar foto/huella dactilar
   - Comparar con BD y crear Asistencia

## Monitoring

Verificar registros biométricos:

```bash
# En Django shell
python manage.py shell
>>> from asistencia.models import Asistencia
>>> Asistencia.objects.filter(metodo='BARCODE').count()
42
>>> Asistencia.objects.filter(metodo='BARCODE').latest('fecha').miembro
<Miembro: Juan Pérez>
```

O en admin:
```
http://localhost:8000/admin/asistencia/asistencia/
→ Filtrar por "Método: Código de barras"
```

## Troubleshooting

| Problema | Causa | Solución |
|---|---|---|
| Input no captura código | Focus perdido | Click en interfaz o agregar event listener global |
| Escaneo funciona pero sin visual | JS error | Revisar console del navegador (F12) |
| API responde 404 | Carnet no existe | Revisar número de carnet, crear si falta |
| Requiere login repetido | Session expirada | Usar session larga: SESSION_COOKIE_AGE |
| No funciona en producción | HTTPS vs HTTP | Usar wss:// en producción |

---

**Status:** ✅ Implementado y Testeado  
**Deadline:** 2026-06-18  
**RF:** 11 (Biometric Reader Integration)
