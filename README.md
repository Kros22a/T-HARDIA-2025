# T-Hardia - Hardware Information Platform

Plataforma web avanzada de información de hardware con comparaciones IA, encuestas y blog.

## Características

- 🖥️ Comparaciones de hardware generadas por IA (GROQ)
- 📊 Sistema de encuestas con preguntas aleatorias
- 👥 Registro de usuarios y panel administrativo
- 📝 Blog con artículos técnicos y guías
- 🎨 Animaciones 3D con Three.js
- 🔥 Integración con Firebase
- ☁️ Despliegue en Vercel

## Tecnologías

- **Backend**: Python + FastAPI
- **Frontend**: HTML5, CSS3, JavaScript + Three.js
- **Base de Datos**: Firebase Firestore
- **IA**: GROQ API
- **Despliegue**: Vercel

## Instalación Local

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/t-hardia.git
cd t-hardia


## Crear usuario admin (manual)

Puedes crear el admin de dos formas:

### Opción A — Manual vía consola de Firebase
1. Abre la consola de Firebase → Firestore → Colección `users`.
2. Crea un nuevo documento con ID = `admin@t-hardia.com` y el siguiente contenido:
```json
{
  "email": "admin@t-hardia.com",
  "name": "Administrador T-Hardia",
  "role": "admin",
  "password": "<bcrypt hash de la contraseña>",
  "created_at": "2025-10-24T00:00:00Z"
}
```
> Recomendación: no almacenes contraseñas en texto plano. Usa un hash bcrypt.

### Opción B — Usar el script helper
1. Define la variable de entorno `FIREBASE_CONFIG` con el JSON del service account.
2. Ejecuta:
```bash
pip install firebase-admin passlib[bcrypt]
python scripts/create_admin.py --email admin@t-hardia.com --password "TuPassSegura"
```
Esto creará el documento con `role: "admin"` y la contraseña hasheada.

