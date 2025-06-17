from .home import home_bp
from .usuario import usuario_bp
def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(usuario_bp)