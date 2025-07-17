import os
from flask import Flask, redirect, url_for
from config import config
from extensions import init_extensions, db
from routes import register_blueprints

def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Initialize default users with fixed credentials
        from controllers.auth_controller import AuthController
        success, message = AuthController.inicializar_usuarios()
        if success:
            print("✅ Usuarios inicializados correctamente:")
            print("   ADMIN - Usuario: admin / Contraseña: admin123")
            print("   USUARIO - Usuario: usuario / Contraseña: admin123")
        else:
            print(f"❌ Error inicializando usuarios: {message}")
    
    # Root route redirect
    @app.route('/')
    def index():
        return redirect(url_for('home.index'))
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return redirect(url_for('home.index'))
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return redirect(url_for('home.index'))
    
    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
