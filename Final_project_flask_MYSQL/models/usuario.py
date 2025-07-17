from extensions import db
from flask_login import UserMixin
from datetime import datetime

class Usuario(UserMixin, db.Model):
    """Model for user management (simplified)"""
    
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    es_admin = db.Column(db.Boolean, default=False, nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, username, email, password_hash, nombre, apellido, es_admin=False):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.nombre = nombre
        self.apellido = apellido
        self.es_admin = es_admin
    
    def __repr__(self):
        return f'<Usuario {self.username}>'
    
    def get_id(self):
        return str(self.id)
    
    def is_active(self):
        return self.activo
    
    def is_admin(self):
        """Check if user is admin"""
        return self.es_admin
    
    def get_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    def get_full_name(self):
        """Alias for get_nombre_completo() for compatibility"""
        return self.get_nombre_completo()
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'es_admin': self.es_admin,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
