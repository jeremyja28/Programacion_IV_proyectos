#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Depurar problema con ruta fija Ibarra-Loja
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.config import Config
from models.database import db
from flask import Flask
from models.entities.ciudad import Ciudad
from models.entities.ruta import Ruta
from controllers.grafo_utils import camino_optimo_con_costera, construir_grafo

def debug_ciudades():
    """Depurar las ciudades Ibarra y Loja"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        try:
            print("🔍 DEPURANDO CIUDADES...")
            
            # Buscar todas las ciudades que contengan "Ibarra"
            print("\n📍 Buscando ciudades con 'Ibarra':")
            ciudades_ibarra = Ciudad.query.filter(Ciudad.nombre.like('%Ibarra%')).all()
            for ciudad in ciudades_ibarra:
                print(f"   ID: {ciudad.id}, Nombre: '{ciudad.nombre}', Provincia: {ciudad.provincia.nombre}")
            
            # Buscar todas las ciudades que contengan "Loja"
            print("\n📍 Buscando ciudades con 'Loja':")
            ciudades_loja = Ciudad.query.filter(Ciudad.nombre.like('%Loja%')).all()
            for ciudad in ciudades_loja:
                print(f"   ID: {ciudad.id}, Nombre: '{ciudad.nombre}', Provincia: {ciudad.provincia.nombre}")
            
            # Buscar exactamente por nombre
            print("\n🎯 Búsqueda exacta:")
            ibarra = Ciudad.query.filter_by(nombre='Ibarra').first()
            loja = Ciudad.query.filter_by(nombre='Loja').first()
            
            print(f"Ibarra exacta: {ibarra.nombre if ibarra else 'No encontrada'}")
            print(f"Loja exacta: {loja.nombre if loja else 'No encontrada'}")
            
            if ibarra and loja:
                print(f"\n✅ Ambas ciudades encontradas:")
                print(f"   Ibarra - ID: {ibarra.id}")
                print(f"   Loja - ID: {loja.id}")
                
                # Verificar rutas desde Ibarra
                print(f"\n🛣️  Rutas desde Ibarra:")
                rutas_ibarra = Ruta.query.filter_by(ciudad_origen_id=ibarra.id).all()
                for ruta in rutas_ibarra:
                    destino = Ciudad.query.get(ruta.ciudad_destino_id)
                    print(f"   Ibarra → {destino.nombre}: ${ruta.peso}")
                
                # Verificar rutas hacia Loja
                print(f"\n🛣️  Rutas hacia Loja:")
                rutas_loja = Ruta.query.filter_by(ciudad_destino_id=loja.id).all()
                for ruta in rutas_loja:
                    origen = Ciudad.query.get(ruta.ciudad_origen_id)
                    print(f"   {origen.nombre} → Loja: ${ruta.peso}")
                
                # Probar el algoritmo
                print(f"\n🔄 Probando algoritmo de ruta...")
                resultado = camino_optimo_con_costera(ibarra.id, loja.id)
                print(f"Resultado: {resultado}")
                
                return True
            else:
                print("\n❌ No se encontraron ambas ciudades")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False

def debug_grafo():
    """Depurar el grafo"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        try:
            print("\n🕸️  DEPURANDO GRAFO...")
            
            G = construir_grafo()
            print(f"Nodos en el grafo: {len(G.nodes())}")
            print(f"Aristas en el grafo: {len(G.edges())}")
            
            # Verificar si Ibarra y Loja están en el grafo
            if 'Ibarra' in G.nodes():
                print("✅ Ibarra está en el grafo")
            else:
                print("❌ Ibarra NO está en el grafo")
            
            if 'Loja' in G.nodes():
                print("✅ Loja está en el grafo")
            else:
                print("❌ Loja NO está en el grafo")
            
            # Mostrar todos los nodos para verificar
            print(f"\n📋 Todos los nodos del grafo:")
            for i, nodo in enumerate(sorted(G.nodes())):
                print(f"   {i+1:2d}. {nodo}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Función principal"""
    print("🐛 DEPURACIÓN RUTA FIJA IBARRA-LOJA")
    print("=" * 50)
    
    ciudades_ok = debug_ciudades()
    grafo_ok = debug_grafo()
    
    if ciudades_ok and grafo_ok:
        print("\n✅ DEPURACIÓN COMPLETADA")
    else:
        print("\n❌ ERRORES ENCONTRADOS")

if __name__ == "__main__":
    main()
