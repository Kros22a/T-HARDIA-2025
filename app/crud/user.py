from datetime import datetime
from app.models.user import User, UserCreate
from app.core.security import hash_password
from app.core.firebase import db

# Referencia a la colección de usuarios
users_ref = db.collection("users")

# 🔹 Crear un nuevo usuario
def create_user(user_in: UserCreate) -> User:
    """Crea un nuevo usuario en Firestore."""
    # Verificar si el correo ya está registrado
    existing_user = users_ref.where("email", "==", user_in.email).limit(1).stream()
    if any(existing_user):
        raise ValueError("El correo ya está registrado.")

    hashed_password = hash_password(user_in.password)
    user_data = {
        "email": user_in.email,
        "username": user_in.username,
        "password_hash": hashed_password,
        "is_admin": False,
        "created_at": datetime.utcnow().isoformat(),
        "last_login": None
    }

    # Guardar en Firestore
    doc_ref = users_ref.document()
    doc_ref.set(user_data)
    user_data["id"] = doc_ref.id

    return User(**user_data)

# 🔹 Obtener un usuario por correo
def get_user_by_email(email: str):
    """Obtiene un usuario por correo electrónico."""
    query = users_ref.where("email", "==", email).limit(1).stream()
    for doc in query:
        data = doc.to_dict()
        data["id"] = doc.id
        return User(**data)
    return None

# 🔹 Autenticar usuario (login)
def authenticate_user(email: str, password: str):
    """Verifica las credenciales de inicio de sesión."""
    query = users_ref.where("email", "==", email).limit(1).stream()
    for doc in query:
        data = doc.to_dict()
        stored_password = data.get("password_hash")

        # Comparar contraseñas
        if stored_password and stored_password == hash_password(password):
            # Actualizar la fecha de último acceso
            users_ref.document(doc.id).update({
                "last_login": datetime.utcnow().isoformat()
            })
            data["id"] = doc.id
            return User(**data)

    return None

# 🔹 Listar todos los usuarios (solo para admin)
def get_all_users() -> list[User]:
    """Obtiene todos los usuarios registrados."""
    docs = users_ref.stream()
    users = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        users.append(User(**data))
    return users

# 🔹 Eliminar un usuario
def delete_user(user_id: str) -> bool:
    """Elimina un usuario por ID."""
    try:
        users_ref.document(user_id).delete()
        return True
    except Exception:
        return False
