#!/usr/bin/env python3
"""Script helper para crear un usuario admin en Firestore.

USO:
- Exporta la variable de entorno FIREBASE_CONFIG con el JSON de credenciales del service account.
- Ejecuta: python scripts/create_admin.py --email admin@t-hardia.com --password "TuPassSegura"
"""
import os, json, argparse
from datetime import datetime
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except Exception as e:
    raise SystemExit("Necesitas instalar firebase_admin: pip install firebase-admin") from e

try:
    from passlib.hash import bcrypt
except Exception as e:
    raise SystemExit("Necesitas instalar passlib: pip install passlib[bcrypt]") from e

def init_db():
    cfg = os.getenv("FIREBASE_CONFIG")
    if not cfg:
        raise RuntimeError("Define la variable FIREBASE_CONFIG con el JSON de credenciales")
    cred_dict = json.loads(cfg)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
    return firestore.client()

def create_admin(email, password, name="Administrador"):
    db = init_db()
    pw_hash = bcrypt.hash(password)
    doc_ref = db.collection("users").document(email)
    doc_ref.set({
        "email": email,
        "name": name,
        "role": "admin",
        "password": pw_hash,
        "created_at": datetime.utcnow().isoformat() + "Z"
    })
    print(f"Admin creado: {email}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    args = parser.parse_args()
    create_admin(args.email, args.password)

if __name__ == '__main__':
    main()
