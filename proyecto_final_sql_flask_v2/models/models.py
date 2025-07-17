
from models.database import db, bcrypt
from models.entities import User, Provincia, Ciudad, Ruta
from models.repositories import (
    UserRepository, 
    ProvinciaRepository, 
    CiudadRepository, 
    RutaRepository
)
from models.services import UserService, GrafoService

# Exportar todo para mantener compatibilidad
__all__ = [
    'db', 
    'bcrypt', 
    'User', 
    'Provincia', 
    'Ciudad', 
    'Ruta',
    'UserRepository',
    'ProvinciaRepository', 
    'CiudadRepository', 
    'RutaRepository',
    'UserService',
    'GrafoService'
]
