from .home_routes import home_bp
from .user_routes import user_bp
from .auth_routes import auth_bp
from .grafo_routes import grafo_bp

def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(grafo_bp)
