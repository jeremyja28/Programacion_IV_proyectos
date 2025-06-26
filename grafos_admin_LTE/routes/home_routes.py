from flask import blueprints, render_template, request

home_bp = blueprints.Blueprint('home', __name__)
@home_bp.route('/')
def home():
    return render_template('home.html', current_path=request.path)