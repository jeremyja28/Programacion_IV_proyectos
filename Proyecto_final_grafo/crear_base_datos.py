#!/usr/bin/env python3
"""
Script para crear la nueva base de datos flask_proyecto_final
"""

import pymysql

def crear_base_datos():
    """Crea la base de datos flask_proyecto_final"""
    try:
        # Conectar a MySQL sin especificar una base de datos
        # En Laragon, el usuario root por defecto no tiene contraseña
        connection = pymysql.connect(
            host='localhost',
            port=3307,
            user='root',
            password=''  # Laragon por defecto no tiene contraseña
        )
        
        with connection.cursor() as cursor:
            # Crear la base de datos si no existe
            cursor.execute("CREATE DATABASE IF NOT EXISTS flask_proyecto_final")
            print("✅ Base de datos 'flask_proyecto_final' creada exitosamente")
            
            # Verificar que se creó
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            
            print("📊 Bases de datos disponibles:")
            for db in databases:
                print(f"   - {db[0]}")
        
        connection.close()
        return True
            
    except Exception as e:
        print(f"❌ Error al conectar con MySQL: {e}")
        print("💡 Intentando con diferentes configuraciones...")
        return intentar_otras_configuraciones()

def intentar_otras_configuraciones():
    """Intenta diferentes configuraciones de conexión"""
    configuraciones = [
        {'password': '', 'desc': 'sin contraseña (Laragon default)'},
        {'password': 'admin123', 'desc': 'con contraseña admin123'},
        {'password': 'root', 'desc': 'con contraseña root'},
        {'port': 3306, 'password': '', 'desc': 'puerto 3306 sin contraseña'},
    ]
    
    for config in configuraciones:
        try:
            print(f"🔄 Intentando {config['desc']}...")
            
            connection_params = {
                'host': 'localhost',
                'port': config.get('port', 3307),
                'user': 'root',
                'password': config['password']
            }
            
            connection = pymysql.connect(**connection_params)
            
            with connection.cursor() as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS flask_proyecto_final")
                print("✅ Base de datos 'flask_proyecto_final' creada exitosamente")
                
                cursor.execute("SHOW DATABASES")
                databases = cursor.fetchall()
                
                print("📊 Bases de datos disponibles:")
                for db in databases:
                    print(f"   - {db[0]}")
            
            connection.close()
            
            # Si llegamos aquí, la conexión fue exitosa
            print(f"✅ Conexión exitosa con: {config['desc']}")
            return True
            
        except Exception as e:
            print(f"❌ Falló con {config['desc']}: {e}")
            continue
    
    return False

if __name__ == "__main__":
    print("🔧 CREANDO NUEVA BASE DE DATOS")
    print("=" * 50)
    print("📊 Base de datos: flask_proyecto_final")
    print("🔗 Host: localhost:3307")
    print("👤 Usuario: root")
    print("🔑 Contraseña: (probando diferentes configuraciones)")
    print("=" * 50)
    
    if crear_base_datos():
        print("\n✅ ¡Base de datos creada exitosamente!")
        print("📌 Ahora ejecuta: python reset_database.py")
    else:
        print("\n❌ Error al crear la base de datos")
        print("📌 Verifica que Laragon esté ejecutándose")
        print("📌 Abre Laragon y verifica las credenciales de MySQL")
        print("📌 Puedes intentar cambiar la contraseña en phpMyAdmin")
