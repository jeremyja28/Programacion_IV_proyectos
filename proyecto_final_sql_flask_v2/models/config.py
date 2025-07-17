# Importa el módulo os para acceder a las variables de entorno del sistema
import os

# Importa la función load_dotenv para cargar las variables desde el archivo .env
from dotenv import load_dotenv

# Carga automáticamente las variables definidas en el archivo .env al entorno del sistema
load_dotenv()

# Define una clase de configuración para la aplicación Flask
class Config:
    # Construye la URI de conexión a MySQL usando las variables de entorno cargadas
    # Formato: mysql+pymysql://usuario:contraseña@host:puerto/nombre_base
    # Base de datos: proyecto_final_version2
    # Configuración con charset UTF-8 para caracteres especiales
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASSWORD', '')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3307')}/{os.getenv('DB_NAME', 'proyecto_final_version2')}?charset=utf8mb4"
    
    # Desactiva el rastreo de modificaciones de objetos (recomendado para rendimiento)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración adicional para la conexión a la base de datos
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Verifica conexiones antes de usar
        'pool_recycle': 3600,   # Recicla conexiones cada hora
        'pool_timeout': 20,     # Timeout de 20 segundos para obtener conexión
        'max_overflow': 20,     # Máximo de conexiones adicionales
        'echo': False           # No mostrar SQL en consola
    }
    
    # Configuración para Flask-Login y seguridad
    SECRET_KEY = os.getenv('SECRET_KEY', 'tu-clave-secreta-super-segura-aqui')
    
    # Configuración de sesiones
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
