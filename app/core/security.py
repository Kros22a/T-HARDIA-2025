import hashlib
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

# Configuración para JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

if not SECRET_KEY:
    raise ValueError("❌ SECRET_KEY environment variable is not set.")

# 🔐 Función para hashear contraseñas
def hash_password(password: str) -> str:
    """Devuelve el hash SHA-256 de la contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

# 🔑 Generar token JWT
def create_access_token(data: dict):
    """Crea un token JWT con expiración"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
