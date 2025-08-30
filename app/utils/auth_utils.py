from bcrypt import gensalt, hashpw

from app.core.settings.configdb import settings

def encode_password_old(password:str):
    """Cifra la contraseña antes de almacenarla"""
    return hashpw(password.encode(settings.ENCODING),gensalt()).decode(settings.ENCODING)



def encode_password(password: str) -> str:
    """
    Codifica una contraseña usando bcrypt
    """
    salt = gensalt()
    hashed_password = hashpw(password.encode(settings.ENCODING), salt)
    return hashed_password.decode(settings.ENCODING)