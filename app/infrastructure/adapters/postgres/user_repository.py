from typing import List, Optional
from bcrypt import checkpw, hashpw
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.core.logger.config import LoggerConfig
from app.core.settings.configdb import settings
from app.domain.models.user import User
from app.domain.ports.user_repository import UserRepository
from app.infrastructure.database.postgres import get_db
from app.utils.auth_utils import encode_password


class PostgresUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db
        self.logger = LoggerConfig(file_name='user_repository',debug=True).get_logger()

    # Operaciones de CRUD básicas

    def create(self, user: User) -> User:
        
        user.password = encode_password(user.password)
        self._validate_user(user)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_id(self, user_id:int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first() 
    
    def get_all(self) -> Optional[List[User]]:
        return self.db.query(User).all()
    
    def get_by_email_user(self, username:str = None, email:str = None) -> Optional[User]:

        db_user = self.db.query(User).filter(
            or_(
                User.username == username,
                User.email == email
            )
        ).first()

        return db_user
    
    def update(self, user_id:int, user_data:dict) -> Optional[User]:
       
        user_update = self.get_by_id(user_id)

        if not user_update:
            return None
        
        if 'password' in user_data:
            # self._validate_internal_code(user_data['internal_code'], user_id)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Opción de cambio de password no disponible"
            )
        
        for key, value in user_data.items():
            setattr(user_update, key, value)
        self.db.commit()
        self.db.refresh(user_update)
        return user_update

    def delete(self, user_id:int) -> bool:
        user_delete = self.get_by_id(user_id)
        if user_delete:
            self.db.delete(user_delete)
            self.db.commit()
            return True
        else:
            return False

    ##Operaciones de validación
    
    def _validate_user(self,user: User):
        db_user = self.get_by_email_user(user.username, user.email)

        if db_user:
            if db_user.username == user.username:
                message = "El nombre de usuario ya está en uso."
                self.logger.warning(message)
                raise HTTPException(status_code=400, detail=message)
            if db_user.email == user.email:
                message = "El correo electrónico ya está registrado."
                self.logger.warning(message)
                raise HTTPException(status_code=400, detail=message)
            
     # Método para verificar contraseña
    def check_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica que la contraseña ingresada coincida con la almacenada
        """
        try:
            return checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            self.logger.error(f"Error al verificar contraseña: {e}")
            return False


