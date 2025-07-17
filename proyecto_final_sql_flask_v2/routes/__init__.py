from .home_routes import home_bp
from .ruta_fija_routes import ruta_fija_bp
from .rutaeconomica_routes import rutaeconomica_bp
from .auth_routes import auth_bp
from .admin_routes import admin_bp
from flask import Blueprint

def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(ruta_fija_bp)
    app.register_blueprint(rutaeconomica_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    