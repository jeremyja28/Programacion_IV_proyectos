import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import io
from models.models import Ciudad, Ruta

# Construir el grafo dirigido y ponderado desde la base de datos
def construir_grafo():
    G = nx.DiGraph()
    
    # Obtener todas las rutas activas de la base de datos
    rutas = Ruta.query.filter_by(estado='activa').all()
    
    for ruta in rutas:
        G.add_edge(
            ruta.ciudad_origen.nombre, 
            ruta.ciudad_destino.nombre, 
            weight=ruta.costo,
            distancia=ruta.distancia,
            tiempo=ruta.tiempo_estimado or 0
        )
    
    return G

# Función para renderizar el grafo como imagen
def grafo_a_imagen():
    G = construir_grafo()
    
    if len(G.nodes()) == 0:
        # Si no hay nodos, crear un gráfico vacío
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.text(0.5, 0.5, 'No hay rutas disponibles', ha='center', va='center', fontsize=16)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    else:
        pos = nx.spring_layout(G, seed=85)
        pesos = nx.get_edge_attributes(G, 'weight')

        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Dibujar ciudades costeras en color diferente
        ciudades_costeras = [c.nombre for c in Ciudad.query.filter_by(es_costera=True).all()]
        node_colors = ['lightcoral' if node in ciudades_costeras else 'lightblue' for node in G.nodes()]
        
        nx.draw(G, pos, with_labels=True, node_color=node_colors, 
                node_size=2000, font_weight='bold', arrows=True, 
                edge_color='gray', font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos, font_size=8)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf

def camino_optimo_con_costera(ciudad_origen_id, ciudad_destino_id):
    """
    Encuentra el camino óptimo entre dos ciudades, considerando si pasa por ciudades costeras
    """
    G = construir_grafo()
    
    # Obtener nombres de las ciudades
    ciudad_origen = Ciudad.query.get(ciudad_origen_id)
    ciudad_destino = Ciudad.query.get(ciudad_destino_id)
    
    if not ciudad_origen or not ciudad_destino:
        return {
            "camino": [],
            "costo": None,
            "valido": False,
            "error": "Ciudad no encontrada"
        }
    
    origen_nombre = ciudad_origen.nombre
    destino_nombre = ciudad_destino.nombre
    
    try:
        camino = nx.dijkstra_path(G, origen_nombre, destino_nombre, weight='weight')
        costo = nx.dijkstra_path_length(G, origen_nombre, destino_nombre, weight='weight')
        
        # Verificar si el camino pasa por alguna ciudad costera
        ciudades_costeras = {c.nombre for c in Ciudad.query.filter_by(es_costera=True).all()}
        contiene_costera = any(ciudad in ciudades_costeras for ciudad in camino)
        
        return {
            "camino": camino,
            "costo": costo,
            "valido": contiene_costera,
            "ciudades_costeras": list(ciudades_costeras.intersection(set(camino)))
        }
    except nx.NetworkXNoPath:
        return {
            "camino": [],
            "costo": None,
            "valido": False,
            "error": "No existe ruta entre las ciudades seleccionadas"
        }

def obtener_ciudades():
    """Obtiene todas las ciudades de la base de datos"""
    return Ciudad.query.all()

def obtener_rutas_activas():
    """Obtiene todas las rutas activas"""
    return Ruta.query.filter_by(estado='activa').all()

def estadisticas_grafo():
    """Obtiene estadísticas del grafo"""
    G = construir_grafo()
    
    return {
        'total_ciudades': len(G.nodes()),
        'total_rutas': len(G.edges()),
        'ciudades_conectadas': len([n for n in G.nodes() if G.degree(n) > 0]),
        'densidad': nx.density(G) if len(G.nodes()) > 1 else 0,
        'es_conectado': nx.is_weakly_connected(G) if len(G.nodes()) > 0 else False
    }
