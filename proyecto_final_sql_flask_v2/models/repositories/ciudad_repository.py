# Repositorio de ciudad
from typing import Optional, List
from models.entities.ciudad import Ciudad
from models.repositories.base_repository import BaseRepository


class CiudadRepository(BaseRepository):
    def __init__(self):
        super().__init__(Ciudad)
    
    def get_by_nombre(self, nombre: str) -> List[Ciudad]:
        # Obtiene ciudades por nombre (puede haber varias en diferentes provincias)
        return Ciudad.query.filter_by(nombre=nombre).all()
    
    def get_by_provincia(self, provincia_id: int) -> List[Ciudad]:
        # Obtiene todas las ciudades de una provincia
        return Ciudad.query.filter_by(provincia_id=provincia_id).all()
    
    def get_by_nombre_y_provincia(self, nombre: str, provincia_id: int) -> Optional[Ciudad]:
        # Obtiene una ciudad específica por nombre y provincia
        return Ciudad.query.filter_by(nombre=nombre, provincia_id=provincia_id).first()
    
    def get_costeras(self) -> List[Ciudad]:
        # Obtiene todas las ciudades costeras
        return Ciudad.query.filter_by(es_costera=True).all()
    
    def get_no_costeras(self) -> List[Ciudad]:
        # Obtiene todas las ciudades no costeras
        return Ciudad.query.filter_by(es_costera=False).all()
    
    def get_con_rutas(self) -> List[Ciudad]:
        # Obtiene ciudades que tienen al menos una ruta
        return Ciudad.query.filter(Ciudad.rutas_origen.any()).all()
    
    def get_sin_rutas(self) -> List[Ciudad]:
        # Obtiene ciudades que no tienen rutas
        return Ciudad.query.filter(~Ciudad.rutas_origen.any()).all()
    
    def get_ordenadas_por_nombre(self) -> List[Ciudad]:
        # Obtiene todas las ciudades ordenadas por nombre
        return Ciudad.query.order_by(Ciudad.nombre).all()
    
    def ciudad_existe_en_provincia(self, nombre: str, provincia_id: int) -> bool:
        # Verifica si una ciudad ya existe en una provincia específica
        return Ciudad.query.filter_by(nombre=nombre, provincia_id=provincia_id).first() is not None
    
    def get_estadisticas(self) -> dict:
        # Obtiene estadísticas de ciudades
        total_ciudades = self.count()
        ciudades_costeras = len(self.get_costeras())
        ciudades_con_rutas = len(self.get_con_rutas())
        
        return {
            'total_ciudades': total_ciudades,
            'ciudades_costeras': ciudades_costeras,
            'ciudades_no_costeras': total_ciudades - ciudades_costeras,
            'ciudades_con_rutas': ciudades_con_rutas,
            'ciudades_sin_rutas': total_ciudades - ciudades_con_rutas
        }
