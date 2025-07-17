#!/usr/bin/env python3
"""
Script para corregir todos los problemas de endpoints en la aplicación
"""

import os
import re

def fix_endpoint_references():
    """Corrige todas las referencias a endpoints incorrectos"""
    
    files_to_fix = [
        'routes/auth_routes.py',
        'routes/admin_routes.py',
        'templates/base.html',
        'templates/auth/login.html',
        'templates/auth/register.html'
    ]
    
    # Mapeo de endpoints incorrectos a correctos
    endpoint_fixes = {
        'home.index': 'home.home',
        'ruta_economica.index': 'ruta_economica.ruta_economica',
        'ruta_fija.index': 'ruta_fija.ruta_fija'
    }
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    for file_path in files_to_fix:
        full_path = os.path.join(base_path, file_path)
        
        if not os.path.exists(full_path):
            print(f"⚠️  Archivo no encontrado: {file_path}")
            continue
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Aplicar correcciones
            for old_endpoint, new_endpoint in endpoint_fixes.items():
                pattern = rf"url_for\(['\"]({old_endpoint})['\"]\)"
                replacement = f"url_for('{new_endpoint}')"
                content = re.sub(pattern, replacement, content)
            
            # Verificar si hubo cambios
            if content != original_content:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Corregido: {file_path}")
            else:
                print(f"✓ OK: {file_path}")
                
        except Exception as e:
            print(f"❌ Error procesando {file_path}: {str(e)}")

if __name__ == "__main__":
    print("🔧 CORRECCIÓN DE ENDPOINTS")
    print("=" * 40)
    
    fix_endpoint_references()
    
    print("\n✅ Corrección completada")
    print("🚀 Ahora puedes ejecutar la aplicación con 'start_fixed.bat'")
