from models import db, Ruta
from app import create_app
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        result = db.session.execute(text('DESCRIBE rutas'))
        print('Estructura de la tabla rutas:')
        for row in result:
            print(row)
    except Exception as e:
        print(f"Error: {e}")
        print("Intentando verificar si la tabla existe...")
        try:
            result = db.session.execute(text('SHOW TABLES'))
            print('Tablas disponibles:')
            for row in result:
                print(row)
        except Exception as e2:
            print(f"Error al mostrar tablas: {e2}")
