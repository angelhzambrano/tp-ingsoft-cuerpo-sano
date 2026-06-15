"""
Cuerpo Sano Design System
Sistema de colores y estilos coherentes para la aplicación
"""

# ============================================================================
# PALETA DE COLORES
# ============================================================================

# Colores Primarios
PRIMARY = "#0D9488"
PRIMARY_DARK = "#0D7377"
PRIMARY_LIGHT = "#14B8A6"

# Colores Semánticos
SUCCESS = "#10B981"
WARNING = "#F59E0B"
DANGER = "#EF4444"
INFO = "#3B82F6"

# Colores Neutrales
DARK = "#1F2937"
DARK_SECONDARY = "#4B5563"
LIGHT = "#F3F4F6"
LIGHT_SECONDARY = "#E5E7EB"
GRAY = "#9CA3AF"

# ============================================================================
# ESPACIADO (en rem y px)
# ============================================================================

SPACING = {
    'xs': '0.25rem',      # 4px
    'sm': '0.5rem',       # 8px
    'md': '1rem',         # 16px
    'lg': '1.5rem',       # 24px
    'xl': '2rem',         # 32px
    '2xl': '3rem',        # 48px
}

# ============================================================================
# BORDER RADIUS
# ============================================================================

BORDER_RADIUS = {
    'sm': '0.375rem',     # 6px
    'md': '0.5rem',       # 8px
    'lg': '0.75rem',      # 12px
    'xl': '1rem',         # 16px
}

# ============================================================================
# SOMBRAS (Box Shadows)
# ============================================================================

SHADOWS = {
    'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
}

# ============================================================================
# ESTADOS DE APLICACIÓN
# ============================================================================

STATUS_COLORS = {
    'ACTIVA': SUCCESS,
    'PENDIENTE': WARNING,
    'CANCELADA': DANGER,
    'INACTIVA': GRAY,
    'COMPLETADA': SUCCESS,
}

ROLE_COLORS = {
    'Admin': PRIMARY,
    'Miembro': SUCCESS,
    'Entrenador': PRIMARY_LIGHT,
    'Recepcion': INFO,
}

# ============================================================================
# UTILIDADES PARA TEMPLATES
# ============================================================================

def get_badge_class(status):
    """Retorna la clase de badge según el estado"""
    status_map = {
        'ACTIVA': 'badge-success',
        'PENDIENTE': 'badge-warning',
        'CANCELADA': 'badge-danger',
        'INACTIVA': 'badge-ghost',
        'COMPLETADA': 'badge-success',
    }
    return status_map.get(status, 'badge')


def get_status_color(status):
    """Retorna el color hex del estado"""
    return STATUS_COLORS.get(status, DARK)


def get_role_color(role):
    """Retorna el color hex del rol"""
    return ROLE_COLORS.get(role, DARK)


# ============================================================================
# COLORES PARA GRÁFICOS Y REPORTES
# ============================================================================

CHART_COLORS = {
    'primary': PRIMARY,
    'secondary': PRIMARY_LIGHT,
    'success': SUCCESS,
    'warning': WARNING,
    'danger': DANGER,
    'info': INFO,
}

# ============================================================================
# GRADIENTES
# ============================================================================

GRADIENTS = {
    'primary': f'linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%)',
    'success': f'linear-gradient(135deg, {SUCCESS} 0%, #059669 100%)',
    'warning': f'linear-gradient(135deg, {WARNING} 0%, #D97706 100%)',
    'danger': f'linear-gradient(135deg, {DANGER} 0%, #DC2626 100%)',
}

# ============================================================================
# CONTEXT PARA TEMPLATES DJANGO
# ============================================================================

def get_design_system_context():
    """
    Retorna un diccionario con el design system para pasar a templates

    Uso en views:
    ```python
    context = {
        'page': 'dashboard',
        **get_design_system_context()
    }
    ```
    """
    return {
        'design': {
            'colors': {
                'primary': PRIMARY,
                'primary_dark': PRIMARY_DARK,
                'primary_light': PRIMARY_LIGHT,
                'success': SUCCESS,
                'warning': WARNING,
                'danger': DANGER,
                'info': INFO,
                'dark': DARK,
                'gray': GRAY,
                'light': LIGHT,
            },
            'spacing': SPACING,
            'radius': BORDER_RADIUS,
            'shadows': SHADOWS,
            'status_colors': STATUS_COLORS,
            'role_colors': ROLE_COLORS,
        }
    }
