#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Limpiar archivos innecesarios del proyecto
"""

import os
import shutil
import sys

def limpiar_proyecto():
    """Eliminar archivos innecesarios"""
    
    # Archivos .bat a eliminar
    archivos_bat = [
        'reiniciar_simple.bat',
        'reiniciar_limpio.bat', 
        'probar_app.bat',
        'iniciar_app.bat',
        'importar_con_tildes.bat',
        'importar_bd.bat',
        'ejecutar_app.bat',
        'actualizar_bd.bat'
    ]
    
    # Archivos .md a eliminar (mantener solo README.md)
    archivos_md = [
        'SOLUCION_ESTILOS.md',
        'SISTEMA_OPTIMIZADO.md',
        'REFACTORIZACION_SOLID_COMPLETADA.md',
        'LARAGON_README.md',
        'INSTRUCCIONES_SISTEMA_SIMPLE.md',
        'INSTRUCCIONES_PUERTO_3307.md',
        'INSTRUCCIONES_COMPLETAS.md',
        'FIX_SUMMARY.md',
        'FIX_DASHBOARD_TEMPLATE.md',
        'FIX_CIUDADES_TEMPLATE.md',
        'FIX_ALL_ADMIN_TEMPLATES.md',
        'CAMBIOS_ECUADOR.md',
        'ADMIN_TEMPLATES_COMPLETAMENTE_ARREGLADOS.md'
    ]
    
    # Archivos .py de prueba a eliminar
    archivos_py_test = [
        'verificar_ibarra_loja.py',
        'verify_db.py',
        'test_simple.py',
        'test_optimizado.py',
        'test_login.py',
        'test_final.py',
        'test_conexion.py',
        'test_app.py',
        'test_tildes.py',
        'verificar_sistema.py',
        'start_clean.py',
        'resumen_sistema.py',
        'reset_simple.py',
        'reset_database_simple.py',
        'reset_database.py',
        'regenerar_admin.py',
        'probar_registro.py',
        'import_sql.py',
        'fix_users.py',
        'crear_usuarios.py',
        'forms.py'  # Si no se usa
    ]
    
    eliminados = []
    
    print("🧹 LIMPIANDO ARCHIVOS INNECESARIOS")
    print("=" * 50)
    
    # Eliminar archivos .bat
    print("\n📁 Eliminando archivos .bat...")
    for archivo in archivos_bat:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
                eliminados.append(archivo)
                print(f"   ✅ {archivo}")
            except Exception as e:
                print(f"   ❌ Error eliminando {archivo}: {e}")
    
    # Eliminar archivos .md
    print("\n📄 Eliminando archivos .md innecesarios...")
    for archivo in archivos_md:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
                eliminados.append(archivo)
                print(f"   ✅ {archivo}")
            except Exception as e:
                print(f"   ❌ Error eliminando {archivo}: {e}")
    
    # Eliminar archivos .py de prueba
    print("\n🐍 Eliminando archivos .py de prueba...")
    for archivo in archivos_py_test:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
                eliminados.append(archivo)
                print(f"   ✅ {archivo}")
            except Exception as e:
                print(f"   ❌ Error eliminando {archivo}: {e}")
    
    # Eliminar archivos SQL innecesarios (mantener solo el principal)
    archivos_sql_innecesarios = [
        'codigos_sql/database_schema.sql',
        'codigos_sql/database_simple.sql',
        'codigos_sql/final_project_PrograIV_CLEAN.sql',
        'codigos_sql/final_project_PrograIV_FINAL.sql',
        'codigos_sql/final_project_PrograIV_NODUPE.sql',
        'codigos_sql/final_project_PrograIV.sql',
        'codigos_sql/import_phpmyadmin.sql',
        'codigos_sql/laragon_database.sql',
        'codigos_sql/sistema_rutas_simple.sql'
    ]
    
    print("\n🗄️  Eliminando archivos SQL innecesarios...")
    for archivo in archivos_sql_innecesarios:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
                eliminados.append(archivo)
                print(f"   ✅ {archivo}")
            except Exception as e:
                print(f"   ❌ Error eliminando {archivo}: {e}")
    
    print(f"\n📊 RESUMEN:")
    print(f"   Archivos eliminados: {len(eliminados)}")
    print(f"   Archivos mantenidos: app.py, controllers/, models/, routes/, templates/, static/")
    print(f"   Base de datos: codigos_sql/database_con_tildes_correctas.sql")
    print(f"   Documentación: README.md (actualizado)")
    
    return eliminados

def main():
    """Función principal"""
    try:
        eliminados = limpiar_proyecto()
        print(f"\n✅ LIMPIEZA COMPLETADA!")
        print(f"   Se eliminaron {len(eliminados)} archivos innecesarios")
        print(f"   El proyecto está ahora más limpio y organizado")
        
        # Eliminar este archivo después de ejecutarse
        print(f"\n🗑️  Eliminando este script de limpieza...")
        os.remove(__file__)
        
    except Exception as e:
        print(f"\n❌ Error en la limpieza: {e}")

if __name__ == "__main__":
    main()
