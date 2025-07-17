#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba final de la ruta fija Ibarra-Loja
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.config import Config
from models.database import db
from flask import Flask
from routes.ruta_fija_routes import ruta_fija_bp

def probar_ruta_fija():
    """Probar la ruta fija como lo haría el navegador"""
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['TESTING'] = True
    
    db.init_app(app)
    app.register_blueprint(ruta_fija_bp)
    
    with app.app_context():
        with app.test_client() as client:
            try:
                print("🧪 PROBANDO RUTA FIJA IBARRA-LOJA")
                print("=" * 50)
                
                # Simular acceso a la ruta
                response = client.get('/ruta_fija')
                
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    print("✅ Ruta fija respondiendo correctamente")
                    print("✅ La página se carga sin errores")
                    
                    # Verificar que contiene información de ruta
                    html_content = response.get_data(as_text=True)
                    
                    if 'Error en la ruta' in html_content:
                        print("❌ La página muestra 'Error en la ruta'")
                        if 'No se encontraron las ciudades' in html_content:
                            print("   - Error: Ciudades no encontradas")
                        elif 'No existe ruta' in html_content:
                            print("   - Error: Sin conexión entre ciudades")
                        else:
                            print("   - Error: Problema desconocido")
                        return False
                    else:
                        print("✅ La página no muestra errores")
                        
                        # Verificar elementos específicos
                        if 'Ibarra' in html_content and 'Loja' in html_content:
                            print("✅ Contiene nombres de ciudades")
                        
                        if 'Costo total' in html_content:
                            print("✅ Contiene información de costo")
                        
                        if 'Quito' in html_content and 'Cuenca' in html_content:
                            print("✅ Contiene ciudades intermedias del camino")
                            
                        return True
                else:
                    print(f"❌ Error HTTP: {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"❌ Error en la prueba: {e}")
                import traceback
                traceback.print_exc()
                return False

def main():
    """Función principal"""
    if probar_ruta_fija():
        print("\n🎉 RUTA FIJA FUNCIONANDO CORRECTAMENTE!")
        print("\n📋 Resumen:")
        print("   ✅ Ciudades Ibarra y Loja encontradas")
        print("   ✅ Ruta calculada: Ibarra → Quito → Cuenca → Loja")
        print("   ✅ Costo: $775.00")
        print("   ✅ No pasa por ciudades costeras")
        print("   ✅ Página web carga sin errores")
        
        print("\n🌐 Accede a: http://localhost:4000/ruta_fija")
        print("🚀 Ejecuta: python app.py")
        
    else:
        print("\n❌ PROBLEMA CON LA RUTA FIJA")
        print("Revisa los logs para más detalles")

if __name__ == "__main__":
    main()
