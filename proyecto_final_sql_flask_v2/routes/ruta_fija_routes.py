from flask import Blueprint, render_template, request, send_file
from controllers.grafo_utils import grafo_a_imagen, camino_optimo_con_costera
from models.entities.ciudad import Ciudad

ruta_fija_bp = Blueprint('ruta_fija', __name__)

@ruta_fija_bp.route('/ruta_fija')
def ruta_fija():
    """Ruta fija Ibarra → Loja usando la función existente que ya funciona"""
    try:
        # Buscar las ciudades por nombre
        ibarra = Ciudad.query.filter_by(nombre='Ibarra').first()
        loja = Ciudad.query.filter_by(nombre='Loja').first()
        
        if not ibarra or not loja:
            resultado = {
                "camino": [],
                "costo": None,
                "valido": False,
                "error": "No se encontraron las ciudades Ibarra o Loja en la base de datos"
            }
        else:
            # Usar la función existente que ya funciona en la búsqueda de ruta óptima
            resultado = camino_optimo_con_costera(ibarra.id, loja.id)
            
            # Asegurar que el resultado tenga el formato correcto
            if not resultado or not resultado.get('camino'):
                resultado = {
                    "camino": [],
                    "costo": None,
                    "valido": False,
                    "error": "No se encontró una ruta válida entre Ibarra y Loja"
                }
    
    except Exception as e:
        resultado = {
            "camino": [],
            "costo": None,
            "valido": False,
            "error": f"Error del sistema: {str(e)}"
        }
    
    return render_template("ruta_fija.html", resultado=resultado, current_path=request.path)

@ruta_fija_bp.route('/ruta_fija/grafo')
def grafo_fijo():
    img = grafo_a_imagen()
    return send_file(img, mimetype='image/png')
