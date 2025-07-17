#Entidad usuario
from flask_login import UserMixin
from datetime import datetime
from models.database import db, bcrypt


class User(UserMixin, db.Model):

    __tablename__ = 'usuarios'  # Volver a usar la tabla usuarios
    
    # Campos de la tabla
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    es_admin = db.Column(db.Boolean, default=False)  # Campo es_admin de la tabla usuarios
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password: str) -> None:
        # Establece la contraseña del usuario de forma segura
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        #Verifica si la contraseña proporcionada es correcta
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def is_admin(self) -> bool:
        # Verifica si el usuario tiene permisos de administrador
        return self.es_admin  # Usar el campo es_admin de la tabla usuarios
    
    @property
    def is_active(self):
        #Propiedad para Flask-Login
        return True
    
    def to_dict(self) -> dict:
        #Convierte el usuario a diccionario para JSON
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'es_admin': self.es_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': True
        }
    
    def __repr__(self) -> str:
        return f'<User {self.username}>'
