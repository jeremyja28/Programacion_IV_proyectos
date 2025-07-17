from extensions import db
from models.usuario import Usuario
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

class AuthController:
    """Controller for authentication (simplified - fixed credentials)"""
    
    # Credenciales fijas
    CREDENCIALES = {
        'admin': {
            'password': 'admin123',
            'nombre': 'Administrador',
            'apellido': 'Sistema',
            'email': 'admin@admin.com',
            'es_admin': True
        },
        'usuario': {
            'password': 'admin123',
            'nombre': 'Usuario',
            'apellido': 'Normal',
            'email': 'usuario@usuario.com',
            'es_admin': False
        }
    }
    
    @staticmethod
    def login(username, password):
        """Login with fixed credentials"""
        try:
            # Verificar credenciales fijas
            if username in AuthController.CREDENCIALES:
                cred = AuthController.CREDENCIALES[username]
                if password == cred['password']:
                    # Buscar usuario en BD o crearlo si no existe
                    user = Usuario.query.filter_by(username=username).first()
                    if not user:
                        # Crear usuario si no existe
                        user = Usuario(
                            username=username,
                            email=cred['email'],
                            password_hash=generate_password_hash(password),
                            nombre=cred['nombre'],
                            apellido=cred['apellido'],
                            es_admin=cred['es_admin']
                        )
                        db.session.add(user)
                        db.session.commit()
                    
                    login_user(user)
                    return True, f"Bienvenido {user.nombre}!", user
                else:
                    return False, "Contraseña incorrecta", None
            else:
                return False, "Usuario no encontrado", None
                
        except Exception as e:
            db.session.rollback()
            return False, f"Error en login: {str(e)}", None
    
    @staticmethod
    def logout():
        """Logout user"""
        try:
            logout_user()
            return True, "Sesión cerrada correctamente"
        except Exception as e:
            return False, f"Error en logout: {str(e)}"
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID for Flask-Login"""
        try:
            return Usuario.query.get(int(user_id))
        except:
            return None
    
    @staticmethod
    def inicializar_usuarios():
        """Initialize default users in database"""
        try:
            for username, cred in AuthController.CREDENCIALES.items():
                user = Usuario.query.filter_by(username=username).first()
                if not user:
                    user = Usuario(
                        username=username,
                        email=cred['email'],
                        password_hash=generate_password_hash(cred['password']),
                        nombre=cred['nombre'],
                        apellido=cred['apellido'],
                        es_admin=cred['es_admin']
                    )
                    db.session.add(user)
            
            db.session.commit()
            return True, "Usuarios inicializados correctamente"
        except Exception as e:
            db.session.rollback()
            return False, f"Error inicializando usuarios: {str(e)}"
