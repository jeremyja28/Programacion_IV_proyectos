from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'admin' o 'user'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.username}>'

class Provincia(db.Model):
    __tablename__ = 'provincias'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    codigo = db.Column(db.String(10), unique=True, nullable=True)  # Código ISO o similar
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    ciudades = db.relationship('Ciudad', backref='provincia', lazy='dynamic')
    
    def __repr__(self):
        return f'<Provincia {self.nombre}>'

class Ciudad(db.Model):
    __tablename__ = 'ciudades'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    provincia_id = db.Column(db.Integer, db.ForeignKey('provincias.id'), nullable=False)
    es_costera = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    rutas_origen = db.relationship('Ruta', foreign_keys='Ruta.ciudad_origen_id', backref='ciudad_origen', lazy='dynamic')
    rutas_destino = db.relationship('Ruta', foreign_keys='Ruta.ciudad_destino_id', backref='ciudad_destino', lazy='dynamic')
    
    # Constraint para evitar ciudades duplicadas en la misma provincia
    __table_args__ = (db.UniqueConstraint('nombre', 'provincia_id', name='unique_ciudad_provincia'),)
    
    def __repr__(self):
        return f'<Ciudad {self.nombre}, {self.provincia.nombre}>'

class Ruta(db.Model):
    __tablename__ = 'rutas'
    
    id = db.Column(db.Integer, primary_key=True)
    ciudad_origen_id = db.Column(db.Integer, db.ForeignKey('ciudades.id'), nullable=False)
    ciudad_destino_id = db.Column(db.Integer, db.ForeignKey('ciudades.id'), nullable=False)
    peso = db.Column(db.Float, nullable=False)  # Distancia/peso de la ruta
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraint para evitar rutas duplicadas
    __table_args__ = (db.UniqueConstraint('ciudad_origen_id', 'ciudad_destino_id', name='unique_ruta'),)
    
    def __repr__(self):
        return f'<Ruta {self.ciudad_origen.nombre} -> {self.ciudad_destino.nombre}>'
