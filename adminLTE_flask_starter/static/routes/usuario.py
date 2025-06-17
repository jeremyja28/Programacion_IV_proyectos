from flask import Blueprint, render_template

usuario_bp = Blueprint('usuario', __name__)
@usuario_bp.route('/usuario')
def usuario():
    return render_template("usuario.html")