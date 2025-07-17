from extensions import db

class Ruta(db.Model):
    """Model for routes management (simplified - only weight/distance)"""
    
    __tablename__ = 'rutas'
    
    id = db.Column(db.Integer, primary_key=True)
    peso = db.Column(db.Numeric(10, 2), nullable=False)
    ciudad_origen_id = db.Column(db.Integer, db.ForeignKey('ciudades.id'), nullable=False)
    ciudad_destino_id = db.Column(db.Integer, db.ForeignKey('ciudades.id'), nullable=False)
    
    # Constraints handled by database
    __table_args__ = (
        db.CheckConstraint('peso > 0', name='chk_positive_weight'),
        db.CheckConstraint('ciudad_origen_id != ciudad_destino_id', name='chk_different_cities'),
        db.UniqueConstraint('ciudad_origen_id', 'ciudad_destino_id', name='unique_route')
    )
    
    def __init__(self, peso, ciudad_origen_id, ciudad_destino_id):
        self.peso = peso
        self.ciudad_origen_id = ciudad_origen_id
        self.ciudad_destino_id = ciudad_destino_id
    
    def __repr__(self):
        return f'<Ruta {self.ciudad_origen.nombre} -> {self.ciudad_destino.nombre} (Peso: {self.peso})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'peso': float(self.peso),
            'ciudad_origen_id': self.ciudad_origen_id,
            'ciudad_destino_id': self.ciudad_destino_id,
            'ciudad_origen_nombre': self.ciudad_origen.nombre if self.ciudad_origen else None,
            'ciudad_destino_nombre': self.ciudad_destino.nombre if self.ciudad_destino else None,
            'ciudad_origen_costera': self.ciudad_origen.es_costera if self.ciudad_origen else False,
            'ciudad_destino_costera': self.ciudad_destino.es_costera if self.ciudad_destino else False
        }
