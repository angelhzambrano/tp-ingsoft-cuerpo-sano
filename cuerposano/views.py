from django.http import JsonResponse
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime, time
from miembros.models import Miembro
from entrenadores.models import Entrenador
from membresias.models import Membresia
from actividades.models import Inscripcion, HorarioClase


def home(request):
    """Página de inicio - redirige a dashboard si está autenticado"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def ping(request):
    """Ultra simple health check - no DB access"""
    return JsonResponse({'status': 'alive', 'message': 'WSGI is running'})


def test_template(request):
    """Test basic template rendering"""
    try:
        return render(request, 'registration/login.html', {})
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'type': type(e).__name__
        }, status=500)


def setup(request):
    """Setup test data - visita una sola vez para crear usuarios y datos de prueba"""
    from django.core.management import call_command
    from io import StringIO

    out = StringIO()
    try:
        call_command('setup_test_data', stdout=out, stderr=out)
        return JsonResponse({
            'status': 'success',
            'message': 'Setup completado',
            'output': out.getvalue()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'output': out.getvalue()
        }, status=500)


def healthz(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({'status': 'ok', 'db': 'connected'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'detail': str(e)}, status=503)


def custom_logout(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    """Dashboard principal según rol del usuario"""
    try:
        context = {
            'is_admin': request.user.groups.filter(name='Admin').exists(),
            'is_recepcion': request.user.groups.filter(name='Recepcion').exists(),
            'is_entrenador': request.user.groups.filter(name='Entrenador').exists(),
            'is_miembro': request.user.groups.filter(name='Miembro').exists(),
        }

        if context['is_admin']:
            context['stats'] = {
                'miembros': Miembro.objects.count(),
                'entrenadores': Entrenador.objects.count(),
                'activos': Miembro.objects.filter(activo=True).count(),
            }
        elif context['is_entrenador']:
            try:
                entrenador = request.user.entrenador
                context['entrenador'] = entrenador
                # Obtener clases asignadas
                clases_asignadas = HorarioClase.objects.filter(
                    entrenador=entrenador
                ).select_related('actividad').order_by('dia_semana', 'hora_inicio')
                context['clases_asignadas'] = clases_asignadas
            except Entrenador.DoesNotExist:
                context['sin_asignacion'] = True
        elif context['is_miembro']:
            try:
                miembro = request.user.miembro
                context['miembro'] = miembro
                # Obtener membresía activa
                membresia = Membresia.objects.filter(
                    miembro=miembro,
                    estado='ACTIVA',
                    fecha_fin__gte=timezone.now().date()
                ).first()
                context['membresia'] = membresia

                # Obtener inscripciones activas
                inscripciones = Inscripcion.objects.filter(
                    miembro=miembro,
                    estado='ACTIVA'
                ).select_related('horario__actividad', 'horario__entrenador').order_by('horario__dia_semana', 'horario__hora_inicio')
                context['inscripciones'] = inscripciones

                # Obtener próxima clase (hoy o después)
                hoy = timezone.now().date()
                ahora = timezone.now().time()
                dias_semana = ['LUN', 'MAR', 'MIE', 'JUE', 'VIE', 'SAB', 'DOM']
                hoy_dia_semana = dias_semana[hoy.weekday()]

                proxima_clase = None
                for inscripcion in inscripciones:
                    horario_dia = inscripcion.horario.dia_semana
                    # Si es hoy y la hora aún no pasó
                    if horario_dia == hoy_dia_semana and inscripcion.horario.hora_inicio > ahora:
                        if not proxima_clase or inscripcion.horario.hora_inicio < proxima_clase.horario.hora_inicio:
                            proxima_clase = inscripcion
                    # Si es después de hoy
                    elif dias_semana.index(horario_dia) > dias_semana.index(hoy_dia_semana):
                        if not proxima_clase:
                            proxima_clase = inscripcion

                context['proxima_clase'] = proxima_clase
            except Miembro.DoesNotExist:
                context['sin_asignacion'] = True

        return render(request, 'dashboard.html', context)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'type': type(e).__name__,
            'user': str(request.user),
            'groups': list(request.user.groups.values_list('name', flat=True))
        }, status=500)


@login_required
def home_redirect(request):
    """Redirige al dashboard"""
    return redirect('dashboard')
