"""
Repositorio de Ruta - Responsabilidad: Acceso a datos de rutas
"""
from typing import Optional, List, Tuple
from models.entities.ruta import Ruta
from models.repositories.base_repository import BaseRepository


class RutaRepository(BaseRepository):
    """
    Repositorio para operaciones de datos de rutas
    
    Responsabilidades:
    - Operaciones CRUD específicas para rutas
    - Consultas de grafos y conexiones
    - Algoritmos de rutas
    """
    
    def __init__(self):
        super().__init__(Ruta)
    
    def get_by_ciudades(self, origen_id: int, destino_id: int) -> Optional[Ruta]:
        """Obtiene una ruta específica entre dos ciudades"""
        return Ruta.query.filter_by(
            ciudad_origen_id=origen_id,
            ciudad_destino_id=destino_id
        ).first()
    
    def get_desde_ciudad(self, ciudad_id: int) -> List[Ruta]:
        """Obtiene todas las rutas que salen de una ciudad"""
        return Ruta.query.filter_by(ciudad_origen_id=ciudad_id).all()
    
    def get_hacia_ciudad(self, ciudad_id: int) -> List[Ruta]:
        """Obtiene todas las rutas que llegan a una ciudad"""
        return Ruta.query.filter_by(ciudad_destino_id=ciudad_id).all()
    
    def get_rutas_ciudad(self, ciudad_id: int) -> List[Ruta]:
        """Obtiene todas las rutas relacionadas con una ciudad (origen o destino)"""
        return Ruta.query.filter(
            (Ruta.ciudad_origen_id == ciudad_id) | 
            (Ruta.ciudad_destino_id == ciudad_id)
        ).all()
    
    def ruta_existe(self, origen_id: int, destino_id: int) -> bool:
        """Verifica si existe una ruta entre dos ciudades"""
        return self.get_by_ciudades(origen_id, destino_id) is not None
    
    def get_rutas_bidireccionales(self) -> List[Tuple[Ruta, Ruta]]:
        """Obtiene pares de rutas bidireccionales"""
        rutas = self.get_all()
        bidireccionales = []
        
        for ruta in rutas:
            ruta_inversa = self.get_by_ciudades(ruta.ciudad_destino_id, ruta.ciudad_origen_id)
            if ruta_inversa and ruta.id < ruta_inversa.id:  # Evitar duplicados
                bidireccionales.append((ruta, ruta_inversa))
        
        return bidireccionales
    
    def get_rutas_unidireccionales(self) -> List[Ruta]:
        """Obtiene rutas que no tienen ruta inversa"""
        rutas = self.get_all()
        unidireccionales = []
        
        for ruta in rutas:
            if not self.ruta_existe(ruta.ciudad_destino_id, ruta.ciudad_origen_id):
                unidireccionales.append(ruta)
        
        return unidireccionales
    
    def get_ruta_mas_corta(self) -> Optional[Ruta]:
        """Obtiene la ruta con menor peso/distancia"""
        return Ruta.query.order_by(Ruta.peso.asc()).first()
    
    def get_ruta_mas_larga(self) -> Optional[Ruta]:
        """Obtiene la ruta con mayor peso/distancia"""
        return Ruta.query.order_by(Ruta.peso.desc()).first()
    
    def get_rutas_ordenadas_por_distancia(self, ascendente: bool = True) -> List[Ruta]:
        """Obtiene rutas ordenadas por distancia"""
        if ascendente:
            return Ruta.query.order_by(Ruta.peso.asc()).all()
        else:
            return Ruta.query.order_by(Ruta.peso.desc()).all()
    
    def get_matriz_adyacencia(self) -> dict:
        """Obtiene la matriz de adyacencia para algoritmos de grafos"""
        rutas = self.get_all()
        matriz = {}
        
        for ruta in rutas:
            if ruta.ciudad_origen_id not in matriz:
                matriz[ruta.ciudad_origen_id] = {}
            matriz[ruta.ciudad_origen_id][ruta.ciudad_destino_id] = float(ruta.peso)
        
        return matriz
    
    def get_estadisticas(self) -> dict:
        """Obtiene estadísticas de rutas"""
        total_rutas = self.count()
        bidireccionales = len(self.get_rutas_bidireccionales())
        unidireccionales = len(self.get_rutas_unidireccionales())
        
        ruta_corta = self.get_ruta_mas_corta()
        ruta_larga = self.get_ruta_mas_larga()
        
        return {
            'total_rutas': total_rutas,
            'rutas_bidireccionales': bidireccionales * 2,  # Cada par cuenta como 2 rutas
            'rutas_unidireccionales': unidireccionales,
            'distancia_minima': float(ruta_corta.peso) if ruta_corta else 0,
            'distancia_maxima': float(ruta_larga.peso) if ruta_larga else 0
        }
