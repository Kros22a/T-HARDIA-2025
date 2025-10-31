from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.security import SECRET_KEY  # usa tu clave definida en security.py
from app.crud.user import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Obtiene el usuario autenticado a partir del token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user
