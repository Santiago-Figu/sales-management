import sys
from pathlib import Path
from typing import Optional
from fastapi import Depends
from datetime import UTC, datetime, timedelta, timezone
from jose import JWTError, jwt
from cryptography.fernet import Fernet
from app.core.logger.config import LoggerConfig
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.settings.configdb import settings
from sqlalchemy.orm import Session
from app.infrastructure.database.postgres import get_db
from app.infrastructure.adapters.postgres.user_repository import PostgresUserRepository

# obtener el logger
logger = LoggerConfig(file_name='jwt_config',debug=True).get_logger()

# Crear una instancia de HTTPBearer
security = HTTPBearer()

class TokenJwt:

    def __init__(self, db: Optional[Session] = None):
        # Clave secreta para firmar los tokens JWT
        self.SECRET_KEY = settings.SECRET_KEY
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY no está configurada.")
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 10

        # Clave para cifrar el token JWT
        self.FERNET_KEY = settings.FERNET_KEY
        if not self.FERNET_KEY:
            raise ValueError("FERNET_KEY no está configurada.")
        self.cipher_suite = Fernet(self.FERNET_KEY)
        
        # Sesión de base de datos (opcional)
        self.db = db

    def create_access_token(self, data: dict):
        """Genera un token JWT con la información del usuario."""
        token = None
        try:
            logger.info(f"Generando token de acceso para el usuario {data['username']}")
            to_encode = data.copy()
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
            
            # Cifra el token JWT
            encrypted_token = self.cipher_suite.encrypt(encoded_jwt.encode())
            token = encrypted_token.decode()
        except Exception as e:
            logger.error(f"Ocurrió un error al generar el Token: {e}")
        finally:
            return {"access_token": str(token), "token_type": "bearer"}
        
    def get_tokenJwt(self, token):
        jwt_token = self.cipher_suite.decrypt(token).decode()
        logger.debug("tokenJwt", jwt_token)

    def validate_token(self, token: str, verify_db: bool = False):
        """Valida el token JWT y opcionalmente verifica en la base de datos."""
        payload = None
        error = None
        logger.info('Validando token')
        
        try:
            # Descifra el token JWT
            decrypted_token = self.cipher_suite.decrypt(token.encode()).decode()
            # Decodifica el token JWT
            payload = jwt.decode(decrypted_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            logger.debug(f'payload: {payload}')
            
            # Verifica si el token ha expirado
            expire = payload.get("exp")
            if expire is None:
                error = "Token expirado"
                logger.error(f"{error}")
            else:
                # Convertir la marca de tiempo a datetime con zona horaria UTC
                expire_datetime = datetime.fromtimestamp(expire, tz=UTC)
                if expire_datetime < datetime.now(UTC):
                    error = "Token expirado"
                    logger.error(f"{error}")
            
            # Verificación en base de datos (si se solicita y hay conexión)
            if verify_db and self.db and not error:
                db_error = self._verify_user_in_db(payload)
                if db_error:
                    error = db_error
                else:
                    logger.info('Token válido y usuario verificado en BD')
                    
        except JWTError as e:
            logger.error(f"Error al validar el token: {e}")
            error = "Token inválido"
        except Exception as e:
            logger.error(f"Error al validar el token: {e}")
            error = "Token inválido"
        
        return payload, error
    
    def _verify_user_in_db(self, payload: dict) -> Optional[str]:
        """Verifica que el usuario del token exista en la base de datos."""
        try:
            user_id = payload.get("sub")
            username = payload.get("username")
            email = payload.get("email")
            
            if not user_id:
                return "ID de usuario no encontrado en el token"
            
            # Usar el repositorio para buscar el usuario
            repo = PostgresUserRepository(self.db)
            user = repo.get_by_id(int(user_id))
            
            if not user:
                return "Usuario no encontrado en la base de datos"
            
            # Verificar que los datos coincidan
            if user.username != username:
                return "Nombre de usuario no coincide"
                
            if user.email != email:
                return "Email no coincide"
                
            # Verificar que el usuario esté activo
            if not user.active:
                return "Usuario inactivo"
                
            return None
            
        except Exception as e:
            logger.error(f"Error al verificar usuario en BD: {e}")
            return f"Error de verificación en base de datos: {str(e)}"

    @staticmethod
    def generate_fernet_key():
        # Generar una clave válida
        FERNET_KEY = Fernet.generate_key()
        logger.debug(FERNET_KEY)

# Función para extraer el token de las credenciales de autorización
def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Extrae el token de las credenciales de autorización."""
    return credentials.credentials

# Función para obtener el validador de tokens con verificación de BD
def get_token_validator(db: Session = Depends(get_db)):
    """Retorna una instancia de TokenJwt con conexión a BD."""
    return TokenJwt(db=db)

if __name__ == "__main__":
    TokenJwt.generate_fernet_key()