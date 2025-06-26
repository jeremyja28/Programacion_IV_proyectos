from .home import home_bp
from .dashboards import dashboard1_bp, dashboard2_bp

def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(dashboard1_bp)
    app.register_blueprint(dashboard2_bp)