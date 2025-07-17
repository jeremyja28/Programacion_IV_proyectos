"""
Repositorio de Provincia - Responsabilidad: Acceso a datos de provincias
"""
from typing import Optional, List
from models.entities.provincia import Provincia
from models.repositories.base_repository import BaseRepository


class ProvinciaRepository(BaseRepository):
    """
    Repositorio para operaciones de datos de provincias
    
    Responsabilidades:
    - Operaciones CRUD específicas para provincias
    - Consultas geográficas
    - Relaciones con ciudades
    """
    
    def __init__(self):
        super().__init__(Provincia)
    
    def get_by_nombre(self, nombre: str) -> Optional[Provincia]:
        """Obtiene una provincia por nombre"""
        return Provincia.query.filter_by(nombre=nombre).first()
    
    def get_by_codigo(self, codigo: str) -> Optional[Provincia]:
        """Obtiene una provincia por código"""
        return Provincia.query.filter_by(codigo=codigo).first()
    
    def nombre_exists(self, nombre: str) -> bool:
        """Verifica si un nombre de provincia ya existe"""
        return Provincia.query.filter_by(nombre=nombre).first() is not None
    
    def codigo_exists(self, codigo: str) -> bool:
        """Verifica si un código de provincia ya existe"""
        return Provincia.query.filter_by(codigo=codigo).first() is not None
    
    def get_ordenadas_por_nombre(self) -> List[Provincia]:
        """Obtiene todas las provincias ordenadas por nombre"""
        return Provincia.query.order_by(Provincia.nombre).all()
    
    def get_con_ciudades(self) -> List[Provincia]:
        """Obtiene provincias que tienen al menos una ciudad"""
        return Provincia.query.filter(Provincia.ciudades.any()).all()
    
    def get_estadisticas(self) -> dict:
        """Obtiene estadísticas de provincias"""
        total_provincias = self.count()
        provincias_con_ciudades = len(self.get_con_ciudades())
        
        return {
            'total_provincias': total_provincias,
            'provincias_con_ciudades': provincias_con_ciudades,
            'provincias_sin_ciudades': total_provincias - provincias_con_ciudades
        }
