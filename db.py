import sqlite3, random, string, csv
from datetime import date
from pathlib import Path

CARPETA = Path(__file__).parent / "data"
RUTA_DB = CARPETA / "khipu.db"

FRANJAS = [("08:00", "10:00"), ("10:00", "12:00"), ("12:00", "14:00"),
           ("14:00", "16:00"), ("16:00", "18:00"), ("18:00", "20:00")]
DIAS = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
ESTADOS = ["pendiente", "aceptada", "rechazada", "finalizada"]
ACTIVAS = ("pendiente", "aceptada")

ESQUEMA = """
CREATE TABLE IF NOT EXISTS componentes (
    codigo TEXT PRIMARY KEY, nombre TEXT NOT NULL, categoria TEXT, encapsulado TEXT,
    descripcion TEXT, stock INTEGER NOT NULL DEFAULT 0, ubicacion TEXT);
CREATE TABLE IF NOT EXISTS equivalencias (
    original TEXT NOT NULL, equivalente TEXT NOT NULL, condicion TEXT, verificado TEXT);
CREATE TABLE IF NOT EXISTS laboratorios (
    codigo TEXT PRIMARY KEY, nombre TEXT NOT NULL, capacidad INTEGER, ubicacion TEXT);
CREATE TABLE IF NOT EXISTS horario_clases (
    laboratorio TEXT, dia TEXT, inicio TEXT, fin TEXT, curso TEXT);
CREATE TABLE IF NOT EXISTS solicitudes (
    codigo TEXT PRIMARY KEY, laboratorio TEXT NOT NULL, fecha TEXT NOT NULL, inicio TEXT NOT NULL, fin TEXT NOT NULL, motivo TEXT, estado TEXT NOT NULL DEFAULT 'pendiente', nota TEXT,
    creada TEXT DEFAULT (datetime('now', 'localtime')));
CREATE TABLE IF NOT EXISTS estudiantes_solicitud (
    solicitud TEXT NOT NULL, nombre TEXT NOT NULL, codigo_alumno TEXT NOT NULL, correo TEXT);
CREATE TABLE IF NOT EXISTS items_solicitud (
    solicitud TEXT NOT NULL, componente TEXT NOT NULL, cantidad INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS consultas (
    id INTEGER PRIMARY KEY AUTOINCREMENT, tipo TEXT, texto TEXT, respuesta TEXT,
    creada TEXT DEFAULT (datetime('now', 'localtime')));
"""

def conectar():
    con = sqlite3.connect(RUTA_DB, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con

def normalizar(codigo: str) -> str:
    return str(codigo).upper().replace(" ", "").replace("-", "")

def _leer_csv(nombre):
    with open(CARPETA / nombre, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def iniciar():
    """Crea las tablas y carga los CSV (solo si la base está vacía)."""
    con = conectar()
    con.executescript(ESQUEMA)
    if con.execute("SELECT COUNT(*) FROM componentes").fetchone()[0] == 0:
        con.executemany("INSERT INTO componentes VALUES (?,?,?,?,?,?,?)",
            [(normalizar(r["codigo"]), r["nombre"], r["categoria"], r["encapsulado"],
              r["descripcion"], int(r["stock"]), r["ubicacion"]) for r in _leer_csv("inventario.csv")])
        con.executemany("INSERT INTO equivalencias VALUES (?,?,?,?)",
            [(normalizar(r["original"]), normalizar(r["equivalente"]), r["condicion"],
              r["verificado"]) for r in _leer_csv("equivalencias.csv")])
        con.executemany("INSERT INTO laboratorios VALUES (?,?,?,?)",
            [(r["codigo"], r["nombre"], int(r["capacidad"]), r["ubicacion"]) for r in _leer_csv("laboratorios.csv")])
        con.executemany("INSERT INTO horario_clases VALUES (?,?,?,?,?)",
            [(r["laboratorio"], r["dia"], r["inicio"], r["fin"], r["curso"]) for r in _leer_csv("horario_clases.csv")])
        con.commit()


def _filas(sql, params=()):
    con = conectar()
    filas = [dict(f) for f in con.execute(sql, params).fetchall()]
    con.close()
    return filas

def buscar(texto: str, limite: int = 8) -> list[dict]:
    """Busca por código, nombre, categoría o descripción."""
    t, c = f"%{texto.strip()}%", f"%{normalizar(texto)}%"
    return _filas("""SELECT codigo, nombre, categoria, encapsulado, stock, ubicacion
                     FROM componentes
                     WHERE codigo LIKE ? OR nombre LIKE ? OR categoria LIKE ? OR descripcion LIKE ?
                     ORDER BY (codigo LIKE ?) DESC, stock DESC LIMIT ?""",
                  (c, t, t, t, c, limite))

def obtener(codigo: str) -> dict | None:
    f = _filas("SELECT * FROM componentes WHERE codigo=?", (normalizar(codigo),))
    return f[0] if f else None

def equivalentes(codigo: str) -> list[dict]:
    """Equivalentes curados + su stock (en ambos sentidos)."""
    c = normalizar(codigo)
    filas = _filas("""
        SELECT e.equivalente AS codigo, e.condicion, c.stock, c.ubicacion, e.rowid AS orden
        FROM equivalencias e LEFT JOIN componentes c ON c.codigo = e.equivalente
        WHERE e.original = ?
        UNION ALL
        SELECT e.original, e.condicion, c.stock, c.ubicacion, e.rowid
        FROM equivalencias e LEFT JOIN componentes c ON c.codigo = e.original
        WHERE e.equivalente = ?
        ORDER BY orden""", (c, c))
    return [{k: v for k, v in f.items() if k != "orden"} for f in filas]

def listar_componentes() -> list[dict]:
    return _filas("SELECT * FROM componentes ORDER BY categoria, codigo")        

def listar_laboratorios() -> list[dict]:
    return _filas("SELECT * FROM laboratorios ORDER BY codigo")

def listar_horario() -> list[dict]:
    return _filas("SELECT * FROM horario_clases ORDER BY laboratorio, dia, inicio")

def _se_cruzan(i1, f1, i2, f2) -> bool:
    return i1 < f2 and i2 < f1

def estado_laboratorios(fecha: str, inicio: str, fin: str) -> list[dict]:
    """Cada laboratorio con 'ocupado' (True/False) y 'motivo' para esa fecha y franja."""
    dia = DIAS[date.fromisoformat(fecha).weekday()]
    resultado = []
    for lab in listar_laboratorios():
        motivo = None
        for c in _filas("SELECT * FROM horario_clases WHERE laboratorio=? AND dia=?", (lab["codigo"], dia)):
            if _se_cruzan(inicio, fin, c["inicio"], c["fin"]):
                motivo = f"Clase: {c['curso']}"
        for s in _filas(f"SELECT * FROM solicitudes WHERE laboratorio=? AND fecha=? AND estado IN {ACTIVAS}", (lab["codigo"], fecha)):
            if _se_cruzan(inicio, fin, s["inicio"], s["fin"]):
                motivo = "Reservado"
        resultado.append(lab | {"ocupado": motivo is not None, "motivo": motivo or ""})
    return resultado

def disponibles_en_franja(fecha: str, inicio: str, fin: str) -> dict[str, int]:
    """Componentes disponibles: stock menos lo reservado en franjas que se cruzan."""
    disp = {c["codigo"]: c["stock"] for c in listar_componentes()}
    for s in _filas(f"SELECT * FROM solicitudes WHERE fecha=? AND estado IN {ACTIVAS}", (fecha,)):
        if _se_cruzan(inicio, fin, s["inicio"], s["fin"]):
            for it in _filas("SELECT * FROM items_solicitud WHERE solicitud=?", (s["codigo"],)):
                disp[it["componente"]] = disp.get(it["componente"], 0) - it["cantidad"]
    return disp    

def crear_solicitud(laboratorio, fecha, inicio, fin, motivo, estudiantes: list[dict], items: list[tuple[str, int]]) -> str:
    """Valida todo y guarda la solicitud de laboratorio."""
    estudiantes = [e for e in estudiantes if str(e.get("nombre") or "").strip() and str(e.get("codigo_alumno") or "").strip()]
    if len(estudiantes) < 2:
        raise ValueError("Se necesitan al menos 2 estudiantes con nombre y código.")
    for e in estudiantes:
        correo = str(e.get("correo") or "").strip()
        if correo and not correo.endswith("@unmsm.edu.pe"):
            raise ValueError(f"El correo {correo} debe ser @unmsm.edu.pe")
    if not str(motivo or "").strip():
        raise ValueError("Escribe el motivo de la reserva.")
    
    lab = next((l for l in estado_laboratorios(fecha, inicio, fin) if l["codigo"] == laboratorio), None)
    if lab is None:
        raise ValueError("Ese laboratorio no existe.")
    if lab["ocupado"]:
        raise ValueError(f"{lab['nombre']} está ocupado en esa franja ({lab['motivo']}).")
        
    disp = disponibles_en_franja(fecha, inicio, fin)
    items = [(normalizar(c), int(n)) for c, n in items if c and int(n or 0) > 0]
    for cod, cant in items:
        if cod not in disp:
            raise ValueError(f"{cod} no existe en el almacén.")
        if cant > disp[cod]:
            raise ValueError(f"{cod}: pediste {cant}, en esa franja hay {max(disp[cod], 0)}.")
            
    codigo = "LAB-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    con = conectar()
    con.execute("INSERT INTO solicitudes (codigo, laboratorio, fecha, inicio, fin, motivo) VALUES (?,?,?,?,?,?)", 
                (codigo, laboratorio, fecha, inicio, fin, motivo.strip()))
    con.executemany("INSERT INTO estudiantes_solicitud VALUES (?,?,?,?)",
                    [(codigo, e["nombre"].strip(), str(e["codigo_alumno"]).strip(), str(e.get("correo") or "").strip()) for e in estudiantes])
    con.executemany("INSERT INTO items_solicitud VALUES (?,?,?)", [(codigo, c, n) for c, n in items])
    con.commit()
    con.close()
    return codigo

def ver_solicitud(codigo: str) -> dict | None:
    codigo = codigo.strip().upper()
    s = _filas("SELECT s.*, l.nombre AS lab_nombre FROM solicitudes s LEFT JOIN laboratorios l ON l.codigo = s.laboratorio WHERE s.codigo = ?", (codigo,))
    if not s:
        return None
    s = s[0]
    s["estudiantes"] = _filas("SELECT nombre, codigo_alumno, correo FROM estudiantes_solicitud WHERE solicitud=?", (codigo,))
    s["items"] = _filas("SELECT componente, cantidad FROM items_solicitud WHERE solicitud=?", (codigo,))
    return s

def listar_solicitudes(estado: str | None = None) -> list[dict]:
    if estado:
        codigos = _filas("SELECT codigo FROM solicitudes WHERE estado=? ORDER BY fecha, inicio", (estado,))
    else:
        codigos = _filas("SELECT codigo FROM solicitudes ORDER BY fecha, inicio")
    return [ver_solicitud(c["codigo"]) for c in codigos]

def cambiar_estado(codigo: str, estado: str, nota: str = ""):
    if estado not in ESTADOS:
        raise ValueError(f"Estado inválido: {estado}")
    con = conectar()
    con.execute("UPDATE solicitudes SET estado=?, nota=? WHERE codigo=?", (estado, nota, codigo))
    con.commit()
    con.close()

def reemplazar_tabla(tabla: str, filas: list[dict]):
    columnas = {"componentes": ["codigo", "nombre", "categoria", "encapsulado", "descripcion", "stock", "ubicacion"],
                "laboratorios": ["codigo", "nombre", "capacidad", "ubicacion"],
                "horario_clases": ["laboratorio", "dia", "inicio", "fin", "curso"]}[tabla]
    limpias = []
    for f in filas:
        if not str(f.get(columnas[0]) or "").strip():
            continue
        fila = [f.get(c) for c in columnas]
        if tabla == "componentes":
            fila[0] = normalizar(fila[0])
            fila[5] = int(fila[5] or 0)
        limpias.append(fila)
    con = conectar()
    con.execute(f"DELETE FROM {tabla}")
    con.executemany(f"INSERT INTO {tabla} VALUES ({','.join(['?']*len(columnas))})", limpias)
    con.commit()
    con.close()

def demanda(limite: int = 10) -> dict:
    return {
        "mas_pedidos": _filas("SELECT componente, SUM(cantidad) AS unidades, COUNT(*) AS solicitudes FROM items_solicitud GROUP BY componente ORDER BY unidades DESC LIMIT ?", (limite,)),
        "agotados": _filas("SELECT codigo, nombre FROM componentes WHERE stock = 0 ORDER BY codigo"),
        "consultas": _filas("SELECT COUNT(*) AS total FROM consultas")[0]["total"],
    }

def registrar_consulta(tipo: str, texto: str, respuesta: str):
    con = conectar()
    con.execute("INSERT INTO consultas (tipo, texto, respuesta) VALUES (?,?,?)", (tipo, texto, respuesta))
    con.commit()
    con.close()

    