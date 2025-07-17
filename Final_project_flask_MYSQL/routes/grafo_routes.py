from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from controllers.grafo_controller import GrafoController
from controllers.auth_controller import AuthController

grafo_bp = Blueprint('grafo', __name__, url_prefix='/grafo')

@grafo_bp.route('/')
@login_required
def index():
    """Graph main page"""
    return render_template('grafo/index.html')

@grafo_bp.route('/visualizar')
@login_required
def visualizar():
    """Graph visualization page"""
    image_base64 = GrafoController.grafo_a_imagen()
    stats = GrafoController.get_graph_stats()
    
    return render_template('grafo/visualizar.html', 
                         image_base64=image_base64, 
                         stats=stats)

@grafo_bp.route('/provincias')
@login_required
def list_provinces():
    """List all provinces"""
    provinces = GrafoController.get_all_provinces()
    return render_template('grafo/provincias.html', provinces=provinces)

@grafo_bp.route('/provincias/create', methods=['GET', 'POST'])
@login_required
def create_province():
    """Create new province - Admin only"""
    if not current_user.is_admin():
        flash('No tienes permisos para crear provincias', 'error')
        return redirect(url_for('grafo.list_provinces'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        codigo = request.form.get('codigo')
        
        if not nombre or not codigo:
            flash('Por favor, complete todos los campos', 'error')
            return render_template('grafo/create_province.html')
        
        success, message, province = GrafoController.create_province(nombre, codigo)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('grafo.list_provinces'))
        else:
            flash(message, 'error')
    
    return render_template('grafo/create_province.html')

@grafo_bp.route('/ciudades')
@login_required
def list_cities():
    """List all cities"""
    cities = GrafoController.get_all_cities()
    return render_template('grafo/ciudades.html', cities=cities)

@grafo_bp.route('/ciudades/create', methods=['GET', 'POST'])
@login_required
def create_city():
    """Create new city - Admin only"""
    if not current_user.is_admin():
        flash('No tienes permisos para crear ciudades', 'error')
        return redirect(url_for('grafo.list_cities'))
    
    provinces = GrafoController.get_all_provinces()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        provincia_id = request.form.get('provincia_id')
        es_costera = request.form.get('es_costera', False)
        
        if not nombre or not provincia_id:
            flash('Por favor, complete todos los campos', 'error')
            return render_template('grafo/create_city.html', provinces=provinces)
        
        success, message, city = GrafoController.create_city(
            nombre, int(provincia_id), bool(es_costera)
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('grafo.list_cities'))
        else:
            flash(message, 'error')
    
    return render_template('grafo/create_city.html', provinces=provinces)

@grafo_bp.route('/rutas')
@login_required
def list_routes():
    """List all routes"""
    routes = GrafoController.get_all_routes()
    return render_template('grafo/rutas.html', routes=routes)

@grafo_bp.route('/rutas/create', methods=['GET', 'POST'])
@login_required
def create_route():
    """Create new route - Admin only"""
    if not current_user.is_admin():
        flash('No tienes permisos para crear rutas', 'error')
        return redirect(url_for('grafo.list_routes'))
    
    cities = GrafoController.get_all_cities()
    
    if request.method == 'POST':
        ciudad_origen_id = request.form.get('ciudad_origen_id')
        ciudad_destino_id = request.form.get('ciudad_destino_id')
        distancia = request.form.get('distancia')
        tiempo_estimado = request.form.get('tiempo_estimado')
        
        if not ciudad_origen_id or not ciudad_destino_id or not distancia:
            flash('Por favor, complete todos los campos obligatorios', 'error')
            return render_template('grafo/create_route.html', cities=cities)
        
        try:
            distancia = float(distancia)
            tiempo_estimado = float(tiempo_estimado) if tiempo_estimado else None
        except ValueError:
            flash('La distancia y tiempo deben ser números válidos', 'error')
            return render_template('grafo/create_route.html', cities=cities)
        
        success, message, route = GrafoController.create_route(
            int(ciudad_origen_id), 
            int(ciudad_destino_id), 
            distancia, 
            tiempo_estimado
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('grafo.list_routes'))
        else:
            flash(message, 'error')
    
    return render_template('grafo/create_route.html', cities=cities)

@grafo_bp.route('/rutas/<int:route_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_route(route_id):
    """Edit route - Admin only"""
    if not current_user.is_admin():
        flash('No tienes permisos para editar rutas', 'error')
        return redirect(url_for('grafo.list_routes'))
    
    from models.ruta import Ruta
    route = Ruta.query.get_or_404(route_id)
    
    if request.method == 'POST':
        distancia = request.form.get('distancia')
        tiempo_estimado = request.form.get('tiempo_estimado')
        
        if not distancia:
            flash('La distancia es obligatoria', 'error')
            return render_template('grafo/edit_route.html', route=route)
        
        try:
            distancia = float(distancia)
            tiempo_estimado = float(tiempo_estimado) if tiempo_estimado else None
        except ValueError:
            flash('La distancia y tiempo deben ser números válidos', 'error')
            return render_template('grafo/edit_route.html', route=route)
        
        success, message, updated_route = GrafoController.update_route(
            route_id, distancia, tiempo_estimado
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('grafo.list_routes'))
        else:
            flash(message, 'error')
    
    return render_template('grafo/edit_route.html', route=route)

@grafo_bp.route('/rutas/<int:route_id>/delete', methods=['POST'])
@login_required
def delete_route(route_id):
    """Delete route - Admin only"""
    if not current_user.is_admin():
        flash('No tienes permisos para eliminar rutas', 'error')
        return redirect(url_for('grafo.list_routes'))
    
    success, message = GrafoController.delete_route(route_id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('grafo.list_routes'))

@grafo_bp.route('/ruta-optima', methods=['GET', 'POST'])
@login_required
def ruta_optima():
    """Find optimal route"""
    cities = GrafoController.get_all_cities()
    result = None
    
    if request.method == 'POST':
        origen = request.form.get('origen')
        destino = request.form.get('destino')
        tipo_ruta = request.form.get('tipo_ruta', 'normal')
        
        if not origen or not destino:
            flash('Por favor, seleccione ciudades de origen y destino', 'error')
            return render_template('grafo/ruta_optima.html', cities=cities)
        
        if tipo_ruta == 'costera':
            result = GrafoController.camino_optimo_con_costera(origen, destino)
        else:
            result = GrafoController.camino_optimo_dijkstra(origen, destino)
        
        if not result.get('success', False):
            flash(result.get('message', 'Error calculando ruta'), 'error')
    
    return render_template('grafo/ruta_optima.html', cities=cities, result=result)

@grafo_bp.route('/api/stats')
@login_required
def api_graph_stats():
    """API endpoint for graph statistics"""
    stats = GrafoController.get_graph_stats()
    return jsonify(stats)

@grafo_bp.route('/api/ciudades/<int:provincia_id>')
@login_required
def api_cities_by_province(provincia_id):
    """API endpoint to get cities by province"""
    from models.ciudad import Ciudad
    cities = Ciudad.query.filter_by(provincia_id=provincia_id, activa=True).all()
    return jsonify([{'id': city.id, 'nombre': city.nombre} for city in cities])
