from extensions import db

class Provincia(db.Model):
    """Model for provinces management (simplified)"""
    
    __tablename__ = 'provincias'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    
    # Relationships
    ciudades = db.relationship('Ciudad', backref='provincia', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, nombre):
        self.nombre = nombre
    
    def __repr__(self):
        return f'<Provincia {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'ciudades_count': len(self.ciudades)
        }
