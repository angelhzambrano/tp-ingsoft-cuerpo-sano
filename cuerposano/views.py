from django.http import JsonResponse
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def healthz(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({'status': 'ok', 'db': 'connected'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'detail': str(e)}, status=503)


@login_required
def home_redirect(request):
    if request.user.groups.filter(name='Recepcion').exists():
        return redirect('asistencia:registro')
    elif request.user.groups.filter(name='Entrenador').exists():
        return redirect('entrenadores:lista')
    else:
        return redirect('miembros:lista')
