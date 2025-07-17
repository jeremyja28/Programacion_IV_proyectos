"""
Base de datos y configuración central
"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Instancias globales
db = SQLAlchemy()
bcrypt = Bcrypt()
