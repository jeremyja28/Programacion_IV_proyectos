from extensions import db

class Ciudad(db.Model):
    """Model for cities management (simplified)"""
    
    __tablename__ = 'ciudades'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    es_costera = db.Column(db.Boolean, default=False, nullable=False)
    provincia_id = db.Column(db.Integer, db.ForeignKey('provincias.id'), nullable=False)
    
    # Relationships
    rutas_origen = db.relationship('Ruta', foreign_keys='Ruta.ciudad_origen_id', backref='ciudad_origen', lazy=True)
    rutas_destino = db.relationship('Ruta', foreign_keys='Ruta.ciudad_destino_id', backref='ciudad_destino', lazy=True)
    
    # Unique constraint handled by database
    __table_args__ = (db.UniqueConstraint('nombre', 'provincia_id', name='unique_city_province'),)
    
    def __init__(self, nombre, es_costera, provincia_id):
        self.nombre = nombre
        self.es_costera = es_costera
        self.provincia_id = provincia_id
    
    def __repr__(self):
        return f'<Ciudad {self.nombre} ({"Costera" if self.es_costera else "Interior"})>'
    
    def get_rutas_salida(self):
        """Get all routes starting from this city"""
        return self.rutas_origen
    
    def get_rutas_llegada(self):
        """Get all routes ending at this city"""
        return self.rutas_destino
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'es_costera': self.es_costera,
            'provincia_id': self.provincia_id,
            'provincia_nombre': self.provincia.nombre if self.provincia else None,
            'rutas_count': len(self.rutas_origen) + len(self.rutas_destino)
        }
