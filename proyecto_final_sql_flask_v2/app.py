from flask import Flask, send_file, render_template, request
from flask_login import LoginManager
from models.config import Config
from models import db, bcrypt, User, Provincia, Ciudad
from routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensiones
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Context processor para variables globales en templates
    @app.context_processor
    def inject_globals():
        return {
            'current_path': request.path if request else None
        }
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Ruta raíz que redirija al login
    @app.route('/')
    def index():
        from flask import redirect, url_for
        from flask_login import current_user
        
        if current_user.is_authenticated:
            if current_user.is_admin():
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('home.home'))
        else:
            return redirect(url_for('auth.login'))
    
    # Crear tablas de base de datos
    with app.app_context():
        try:
            # Crear todas las tablas
            db.create_all()
            print("[OK] Tablas de base de datos verificadas/creadas")
            
            # Verificar si necesitamos inicializar datos
            try:
                # Refrescar la conexión antes de hacer consultas
                from sqlalchemy import text
                db.session.execute(text("SELECT 1"))
                
                # Intentar acceder a las tablas para verificar si existen
                provincia_count = Provincia.query.count()
                ciudad_count = Ciudad.query.count()
                admin_count = User.query.filter_by(username='admin').count()
                
                print(f"[INFO] Estado actual: {provincia_count} provincias, {ciudad_count} ciudades, {admin_count} admin")
                
                if provincia_count == 0 or ciudad_count == 0 or admin_count == 0:
                    print("[WARNING] Base de datos vacía o incompleta")
                else:
                    print("[OK] Base de datos inicializada correctamente")
                    
            except Exception as e:
                print(f"[WARNING] Error accediendo a las tablas: {str(e)}")                
        except Exception as e:
            print(f"[ERROR] Error creando tablas: {str(e)}")
    # Agregar ruta para favicon
    @app.route('/favicon.ico')
    def favicon():
        return send_file('static/img/Logo_J.png', mimetype='image/png')
    
    # Agregar manejo de errores específicos para la base de datos
    @app.errorhandler(500)
    def handle_internal_error(error):
        if "Can't connect to MySQL server" in str(error):
            return render_template('error.html', 
                                 error="Error de conexión a la base de datos",
                                 message="Por favor, asegúrate de que Laragon esté ejecutándose con MySQL en puerto 3307."), 500
        # Para otros errores 500, mostrar página de error 
        return render_template('error.html', 
                             error="Error interno del servidor",
                             message="Ha ocurrido un error interno. Por favor, intenta de nuevo más tarde."), 500
    
    # Manejo de errores 404
    @app.errorhandler(404)
    def handle_not_found(error):
        return render_template('error.html', 
                             error="Página no encontrada",
                             message="La página que buscas no existe."), 404
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=4000)