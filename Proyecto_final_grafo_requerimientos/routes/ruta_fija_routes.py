from flask import Blueprint, render_template, request, send_file
from controllers.grafo_utils import grafo_a_imagen, camino_optimo_con_costera

ruta_fija_bp = Blueprint('ruta_fija', __name__)

@ruta_fija_bp.route('/ruta_fija')
def ruta_fija():
    resultado = camino_optimo_con_costera('Ibarra', 'Loja')
    return render_template("ruta_fija.html", resultado=resultado, current_path=request.path)

@ruta_fija_bp.route('/ruta_fija/grafo')
def grafo_fijo():
    img = grafo_a_imagen()
    return send_file(img, mimetype='image/png')
