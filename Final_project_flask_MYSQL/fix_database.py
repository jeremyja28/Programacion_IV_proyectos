#!/usr/bin/env python3
"""
Script to fix database users with correct password hashes
Run this script to fix the login issue
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models.usuario import Usuario
from werkzeug.security import generate_password_hash

def fix_database_users():
    """Fix database users with correct password hashes"""
    app = create_app()
    
    with app.app_context():
        try:
            # Delete existing users
            Usuario.query.delete()
            
            # Create users with correct hashes
            admin_hash = generate_password_hash('admin123')
            user_hash = generate_password_hash('admin123')
            
            # Create admin user
            admin = Usuario(
                username='admin',
                email='admin@admin.com',
                password_hash=admin_hash,
                nombre='Administrador',
                apellido='Sistema',
                es_admin=True
            )
            
            # Create regular user
            usuario = Usuario(
                username='usuario',
                email='usuario@usuario.com',
                password_hash=user_hash,
                nombre='Usuario',
                apellido='Normal',
                es_admin=False
            )
            
            # Add to database
            db.session.add(admin)
            db.session.add(usuario)
            db.session.commit()
            
            print("✅ Base de datos arreglada exitosamente")
            print("📋 Credenciales de acceso:")
            print("   ADMIN - Usuario: admin / Contraseña: admin123")
            print("   USUARIO - Usuario: usuario / Contraseña: admin123")
            
            # Verify users
            users = Usuario.query.all()
            print(f"\n📊 Usuarios en la base de datos: {len(users)}")
            for user in users:
                print(f"   - {user.username} ({user.get_full_name()})")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_database_users()
