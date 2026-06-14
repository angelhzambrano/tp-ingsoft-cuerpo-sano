# 💪 Cuerpo Sano - Sistema de Gestión

Sistema de gestión integral para gimnasios con control de asistencias, membresías, actividades y reportes.

## 🚀 Acceso Rápido

**URL:** https://cuerpo-sano.onrender.com

**Usuario Demo:** `admin` / `admin123`

> ⚠️ Este es usuario de demostración. Para producción, cambiar las credenciales en el panel de administración.

---

## 👥 Roles y Permisos

El sistema tiene 3 roles principales:

### 👨‍💼 **Admin**
- Acceso total a todas las funcionalidades
- Crear/editar miembros y membresías
- Ver reportes y gráficos
- Crear actividades
- Gestionar cobros
- Acceso al lector biométrico

**Menú disponible:**
- 👥 Miembros
- 🎟️ Membresías
- 📱 Asistencia (biométrico)
- 🏋️ Actividades
- 💳 Cobros
- 📊 Reportes

### 📞 **Recepción**
- Registrar asistencias (manual o biométrico)
- Ver lista de miembros
- Gestionar cobros
- Acceso al lector biométrico

**Menú disponible:**
- 📱 Asistencia
- 👥 Miembros
- 💳 Cobros

### 🏋️ **Entrenador**
- Ver su propio registro de asistencia
- Consultar actividades programadas

**Menú disponible:**
- 📋 Mi Asistencia
- 🏋️ Actividades

---

## 📋 Flujos Principales

### 1️⃣ **Registro de Asistencia**

#### Opción A: Lector Biométrico (Recomendado)
1. Ir a **Asistencia** → **Lector Biométrico**
2. Escanear el código de barras del carnet
3. El sistema registra automáticamente la asistencia
4. Aparece confirmación con el nombre del miembro

#### Opción B: Registro Manual
1. Ir a **Asistencia** → **Registro Manual**
2. Seleccionar el miembro
3. Hacer clic en "Registrar Asistencia"

### 2️⃣ **Gestionar Miembros**

1. Ir a **Miembros**
2. Ver lista de miembros activos
3. Opciones por miembro:
   - 👁️ **Ver** - Detalles completos
   - ✏️ **Editar** - Modificar información
   - 🎫 **Carnet** - Ver código de barras

Para crear nuevo miembro:
1. Clic en **➕ Nuevo Miembro**
2. Completar datos:
   - Nombre y apellido
   - DNI (único)
   - Email (opcional)
   - Teléfono
   - Tipo de miembro (Regular/Estudiante/VIP)
3. Se genera automáticamente:
   - Carnet con código de barras
   - Membresía inicial

### 3️⃣ **Membresías**

1. Ir a **Membresías**
2. Ver planes disponibles (Plan Mensual por defecto)
3. Cada miembro tiene asignada una membresía con:
   - Fecha de inicio
   - Fecha de vencimiento
   - Estado (Activa/Vencida)

### 4️⃣ **Reportes y Estadísticas**

1. Ir a **Reportes**
2. Ver estadísticas generales:
   - 📍 **Total de asistencias**
   - 👥 **Miembros únicos**
   - 📊 **Promedio diario**
   - 📅 **Días con registro**

3. Gráficos interactivos:
   - **Asistencias por método** - Código de barras vs. Manual
   - **Top 5 miembros** - Más concurrentes (con medallas 🥇🥈🥉)

4. **Descargar Excel**
   - Clic en "📊 Descargar Excel"
   - Se descarga archivo con:
     - Listado detallado de asistencias
     - Columnas: Fecha, Hora, Miembro, DNI, Tipo, Método

5. **Filtros avanzados**
   - Rango de fechas
   - Por miembro específico
   - Por método (Código/Manual)

---

## 🎯 Casos de Uso Comunes

### Abrir el gimnasio
1. Ir a **Asistencia** → **Lector Biométrico**
2. Tener lector biométrico listo
3. Conforme lleguen miembros, escanear sus carnets
4. El sistema registra automáticamente

### Verificar asistencias del día
1. Ir a **Reportes**
2. Los filtros cargan automáticamente el día actual
3. Ver gráficos en tiempo real
4. Tabla detallada con últimas 50 asistencias

### Crear reporte mensual
1. Ir a **Reportes**
2. Ajustar fechas al mes deseado
3. Clic en **🔍 Filtrar**
4. Clic en **📊 Descargar Excel**
5. Abrir en Excel/Google Sheets para análisis

### Registrar nuevo miembro
1. Ir a **Miembros**
2. Clic en **➕ Nuevo Miembro**
3. Completar datos
4. Se genera carnet automático
5. Miembro listo para usar el lector biométrico

---

## 🔒 Notas de Seguridad

- ✅ Las contraseñas se guardan encriptadas
- ✅ No se almacenan datos sensibles en texto plano
- ✅ El acceso a reportes está limitado por rol
- ✅ Las asistencias son registros inmutables (auditoría)
- ⚠️ Cambiar credenciales de admin regularmente
- ⚠️ No compartir usuarios - cada staff tiene su cuenta

---

## 📊 Datos de Prueba

Al iniciar por primera vez, el sistema carga automáticamente:

**Miembros de prueba:**
- Juan Pérez (DNI: 12345679)
- María García (DNI: 12345680)
- Carlos Martinez (DNI: 12345681)
- Ana López (DNI: 12345682)

**Carnets de prueba:**
- CS-00001 a CS-00004

**Membresía:**
- Plan Mensual (30 días válidos)

Estos datos se pueden eliminar o modificar libremente.

---

## ⚡ Características Técnicas

- **Framework:** Django 5.0.6
- **Base de datos:** PostgreSQL (Neon)
- **Hosting:** Render.com (auto-deploy desde GitHub)
- **Almacenamiento de imágenes:** Cloudinary
- **Interfaz:** DaisyUI + TailwindCSS
- **Gráficos:** Chart.js
- **Excel:** openpyxl

---

## 🆘 Soporte y Problemas

### Página tarda en cargar
- Normal en Render Free tier (cold start)
- Después del primer acceso es más rápido
- Si persiste, recargar la página

### Lector biométrico no registra
- Verificar que el carnet sea válido
- Intentar leer nuevamente con menos presión
- Si falla, usar **Registro Manual**

### No veo mis datos
- Verificar que el filtro de fechas sea correcto
- Si no hay datos, no habrá gráficos
- Registrar algunas asistencias primero

### Olvidé contraseña
- Contactar al administrador del sistema
- Se resetea desde el panel de administración

---

## 📅 Próximas Mejoras Planeadas

- [ ] Integración con pagos online
- [ ] Fotos de miembros
- [ ] Envío de recordatorios por email
- [ ] App móvil nativa
- [ ] Integración con redes sociales

---

## 📞 Contacto

**Desarrollador:** Angel Zambrano  
**Email:** angelhzambrano@gmail.com  
**Repositorio:** https://github.com/angelhzambrano/tp-ingsoft-cuerpo-sano

---

**Versión:** 1.0.0  
**Última actualización:** Junio 2026  
**Estado:** Production Ready ✅
