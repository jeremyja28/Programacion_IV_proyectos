#!/usr/bin/env python3
"""
Script para resetear la base de datos y recrear las tablas con la nueva estructura
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models.models import db, User, Provincia, Ciudad, Ruta

def reset_database():
    """Elimina todas las tablas y las recrea con la nueva estructura"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🗑️  Eliminando tablas existentes...")
            
            # Eliminar todas las tablas
            db.drop_all()
            print("✅ Tablas eliminadas exitosamente")
            
            # Recrear todas las tablas con la nueva estructura
            print("🔧 Creando tablas con nueva estructura...")
            db.create_all()
            print("✅ Tablas creadas exitosamente")
            
            # Crear provincias del Ecuador
            print("🏛️  Creando provincias...")
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
            print(f"✅ {len(provincias_ecuador)} provincias creadas")
            
            # Crear ciudades iniciales
            print("🏙️  Creando ciudades iniciales...")
            pichincha = Provincia.query.filter_by(nombre='Pichincha').first()
            guayas = Provincia.query.filter_by(nombre='Guayas').first()
            azuay = Provincia.query.filter_by(nombre='Azuay').first()
            manabi = Provincia.query.filter_by(nombre='Manabí').first()
            esmeraldas = Provincia.query.filter_by(nombre='Esmeraldas').first()
            el_oro = Provincia.query.filter_by(nombre='El Oro').first()
            tungurahua = Provincia.query.filter_by(nombre='Tungurahua').first()
            imbabura = Provincia.query.filter_by(nombre='Imbabura').first()
            loja = Provincia.query.filter_by(nombre='Loja').first()
            cotopaxi = Provincia.query.filter_by(nombre='Cotopaxi').first()
            
            ciudades_iniciales = [
                {'nombre': 'Quito', 'provincia_id': pichincha.id, 'es_costera': False},
                {'nombre': 'Guayaquil', 'provincia_id': guayas.id, 'es_costera': True},
                {'nombre': 'Cuenca', 'provincia_id': azuay.id, 'es_costera': False},
                {'nombre': 'Manta', 'provincia_id': manabi.id, 'es_costera': True},
                {'nombre': 'Portoviejo', 'provincia_id': manabi.id, 'es_costera': False},
                {'nombre': 'Machala', 'provincia_id': el_oro.id, 'es_costera': True},
                {'nombre': 'Esmeraldas', 'provincia_id': esmeraldas.id, 'es_costera': True},
                {'nombre': 'Ambato', 'provincia_id': tungurahua.id, 'es_costera': False},
                {'nombre': 'Ibarra', 'provincia_id': imbabura.id, 'es_costera': False},
                {'nombre': 'Loja', 'provincia_id': loja.id, 'es_costera': False},
                {'nombre': 'Latacunga', 'provincia_id': cotopaxi.id, 'es_costera': False},
            ]
            
            for ciudad_data in ciudades_iniciales:
                ciudad = Ciudad(**ciudad_data)
                db.session.add(ciudad)
            
            db.session.commit()
            print(f"✅ {len(ciudades_iniciales)} ciudades creadas")
            
            # Crear usuario administrador
            print("👤 Creando usuario administrador...")
            admin = User(
                username='admin',
                email='admin@proyecto.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuario administrador creado")
            
            # Crear algunas rutas de ejemplo
            print("🛣️  Creando rutas de ejemplo...")
            quito_ciudad = Ciudad.query.filter_by(nombre='Quito').first()
            guayaquil_ciudad = Ciudad.query.filter_by(nombre='Guayaquil').first()
            cuenca_ciudad = Ciudad.query.filter_by(nombre='Cuenca').first()
            manta_ciudad = Ciudad.query.filter_by(nombre='Manta').first()
            ambato_ciudad = Ciudad.query.filter_by(nombre='Ambato').first()
            ibarra_ciudad = Ciudad.query.filter_by(nombre='Ibarra').first()
            loja_ciudad = Ciudad.query.filter_by(nombre='Loja').first()
            
            rutas_ejemplo = [
                {'ciudad_origen_id': quito_ciudad.id, 'ciudad_destino_id': guayaquil_ciudad.id, 'distancia': 420.0, 'costo': 25.0, 'created_by': admin.id},
                {'ciudad_origen_id': quito_ciudad.id, 'ciudad_destino_id': cuenca_ciudad.id, 'distancia': 465.0, 'costo': 30.0, 'created_by': admin.id},
                {'ciudad_origen_id': guayaquil_ciudad.id, 'ciudad_destino_id': manta_ciudad.id, 'distancia': 190.0, 'costo': 15.0, 'created_by': admin.id},
                {'ciudad_origen_id': quito_ciudad.id, 'ciudad_destino_id': ambato_ciudad.id, 'distancia': 135.0, 'costo': 10.0, 'created_by': admin.id},
                {'ciudad_origen_id': quito_ciudad.id, 'ciudad_destino_id': ibarra_ciudad.id, 'distancia': 115.0, 'costo': 8.0, 'created_by': admin.id},
                {'ciudad_origen_id': cuenca_ciudad.id, 'ciudad_destino_id': loja_ciudad.id, 'distancia': 210.0, 'costo': 12.0, 'created_by': admin.id},
                {'ciudad_origen_id': ambato_ciudad.id, 'ciudad_destino_id': cuenca_ciudad.id, 'distancia': 145.0, 'costo': 9.0, 'created_by': admin.id},
                {'ciudad_origen_id': ibarra_ciudad.id, 'ciudad_destino_id': loja_ciudad.id, 'distancia': 780.0, 'costo': 45.0, 'created_by': admin.id},
            ]
            
            for ruta_data in rutas_ejemplo:
                ruta = Ruta(**ruta_data)
                db.session.add(ruta)
            
            db.session.commit()
            print(f"✅ {len(rutas_ejemplo)} rutas de ejemplo creadas")
            
            print("\n🎉 ¡Base de datos reseteada exitosamente!")
            print("=" * 60)
            print("📋 RESUMEN:")
            print(f"   Provincias: {Provincia.query.count()}")
            print(f"   Ciudades: {Ciudad.query.count()}")
            print(f"   Rutas: {Ruta.query.count()}")
            print(f"   Usuarios: {User.query.count()}")
            print("\n🔑 Credenciales de acceso:")
            print("   Usuario: admin")
            print("   Contraseña: admin123")
            print("   URL: http://localhost:4000")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al resetear la base de datos: {str(e)}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("🔄 RESETEO DE BASE DE DATOS")
    print("=" * 60)
    print("⚠️  ADVERTENCIA: Este script eliminará todos los datos existentes")
    
    respuesta = input("\n¿Continuar? (s/N): ").lower()
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        if reset_database():
            print("\n✅ Proceso completado exitosamente")
        else:
            print("\n❌ Error en el proceso")
    else:
        print("\n❌ Operación cancelada")
