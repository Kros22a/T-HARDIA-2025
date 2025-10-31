import firebase_admin
from firebase_admin import credentials, firestore
import os

# Para evitar inicialización doble
firebase_app = None
db = None

def get_db():
    global firebase_app, db

    if db:
        return db  # ✅ Ya existe una conexión válida

    try:
        if not firebase_admin._apps:
            cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "app/config/firebase_credentials.json")
            cred = credentials.Certificate(cred_path)
            firebase_app = firebase_admin.initialize_app(cred)
            print("✅ Firebase Firestore conectado correctamente.")
        else:
            firebase_app = firebase_admin.get_app()

        db = firestore.client(firebase_app)
        return db

    except Exception as e:
        print(f"❌ Error al conectar con Firebase Firestore: {e}")
        return None
