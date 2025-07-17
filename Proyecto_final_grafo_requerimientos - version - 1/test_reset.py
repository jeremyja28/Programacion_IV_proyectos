#!/usr/bin/env python3
"""
Script de prueba para resetear la base de datos con datos de Ecuador
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models.models import db, User, Provincia, Ciudad, Ruta

def test_reset():
    """Prueba del reseteo de base de datos"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔄 Iniciando reseteo de base de datos...")
            
            # Eliminar todas las tablas
            db.drop_all()
            print("✅ Tablas eliminadas")
            
            # Recrear todas las tablas
            db.create_all()
            print("✅ Tablas recreadas")
            
            # Crear provincias del Ecuador
            provincias_ecuador = [
                'Azuay', 'Bolívar', 'Cañar', 'Carchi', 'Chimborazo',
                'Cotopaxi', 'El Oro', 'Esmeraldas', 'Galápagos', 'Guayas',
                'Imbabura', 'Loja', 'Los Ríos', 'Manabí', 'Morona Santiago',
                'Napo', 'Orellana', 'Pastaza', 'Pichincha', 'Santa Elena',
                'Santo Domingo de los Tsáchilas', 'Sucumbíos', 'Tungurahua', 'Zamora Chinchipe'
            ]
            
            for provincia_nombre in provincias_ecuador:
                provincia = Provincia(nombre=provincia_nombre)
                db.session.add(provincia)
            
            db.session.commit()
            print(f"✅ {len(provincias_ecuador)} provincias de Ecuador creadas")
            
            # Crear ciudades
            pichincha = Provincia.query.filter_by(nombre='Pichincha').first()
            guayas = Provincia.query.filter_by(nombre='Guayas').first()
            azuay = Provincia.query.filter_by(nombre='Azuay').first()
            
            ciudades_iniciales = [
                {'nombre': 'Quito', 'provincia_id': pichincha.id, 'es_costera': False, 'latitud': -0.1807, 'longitud': -78.4678},
                {'nombre': 'Guayaquil', 'provincia_id': guayas.id, 'es_costera': True, 'latitud': -2.1709, 'longitud': -79.9224},
                {'nombre': 'Cuenca', 'provincia_id': azuay.id, 'es_costera': False, 'latitud': -2.9001, 'longitud': -79.0059},
            ]
            
            for ciudad_data in ciudades_iniciales:
                ciudad = Ciudad(**ciudad_data)
                db.session.add(ciudad)
            
            db.session.commit()
            print(f"✅ {len(ciudades_iniciales)} ciudades creadas")
            
            # Crear usuario admin
            admin = User(
                username='admin',
                email='admin@proyecto.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuario admin creado")
            
            print("\n🎉 ¡Reseteo completado exitosamente!")
            print(f"📊 Provincias: {Provincia.query.count()}")
            print(f"📊 Ciudades: {Ciudad.query.count()}")
            print(f"👤 Usuarios: {User.query.count()}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == "__main__":
    print("🔄 TEST DE RESETEO DE BASE DE DATOS PARA ECUADOR")
    print("=" * 60)
    test_reset()
