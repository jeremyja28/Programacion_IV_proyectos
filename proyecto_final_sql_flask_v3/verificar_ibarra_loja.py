#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar ciudades Ibarra y Loja
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.config import Config
from models.database import db
from flask import Flask
from models.entities.ciudad import Ciudad
from controllers.grafo_utils import camino_optimo_con_costera

def verificar_ciudades():
    """Verificar que las ciudades Ibarra y Loja existen"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        try:
            # Buscar ciudades
            ibarra = Ciudad.query.filter_by(nombre='Ibarra').first()
            loja = Ciudad.query.filter_by(nombre='Loja').first()
            
            print("🔍 Verificando ciudades...")
            print(f"Ibarra: {'✅ Encontrada' if ibarra else '❌ No encontrada'}")
            print(f"Loja: {'✅ Encontrada' if loja else '❌ No encontrada'}")
            
            if ibarra and loja:
                print(f"\n📍 Detalles:")
                print(f"Ibarra - ID: {ibarra.id}, Provincia: {ibarra.provincia.nombre}")
                print(f"Loja - ID: {loja.id}, Provincia: {loja.provincia.nombre}")
                
                # Probar la ruta
                print(f"\n🛣️  Probando ruta Ibarra -> Loja:")
                resultado = camino_optimo_con_costera(ibarra.id, loja.id)
                
                if resultado['valido']:
                    print(f"✅ Ruta encontrada!")
                    print(f"💰 Costo: {resultado['costo']}")
                    print(f"🏙️  Camino: {' -> '.join(resultado['camino'])}")
                    print(f"🏖️  Ciudades costeras: {resultado.get('ciudades_costeras', [])}")
                else:
                    print(f"❌ Error: {resultado.get('error', 'No se pudo encontrar ruta')}")
                    
                return True
            else:
                print("\n❌ No se pueden probar las rutas sin ambas ciudades")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

def main():
    """Función principal"""
    print("🔍 VERIFICANDO RUTA FIJA IBARRA-LOJA")
    print("=" * 50)
    
    if verificar_ciudades():
        print("\n✅ VERIFICACIÓN EXITOSA!")
    else:
        print("\n❌ VERIFICACIÓN FALLÓ!")

if __name__ == "__main__":
    main()
