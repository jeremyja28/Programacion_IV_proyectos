"""
Repositorio Base - Responsabilidad: Operaciones CRUD genéricas
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Any
from models.database import db


class BaseRepository(ABC):
    """
    Repositorio base con operaciones CRUD genéricas
    
    Responsabilidades:
    - Definir interfaz común para todos los repositorios
    - Implementar operaciones CRUD básicas
    - Manejo de transacciones
    """
    
    def __init__(self, model_class):
        self.model_class = model_class
    
    def create(self, **kwargs) -> Any:
        """Crea una nueva instancia del modelo"""
        instance = self.model_class(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance
    
    def get_by_id(self, id: int) -> Optional[Any]:
        """Obtiene una instancia por ID"""
        return self.model_class.query.get(id)
    
    def get_all(self) -> List[Any]:
        """Obtiene todas las instancias"""
        return self.model_class.query.all()
    
    def update(self, instance: Any, **kwargs) -> Any:
        """Actualiza una instancia existente"""
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        db.session.commit()
        return instance
    
    def delete(self, instance: Any) -> bool:
        """Elimina una instancia"""
        try:
            db.session.delete(instance)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False
    
    def count(self) -> int:
        """Cuenta el número total de instancias"""
        return self.model_class.query.count()
    
    def exists(self, id: int) -> bool:
        """Verifica si existe una instancia con el ID dado"""
        return self.model_class.query.get(id) is not None
