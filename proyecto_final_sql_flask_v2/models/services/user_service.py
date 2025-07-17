# swervicio usuario
from typing import Optional, List, Dict, Any
from models.entities.user import User
from models.repositories.user_repository import UserRepository


class UserService:
    
    def __init__(self):
        self.user_repository = UserRepository()
    
    def create_user(self, username: str, email: str, password: str, role: str = 'user') -> Dict[str, Any]:
        # Validaciones
        errors = self._validate_user_data(username, email, password)
        if errors:
            return {'success': False, 'errors': errors}
        
        # Verificar si el usuario ya existe
        if self.user_repository.username_exists(username):
            return {'success': False, 'errors': ['El nombre de usuario ya existe']}
        
        if self.user_repository.email_exists(email):
            return {'success': False, 'errors': ['El email ya está registrado']}
        
        # Crear usuario
        try:
            user = self.user_repository.create_user(username, email, password, role)
            return {'success': True, 'user': user.to_dict()}
        except Exception as e:
            return {'success': False, 'errors': [f'Error al crear usuario: {str(e)}']}
    
    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        # Autentica un usuario con nombre de usuario y contraseña
        if not username or not password:
            return {'success': False, 'errors': ['Username y contraseña son requeridos']}
        
        user = self.user_repository.authenticate(username, password)
        if user:
            if not user.is_active:
                return {'success': False, 'errors': ['Usuario desactivado']}
            return {'success': True, 'user': user.to_dict()}
        else:
            return {'success': False, 'errors': ['Credenciales inválidas']}
    

    def get_user_statistics(self) -> Dict[str, Any]:
        # Obtiene estadísticas de usuarios
        try:
            total_users = self.user_repository.count()
            active_users = len(self.user_repository.get_active_users())
            admin_users = len(self.user_repository.get_admins())
            
            return {
                'total_users': total_users,
                'active_users': active_users,
                'inactive_users': total_users - active_users,
                'admin_users': admin_users,
                'regular_users': total_users - admin_users
            }
        except Exception as e:
            return {'error': f'Error obteniendo estadísticas: {str(e)}'}
    
    def _validate_user_data(self, username: str, email: str, password: str) -> List[str]:
        #Valida los datos del usuario
        errors = []
        
        # Validar username
        if not username or len(username.strip()) < 3:
            errors.append('El nombre de usuario debe tener al menos 3 caracteres')
        
        if len(username) > 80:
            errors.append('El nombre de usuario no puede tener más de 80 caracteres')
        
        # Validar email
        if not email or '@' not in email:
            errors.append('Email inválido')
        
        if len(email) > 120:
            errors.append('El email no puede tener más de 120 caracteres')
        
        # Validar password
        if not password or len(password) < 6:
            errors.append('La contraseña debe tener al menos 6 caracteres')
        
        return errors
