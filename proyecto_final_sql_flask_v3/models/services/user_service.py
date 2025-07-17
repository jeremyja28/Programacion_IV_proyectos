"""
Servicio de Usuario - Responsabilidad: Lógica de negocio para usuarios
"""
from typing import Optional, List, Dict, Any
from models.entities.user import User
from models.repositories.user_repository import UserRepository


class UserService:
    """
    Servicio para lógica de negocio de usuarios
    
    Responsabilidades:
    - Validaciones de negocio
    - Procesos complejos de usuarios
    - Coordinación entre repositorios
    """
    
    def __init__(self):
        self.user_repository = UserRepository()
    
    def create_user(self, username: str, email: str, password: str, role: str = 'user') -> Dict[str, Any]:
        """
        Crea un nuevo usuario con validaciones
        
        Returns:
            dict: Resultado de la operación con usuario creado o errores
        """
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
        """
        Autentica un usuario
        
        Returns:
            dict: Resultado de la autenticación
        """
        if not username or not password:
            return {'success': False, 'errors': ['Username y contraseña son requeridos']}
        
        user = self.user_repository.authenticate(username, password)
        if user:
            if not user.is_active:
                return {'success': False, 'errors': ['Usuario desactivado']}
            return {'success': True, 'user': user.to_dict()}
        else:
            return {'success': False, 'errors': ['Credenciales inválidas']}
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por ID"""
        return self.user_repository.get_by_id(user_id)
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Obtiene todos los usuarios como diccionarios"""
        users = self.user_repository.get_all()
        return [user.to_dict() for user in users]
    
    def update_user(self, user_id: int, **kwargs) -> Dict[str, Any]:
        """Actualiza un usuario existente"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return {'success': False, 'errors': ['Usuario no encontrado']}
        
        # Validar email si se está actualizando
        if 'email' in kwargs:
            if self.user_repository.email_exists(kwargs['email']) and user.email != kwargs['email']:
                return {'success': False, 'errors': ['El email ya está registrado']}
        
        # Validar username si se está actualizando
        if 'username' in kwargs:
            if self.user_repository.username_exists(kwargs['username']) and user.username != kwargs['username']:
                return {'success': False, 'errors': ['El nombre de usuario ya existe']}
        
        try:
            updated_user = self.user_repository.update(user, **kwargs)
            return {'success': True, 'user': updated_user.to_dict()}
        except Exception as e:
            return {'success': False, 'errors': [f'Error al actualizar usuario: {str(e)}']}
    
    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """Elimina un usuario"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return {'success': False, 'errors': ['Usuario no encontrado']}
        
        try:
            success = self.user_repository.delete(user)
            if success:
                return {'success': True, 'message': 'Usuario eliminado exitosamente'}
            else:
                return {'success': False, 'errors': ['Error al eliminar usuario']}
        except Exception as e:
            return {'success': False, 'errors': [f'Error al eliminar usuario: {str(e)}']}
    
    def toggle_user_status(self, user_id: int) -> Dict[str, Any]:
        """Activa/desactiva un usuario"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return {'success': False, 'errors': ['Usuario no encontrado']}
        
        try:
            if user.is_active:
                updated_user = self.user_repository.deactivate_user(user)
                message = 'Usuario desactivado'
            else:
                updated_user = self.user_repository.activate_user(user)
                message = 'Usuario activado'
            
            return {'success': True, 'user': updated_user.to_dict(), 'message': message}
        except Exception as e:
            return {'success': False, 'errors': [f'Error al cambiar estado: {str(e)}']}
    
    def get_user_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de usuarios"""
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
        """Valida los datos del usuario"""
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
