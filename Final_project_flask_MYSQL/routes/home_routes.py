from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from controllers.user_controller import UserController
from controllers.grafo_controller import GrafoController

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@login_required
def index():
    """Home page - Dashboard"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    # Get dashboard statistics
    user_stats = UserController.get_user_stats()
    graph_stats = GrafoController.get_graph_stats()
    
    return render_template('home.html', 
                         user_stats=user_stats,
                         graph_stats=graph_stats)

@home_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page - same as home"""
    return redirect(url_for('home.index'))
