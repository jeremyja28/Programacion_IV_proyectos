from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, logout_user, current_user
from controllers.auth_controller import AuthController
from controllers.user_controller import UserController

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        if not username or not password:
            flash('Por favor, complete todos los campos', 'error')
            return render_template('auth/login.html')
        
        success, message, user = AuthController.login(username, password)
        
        if success:
            flash(f'Bienvenido {user.get_full_name()}', 'success')
            # Redirect to next page or home
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('home.index'))
        else:
            flash(message, 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout user"""
    success, message = AuthController.logout()
    if success:
        flash('Has cerrado sesión exitosamente', 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register page (only for admins or if no users exist)"""
    # Check if this is the first user (admin setup)
    user_count = UserController.get_user_stats()['total_users']
    is_first_user = user_count == 0
    
    # If not first user, check if current user is admin
    if not is_first_user:
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('No tienes permisos para registrar usuarios', 'error')
            return redirect(url_for('home.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        es_admin = request.form.get('es_admin', False)
        
        # Validate form
        if not all([username, email, password, confirm_password, nombre, apellido]):
            flash('Por favor, complete todos los campos', 'error')
            return render_template('auth/register.html', is_first_user=is_first_user)
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('auth/register.html', is_first_user=is_first_user)
        
        # First user is automatically admin
        if is_first_user:
            es_admin = True
        
        success, message, user = AuthController.register(
            username, email, password, nombre, apellido, es_admin
        )
        
        if success:
            flash(f'Usuario {username} registrado exitosamente', 'success')
            # If first user, log them in automatically
            if is_first_user:
                AuthController.login(username, password)
                return redirect(url_for('home.index'))
            else:
                return redirect(url_for('user.list_users'))
        else:
            flash(message, 'error')
    
    return render_template('auth/register.html', is_first_user=is_first_user)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password page"""
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([old_password, new_password, confirm_password]):
            flash('Por favor, complete todos los campos', 'error')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('Las contraseñas nuevas no coinciden', 'error')
            return render_template('auth/change_password.html')
        
        success, message = AuthController.change_password(
            current_user.id, old_password, new_password
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('home.index'))
        else:
            flash(message, 'error')
    
    return render_template('auth/change_password.html')

@auth_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('auth/profile.html', user=current_user)
