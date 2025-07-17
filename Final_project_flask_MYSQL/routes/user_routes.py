from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from controllers.user_controller import UserController
from controllers.auth_controller import AuthController

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/')
@login_required
def index():
    """Alias for list_users to support url_for('user.index')"""
    return list_users()

@user_bp.route('/list')
@login_required
def list_users():
    """List all users - Admin only"""
    if not current_user.is_admin():
        flash('No tienes permisos para ver usuarios', 'error')
        return redirect(url_for('home.index'))
    
    users = UserController.get_all_users(include_inactive=True)
    return render_template('users/list.html', users=users)

@user_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_user():
    """Create new user - Admin only"""
    if not current_user.is_admin():
        flash('No tienes permisos para crear usuarios', 'error')
        return redirect(url_for('home.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        es_admin = request.form.get('es_admin', False)
        
        if not all([username, email, password, nombre, apellido]):
            flash('Por favor, complete todos los campos', 'error')
            return render_template('users/create.html')
        
        success, message, user = UserController.create_user(
            username, email, password, nombre, apellido, bool(es_admin)
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('user.list_users'))
        else:
            flash(message, 'error')
    
    return render_template('users/create.html')

@user_bp.route('/<int:user_id>')
@login_required
def view_user(user_id):
    """View user details"""
    # Users can only view their own profile, admins can view all
    if not current_user.is_admin() and user_id != current_user.id:
        flash('No tienes permisos para ver este usuario', 'error')
        return redirect(url_for('home.index'))
    
    user = UserController.get_user_by_id(user_id)
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('user.list_users'))
    
    return render_template('users/view.html', user=user)

@user_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Edit user - Admin only or own profile"""
    user = UserController.get_user_by_id(user_id)
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('user.list_users'))
    
    # Check permissions
    if not current_user.is_admin() and user_id != current_user.id:
        flash('No tienes permisos para editar este usuario', 'error')
        return redirect(url_for('home.index'))
    
    if request.method == 'POST':
        data = {}
        data['username'] = request.form.get('username')
        data['email'] = request.form.get('email')
        data['nombre'] = request.form.get('nombre')
        data['apellido'] = request.form.get('apellido')
        
        # Only admins can change admin status
        if current_user.is_admin():
            data['es_admin'] = request.form.get('es_admin', False)
        
        success, message, updated_user = UserController.update_user(user_id, **data)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('user.view_user', user_id=user_id))
        else:
            flash(message, 'error')
    
    return render_template('users/edit.html', user=user)

@user_bp.route('/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete user - Admin only"""
    if not current_user.is_admin():
        flash('No tienes permisos para eliminar usuarios', 'error')
        return redirect(url_for('home.index'))
    
    if user_id == current_user.id:
        flash('No puedes eliminar tu propio usuario', 'error')
        return redirect(url_for('user.list_users'))
    
    success, message = UserController.delete_user(user_id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('user.list_users'))

@user_bp.route('/<int:user_id>/reactivate', methods=['POST'])
@login_required
def reactivate_user(user_id):
    """Reactivate user - Admin only"""
    if not current_user.is_admin():
        flash('No tienes permisos para reactivar usuarios', 'error')
        return redirect(url_for('home.index'))
    
    success, message = UserController.reactivate_user(user_id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('user.list_users'))

@user_bp.route('/search')
@login_required
def search_users():
    """Search users - Admin only"""
    if not current_user.is_admin():
        flash('No tienes permisos para buscar usuarios', 'error')
        return redirect(url_for('home.index'))
    
    search_term = request.args.get('q', '')
    
    if not search_term:
        flash('Por favor, ingrese un término de búsqueda', 'error')
        return redirect(url_for('user.list_users'))
    
    users = UserController.search_users(search_term, include_inactive=True)
    return render_template('users/search_results.html', users=users, search_term=search_term)

@user_bp.route('/api/stats')
@login_required
def api_user_stats():
    """API endpoint for user statistics"""
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    stats = UserController.get_user_stats()
    return jsonify(stats)