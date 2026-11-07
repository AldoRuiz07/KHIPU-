"""ia_proyecto.py - idea de proyecto -> lista de componentes y tips (dueño: P3)."""
import json
from google.genai import types
from config_ia import generar
import db

PROMPT_BOM = """Eres un ingeniero electrónico que ayuda a estudiantes de pregrado de la FIEE-UNMSM.

A partir de la idea de proyecto, responde SOLO un JSON con dos claves:
  "componentes": lista de objetos con
      "codigo": código comercial más común (ej. "LM358", "BC547", "HC-SR04"),
      "funcion": para qué sirve en este proyecto (máx. 8 palabras),
      "cantidad": número entero;
  "tips": lista de 2 a 3 consejos prácticos y breves para armar el proyecto.

No incluyas resistencias ni condensadores sueltos, cables ni protoboard. Máximo 12 componentes.

PROYECTO:
"""


def proyecto_a_bom(idea: str) -> dict:
    """Devuelve {'componentes': [...], 'tips': [...]}."""
    config = types.GenerateContentConfig(response_mime_type="application/json",
                                         temperature=0.2)
    for _ in range(2):                      # si el JSON viene roto, reintenta 1 vez
        r = generar(PROMPT_BOM + idea[:8000], config)
        try:
            datos = json.loads(r.text)
            if isinstance(datos, list):     # por si el modelo devuelve solo la lista
                datos = {"componentes": datos, "tips": []}
            db.registrar_consulta("proyecto", idea[:500], r.text)
            return {"componentes": datos.get("componentes", []),
                    "tips": datos.get("tips", [])}
        except (json.JSONDecodeError, AttributeError):
            pass
    raise ValueError("No pude entender el proyecto. Intenta describirlo más corto.")
