#!/usr/bin/env python3
"""
Script de prueba para verificar que la aplicación funciona correctamente
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Prueba que todas las importaciones funcionen correctamente"""
    try:
        print("Probando importaciones...")
        
        # Importar Flask y extensiones
        from flask import Flask
        from flask_login import LoginManager
        from flask_bcrypt import Bcrypt
        from flask_sqlalchemy import SQLAlchemy
        print("✓ Flask y extensiones importadas correctamente")
        
        # Importar modelos
        from models.config import Config
        from models.models import db, bcrypt, User, Ciudad, Ruta
        print("✓ Modelos importados correctamente")
        
        # Importar controladores
        from controllers.grafo_utils import obtener_ciudades, camino_optimo_con_costera
        print("✓ Controladores importados correctamente")
        
        # Importar rutas
        from routes import register_blueprints
        print("✓ Rutas importadas correctamente")
        
        # Crear aplicación de prueba
        app = Flask(__name__)
        app.config.from_object(Config)
        
        # Inicializar extensiones
        db.init_app(app)
        bcrypt.init_app(app)
        
        with app.app_context():
            print("✓ Aplicación Flask creada correctamente")
            
        print("\n🎉 ¡Todas las importaciones funcionan correctamente!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error en las importaciones: {str(e)}")
        return False

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    try:
        print("\nProbando conexión a la base de datos...")
        
        from app import create_app
        app = create_app()
        
        with app.app_context():
            from models.models import db
            # Intentar conectar a la base de datos
            db.engine.connect()
            print("✓ Conexión a la base de datos exitosa")
            return True
            
    except Exception as e:
        print(f"❌ Error en la conexión a la base de datos: {str(e)}")
        print("📝 Asegúrate de que:")
        print("   - Laragon esté ejecutándose")
        print("   - MySQL esté en el puerto 3307")
        print("   - La base de datos 'proyecto_rutas' exista")
        return False

if __name__ == "__main__":
    print("🔍 VERIFICACIÓN DEL SISTEMA DE RUTAS")
    print("="*50)
    
    # Verificar importaciones
    imports_ok = test_imports()
    
    if imports_ok:
        # Verificar conexión a base de datos
        db_ok = test_database_connection()
        
        if db_ok:
            print("\n✅ ¡Sistema listo para ejecutar!")
            print("📍 Ejecuta 'start_fixed.bat' para iniciar la aplicación")
        else:
            print("\n⚠️  Sistema funcional pero sin conexión a base de datos")
            print("📍 Configura la base de datos y ejecuta 'start_fixed.bat'")
    else:
        print("\n❌ Sistema no funcional")
        print("📍 Revisa las dependencias y configuración")
