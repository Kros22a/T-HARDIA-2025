from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Optional
from app.models.user import UserCreate, User, Token
from app.crud import user as user_crud
import jwt
from datetime import datetime, timedelta
import os

router = APIRouter(prefix="/users", tags=["Users"])

# 🔹 Configuración JWT
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("❌ SECRET_KEY environment variable is not set.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Genera un JWT"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register", response_model=User)
async def register_user(user: UserCreate):
    """Registrar un nuevo usuario"""
    existing_user = user_crud.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")

    new_user = user_crud.create_user(user)
    return new_user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Inicio de sesión"""
    user = user_crud.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def get_current_user(token: str):
    """Obtener información del usuario autenticado"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Token inválido o expirado.")
        user = user_crud.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado.")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido.")


@router.get("/", response_model=List[User])
async def get_all_users():
    """Listar todos los usuarios"""
    return user_crud.get_all_users()


@router.get("/{user_id}", response_model=User)
async def get_user_by_id(user_id: str):
    """Obtener un usuario por ID"""
    user = user_crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return user
