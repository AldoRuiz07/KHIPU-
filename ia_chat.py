"""ia_chat.py - chat conectado al inventario, acepta fotos y PDFs (dueño: P2)."""
import re
from datetime import date
from google.genai import types, errors
from config_ia import cliente, MODELOS, ERRORES_DE_MODELO, generar
import db
try:
    import lista                 # de P3 (Erik). Mientras no exista, Mi lista funciona igual
except ImportError:
    lista = None

INSTRUCCIONES = """Eres Khipu, asistente del almacén de componentes de la FIEE-UNMSM.
Reglas:
1. NUNCA afirmes si hay o no un componente sin usar antes buscar_en_almacen.
   El stock y la ubicación salen SOLO de las herramientas.
2. Si no hay stock o no alcanza, llama a ver_equivalentes y menciona la condición
   de cada uno (ej. 'pinout distinto'). Los equivalentes vienen verificados por
   estudiantes de Electrónica: NO los marques como sugerencia.
3. Si el estudiante envía una FOTO: identifica el componente leyendo el encapsulado y
   las marcas, di tu nivel de confianza (alta/media/baja) y luego búscalo en el almacén.
4. Si envía un PDF (guía o informe): resume en 2-3 líneas qué se hace, lista los
   componentes necesarios, revisa cada uno con buscar_en_almacen y da 2 tips clave.
5. Si el estudiante PIDE agregar o guardar componentes, llama a agregar_a_mi_lista
   de inmediato, sin preguntar. Usa el código EXACTO que devolvió buscar_en_almacen
   o ver_equivalentes (ej. 'PN2222A', no '2N2222'). Si no hay stock, agrega el
   equivalente disponible y avísalo. Si solo recomiendas, ofrece agregarlos.
6. Antes de sugerir cualquier alternativa (ej. Arduino), búscala con
   buscar_en_almacen y da su stock real. Nunca digas "según stock disponible".
7. Marca como 'sugerencia' solo lo que no venga del inventario (consejos de diseño).
8. Si preguntan por laboratorios u horarios, usa ver_laboratorios_libres. Calcula la
   fecha a partir de HOY (abajo). Las franjas son de 2 horas: 08:00, 10:00, 12:00,
   14:00, 16:00 y 18:00. Di cuáles están libres y, de los ocupados, el motivo.
9. Responde en español, breve y ordenado. Los componentes solo se usan en laboratorio:
   para pedirlos y reservar, el estudiante usa la pestaña Reservar Laboratorio."""

DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

# --- Herramientas: funciones normales. El docstring es lo que lee el modelo.
def buscar_en_almacen(texto: str) -> list:
    """Busca componentes en el almacén FIEE por código, nombre o categoría.
    Devuelve código, nombre, stock en el almacén y ubicación.

    Args:
        texto: código o palabra clave. Ej: 'LM358', 'transistor', 'sensor de distancia'.
    """
    return db.buscar(texto)

def ver_equivalentes(codigo: str) -> list:
    """Devuelve los equivalentes verificados de un componente y su stock.

    Args:
        codigo: código exacto del componente. Ej: '2N2222A'.
    """
    return db.equivalentes(codigo)

def ver_laboratorios_libres(fecha: str, hora_inicio: str) -> dict:
    """Muestra qué laboratorios están libres u ocupados en una fecha y franja de 2 horas.

    Args:
        fecha: fecha en formato AAAA-MM-DD. Ej: '2026-11-09'.
        hora_inicio: hora de inicio HH:MM. Franjas: 08:00, 10:00, 12:00, 14:00, 16:00, 18:00. Ej: '14:00'.
    """
    h = hora_inicio.strip().replace(".", ":")
    if ":" not in h:
        h += ":00"
    if len(h.split(":")[0]) == 1:
        h = "0" + h                                    # '8:00' -> '08:00'
    franja = next((f for f in db.FRANJAS if f[0] <= h < f[1]), None)
    if franja is None:
        return {"error": "Las franjas van de 08:00 a 20:00 en bloques de 2 horas."}
    try:
        date.fromisoformat(fecha)
    except ValueError:
        return {"error": "Fecha inválida, usa AAAA-MM-DD."}
    labs = db.estado_laboratorios(fecha, franja[0], franja[1])
    return {"fecha": fecha, "franja": f"{franja[0]}-{franja[1]}",
            "laboratorios": [{"nombre": l["nombre"], "libre": not l["ocupado"],
                              "motivo": l["motivo"]} for l in labs]}

def _herramientas(mi_lista: list) -> list:
    def agregar_a_mi_lista(codigo: str, cantidad: int) -> dict:
        """Agrega un componente a 'Mi lista' del estudiante, para reservarlo luego
        junto con un laboratorio.

        Args:
            codigo: código exacto del componente en el almacén. Ej: 'PN2222A'.
            cantidad: unidades que necesita. Ej: 2.
        """
        if lista:
            return lista.agregar(mi_lista, codigo, cantidad, origen="chat")
        comp = db.obtener(codigo)                       # version simple sin lista.py
        if comp is None:
            return {"ok": False, "error": f"{codigo} no existe en el almacén"}
        mi_lista.append({"codigo": comp["codigo"], "nombre": comp["nombre"],
                         "cantidad": int(cantidad), "origen": "chat"})
        return {"ok": True, "codigo": comp["codigo"], "cantidad": int(cantidad)}
    return [buscar_en_almacen, ver_equivalentes, ver_laboratorios_libres, agregar_a_mi_lista]

def _crear_chat(modelo: str, mi_lista: list, historial=None):
    hoy = date.today()
    config = types.GenerateContentConfig(
        system_instruction=INSTRUCCIONES + f"\n\nHOY es {DIAS[hoy.weekday()]} {hoy.isoformat()}.",
        tools=_herramientas(mi_lista), temperature=0.2)
    return cliente.chats.create(model=modelo, config=config, history=historial or [])

def nuevo_chat(mi_lista: list) -> dict:
    """El 'estado' del chat: el chat actual, qué modelo usa y la lista del estudiante."""
    return {"chat": _crear_chat(MODELOS[0], mi_lista), "i": 0, "lista": mi_lista}

def _partes(texto: str, archivos):
    """archivos = [(bytes, mime), ...] -> partes para Gemini (fotos y PDFs)."""
    partes = [types.Part.from_bytes(data=b, mime_type=m) for b, m in (archivos or [])]
    return partes + [texto or "Analiza este archivo."]

def preguntar(estado: dict, texto: str, archivos=None) -> str:
    for _ in range(len(MODELOS)):                       # prueba cada modelo una vez
        try:
            respuesta = estado["chat"].send_message(_partes(texto, archivos))
            db.registrar_consulta("chat", texto, respuesta.text)
            return respuesta.text
        except errors.APIError as e:
            if e.code not in ERRORES_DE_MODELO:        # otro error (ej. clave mala)
                raise
            print(f">> {MODELOS[estado['i']]} fallo ({e.code}); paso al siguiente modelo")
            estado["i"] = (estado["i"] + 1) % len(MODELOS)
            estado["chat"] = _crear_chat(MODELOS[estado["i"]], estado["lista"],
                                         estado["chat"].get_history())
    raise RuntimeError("Todos los modelos están ocupados. Intenta de nuevo en un minuto.")

# --- PLAN B: si el tool use falla, Python busca primero y le pasa los datos al modelo.
def preguntar_simple(texto: str, archivos=None) -> str:
    palabras = re.findall(r"[A-Za-z0-9\-]{3,}", texto or "")
    datos = [c for p in palabras for c in db.buscar(p, limite=3)]
    prompt = (INSTRUCCIONES + "\n\nDATOS DEL INVENTARIO (única fuente válida):\n"
              + str(datos) + "\n\nPREGUNTA: " + (texto or ""))
    return generar(_partes(prompt, archivos)).text
