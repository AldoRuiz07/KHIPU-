"""config_ia.py - conexion con Gemini, compartida por todos (dueño: P2)."""
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()                                            # lee el archivo .env (en la laptop)


def valor(nombre: str, defecto: str = "") -> str:
    """Lee una configuracion del .env (laptop) o de los Secrets (Streamlit Cloud)."""
    if os.getenv(nombre):
        return os.getenv(nombre)
    try:
        import streamlit as st
        return str(st.secrets.get(nombre, defecto))
    except Exception:
        return defecto


# Lista de modelos en orden de preferencia, separados por comas en el .env:
#   MODELOS=gemini-3.5-flash-lite,gemini-3.8-flash
# Si un modelo esta saturado (503) o sin cuota (429), se pasa al siguiente.
_lista = valor("MODELOS") or valor("MODELO") or "gemini-3.5-flash-lite"
MODELOS = [m.strip() for m in _lista.split(",") if m.strip()]
MODELO = MODELOS[0]                                      # el principal
ERRORES_DE_MODELO = (503, 429, 404)                      # saturado, sin cuota, no disponible

CLAVE_API = valor("GEMINI_API_KEY")
if not CLAVE_API or CLAVE_API == "pega_aqui_tu_clave":
    raise RuntimeError("Falta GEMINI_API_KEY: ponla en el .env (laptop) o en Secrets (Streamlit Cloud).")
cliente = genai.Client(api_key=CLAVE_API,
                       http_options=types.HttpOptions(timeout=30_000))   # max 30 s por intento

def generar(contenido, config=None):
    """generate_content con cambio automatico de modelo (lo usan Mi proyecto y el plan B)."""
    from google.genai import errors
    for modelo in MODELOS:
        try:
            return cliente.models.generate_content(model=modelo, contents=contenido, config=config)
        except errors.APIError as e:
            if e.code not in ERRORES_DE_MODELO:
                raise
            print(f">> {modelo} fallo ({e.code}); paso al siguiente modelo")
    raise RuntimeError("Todos los modelos estan ocupados. Intenta de nuevo en un minuto.")
