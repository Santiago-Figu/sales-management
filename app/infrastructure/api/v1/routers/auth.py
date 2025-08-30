from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.auth.jwt import TokenJwt
from app.infrastructure.database.postgres import get_db
from app.infrastructure.adapters.postgres.user_repository import PostgresUserRepository
from app.infrastructure.api.v1.schemas.token import LoginResponse
from app.infrastructure.api.v1.schemas.user import UserFind

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=LoginResponse)
def login(form_data: UserFind):
    """Genera un token JWT si las credenciales son válidas."""
    db = next(get_db())
    repo = PostgresUserRepository(db)
    
    # Busca el usuario por username o email
    db_user = repo.get_by_email_user(form_data.username_email, form_data.username_email)

    # Verifica si el usuario existe
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Verifica si la contraseña es correcta
    if not repo.check_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta"
        )

    # Genera el token JWT
    token_data = {
        "sub": str(db_user.id),
        "username": db_user.username,
        "email": db_user.email
    }

    auth = TokenJwt()
    token = auth.create_access_token(token_data)
    
    # Verifica el token (opcional)
    auth.get_tokenJwt(token['access_token'])

    return token