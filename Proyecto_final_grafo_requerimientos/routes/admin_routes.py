from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from models import User, Ciudad, Ruta, Provincia, db
from controllers.grafo_utils import estadisticas_grafo

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Acceso denegado. Se requieren permisos de administrador.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Estadísticas generales con manejo de errores
    try:
        stats = {
            'total_usuarios': User.query.count(),
            'total_provincias': Provincia.query.count(),
            'total_ciudades': Ciudad.query.count(),
            'total_rutas': Ruta.query.count(),
            'ciudades_costeras': Ciudad.query.filter_by(es_costera=True).count()
        }
        
        grafo_stats = estadisticas_grafo()
        
    except Exception as e:
        # Si hay error en la base de datos, mostrar valores por defecto
        print(f"Error en dashboard: {e}")
        stats = {
            'total_usuarios': 0,
            'total_provincias': 0,
            'total_ciudades': 0,
            'total_rutas': 0,
            'ciudades_costeras': 0
        }
        grafo_stats = {
            'total_nodos': 0,
            'total_conexiones': 0,
            'densidad': 0.0
        }
        flash('Error al cargar estadísticas. Verifica la conexión a la base de datos.', 'warning')
    
    return render_template('admin/dashboard.html', stats=stats, grafo_stats=grafo_stats)

# ========== API ENDPOINTS PARA AJAX ==========
@admin_bp.route('/api/ciudades/<int:provincia_id>')
@login_required
@admin_required
def get_ciudades_by_provincia(provincia_id):
    """Obtener ciudades de una provincia específica"""
    ciudades = Ciudad.query.filter_by(provincia_id=provincia_id).all()
    return jsonify([{
        'id': ciudad.id,
        'nombre': ciudad.nombre
    } for ciudad in ciudades])

@admin_bp.route('/api/provincias')
@login_required
@admin_required
def get_provincias():
    """Obtener todas las provincias"""
    provincias = Provincia.query.order_by(Provincia.nombre).all()
    return jsonify([{
        'id': provincia.id,
        'nombre': provincia.nombre
    } for provincia in provincias])

@admin_bp.route('/api/ciudades')
@login_required
@admin_required
def get_all_ciudades():
    """Obtener todas las ciudades con su provincia"""
    ciudades = Ciudad.query.join(Provincia).order_by(Provincia.nombre, Ciudad.nombre).all()
    return jsonify([{
        'id': ciudad.id,
        'nombre': ciudad.nombre,
        'provincia': ciudad.provincia.nombre
    } for ciudad in ciudades])

# ========== GESTIÓN DE PROVINCIAS ==========
@admin_bp.route('/provincias')
@login_required
@admin_required
def provincias():
    provincias = Provincia.query.order_by(Provincia.nombre).all()
    return render_template('admin/provincias.html', provincias=provincias)

@admin_bp.route('/provincias/nueva', methods=['GET', 'POST'])
@login_required
@admin_required
def nueva_provincia():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        codigo = request.form.get('codigo')
        
        if not nombre:
            flash('El nombre de la provincia es obligatorio.', 'warning')
        elif Provincia.query.filter_by(nombre=nombre).first():
            flash('Ya existe una provincia con ese nombre.', 'warning')
        else:
            try:
                provincia = Provincia(nombre=nombre, codigo=codigo)
                db.session.add(provincia)
                db.session.commit()
                flash(f'Provincia "{provincia.nombre}" creada exitosamente.', 'success')
                return redirect(url_for('admin.provincias'))
            except Exception as e:
                db.session.rollback()
                flash('Error al crear la provincia.', 'danger')
    
    return render_template('admin/provincia_form.html', title='Nueva Provincia')

@admin_bp.route('/provincias/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_provincia(id):
    provincia = Provincia.query.get_or_404(id)
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        codigo = request.form.get('codigo')
        
        if not nombre:
            flash('El nombre de la provincia es obligatorio.', 'warning')
        elif nombre != provincia.nombre and Provincia.query.filter_by(nombre=nombre).first():
            flash('Ya existe una provincia con ese nombre.', 'warning')
        else:
            try:
                provincia.nombre = nombre
                provincia.codigo = codigo
                db.session.commit()
                flash(f'Provincia "{provincia.nombre}" actualizada exitosamente.', 'success')
                return redirect(url_for('admin.provincias'))
            except Exception as e:
                db.session.rollback()
                flash('Error al actualizar la provincia.', 'danger')
    
    return render_template('admin/provincia_form.html', title='Editar Provincia', provincia=provincia)

@admin_bp.route('/provincias/<int:id>/eliminar', methods=['POST'])
@login_required
@admin_required
def eliminar_provincia(id):
    provincia = Provincia.query.get_or_404(id)
    
    # Verificar si la provincia tiene ciudades asociadas
    if provincia.ciudades.count() > 0:
        flash(f'No se puede eliminar "{provincia.nombre}" porque tiene ciudades asociadas.', 'warning')
        return redirect(url_for('admin.provincias'))
    
    try:
        db.session.delete(provincia)
        db.session.commit()
        flash(f'Provincia "{provincia.nombre}" eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar la provincia.', 'danger')
    
    return redirect(url_for('admin.provincias'))

# ========== GESTIÓN DE CIUDADES ==========
@admin_bp.route('/ciudades')
@login_required
@admin_required
def ciudades():
    ciudades = Ciudad.query.all()
    return render_template('admin/ciudades.html', ciudades=ciudades)

@admin_bp.route('/ciudades/nueva', methods=['GET', 'POST'])
@login_required
@admin_required
def nueva_ciudad():
    provincias = Provincia.query.order_by(Provincia.nombre).all()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        provincia_id = request.form.get('provincia_id')
        es_costera = request.form.get('es_costera') == 'on'
        
        if not nombre or not provincia_id:
            flash('El nombre de la ciudad y la provincia son obligatorios.', 'warning')
        elif Ciudad.query.filter_by(nombre=nombre, provincia_id=provincia_id).first():
            flash('Ya existe una ciudad con ese nombre en la provincia seleccionada.', 'warning')
        else:
            try:
                ciudad = Ciudad(
                    nombre=nombre,
                    provincia_id=int(provincia_id),
                    es_costera=es_costera
                )
                
                db.session.add(ciudad)
                db.session.commit()
                flash(f'Ciudad "{ciudad.nombre}" creada exitosamente.', 'success')
                return redirect(url_for('admin.ciudades'))
            except Exception as e:
                db.session.rollback()
                flash('Error al crear la ciudad. Verifica los datos ingresados.', 'danger')
    
    return render_template('admin/ciudad_form.html', title='Nueva Ciudad', provincias=provincias)

@admin_bp.route('/ciudades/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_ciudad(id):
    ciudad = Ciudad.query.get_or_404(id)
    provincias = Provincia.query.order_by(Provincia.nombre).all()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        provincia_id = request.form.get('provincia_id')
        es_costera = request.form.get('es_costera') == 'on'
        
        if not nombre or not provincia_id:
            flash('El nombre de la ciudad y la provincia son obligatorios.', 'warning')
        elif (nombre != ciudad.nombre or int(provincia_id) != ciudad.provincia_id) and \
             Ciudad.query.filter_by(nombre=nombre, provincia_id=provincia_id).first():
            flash('Ya existe una ciudad con ese nombre en la provincia seleccionada.', 'warning')
        else:
            try:
                ciudad.nombre = nombre
                ciudad.provincia_id = int(provincia_id)
                ciudad.es_costera = es_costera
                
                db.session.commit()
                flash(f'Ciudad "{ciudad.nombre}" actualizada exitosamente.', 'success')
                return redirect(url_for('admin.ciudades'))
            except Exception as e:
                db.session.rollback()
                flash('Error al actualizar la ciudad. Verifica los datos ingresados.', 'danger')
    
    return render_template('admin/ciudad_form.html', title='Editar Ciudad', ciudad=ciudad, provincias=provincias)

@admin_bp.route('/ciudades/<int:id>/eliminar', methods=['POST'])
@login_required
@admin_required
def eliminar_ciudad(id):
    ciudad = Ciudad.query.get_or_404(id)
    
    # Verificar si la ciudad tiene rutas asociadas
    if ciudad.rutas_origen.count() > 0 or ciudad.rutas_destino.count() > 0:
        flash(f'No se puede eliminar "{ciudad.nombre}" porque tiene rutas asociadas.', 'warning')
        return redirect(url_for('admin.ciudades'))
    
    try:
        db.session.delete(ciudad)
        db.session.commit()
        flash(f'Ciudad "{ciudad.nombre}" eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar la ciudad.', 'danger')
    
    return redirect(url_for('admin.ciudades'))

# ========== GESTIÓN DE RUTAS ==========
@admin_bp.route('/rutas')
@login_required
@admin_required
def rutas():
    rutas = Ruta.query.all()
    return render_template('admin/rutas.html', rutas=rutas)

@admin_bp.route('/rutas/nueva', methods=['GET', 'POST'])
@login_required
@admin_required
def nueva_ruta():
    ciudades = Ciudad.query.order_by(Ciudad.nombre).all()
    
    if request.method == 'POST':
        ciudad_origen_id = request.form.get('ciudad_origen')
        ciudad_destino_id = request.form.get('ciudad_destino')
        peso = request.form.get('peso')
        
        # Validaciones
        if not ciudad_origen_id or not ciudad_destino_id:
            flash('Debe seleccionar ciudad de origen y destino.', 'warning')
        elif ciudad_origen_id == ciudad_destino_id:
            flash('La ciudad de origen y destino no pueden ser la misma.', 'warning')
        elif not peso:
            flash('El peso/distancia es obligatorio.', 'warning')
        else:
            try:
                ruta = Ruta(
                    ciudad_origen_id=int(ciudad_origen_id),
                    ciudad_destino_id=int(ciudad_destino_id),
                    peso=float(peso)
                )
                
                db.session.add(ruta)
                db.session.commit()
                flash('Ruta creada exitosamente.', 'success')
                return redirect(url_for('admin.rutas'))
            except Exception as e:
                db.session.rollback()
                flash('Error al crear la ruta. Puede que ya exista una ruta entre estas ciudades.', 'danger')
    
    return render_template('admin/ruta_form.html', title='Nueva Ruta', ciudades=ciudades)

@admin_bp.route('/rutas/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_ruta(id):
    ruta = Ruta.query.get_or_404(id)
    ciudades = Ciudad.query.order_by(Ciudad.nombre).all()
    
    if request.method == 'POST':
        ciudad_origen_id = request.form.get('ciudad_origen')
        ciudad_destino_id = request.form.get('ciudad_destino')
        peso = request.form.get('peso')
        
        # Validaciones
        if not ciudad_origen_id or not ciudad_destino_id:
            flash('Debe seleccionar ciudad de origen y destino.', 'warning')
        elif ciudad_origen_id == ciudad_destino_id:
            flash('La ciudad de origen y destino no pueden ser la misma.', 'warning')
        elif not peso:
            flash('El peso/distancia es obligatorio.', 'warning')
        else:
            try:
                ruta.ciudad_origen_id = int(ciudad_origen_id)
                ruta.ciudad_destino_id = int(ciudad_destino_id)
                ruta.peso = float(peso)
                
                db.session.commit()
                flash('Ruta actualizada exitosamente.', 'success')
                return redirect(url_for('admin.rutas'))
            except Exception as e:
                db.session.rollback()
                flash('Error al actualizar la ruta.', 'danger')
    
    return render_template('admin/ruta_form.html', title='Editar Ruta', ruta=ruta, ciudades=ciudades)

@admin_bp.route('/rutas/<int:id>/eliminar', methods=['POST'])
@login_required
@admin_required
def eliminar_ruta(id):
    ruta = Ruta.query.get_or_404(id)
    
    try:
        db.session.delete(ruta)
        db.session.commit()
        flash('Ruta eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar la ruta.', 'danger')
    
    return redirect(url_for('admin.rutas'))

# ========== GESTIÓN DE USUARIOS ==========
@admin_bp.route('/usuarios')
@login_required
@admin_required
def usuarios():
    usuarios = User.query.all()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@admin_bp.route('/usuarios/<int:id>/toggle-role', methods=['POST'])
@login_required
@admin_required
def toggle_user_role(id):
    if id == current_user.id:
        flash('No puedes cambiar tu propio rol.', 'warning')
        return redirect(url_for('admin.usuarios'))
    
    user = User.query.get_or_404(id)
    user.role = 'admin' if user.role == 'user' else 'user'
    
    try:
        db.session.commit()
        flash(f'Rol de {user.username} cambiado a {user.role}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al cambiar el rol del usuario.', 'danger')
    
    return redirect(url_for('admin.usuarios'))
