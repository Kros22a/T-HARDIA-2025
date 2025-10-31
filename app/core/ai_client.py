# app/core/ai_client.py
import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"  # ✅ endpoint correcto

def compare_components_ai(component1: str, component2: str):
    if not GROQ_API_KEY:
        raise ValueError("⚠️ Falta la variable de entorno GROQ_API_KEY")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "llama-3.3-70b-versatile",  # ✅ modelo válido
        "messages": [
            {
                "role": "system",
                "content": "Eres un experto en hardware. Compara de forma técnica y concisa dos componentes de PC."
            },
            {
                "role": "user",
                "content": f"Compara {component1} y {component2} en rendimiento, consumo, temperatura y relación precio-rendimiento."
            },
        ],
        "temperature": 0.7,
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)

    if response.status_code != 200:
        raise ValueError(f"Error al realizar la comparación: {response.status_code} {response.text}")

    result = response.json()
    return result["choices"][0]["message"]["content"]
