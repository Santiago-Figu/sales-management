from pydantic_settings import BaseSettings
from pathlib import Path
import os
from typing import Optional

from app.utils.utils import find_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class BarCodeSettings(BaseSettings):
    """
    Clase con valores de configuración tomados de las variables de entorno
    Args:
        CLAVEPAIS: Código del pais de 3 dígitos (ej. '750' para méxico )
        EMPRESAID: ID GS1 de la empresa (default '99999' para pruebas)
    """
    CLAVEPAIS: int = 750 # Código del pais de 3 dígitos (ej. '750' para méxico )
    EMPRESAID: int = 99999
    # Solo para uso en local
    class Config:
        env_file = find_dotenv() or BASE_DIR / '.env'

bar_code_settings = BarCodeSettings()