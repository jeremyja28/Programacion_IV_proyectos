#!/usr/bin/env python3
"""
Script para verificar y recrear el usuario administrador
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models.models import db, User

def reset_admin_user():
    """Elimina y recrea el usuario administrador"""
    app = create_app()
    
    with app.app_context():
        try:
            # Eliminar usuario admin existente si existe
            existing_admin = User.query.filter_by(username='admin').first()
            if existing_admin:
                print("🗑️  Eliminando usuario admin existente...")
                db.session.delete(existing_admin)
                db.session.commit()
                print("✅ Usuario admin eliminado")
            
            # Crear nuevo usuario admin
            print("🔧 Creando nuevo usuario administrador...")
            admin = User(
                username='admin',
                email='admin@proyecto.com',
                role='admin'
            )
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Usuario administrador creado exitosamente")
            print("📋 Credenciales:")
            print("   Usuario: admin")
            print("   Contraseña: admin123")
            print("   Rol: admin")
            
            # Verificar que el usuario se creó correctamente
            test_user = User.query.filter_by(username='admin').first()
            if test_user and test_user.check_password('admin123'):
                print("✅ Verificación exitosa: Usuario admin funciona correctamente")
                return True
            else:
                print("❌ Error: Usuario admin no funciona correctamente")
                return False
                
        except Exception as e:
            print(f"❌ Error al crear usuario admin: {str(e)}")
            db.session.rollback()
            return False

def verify_admin_user():
    """Verifica que el usuario admin existe y funciona"""
    app = create_app()
    
    with app.app_context():
        try:
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                print("❌ Usuario admin no encontrado")
                return False
            
            print(f"✅ Usuario admin encontrado: {admin.username}")
            print(f"📧 Email: {admin.email}")
            print(f"🔑 Rol: {admin.role}")
            
            # Verificar contraseña
            if admin.check_password('admin123'):
                print("✅ Contraseña verificada correctamente")
                return True
            else:
                print("❌ Contraseña incorrecta")
                return False
                
        except Exception as e:
            print(f"❌ Error al verificar usuario admin: {str(e)}")
            return False

if __name__ == "__main__":
    print("🔍 VERIFICACIÓN Y REPARACIÓN DEL USUARIO ADMIN")
    print("=" * 60)
    
    print("\n1. Verificando usuario admin existente...")
    if verify_admin_user():
        print("\n✅ Usuario admin está funcionando correctamente")
    else:
        print("\n⚠️  Usuario admin no funciona. Recreando...")
        if reset_admin_user():
            print("\n✅ Usuario admin recreado exitosamente")
        else:
            print("\n❌ Error al recrear usuario admin")
    
    print("\n🚀 Ahora puedes iniciar sesión con:")
    print("   Usuario: admin")
    print("   Contraseña: admin123")
