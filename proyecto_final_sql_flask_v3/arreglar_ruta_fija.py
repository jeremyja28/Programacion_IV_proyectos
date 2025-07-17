#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arreglar ruta fija Ibarra-Loja de forma definitiva
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.config import Config
from models.database import db
from flask import Flask
from models.entities.ciudad import Ciudad
from models.entities.ruta import Ruta
import networkx as nx

def verificar_y_arreglar():
    """Verificar y arreglar la ruta fija"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        try:
            print("🔍 VERIFICANDO RUTA FIJA IBARRA-LOJA")
            print("=" * 50)
            
            # 1. Verificar que las ciudades existan
            print("1. Verificando ciudades...")
            
            # Buscar con diferentes variantes
            ibarra_variants = ['Ibarra', 'IBARRA', 'ibarra']
            loja_variants = ['Loja', 'LOJA', 'loja']
            
            ibarra = None
            loja = None
            
            for variant in ibarra_variants:
                ibarra = Ciudad.query.filter_by(nombre=variant).first()
                if ibarra:
                    print(f"   ✅ Ibarra encontrada: '{ibarra.nombre}' (ID: {ibarra.id})")
                    break
            
            for variant in loja_variants:
                loja = Ciudad.query.filter_by(nombre=variant).first()
                if loja:
                    print(f"   ✅ Loja encontrada: '{loja.nombre}' (ID: {loja.id})")
                    break
            
            if not ibarra or not loja:
                print("   ❌ No se encontraron las ciudades")
                print("   🔍 Todas las ciudades disponibles:")
                ciudades = Ciudad.query.all()
                for ciudad in ciudades:
                    print(f"      - {ciudad.nombre} (ID: {ciudad.id})")
                return False
            
            # 2. Construir grafo manualmente
            print("\n2. Construyendo grafo...")
            G = nx.DiGraph()
            
            rutas = Ruta.query.all()
            print(f"   Total de rutas en BD: {len(rutas)}")
            
            for ruta in rutas:
                origen = Ciudad.query.get(ruta.ciudad_origen_id)
                destino = Ciudad.query.get(ruta.ciudad_destino_id)
                
                if origen and destino:
                    G.add_edge(origen.nombre, destino.nombre, weight=float(ruta.peso))
            
            print(f"   Nodos en grafo: {len(G.nodes())}")
            print(f"   Aristas en grafo: {len(G.edges())}")
            
            # 3. Verificar conectividad
            print("\n3. Verificando conectividad...")
            
            if ibarra.nombre in G.nodes() and loja.nombre in G.nodes():
                print(f"   ✅ Ambas ciudades están en el grafo")
                
                # Verificar si hay camino
                try:
                    camino = nx.dijkstra_path(G, ibarra.nombre, loja.nombre, weight='weight')
                    costo = nx.dijkstra_path_length(G, ibarra.nombre, loja.nombre, weight='weight')
                    
                    print(f"   ✅ Camino encontrado: {' → '.join(camino)}")
                    print(f"   💰 Costo: ${costo:.2f}")
                    
                    # Verificar ciudades costeras
                    ciudades_costeras = [c.nombre for c in Ciudad.query.filter_by(es_costera=True).all()]
                    costeras_en_camino = [c for c in camino if c in ciudades_costeras]
                    
                    if costeras_en_camino:
                        print(f"   🏖️  Ciudades costeras en el camino: {', '.join(costeras_en_camino)}")
                    else:
                        print(f"   🏔️  No pasa por ciudades costeras")
                    
                    return {
                        "camino": camino,
                        "costo": costo,
                        "valido": len(costeras_en_camino) > 0,
                        "ciudades_costeras": costeras_en_camino
                    }
                    
                except nx.NetworkXNoPath:
                    print(f"   ❌ No existe camino entre {ibarra.nombre} y {loja.nombre}")
                    
                    # Verificar rutas directas desde Ibarra
                    rutas_ibarra = Ruta.query.filter_by(ciudad_origen_id=ibarra.id).all()
                    print(f"   🛣️  Rutas desde Ibarra:")
                    for ruta in rutas_ibarra:
                        destino = Ciudad.query.get(ruta.ciudad_destino_id)
                        print(f"      Ibarra → {destino.nombre}: ${ruta.peso}")
                    
                    return {
                        "camino": [],
                        "costo": None,
                        "valido": False,
                        "error": "No existe ruta entre Ibarra y Loja"
                    }
            else:
                print(f"   ❌ Ciudades no están en el grafo")
                print(f"   Ibarra en grafo: {ibarra.nombre in G.nodes()}")
                print(f"   Loja en grafo: {loja.nombre in G.nodes()}")
                
                return {
                    "camino": [],
                    "costo": None,
                    "valido": False,
                    "error": "Ciudades no están conectadas en el grafo"
                }
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "camino": [],
                "costo": None,
                "valido": False,
                "error": f"Error del sistema: {str(e)}"
            }

def main():
    """Función principal"""
    resultado = verificar_y_arreglar()
    
    if resultado and resultado.get("camino"):
        print("\n✅ RUTA FIJA FUNCIONANDO CORRECTAMENTE")
    else:
        print("\n❌ PROBLEMA CON LA RUTA FIJA")
        print(f"Error: {resultado.get('error', 'Error desconocido')}")

if __name__ == "__main__":
    main()
