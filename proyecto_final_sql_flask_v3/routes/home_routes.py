from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    """Ruta raíz que redirije al login si no está autenticado"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return redirect(url_for('home.home'))

@home_bp.route('/home')
def home():
    return render_template('home.html', current_path=request.path)