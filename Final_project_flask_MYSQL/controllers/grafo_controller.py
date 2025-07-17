from extensions import db
from models.provincia import Provincia
from models.ciudad import Ciudad
from models.ruta import Ruta
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import io
import base64

class GrafoController:
    """Controller for graph management with Dijkstra algorithm (simplified)"""
    
    @staticmethod
    def crear_provincia(nombre):
        """Create a new province"""
        try:
            provincia = Provincia(nombre=nombre)
            db.session.add(provincia)
            db.session.commit()
            return {'success': True, 'provincia': provincia.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def crear_ciudad(nombre, es_costera, provincia_id):
        """Create a new city"""
        try:
            ciudad = Ciudad(nombre=nombre, es_costera=es_costera, provincia_id=provincia_id)
            db.session.add(ciudad)
            db.session.commit()
            return {'success': True, 'ciudad': ciudad.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def crear_ruta(ciudad_origen_id, ciudad_destino_id, peso):
        """Create a new route with weight/distance"""
        try:
            ruta = Ruta(peso=peso, ciudad_origen_id=ciudad_origen_id, ciudad_destino_id=ciudad_destino_id)
            db.session.add(ruta)
            db.session.commit()
            return {'success': True, 'ruta': ruta.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def obtener_provincias():
        """Get all provinces"""
        return Provincia.query.all()
    
    @staticmethod
    def obtener_ciudades():
        """Get all cities"""
        return Ciudad.query.all()
    
    @staticmethod
    def obtener_rutas():
        """Get all routes"""
        return Ruta.query.all()
    
    @staticmethod
    def crear_grafo():
        """Create NetworkX graph from database"""
        G = nx.DiGraph()
        
        # Add cities as nodes
        ciudades = Ciudad.query.all()
        for ciudad in ciudades:
            G.add_node(ciudad.id, 
                      nombre=ciudad.nombre, 
                      es_costera=ciudad.es_costera,
                      provincia=ciudad.provincia.nombre)
        
        # Add routes as edges
        rutas = Ruta.query.all()
        for ruta in rutas:
            G.add_edge(ruta.ciudad_origen_id, ruta.ciudad_destino_id, 
                      weight=float(ruta.peso))
        
        return G
    
    @staticmethod
    def dijkstra_ruta_optima(origen_id, destino_id):
        """Find shortest path using Dijkstra algorithm"""
        try:
            G = GrafoController.crear_grafo()
            
            # Check if nodes exist
            if origen_id not in G.nodes or destino_id not in G.nodes:
                return {'success': False, 'error': 'Ciudad no encontrada'}
            
            # Find shortest path
            try:
                camino = nx.shortest_path(G, origen_id, destino_id, weight='weight')
                distancia = nx.shortest_path_length(G, origen_id, destino_id, weight='weight')
                
                # Get city names for the path
                ciudades_camino = []
                for ciudad_id in camino:
                    ciudad = Ciudad.query.get(ciudad_id)
                    ciudades_camino.append({
                        'id': ciudad_id,
                        'nombre': ciudad.nombre,
                        'es_costera': ciudad.es_costera
                    })
                
                # Check if path passes through coastal city
                pasa_por_costera = any(ciudad['es_costera'] for ciudad in ciudades_camino)
                
                return {
                    'success': True,
                    'camino': camino,
                    'ciudades_camino': ciudades_camino,
                    'distancia_total': distancia,
                    'pasa_por_costera': pasa_por_costera
                }
            except nx.NetworkXNoPath:
                return {'success': False, 'error': 'No hay ruta disponible entre las ciudades'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def obtener_estadisticas():
        """Get basic graph statistics"""
        try:
            # Get data directly from database instead of graph
            total_ciudades = Ciudad.query.count()
            total_rutas = Ruta.query.count()
            ciudades_costeras = Ciudad.query.filter_by(es_costera=True).count()
            ciudades_interiores = total_ciudades - ciudades_costeras
            total_provincias = Provincia.query.count()
            
            return {
                'total_ciudades': total_ciudades,
                'total_rutas': total_rutas,
                'ciudades_costeras': ciudades_costeras,
                'ciudades_interiores': ciudades_interiores,
                'total_provincias': total_provincias
            }
        except Exception as e:
            return {
                'total_ciudades': 0,
                'total_rutas': 0,
                'ciudades_costeras': 0,
                'ciudades_interiores': 0,
                'total_provincias': 0,
                'error': str(e)
            }
    
    @staticmethod
    def get_graph_stats():
        """Alias for obtener_estadisticas() for English compatibility"""
        return GrafoController.obtener_estadisticas()
    
    @staticmethod
    def visualizar_grafo():
        """Generate graph visualization"""
        try:
            G = GrafoController.crear_grafo()
            
            if len(G.nodes) == 0:
                return {'success': False, 'error': 'No hay ciudades para visualizar'}
            
            # Create plot
            plt.figure(figsize=(12, 8))
            
            # Set layout
            pos = nx.spring_layout(G, k=2, iterations=50)
            
            # Separate coastal and interior cities
            coastal_nodes = [n for n in G.nodes if G.nodes[n]['es_costera']]
            interior_nodes = [n for n in G.nodes if not G.nodes[n]['es_costera']]
            
            # Draw nodes
            nx.draw_networkx_nodes(G, pos, nodelist=coastal_nodes, 
                                 node_color='lightblue', node_size=1000, 
                                 label='Ciudades Costeras')
            nx.draw_networkx_nodes(G, pos, nodelist=interior_nodes, 
                                 node_color='lightgreen', node_size=1000, 
                                 label='Ciudades Interiores')
            
            # Draw edges
            nx.draw_networkx_edges(G, pos, alpha=0.6, arrows=True, 
                                 arrowsize=20, edge_color='gray')
            
            # Draw labels
            labels = {n: G.nodes[n]['nombre'] for n in G.nodes}
            nx.draw_networkx_labels(G, pos, labels, font_size=10)
            
            # Draw edge labels (weights)
            edge_labels = {(u, v): f"{G[u][v]['weight']}" for u, v in G.edges}
            nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)
            
            plt.title('Grafo de Ciudades y Rutas')
            plt.legend()
            plt.axis('off')
            
            # Save to base64 string
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', bbox_inches='tight')
            img_buffer.seek(0)
            img_str = base64.b64encode(img_buffer.read()).decode()
            plt.close()
            
            return {'success': True, 'graph_image': img_str}
        except Exception as e:
            return {'success': False, 'error': str(e)}
