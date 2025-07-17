"""
Servicio de Grafo - Responsabilidad: Lógica de negocio para algoritmos de grafos
"""
import networkx as nx
from typing import List, Dict, Any, Optional, Tuple
from models.repositories.ciudad_repository import CiudadRepository
from models.repositories.ruta_repository import RutaRepository


class GrafoService:
    """
    Servicio para lógica de negocio de grafos y rutas
    
    Responsabilidades:
    - Algoritmos de grafos (Dijkstra, etc.)
    - Cálculo de rutas óptimas
    - Estadísticas de red
    """
    
    def __init__(self):
        self.ciudad_repository = CiudadRepository()
        self.ruta_repository = RutaRepository()
    
    def crear_grafo(self) -> nx.Graph:
        """Crea un grafo de NetworkX con las ciudades y rutas"""
        grafo = nx.Graph()
        
        # Agregar ciudades como nodos
        ciudades = self.ciudad_repository.get_all()
        for ciudad in ciudades:
            grafo.add_node(ciudad.id, 
                          nombre=ciudad.nombre, 
                          provincia=ciudad.provincia.nombre,
                          es_costera=ciudad.es_costera)
        
        # Agregar rutas como aristas
        rutas = self.ruta_repository.get_all()
        for ruta in rutas:
            grafo.add_edge(ruta.ciudad_origen_id, 
                          ruta.ciudad_destino_id, 
                          peso=float(ruta.get_peso()))
        
        return grafo
    
    def calcular_ruta_mas_corta(self, origen_id: int, destino_id: int) -> Dict[str, Any]:
        """
        Calcula la ruta más corta entre dos ciudades usando Dijkstra
        
        Returns:
            dict: Información de la ruta más corta
        """
        try:
            grafo = self.crear_grafo()
            
            # Verificar que ambas ciudades existan
            if origen_id not in grafo.nodes or destino_id not in grafo.nodes:
                return {'success': False, 'error': 'Una o ambas ciudades no existen'}
            
            # Calcular ruta más corta
            try:
                ruta = nx.shortest_path(grafo, origen_id, destino_id, weight='peso')
                distancia = nx.shortest_path_length(grafo, origen_id, destino_id, weight='peso')
                
                # Obtener información detallada de la ruta
                ruta_detallada = []
                for i in range(len(ruta) - 1):
                    ciudad_origen = self.ciudad_repository.get_by_id(ruta[i])
                    ciudad_destino = self.ciudad_repository.get_by_id(ruta[i + 1])
                    ruta_obj = self.ruta_repository.get_by_ciudades(ruta[i], ruta[i + 1])
                    
                    ruta_detallada.append({
                        'origen': ciudad_origen.nombre,
                        'destino': ciudad_destino.nombre,
                        'distancia': float(ruta_obj.get_peso()) if ruta_obj else 0
                    })
                
                return {
                    'success': True,
                    'ruta': ruta,
                    'distancia_total': distancia,
                    'numero_paradas': len(ruta) - 1,
                    'ruta_detallada': ruta_detallada
                }
                
            except nx.NetworkXNoPath:
                return {'success': False, 'error': 'No existe ruta entre las ciudades'}
            
        except Exception as e:
            return {'success': False, 'error': f'Error calculando ruta: {str(e)}'}
    
    def obtener_rutas_alternativas(self, origen_id: int, destino_id: int, k: int = 3) -> Dict[str, Any]:
        """
        Obtiene k rutas alternativas entre dos ciudades
        
        Args:
            origen_id: ID de la ciudad origen
            destino_id: ID de la ciudad destino
            k: Número de rutas alternativas a encontrar
            
        Returns:
            dict: Lista de rutas alternativas
        """
        try:
            grafo = self.crear_grafo()
            
            if origen_id not in grafo.nodes or destino_id not in grafo.nodes:
                return {'success': False, 'error': 'Una o ambas ciudades no existen'}
            
            # Encontrar rutas alternativas usando diferentes algoritmos
            rutas_alternativas = []
            
            # Ruta más corta
            ruta_corta = self.calcular_ruta_mas_corta(origen_id, destino_id)
            if ruta_corta['success']:
                rutas_alternativas.append({
                    'tipo': 'Ruta más corta',
                    'ruta': ruta_corta['ruta'],
                    'distancia': ruta_corta['distancia_total'],
                    'paradas': ruta_corta['numero_paradas']
                })
            
            # Intentar encontrar rutas alternativas eliminando aristas
            grafo_temp = grafo.copy()
            for i in range(min(k - 1, 3)):  # Máximo 3 alternativas adicionales
                try:
                    # Eliminar la arista más usada de la ruta anterior
                    if rutas_alternativas:
                        ruta_anterior = rutas_alternativas[-1]['ruta']
                        for j in range(len(ruta_anterior) - 1):
                            if grafo_temp.has_edge(ruta_anterior[j], ruta_anterior[j + 1]):
                                grafo_temp.remove_edge(ruta_anterior[j], ruta_anterior[j + 1])
                                break
                    
                    # Buscar nueva ruta
                    nueva_ruta = nx.shortest_path(grafo_temp, origen_id, destino_id, weight='peso')
                    nueva_distancia = nx.shortest_path_length(grafo_temp, origen_id, destino_id, weight='peso')
                    
                    rutas_alternativas.append({
                        'tipo': f'Ruta alternativa {i + 1}',
                        'ruta': nueva_ruta,
                        'distancia': nueva_distancia,
                        'paradas': len(nueva_ruta) - 1
                    })
                    
                except (nx.NetworkXNoPath, nx.NetworkXError):
                    break
            
            return {
                'success': True,
                'rutas_alternativas': rutas_alternativas,
                'total_rutas': len(rutas_alternativas)
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Error obteniendo rutas alternativas: {str(e)}'}
    
    def obtener_estadisticas_grafo(self) -> Dict[str, Any]:
        """Obtiene estadísticas del grafo de ciudades y rutas"""
        try:
            grafo = self.crear_grafo()
            
            # Estadísticas básicas
            num_ciudades = grafo.number_of_nodes()
            num_rutas = grafo.number_of_edges()
            
            # Conectividad
            es_conectado = nx.is_connected(grafo)
            componentes = nx.number_connected_components(grafo)
            
            # Centralidad
            centralidad = nx.degree_centrality(grafo)
            ciudad_mas_conectada = max(centralidad, key=centralidad.get) if centralidad else None
            
            # Distancias
            if es_conectado:
                diametro = nx.diameter(grafo)
                radio = nx.radius(grafo)
                centro = nx.center(grafo)
            else:
                diametro = None
                radio = None
                centro = []
            
            # Información de la ciudad más conectada
            ciudad_central = None
            if ciudad_mas_conectada:
                ciudad_obj = self.ciudad_repository.get_by_id(ciudad_mas_conectada)
                ciudad_central = {
                    'id': ciudad_mas_conectada,
                    'nombre': ciudad_obj.nombre if ciudad_obj else 'Desconocida',
                    'conexiones': grafo.degree(ciudad_mas_conectada),
                    'centralidad': centralidad[ciudad_mas_conectada]
                }
            
            return {
                'num_ciudades': num_ciudades,
                'num_rutas': num_rutas,
                'es_conectado': es_conectado,
                'componentes_conexas': componentes,
                'ciudad_mas_conectada': ciudad_central,
                'diametro': diametro,
                'radio': radio,
                'ciudades_centrales': [self.ciudad_repository.get_by_id(c).nombre for c in centro] if centro else []
            }
            
        except Exception as e:
            return {'error': f'Error obteniendo estadísticas: {str(e)}'}
    
    def obtener_ciudades_por_conectividad(self) -> Dict[str, Any]:
        """Obtiene ciudades ordenadas por su conectividad"""
        try:
            grafo = self.crear_grafo()
            
            # Calcular grado de cada ciudad
            grados = dict(grafo.degree())
            
            # Ordenar por conectividad
            ciudades_ordenadas = sorted(grados.items(), key=lambda x: x[1], reverse=True)
            
            # Obtener información detallada
            ciudades_info = []
            for ciudad_id, grado in ciudades_ordenadas:
                ciudad = self.ciudad_repository.get_by_id(ciudad_id)
                if ciudad:
                    ciudades_info.append({
                        'id': ciudad_id,
                        'nombre': ciudad.nombre,
                        'provincia': ciudad.provincia.nombre,
                        'conexiones': grado,
                        'es_costera': ciudad.es_costera
                    })
            
            return {
                'success': True,
                'ciudades': ciudades_info,
                'total_ciudades': len(ciudades_info)
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Error obteniendo conectividad: {str(e)}'}
    
    def validar_ruta_directa(self, origen_id: int, destino_id: int) -> Dict[str, Any]:
        """Valida si existe una ruta directa entre dos ciudades"""
        try:
            ruta = self.ruta_repository.get_by_ciudades(origen_id, destino_id)
            
            if ruta:
                return {
                    'success': True,
                    'existe_ruta_directa': True,
                    'distancia': float(ruta.get_peso()),
                    'ruta_info': ruta.to_dict()
                }
            else:
                return {
                    'success': True,
                    'existe_ruta_directa': False,
                    'mensaje': 'No existe ruta directa entre las ciudades'
                }
                
        except Exception as e:
            return {'success': False, 'error': f'Error validando ruta: {str(e)}'}
