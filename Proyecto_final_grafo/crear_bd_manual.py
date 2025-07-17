#!/usr/bin/env python3
"""
Script alternativo para crear la base de datos usando phpMyAdmin
"""

print("🔧 CREACIÓN DE BASE DE DATOS - MÉTODO ALTERNATIVO")
print("=" * 60)
print()
print("Si el script automático no funciona, puedes crear la base de datos manualmente:")
print()
print("📋 PASOS MANUALES:")
print("1. 🚀 Inicia Laragon")
print("2. 🌐 Abre phpMyAdmin: http://localhost/phpmyadmin/")
print("3. 👤 Usuario: root")
print("4. 🔑 Contraseña: (deja vacío o prueba: admin123, root)")
print("5. 📊 Ve a la pestaña 'Bases de datos'")
print("6. ✨ Crea una nueva base de datos llamada: flask_proyecto_final")
print("7. 📝 Usa cotejamiento: utf8_general_ci")
print()
print("=" * 60)
print()

# Intentar detectar si Laragon está corriendo
import socket

def verificar_mysql():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex(('localhost', 3307))
        sock.close()
        
        if result == 0:
            print("✅ MySQL está ejecutándose en puerto 3307")
            return True
        else:
            print("❌ MySQL no está ejecutándose en puerto 3307")
            return False
    except:
        print("❌ No se puede verificar el estado de MySQL")
        return False

def verificar_phpmyadmin():
    try:
        import urllib.request
        response = urllib.request.urlopen('http://localhost/phpmyadmin/', timeout=3)
        if response.status == 200:
            print("✅ phpMyAdmin está accesible en http://localhost/phpmyadmin/")
            return True
    except:
        print("❌ phpMyAdmin no está accesible")
        return False

print("🔍 VERIFICACIÓN DEL SISTEMA:")
print("-" * 30)
mysql_ok = verificar_mysql()
phpmyadmin_ok = verificar_phpmyadmin()

print()
if mysql_ok and phpmyadmin_ok:
    print("🎉 ¡Todo está funcionando! Puedes crear la base de datos manualmente.")
    print("🌐 Abre: http://localhost/phpmyadmin/")
elif mysql_ok:
    print("⚠️  MySQL funciona pero phpMyAdmin no está accesible.")
    print("🔧 Verifica que Laragon esté completamente iniciado.")
else:
    print("❌ MySQL no está funcionando.")
    print("🚀 Inicia Laragon y asegúrate de que MySQL esté ejecutándose.")

print()
print("📌 CONFIGURACIÓN PARA EL PROYECTO:")
print(f"   Base de datos: flask_proyecto_final")
print(f"   Usuario: root")
print(f"   Contraseña: (vacía o la que tengas configurada)")
print(f"   Puerto: 3307")
print()
print("⚡ Una vez creada la base de datos, ejecuta: python reset_database.py")
