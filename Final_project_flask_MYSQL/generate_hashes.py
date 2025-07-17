#!/usr/bin/env python3
"""
Script to generate correct password hashes and update database
Run this script to fix the password hashes in the database
"""

from werkzeug.security import generate_password_hash

def generate_hashes():
    """Generate correct password hashes"""
    password = "admin123"
    
    # Generate hashes
    admin_hash = generate_password_hash(password)
    user_hash = generate_password_hash(password)
    
    print("=== HASHES GENERADOS ===")
    print(f"Admin hash: {admin_hash}")
    print(f"User hash: {user_hash}")
    
    # Generate SQL update statements
    sql_updates = f"""
-- Update password hashes with correct values
UPDATE usuarios SET password_hash = '{admin_hash}' WHERE username = 'admin';
UPDATE usuarios SET password_hash = '{user_hash}' WHERE username = 'usuario';

-- Verify updates
SELECT username, LEFT(password_hash, 20) as hash_preview FROM usuarios;
"""
    
    print("\n=== SQL PARA ACTUALIZAR BASE DE DATOS ===")
    print(sql_updates)
    
    # Write to file
    with open('update_passwords.sql', 'w', encoding='utf-8') as f:
        f.write(sql_updates)
    
    print("\n✅ Archivo 'update_passwords.sql' creado exitosamente")
    print("📋 Copia el SQL de arriba y ejecútalo en phpMyAdmin")

if __name__ == "__main__":
    generate_hashes()
