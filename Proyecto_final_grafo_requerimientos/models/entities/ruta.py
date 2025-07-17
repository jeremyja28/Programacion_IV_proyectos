"""
Entidad Ruta - Responsabilidad: Manejo de rutas entre ciudades
"""
from datetime import datetime
from models.database import db


class Ruta(db.Model):
    """
    Modelo de Ruta
    
    Responsabilidades:
    - Gestión de conexiones entre ciudades
    - Cálculo de distancias/pesos
    - Información de rutas para algoritmos de grafos
    """
    __tablename__ = 'rutas'
    
    # Campos de la tabla
    id = db.Column(db.Integer, primary_key=True)
    ciudad_origen_id = db.Column(db.Integer, db.ForeignKey('ciudades.id'), nullable=False)
    ciudad_destino_id = db.Column(db.Integer, db.ForeignKey('ciudades.id'), nullable=False)
    peso = db.Column(db.Numeric(10, 2), nullable=False)  # Distancia/peso de la ruta
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraint para evitar rutas duplicadas
    __table_args__ = (db.UniqueConstraint('ciudad_origen_id', 'ciudad_destino_id', name='unique_ruta'),)
    
    def get_distancia(self) -> float:
        """Obtiene la distancia de la ruta como float"""
        return float(self.peso)
    
    def get_ruta_inversa(self):
        """Busca la ruta inversa (destino -> origen)"""
        from models.entities.ruta import Ruta
        return Ruta.query.filter_by(
            ciudad_origen_id=self.ciudad_destino_id,
            ciudad_destino_id=self.ciudad_origen_id
        ).first()
    
    def es_bidireccional(self) -> bool:
        """Verifica si existe una ruta en ambas direcciones"""
        return self.get_ruta_inversa() is not None
    
    def get_descripcion(self) -> str:
        """Obtiene una descripción legible de la ruta"""
        return f"{self.ciudad_origen.nombre} → {self.ciudad_destino.nombre} ({self.peso} km)"
    
    def to_dict(self) -> dict:
        """Convierte la ruta a diccionario para JSON"""
        return {
            'id': self.id,
            'ciudad_origen_id': self.ciudad_origen_id,
            'ciudad_origen_nombre': self.ciudad_origen.nombre,
            'ciudad_destino_id': self.ciudad_destino_id,
            'ciudad_destino_nombre': self.ciudad_destino.nombre,
            'peso': float(self.peso),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'descripcion': self.get_descripcion(),
            'es_bidireccional': self.es_bidireccional()
        }
    
    def __repr__(self) -> str:
        return f'<Ruta {self.get_descripcion()}>'
