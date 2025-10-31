import os
from dotenv import load_dotenv

# 🔹 Cargar variables de entorno antes de cualquier otra importación
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 🔹 Crear aplicación principal
app = FastAPI(
    title="T-Hardia - Hardware Information Platform",
    description="Advanced hardware information platform with AI comparisons",
    version="1.0.0"
)

# 🔹 Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las fuentes (puedes restringir más adelante)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Incluir los routers principales con prefijo /api/v1
from app.api.v1 import api_router
app.include_router(api_router, prefix="/api/v1")

# 🔹 Endpoints básicos
@app.get("/")
async def root():
    return {"message": "T-Hardia API is running 🚀"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "T-Hardia API is running"}

# 🔹 Servir frontend (solo si existe el directorio "frontend")
if os.path.exists("frontend"):
    try:
        app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
        print("✅ Frontend montado correctamente.")
    except Exception as e:
        print(f"⚠️ Warning: Could not mount static files: {e}")

# 🔹 Punto de entrada
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
