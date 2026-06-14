#!/usr/bin/env python3
"""
Simulador de dispositivo biométrico para Cuerpo Sano (RF-11)

Uso:
    python biometric_simulator.py <numero_carnet> [base_url]

Ejemplo:
    python biometric_simulator.py C001 http://localhost:8000
    python biometric_simulator.py C002
"""

import sys
import json
import requests
from datetime import datetime

DEFAULT_URL = 'http://localhost:8000/asistencia/api/barcode/'

def scan_barcode(numero_carnet, base_url=DEFAULT_URL):
    """Simula escaneo de código de barras"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 📱 Escaneando: {numero_carnet}")
    
    try:
        response = requests.post(
            base_url,
            json={'numero_carnet': numero_carnet},
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        data = response.json()
        
        if data.get('success'):
            print(f"✓ {data.get('message')}")
            print(f"  Miembro: {data.get('miembro')}")
            print(f"  Tipo: {data.get('tipo_miembro')}")
            return True
        else:
            print(f"✗ Error: {data.get('error')}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"✗ Error: No se puede conectar a {base_url}")
        print("  Asegúrate de que Django esté corriendo: python manage.py runserver")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def interactive_mode():
    """Modo interactivo: leer códigos desde stdin"""
    print("=" * 60)
    print("Simulador de Dispositivo Biométrico - Cuerpo Sano")
    print("=" * 60)
    print("Ingresa códigos de carnet (ej: C001, C002)")
    print("Escribe 'salir' para terminar\n")
    
    while True:
        try:
            codigo = input("📱 Código: ").strip()
            
            if codigo.lower() in ('salir', 'exit', 'quit', 'q'):
                print("👋 Adiós!")
                break
            
            if codigo:
                scan_barcode(codigo)
                print()
        except KeyboardInterrupt:
            print("\n👋 Adiós!")
            break
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        interactive_mode()
    else:
        numero_carnet = sys.argv[1]
        base_url = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_URL
        
        # Reemplazar localhost con http://localhost:8000 si es necesario
        if not base_url.startswith('http'):
            base_url = f'http://{base_url}/asistencia/api/barcode/'
        elif not base_url.endswith('/'):
            base_url += '/asistencia/api/barcode/'
        
        scan_barcode(numero_carnet, base_url)
