import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

required_vars = [
    "FIREBASE_PROJECT_ID",
    "FIREBASE_PRIVATE_KEY",
    "FIREBASE_CLIENT_EMAIL",
    "FIREBASE_DATABASE_URL",
    "FIREBASE_TOKEN_URI"
]

missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    raise ValueError(f"⚠️ Faltan variables de entorno para Firebase: {missing}")

firebase_config = {
    "type": "service_account",
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
}

try:
    # ✅ Solo inicializa si no existe ya una app Firebase
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred, {
            "projectId": os.getenv("FIREBASE_PROJECT_ID"),
            "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
        })
    db = firestore.client()
    print("✅ Firebase Firestore conectado correctamente.")
except Exception as e:
    raise RuntimeError(f"🔥 Error al inicializar Firebase: {e}")
