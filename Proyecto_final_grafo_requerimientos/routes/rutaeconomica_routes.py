from flask import Blueprint, render_template, request
from controllers.grafo_utils import *
from flask import send_file

rutaeconomica_bp = Blueprint('ruta_economica', __name__)

@rutaeconomica_bp.route('/grafo')
def ver_grafo():
    img = grafo_a_imagen()
    return send_file(img, mimetype='image/png')

@rutaeconomica_bp.route('/ruta_economica', methods=['GET', 'POST'])
def ruta_economica():
    ciudades = obtener_ciudades()
    resultado = None

    if request.method == 'POST':
        origen_id = request.form.get('ciudad_origen')
        destino_id = request.form.get('ciudad_destino')
        if origen_id and destino_id and origen_id != destino_id:
            resultado = camino_optimo_con_costera(int(origen_id), int(destino_id))

    return render_template('formulario_simple.html', ciudades=ciudades, resultado=resultado, current_path=request.path)