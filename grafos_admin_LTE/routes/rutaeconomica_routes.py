from flask import Blueprint, render_template, request
from grafo_utils import *
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
		origen = request.form.get('origen')
		destino = request.form.get('destino')
		if origen and destino and origen != destino:
			resultado = camino_optimo_con_costera(origen, destino)

	return render_template('formulario.html', ciudades=ciudades, resultado=resultado, current_path=request.path)