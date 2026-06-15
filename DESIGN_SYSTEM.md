# Cuerpo Sano - Design System

Sistema de diseño visual para la aplicación de gestión de gimnasio.

## 🎨 Paleta de Colores

### Colores Primarios

| Color | Valor | Uso |
|-------|-------|-----|
| **Primary** | `#0D9488` | Botones principales, enlaces, elementos destacados |
| **Primary Dark** | `#0D7377` | Estados hover, elementos activos |
| **Primary Light** | `#14B8A6` | Fondos, áreas secundarias |

### Colores Semánticos

| Color | Valor | Uso |
|-------|-------|-----|
| **Success** | `#10B981` | Estados exitosos, confirmaciones, badges activas |
| **Warning** | `#F59E0B` | Alertas, avisos, estados de precaución |
| **Danger** | `#EF4444` | Errores, acciones destructivas, estados críticos |
| **Info** | `#3B82F6` | Información, mensajes informativos |

### Colores Neutrales

| Color | Valor | Uso |
|-------|-------|-----|
| **Dark** | `#1F2937` | Texto principal, headers |
| **Dark Secondary** | `#4B5563` | Texto secundario, subtítulos |
| **Light** | `#F3F4F6` | Fondos suaves, espacios en blanco |
| **Gray** | `#9CA3AF` | Texto deshabilitado, placeholders |

## 📐 Espaciado

```
xs  → 0.25rem (4px)
sm  → 0.5rem  (8px)
md  → 1rem    (16px)
lg  → 1.5rem  (24px)
xl  → 2rem    (32px)
2xl → 3rem    (48px)
```

## 🔘 Border Radius

```
sm  → 0.375rem (6px)
md  → 0.5rem   (8px)
lg  → 0.75rem  (12px)
xl  → 1rem     (16px)
```

## 🪟 Sombras

```
sm  → 0 1px 2px 0 rgba(0, 0, 0, 0.05)
md  → 0 4px 6px -1px rgba(0, 0, 0, 0.1)
lg  → 0 10px 15px -3px rgba(0, 0, 0, 0.1)
xl  → 0 20px 25px -5px rgba(0, 0, 0, 0.1)
```

## 🚀 Uso en HTML/Tailwind

### Botones

```html
<!-- Primary Button -->
<button class="btn-primary">Confirmar</button>

<!-- Secondary Button -->
<button class="btn-secondary">Cancelar</button>

<!-- Ghost Button -->
<button class="btn-ghost">Más opciones</button>

<!-- Tamaños -->
<button class="btn-primary btn-sm">Pequeño</button>
<button class="btn-primary btn-lg">Grande</button>
```

### Cards

```html
<div class="card">
  <h2 class="card-title">Título de la Card</h2>
  <div class="card-body">
    <p>Contenido de la card</p>
  </div>
</div>
```

### Badges

```html
<!-- Success Badge -->
<span class="badge badge-success">✓ Activa</span>

<!-- Warning Badge -->
<span class="badge badge-warning">⚠ Pendiente</span>

<!-- Danger Badge -->
<span class="badge badge-danger">✗ Cancelada</span>

<!-- Primary Badge -->
<span class="badge badge-primary">Info</span>
```

### Forms

```html
<div class="form-group">
  <label class="form-label">Nombre</label>
  <input type="text" class="form-control" placeholder="Ingresa tu nombre">
</div>
```

### Alerts

```html
<!-- Info Alert -->
<div class="alert alert-info">
  ℹ️ Este es un mensaje informativo
</div>

<!-- Success Alert -->
<div class="alert alert-success">
  ✓ Operación completada exitosamente
</div>

<!-- Warning Alert -->
<div class="alert alert-warning">
  ⚠ Verifica los datos antes de continuar
</div>

<!-- Danger Alert -->
<div class="alert alert-danger">
  ✗ Ocurrió un error inesperado
</div>
```

## 🎨 Uso en CSS Variables

```css
/* En tus estilos personalizados */
.mi-elemento {
  background-color: var(--primary);
  color: white;
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.texto-secundario {
  color: var(--dark-secondary);
  font-size: 0.875rem;
}
```

## 🎯 Tailwind Classes Disponibles

```html
<!-- Colores de fondo -->
<div class="bg-primary-600">Primary</div>
<div class="bg-success-500">Success</div>
<div class="bg-warning-500">Warning</div>
<div class="bg-danger-500">Danger</div>

<!-- Colores de texto -->
<p class="text-primary-600">Texto primario</p>
<p class="text-neutral-600">Texto neutral</p>

<!-- Bordes -->
<div class="border-primary-600">Con borde primario</div>

<!-- Espaciado -->
<div class="p-lg">Padding large</div>
<div class="m-xl">Margin extra large</div>

<!-- Border Radius -->
<div class="rounded-lg">Bordes redondeados</div>

<!-- Sombras -->
<div class="shadow-md">Con sombra mediana</div>
<div class="shadow-lg">Con sombra grande</div>
```

## 📦 Cómo Integrar

### 1. CSS Variables (Opción Simple)

```html
<!-- En tu base.html -->
<head>
  <link rel="stylesheet" href="{% static 'css/design-system.css' %}">
</head>
```

### 2. Tailwind Config (Opción Avanzada)

```javascript
// tailwind.config.js
const designSystem = require('./tailwind-design-system.config.js');

module.exports = {
  ...designSystem,
  // tus otras configuraciones
};
```

## 🔄 Ejemplos de Componentes

### Dashboard Card

```html
<div class="card">
  <h2 class="card-title">⏰ Próxima Clase</h2>
  <div class="card-body">
    <p class="text-lg font-bold text-primary-600">Pesas</p>
    <p class="text-sm text-neutral-600">📅 Martes • 06:00 - 07:00</p>
    <p class="text-sm text-neutral-600">👨‍🏫 Entrenador Principal</p>
  </div>
</div>
```

### Activity Card

```html
<div class="card">
  <div class="text-4xl mb-4">🏋️</div>
  <h3 class="card-title">Pesas</h3>
  <p class="text-sm text-neutral-600 mb-4">Entrenamiento con pesas</p>
  
  <div class="mb-4">
    <p class="text-xs text-neutral-600">📅 MAR 06:00 - 07:00</p>
    <p class="text-xs text-neutral-600">📅 SAB 10:00 - 11:30</p>
  </div>
  
  <button class="btn-primary w-full">Ver Horarios →</button>
</div>
```

### Form Group

```html
<div class="form-group">
  <label class="form-label">Actividad</label>
  <select class="form-control">
    <option>Selecciona una actividad...</option>
    <option>Pesas</option>
    <option>Yoga</option>
  </select>
</div>

<div class="form-group">
  <label class="form-label">Horario</label>
  <input type="text" class="form-control" value="Martes 06:00 - 07:00" readonly>
</div>

<button class="btn-primary w-full">Confirmar Inscripción</button>
```

## 📋 Actualizando Templates Existentes

### Antes (DaisyUI)
```html
<div class="card bg-gradient-to-r from-blue-50 to-blue-100 shadow-lg">
  <div class="card-body">
    <h2 class="card-title">Título</h2>
  </div>
</div>
```

### Después (Design System)
```html
<div class="card">
  <h2 class="card-title">Título</h2>
  <div class="card-body">
    Contenido
  </div>
</div>
```

## 🎯 Próximos Pasos

1. **Copiar los archivos CSS** a tu proyecto
2. **Actualizar `tailwind.config.js`** con la nueva configuración
3. **Reemplazar DaisyUI clases** con las nuevas clases del design system
4. **Revisar visualmente** cada página en Figma
5. **Validar contraste** y accesibilidad

## 📱 Responsive Design

Usa prefijos de Tailwind para responsive:

```html
<!-- Desktop: primary-600, Mobile: primary-500 -->
<button class="bg-primary-500 md:bg-primary-600">Responsive Button</button>

<!-- Stack verticalmente en mobile -->
<div class="grid grid-cols-1 md:grid-cols-2 gap-lg">
  <div class="card">Card 1</div>
  <div class="card">Card 2</div>
</div>
```

## ✨ Tips & Tricks

- ✅ Usa `text-neutral-600` para texto secundario (mejor que `text-gray-600`)
- ✅ Combina `shadow-md` con `hover:shadow-lg` para feedback visual
- ✅ Usa `badge-success`, `badge-warning` para estados rápidos
- ✅ Los botones tienen tamaños: `btn-sm`, `btn-primary`, `btn-lg`
- ✅ Aprovecha `alert` para mensajes de usuario

---

Documento generado desde Design System Figma
**Colores:** Teal `#0D9488` + Neutrales coherentes
**Última actualización:** Junio 2026
