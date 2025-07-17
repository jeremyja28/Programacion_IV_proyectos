# Manejo de entidades de Ciudad
from datetime import datetime
from models.database import db


class Ciudad(db.Model):
    """
    Modelo de Ciudad
    
    Responsabilidades:
    - Gestión de datos de ciudades
    - Relaciones con provincias y rutas
    - Información geográfica
    """
    __tablename__ = 'ciudades'
    
    # Campos de la tabla
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    provincia_id = db.Column(db.Integer, db.ForeignKey('provincias.id'), nullable=False)
    es_costera = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    rutas_origen = db.relationship('Ruta', foreign_keys='Ruta.ciudad_origen_id', 
                                  backref='ciudad_origen', lazy='dynamic', cascade='all, delete-orphan')
    rutas_destino = db.relationship('Ruta', foreign_keys='Ruta.ciudad_destino_id', 
                                   backref='ciudad_destino', lazy='dynamic', cascade='all, delete-orphan')
    
    # Constraint para evitar ciudades duplicadas en la misma provincia
    __table_args__ = (db.UniqueConstraint('nombre', 'provincia_id', name='unique_ciudad_provincia'),)
    
    def get_rutas_count(self) -> int:
        # Obtiene el número total de rutas desde esta ciudad
        return self.rutas_origen.count()
    
    def get_conexiones_disponibles(self) -> list:
        #Obtiene todas las ciudades conectadas directamente
        rutas = self.rutas_origen.all()
        return [ruta.ciudad_destino for ruta in rutas]
    
    def es_conectada_con(self, otra_ciudad_id: int) -> bool:
        #Verifica si esta ciudad está conectada directamente con otra
        return self.rutas_origen.filter_by(ciudad_destino_id=otra_ciudad_id).first() is not None
    
    def get_nombre_completo(self) -> str:
        #Obtiene el nombre completo: ciudad y provincia
        return f"{self.nombre}, {self.provincia.nombre}"
    
    def to_dict(self) -> dict:
        #Convierte la ciudad a diccionario
        return {
            'id': self.id,
            'nombre': self.nombre,
            'provincia_id': self.provincia_id,
            'provincia_nombre': self.provincia.nombre,
            'es_costera': self.es_costera,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'rutas_count': self.get_rutas_count(),
            'nombre_completo': self.get_nombre_completo()
        }
    
    def __repr__(self) -> str:
        return f'<Ciudad {self.get_nombre_completo()}>'
