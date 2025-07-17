from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            try:
                user = User.query.filter_by(username=username).first()
                if user:
                    print(f"[DEBUG] User found: {user.username}")
                    if user.check_password(password):
                        print(f"[DEBUG] Password correct for user: {user.username}")
                        login_user(user)
                        next_page = request.args.get('next')
                        flash(f'Bienvenido {user.username}!', 'success')
                        
                        if user.is_admin():
                            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
                        else:
                            return redirect(next_page) if next_page else redirect(url_for('home.home'))
                    else:
                        print(f"[DEBUG] Password incorrect for user: {user.username}")
                        flash('Usuario o contraseña incorrectos', 'danger')
                else:
                    print(f"[DEBUG] User not found: {username}")
                    flash('Usuario o contraseña incorrectos', 'danger')
            except Exception as e:
                print(f"[ERROR] Database error during login: {str(e)}")
                flash('Error de conexión a la base de datos. Por favor, verifica que Laragon esté ejecutándose.', 'danger')
        else:
            flash('Por favor complete todos los campos', 'warning')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validaciones básicas
        if not username or not email or not password or not confirm_password:
            flash('Por favor complete todos los campos', 'warning')
        elif len(username) < 3:
            flash('El nombre de usuario debe tener al menos 3 caracteres', 'warning')
        elif len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'warning')
        elif password != confirm_password:
            flash('Las contraseñas no coinciden', 'warning')
        elif User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe', 'warning')
        elif User.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'warning')
        else:
            user = User(
                username=username,
                email=email,
                es_admin=False  # Por defecto los usuarios son regulares, no admin
            )
            user.set_password(password)
            
            try:
                db.session.add(user)
                db.session.commit()
                flash('Registro exitoso! Ahora puedes iniciar sesión.', 'success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                db.session.rollback()
                flash('Error al registrar usuario. Intenta de nuevo.', 'danger')
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('home.home'))
