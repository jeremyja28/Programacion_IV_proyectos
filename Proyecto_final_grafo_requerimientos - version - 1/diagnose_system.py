#!/usr/bin/env python3
"""
Script de diagnóstico completo para la aplicación
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_routes():
    """Verifica que todas las rutas estén registradas correctamente"""
    try:
        from app import create_app
        app = create_app()
        
        print("📋 Rutas registradas en la aplicación:")
        print("-" * 40)
        
        with app.app_context():
            for rule in app.url_map.iter_rules():
                print(f"  {rule.endpoint:25} -> {rule.rule}")
        
        # Verificar endpoints específicos
        endpoints_to_check = [
            'home.home',
            'auth.login',
            'auth.register',
            'auth.logout',
            'admin.dashboard'
        ]
        
        print("\n🔍 Verificando endpoints críticos:")
        print("-" * 40)
        
        for endpoint in endpoints_to_check:
            try:
                with app.test_request_context():
                    from flask import url_for
                    url = url_for(endpoint)
                    print(f"  ✅ {endpoint} -> {url}")
            except Exception as e:
                print(f"  ❌ {endpoint} -> Error: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando rutas: {str(e)}")
        return False

def test_admin_user():
    """Prueba específica del usuario administrador"""
    try:
        from app import create_app
        from models.models import db, User
        
        app = create_app()
        
        with app.app_context():
            # Buscar usuario admin
            admin = User.query.filter_by(username='admin').first()
            
            if not admin:
                print("❌ Usuario admin no encontrado")
                return False
            
            print(f"✅ Usuario admin encontrado:")
            print(f"   ID: {admin.id}")
            print(f"   Username: {admin.username}")
            print(f"   Email: {admin.email}")
            print(f"   Role: {admin.role}")
            print(f"   Active: {admin.is_active}")
            print(f"   Password Hash: {admin.password_hash[:20]}...")
            
            # Probar autenticación
            if admin.check_password('admin123'):
                print("✅ Contraseña 'admin123' funciona correctamente")
                return True
            else:
                print("❌ Contraseña 'admin123' no funciona")
                
                # Intentar recrear el usuario
                print("🔧 Intentando recrear usuario admin...")
                admin.set_password('admin123')
                db.session.commit()
                
                if admin.check_password('admin123'):
                    print("✅ Usuario admin recreado exitosamente")
                    return True
                else:
                    print("❌ No se pudo recrear el usuario admin")
                    return False
                    
    except Exception as e:
        print(f"❌ Error verificando usuario admin: {str(e)}")
        return False

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    try:
        from app import create_app
        from models.models import db
        
        app = create_app()
        
        with app.app_context():
            # Probar conexión
            db.engine.connect()
            print("✅ Conexión a base de datos exitosa")
            
            # Verificar tablas
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"📊 Tablas encontradas: {', '.join(tables)}")
            
            # Contar registros
            from models.models import User, Ciudad, Ruta
            user_count = User.query.count()
            ciudad_count = Ciudad.query.count()
            ruta_count = Ruta.query.count()
            
            print(f"👥 Usuarios: {user_count}")
            print(f"🏙️  Ciudades: {ciudad_count}")
            print(f"🛣️  Rutas: {ruta_count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error en base de datos: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 DIAGNÓSTICO COMPLETO DEL SISTEMA")
    print("=" * 60)
    
    print("\n1. Verificando rutas de la aplicación...")
    routes_ok = test_routes()
    
    print("\n2. Verificando conexión a base de datos...")
    db_ok = test_database_connection()
    
    print("\n3. Verificando usuario administrador...")
    admin_ok = test_admin_user()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 60)
    
    print(f"Rutas:     {'✅ OK' if routes_ok else '❌ ERROR'}")
    print(f"Base de datos: {'✅ OK' if db_ok else '❌ ERROR'}")
    print(f"Usuario admin: {'✅ OK' if admin_ok else '❌ ERROR'}")
    
    if routes_ok and db_ok and admin_ok:
        print("\n🎉 ¡Sistema completamente funcional!")
        print("🚀 Puedes ejecutar 'start_fixed.bat' para iniciar la aplicación")
    else:
        print("\n⚠️  El sistema tiene problemas que necesitan ser corregidos")
    
    print("\n📌 Credenciales de acceso:")
    print("   Usuario: admin")
    print("   Contraseña: admin123")
    print("   URL: http://localhost:4000")
