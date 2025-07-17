"""
Entidad Provincia - Responsabilidad: Manejo de provincias del Ecuador
"""
from datetime import datetime
from models.database import db


class Provincia(db.Model):
    """
    Modelo de Provincia
    
    Responsabilidades:
    - Gestión de datos de provincias
    - Relaciones con ciudades
    - Información geográfica básica
    """
    __tablename__ = 'provincias'
    
    # Campos de la tabla
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    codigo = db.Column(db.String(10), unique=True, nullable=True)  # Código ISO o similar
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    ciudades = db.relationship('Ciudad', backref='provincia', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_ciudades_count(self) -> int:
        """Obtiene el número de ciudades en la provincia"""
        return self.ciudades.count()
    
    def get_ciudades_costeras(self) -> list:
        """Obtiene las ciudades costeras de la provincia"""
        return self.ciudades.filter_by(es_costera=True).all()
    
    def to_dict(self) -> dict:
        """Convierte la provincia a diccionario para JSON"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'codigo': self.codigo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'ciudades_count': self.get_ciudades_count()
        }
    
    def __repr__(self) -> str:
        return f'<Provincia {self.nombre}>'
