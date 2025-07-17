"""
Script de inicialización de datos para el sistema de rutas
"""
from models.models import db, User, Ciudad, Ruta

def init_data():
    """Inicializa datos de ejemplo en la base de datos"""
    
    # Crear ciudades de ejemplo
    ciudades_data = [
        {'nombre': 'Ibarra', 'es_costera': False, 'latitud': 0.3516, 'longitud': -78.1312},
        {'nombre': 'Quito', 'es_costera': False, 'latitud': -0.1807, 'longitud': -78.4678},
        {'nombre': 'Santo Domingo', 'es_costera': False, 'latitud': -0.2532, 'longitud': -79.1745},
        {'nombre': 'Manta', 'es_costera': True, 'latitud': -0.9517, 'longitud': -80.7217},
        {'nombre': 'Portoviejo', 'es_costera': True, 'latitud': -1.0506, 'longitud': -80.4542},
        {'nombre': 'Guayaquil', 'es_costera': True, 'latitud': -2.1962, 'longitud': -79.8862},
        {'nombre': 'Cuenca', 'es_costera': False, 'latitud': -2.9001, 'longitud': -79.0059},
        {'nombre': 'Loja', 'es_costera': False, 'latitud': -3.9928, 'longitud': -79.2042},
    ]
    
    ciudades_creadas = {}
    for ciudad_data in ciudades_data:
        ciudad_existente = Ciudad.query.filter_by(nombre=ciudad_data['nombre']).first()
        if not ciudad_existente:
            ciudad = Ciudad(**ciudad_data)
            db.session.add(ciudad)
            db.session.flush()  # Para obtener el ID
            ciudades_creadas[ciudad_data['nombre']] = ciudad
        else:
            ciudades_creadas[ciudad_data['nombre']] = ciudad_existente
    
    # Crear usuario administrador si no existe
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin = User(
            username='admin',
            email='admin@rutas.com',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.flush()
        admin_user = admin
    
    # Crear rutas de ejemplo
    rutas_data = [
        {'origen': 'Ibarra', 'destino': 'Quito', 'distancia': 115, 'costo': 10, 'tiempo': 2.0},
        {'origen': 'Quito', 'destino': 'Santo Domingo', 'distancia': 134, 'costo': 15, 'tiempo': 2.5},
        {'origen': 'Quito', 'destino': 'Manta', 'distancia': 269, 'costo': 30, 'tiempo': 5.0},
        {'origen': 'Santo Domingo', 'destino': 'Manta', 'distancia': 168, 'costo': 12, 'tiempo': 3.0},
        {'origen': 'Manta', 'destino': 'Portoviejo', 'distancia': 35, 'costo': 5, 'tiempo': 0.7},
        {'origen': 'Portoviejo', 'destino': 'Guayaquil', 'distancia': 194, 'costo': 20, 'tiempo': 3.5},
        {'origen': 'Guayaquil', 'destino': 'Cuenca', 'distancia': 193, 'costo': 25, 'tiempo': 3.8},
        {'origen': 'Cuenca', 'destino': 'Loja', 'distancia': 210, 'costo': 18, 'tiempo': 4.0},
        {'origen': 'Quito', 'destino': 'Cuenca', 'distancia': 432, 'costo': 35, 'tiempo': 8.0},
        {'origen': 'Santo Domingo', 'destino': 'Guayaquil', 'distancia': 290, 'costo': 22, 'tiempo': 5.5},
        {'origen': 'Guayaquil', 'destino': 'Loja', 'distancia': 447, 'costo': 40, 'tiempo': 8.5},
    ]
    
    for ruta_data in rutas_data:
        origen = ciudades_creadas[ruta_data['origen']]
        destino = ciudades_creadas[ruta_data['destino']]
        
        # Verificar si la ruta ya existe
        ruta_existente = Ruta.query.filter_by(
            ciudad_origen_id=origen.id,
            ciudad_destino_id=destino.id
        ).first()
        
        if not ruta_existente:
            ruta = Ruta(
                ciudad_origen_id=origen.id,
                ciudad_destino_id=destino.id,
                distancia=ruta_data['distancia'],
                costo=ruta_data['costo'],
                tiempo_estimado=ruta_data['tiempo'],
                estado='activa',
                created_by=admin_user.id
            )
            db.session.add(ruta)
    
    try:
        db.session.commit()
        print("✅ Datos de ejemplo creados exitosamente!")
        print("🔑 Usuario administrador: admin / admin123")
        print(f"🏙️  Ciudades creadas: {len(ciudades_data)}")
        print(f"🛣️  Rutas creadas: {len(rutas_data)}")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error al crear datos: {e}")

if __name__ == "__main__":
    from app import create_app
    
    app = create_app()
    with app.app_context():
        init_data()
