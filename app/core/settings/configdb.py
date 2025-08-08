from pydantic_settings import BaseSettings
from pathlib import Path
import os
from typing import Optional

from app.utils.utils import find_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    # Configuración PostgreSQL
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'admin'
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: str = '5432'
    POSTGRES_DB: str = 'sales_db'
    POSTGRES_SCHEMA: str = 'public'

    # Auth

    SECRET_KEY: str = 'tu_secret_key'
    FERNET_KEY: str = 'tu_fernet_key'
    
    # Configuración MongoDB
    MONGO_USER: Optional[str] = None
    MONGO_PASSWORD: Optional[str] = None
    MONGO_SERVER: str = 'localhost'
    MONGO_PORT: str = '27017'
    MONGO_DB: str = 'tu_db'
    
    # Solo para uso en local
    class Config:
        env_file = find_dotenv() or BASE_DIR / '.env'

settings = Settings()