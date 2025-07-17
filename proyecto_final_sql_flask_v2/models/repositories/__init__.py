# models/repositories/__init__.py
from .base_repository import BaseRepository
from .user_repository import UserRepository
from .provincia_repository import ProvinciaRepository
from .ciudad_repository import CiudadRepository
from .ruta_repository import RutaRepository

__all__ = [
    'BaseRepository', 
    'UserRepository', 
    'ProvinciaRepository', 
    'CiudadRepository', 
    'RutaRepository'
]
