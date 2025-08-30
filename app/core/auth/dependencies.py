# app/core/auth/dependencies.py
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.auth.jwt import TokenJwt, get_token
from app.infrastructure.database.postgres import get_db
from app.infrastructure.adapters.postgres.user_repository import PostgresUserRepository

async def get_current_user(
    token: str = Depends(get_token),
    db: Session = Depends(get_db)
):
    """
    Dependency que obtiene el usuario actual validando el token en la BD
    """
    jwt_handler = TokenJwt(db=db)
    payload, error = jwt_handler.validate_token(token, verify_db=True)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Obtener usuario completo de la BD
    user_id = payload.get("sub")
    repo = PostgresUserRepository(db)
    user = repo.get_by_id(int(user_id))
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return user

async def get_current_active_user(current_user = Depends(get_current_user)):
    """
    Dependency que verifica que el usuario esté activo
    """
    if not current_user.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user