from models.usuario import Usuario
from extensions import db
from datetime import datetime

class UserController:
    """User management controller following SRP (Single Responsibility Principle)"""
    
    @staticmethod
    def get_all_users(include_inactive=False):
        """
        Get all users
        Returns: list of Usuario objects
        """
        try:
            if include_inactive:
                return Usuario.query.all()
            else:
                return Usuario.query.filter_by(activo=True).all()
        except Exception as e:
            print(f"Error getting users: {str(e)}")
            return []
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID
        Returns: Usuario object or None
        """
        try:
            return Usuario.query.get(user_id)
        except Exception as e:
            print(f"Error getting user by ID: {str(e)}")
            return None
    
    @staticmethod
    def get_user_by_username(username):
        """
        Get user by username
        Returns: Usuario object or None
        """
        try:
            return Usuario.query.filter_by(username=username).first()
        except Exception as e:
            print(f"Error getting user by username: {str(e)}")
            return None
    
    @staticmethod
    def get_user_by_email(email):
        """
        Get user by email
        Returns: Usuario object or None
        """
        try:
            return Usuario.query.filter_by(email=email).first()
        except Exception as e:
            print(f"Error getting user by email: {str(e)}")
            return None
    
    @staticmethod
    def create_user(username, email, password, nombre, apellido, es_admin=False):
        """
        Create new user
        Returns: tuple (success: bool, message: str, user: Usuario|None)
        """
        try:
            # Validate unique constraints
            if Usuario.query.filter_by(username=username).first():
                return False, "El nombre de usuario ya existe", None
            
            if Usuario.query.filter_by(email=email).first():
                return False, "El email ya está registrado", None
            
            # Create user
            user = Usuario(
                username=username,
                email=email,
                password=password,
                nombre=nombre,
                apellido=apellido,
                es_admin=es_admin
            )
            
            db.session.add(user)
            db.session.commit()
            
            return True, "Usuario creado exitosamente", user
            
        except Exception as e:
            db.session.rollback()
            return False, f"Error creando usuario: {str(e)}", None
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """
        Update user information
        Returns: tuple (success: bool, message: str, user: Usuario|None)
        """
        try:
            user = Usuario.query.get(user_id)
            if not user:
                return False, "Usuario no encontrado", None
            
            # Update allowed fields
            allowed_fields = ['username', 'email', 'nombre', 'apellido', 'es_admin']
            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    # Check uniqueness for username and email
                    if field == 'username' and value != user.username:
                        if Usuario.query.filter_by(username=value).first():
                            return False, "El nombre de usuario ya existe", None
                    
                    if field == 'email' and value != user.email:
                        if Usuario.query.filter_by(email=value).first():
                            return False, "El email ya está registrado", None
                    
                    setattr(user, field, value)
            
            db.session.commit()
            return True, "Usuario actualizado exitosamente", user
            
        except Exception as e:
            db.session.rollback()
            return False, f"Error actualizando usuario: {str(e)}", None
    
    @staticmethod
    def delete_user(user_id, soft_delete=True):
        """
        Delete user (soft or hard delete)
        Returns: tuple (success: bool, message: str)
        """
        try:
            user = Usuario.query.get(user_id)
            if not user:
                return False, "Usuario no encontrado"
            
            if soft_delete:
                user.activo = False
                db.session.commit()
                return True, "Usuario desactivado exitosamente"
            else:
                db.session.delete(user)
                db.session.commit()
                return True, "Usuario eliminado exitosamente"
                
        except Exception as e:
            db.session.rollback()
            return False, f"Error eliminando usuario: {str(e)}"
    
    @staticmethod
    def reactivate_user(user_id):
        """
        Reactivate user
        Returns: tuple (success: bool, message: str)
        """
        try:
            user = Usuario.query.get(user_id)
            if not user:
                return False, "Usuario no encontrado"
            
            user.activo = True
            db.session.commit()
            return True, "Usuario reactivado exitosamente"
            
        except Exception as e:
            db.session.rollback()
            return False, f"Error reactivando usuario: {str(e)}"
    
    @staticmethod
    def get_user_stats():
        """
        Get user statistics
        Returns: dict with user statistics
        """
        try:
            total_users = Usuario.query.count()
            active_users = Usuario.query.filter_by(activo=True).count()
            admin_users = Usuario.query.filter_by(es_admin=True, activo=True).count()
            
            return {
                'total_users': total_users,
                'active_users': active_users,
                'inactive_users': total_users - active_users,
                'admin_users': admin_users,
                'regular_users': active_users - admin_users
            }
        except Exception as e:
            print(f"Error getting user stats: {str(e)}")
            return {
                'total_users': 0,
                'active_users': 0,
                'inactive_users': 0,
                'admin_users': 0,
                'regular_users': 0
            }
    
    @staticmethod
    def search_users(search_term, include_inactive=False):
        """
        Search users by username, email, or name
        Returns: list of Usuario objects
        """
        try:
            query = Usuario.query.filter(
                (Usuario.username.contains(search_term)) |
                (Usuario.email.contains(search_term)) |
                (Usuario.nombre.contains(search_term)) |
                (Usuario.apellido.contains(search_term))
            )
            
            if not include_inactive:
                query = query.filter_by(activo=True)
            
            return query.all()
            
        except Exception as e:
            print(f"Error searching users: {str(e)}")
            return []
