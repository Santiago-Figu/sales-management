from fastapi import APIRouter, Depends, HTTPException, status
from app.core.auth.dependencies import get_current_active_user, get_current_user
from app.core.auth.jwt import TokenJwt, get_token
from datetime import datetime, UTC
from sqlalchemy.orm import Session
from app.infrastructure.adapters.postgres.user_repository import PostgresUserRepository
from app.infrastructure.database.postgres import get_db

router = APIRouter(prefix="/test", tags=["Token Testing"])

@router.get("/verify")
async def verify_token(token: str = Depends(get_token)):
    """
    Verifica y decodifica un token JWT
    """
    jwt_handler = TokenJwt()
    
    payload, error = jwt_handler.validate_token(token)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "status": "success",
        "message": "Token válido",
        "data": payload
    }

@router.get("/token-info")
async def get_token_info(token: str = Depends(get_token)):
    """
    Obtiene información detallada del token
    """
    jwt_handler = TokenJwt()
    
    payload, error = jwt_handler.validate_token(token)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Información del usuario
    user_info = {
        "user_id": payload.get("sub"),
        "username": payload.get("username"),
        "email": payload.get("email")
    }
    
    # Información del token
    expiration = payload.get("exp")
    if expiration:
        expiration_dt = datetime.fromtimestamp(expiration, tz=UTC)
        time_remaining = expiration_dt - datetime.now(UTC)
    
    token_info = {
        "expiration_timestamp": expiration,
        "expiration_datetime": expiration_dt.isoformat() if expiration else None,
        "time_remaining_seconds": time_remaining.total_seconds() if expiration else None,
        "issued_at": payload.get("iat"),
        "algorithm": "HS256"
    }
    
    return {
        "user": user_info,
        "token": token_info
    }

@router.post("/generate-test-token")
async def generate_test_token():
    """
    Genera un token de prueba con datos de ejemplo
    """
    jwt_handler = TokenJwt()
    
    test_data = {
        "sub": "123",
        "username": "test_user",
        "email": "test@example.com"
    }
    
    token = jwt_handler.create_access_token(test_data)
    return {
        "message": "Token de prueba generado",
        "token": token,
        "test_data": test_data
    }

@router.get("/verify-db")
async def verify_token_with_db(
    token: str = Depends(get_token),
    db: Session = Depends(get_db)
):
    """
    Verifica el token JWT y valida en la base de datos
    """
    jwt_handler = TokenJwt(db=db)
    
    # validate_token con verify_db=True para verificación en BD
    payload, error = jwt_handler.validate_token(token, verify_db=True)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "status": "success",
        "message": "Token válido y usuario verificado en base de datos",
        "user_id": payload.get("sub"),
        "username": payload.get("username"),
        "email": payload.get("email")
    }

@router.get("/user-info")
async def get_user_info_from_token(
    token: str = Depends(get_token),
    db: Session = Depends(get_db)
):
    """
    Obtiene información completa del usuario desde la base de datos usando el token
    """
    jwt_handler = TokenJwt(db=db)
    
    # Primero validar el token
    payload, error = jwt_handler.validate_token(token, verify_db=True)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Obtener información completa del usuario desde la BD
    user_id = payload.get("sub")
    repo = PostgresUserRepository(db)
    user = repo.get_by_id(int(user_id))
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado en la base de datos"
        )
    
    # Devolver información del usuario (excluyendo información sensible)
    return {
        "user_info": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "active": user.active,
            "created": user.created.isoformat() if user.created else None,
            "last_update": user.last_update.isoformat() if user.last_update else None
        },
        "token_info": {
            "user_id_in_token": payload.get("sub"),
            "expiration": payload.get("exp"),
            "issued_at": payload.get("iat")
        }
    }

@router.get("/protected-endpoint")
async def protected_endpoint(current_user = Depends(get_current_active_user)):
    """
    Endpoint protegido que requiere usuario autenticado y activo
    """
    return {
        "message": f"Hola {current_user.first_name} {current_user.last_name}",
        "user_id": current_user.id,
        "username": current_user.username
    }

@router.get("/me")
async def read_users_me(current_user = Depends(get_current_user)):
    """
    Obtiene información del usuario actual
    """
    return {
        "id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "username": current_user.username,
        "email": current_user.email,
        "active": current_user.active
    }