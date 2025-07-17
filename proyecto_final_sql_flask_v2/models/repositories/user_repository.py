#Repositorio de usuarios
from typing import Optional, List
from models.entities.user import User
from models.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    
    def __init__(self):
        super().__init__(User)
    
    def get_by_username(self, username: str) -> Optional[User]:
        # Obtiene un usuario por nombre de usuario
        return User.query.filter_by(username=username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        # Obtiene un usuario por email
        return User.query.filter_by(email=email).first()
    
    def get_admins(self) -> List[User]:
        # Obtiene todos los usuarios administradores
        return User.query.filter_by(role='admin').all()
    
    def get_active_users(self) -> List[User]:
        # Obtiene todos los usuarios activos
        return User.query.filter_by(is_active=True).all()
    
    def username_exists(self, username: str) -> bool:
        # Verifica si un nombre de usuario ya existe
        return User.query.filter_by(username=username).first() is not None
    
    def email_exists(self, email: str) -> bool:
        # Verifica si un email ya existe
        return User.query.filter_by(email=email).first() is not None
    
    def create_user(self, username: str, email: str, password: str, role: str = 'user') -> User:
        # Crea un nuevo usuario con contraseña encriptada
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        return self.create(
            username=username,
            email=email,
            password_hash=user.password_hash,
            role=role
        )
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        # Autentica un usuario con username y contraseña
        user = self.get_by_username(username)
        if user and user.check_password(password):
            return user
        return None
    
    def deactivate_user(self, user: User) -> User:
        # Desactiva un usuario
        return self.update(user, is_active=False)
    
    def activate_user(self, user: User) -> User:
        # Activa un usuario
        return self.update(user, is_active=True)
