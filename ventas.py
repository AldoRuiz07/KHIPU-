"""ventas.py - publicaciones de compra y venta entre estudiantes (dueño: P1).
Flujo: el alumno publica -> confirma con código a su correo UNMSM -> el encargado aprueba -> se ve."""
import random, string, hashlib, json
import db

ESTADOS = ["pendiente", "publicada", "rechazada", "vendida"]
CONDICION = ["Nuevo", "Usado - funciona bien", "Usado - para revisar"]

ESQUEMA = """
CREATE TABLE IF NOT EXISTS publicaciones (
    codigo TEXT PRIMARY KEY, titulo TEXT NOT NULL, cantidad INTEGER NOT NULL, precio REAL NOT NULL,
    condicion TEXT, descripcion TEXT, nombre TEXT NOT NULL, codigo_alumno TEXT NOT NULL,
    correo TEXT NOT NULL, whatsapp TEXT, foto BLOB, foto_tipo TEXT,
    estado TEXT NOT NULL DEFAULT 'pendiente', nota TEXT, verificacion TEXT, huella TEXT,
    creada TEXT DEFAULT (datetime('now', 'localtime')));
"""

def iniciar():
    con = db.conectar()
    con.executescript(ESQUEMA)
    con.close()

def _filas(sql, params=()):
    con = db.conectar()
    filas = [dict(f) for f in con.execute(sql, params).fetchall()]
    con.close()
    return filas

def validar(titulo, cantidad, precio, nombre, codigo_alumno, correo, whatsapp):
    """Revisa los datos SIN guardar. Lanza ValueError con un mensaje claro."""
    if len(str(titulo or "").strip()) < 3:
        raise ValueError("Escribe qué vendes (por ejemplo: Arduino Uno R3).")
    if int(cantidad or 0) < 1:
        raise ValueError("La cantidad debe ser al menos 1.")
    if float(precio if precio is not None else -1) < 0:
        raise ValueError("El precio no puede ser negativo.")
    if not str(nombre or "").strip() or not str(codigo_alumno or "").strip():
        raise ValueError("Pon tu nombre y tu código de alumno.")
    if not str(correo or "").strip().endswith("@unmsm.edu.pe"):
        raise ValueError("Tu correo debe ser @unmsm.edu.pe: ahí llega el código para confirmar.")
    w = str(whatsapp or "").replace(" ", "")
    if w and not (w.isdigit() and len(w) == 9 and w.startswith("9")):
        raise ValueError("El WhatsApp debe tener 9 dígitos y empezar con 9 (o déjalo vacío).")

def _huella(p: dict) -> str:
    datos = {k: p.get(k) for k in ("codigo", "titulo", "cantidad", "precio", "condicion",
                                   "descripcion", "nombre", "codigo_alumno", "correo",
                                   "whatsapp", "verificacion", "creada")}
    return hashlib.sha256(json.dumps(datos, ensure_ascii=False, sort_keys=True).encode()).hexdigest()

def crear(titulo, cantidad, precio, condicion, descripcion, nombre, codigo_alumno, correo,
          whatsapp="", foto: bytes | None = None, foto_tipo: str = "", verificacion: str = "") -> str:
    validar(titulo, cantidad, precio, nombre, codigo_alumno, correo, whatsapp)
    codigo = "PUB-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    con = db.conectar()
    con.execute("""INSERT INTO publicaciones (codigo, titulo, cantidad, precio, condicion, descripcion,
                   nombre, codigo_alumno, correo, whatsapp, foto, foto_tipo, verificacion)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (codigo, titulo.strip(), int(cantidad), float(precio), condicion,
                 str(descripcion or "").strip(), nombre.strip(), str(codigo_alumno).strip(),
                 correo.strip(), str(whatsapp or "").replace(" ", ""), foto, foto_tipo, verificacion))
    con.commit()
    con.close()
    p = obtener(codigo)
    con = db.conectar()
    con.execute("UPDATE publicaciones SET huella=? WHERE codigo=?", (_huella(p), codigo))
    con.commit()
    con.close()
    return codigo

def obtener(codigo: str) -> dict | None:
    f = _filas("SELECT * FROM publicaciones WHERE codigo=?", (codigo.strip().upper(),))
    return f[0] if f else None

def huella_valida(p: dict) -> bool:
    return bool(p.get("huella")) and p["huella"] == _huella(p)

def listar(estado: str | None = None, texto: str = "") -> list[dict]:
    t = f"%{texto.strip()}%"
    if estado:
        return _filas("""SELECT * FROM publicaciones WHERE estado=? AND (titulo LIKE ? OR descripcion LIKE ?)
                         ORDER BY creada DESC""", (estado, t, t))
    return _filas("SELECT * FROM publicaciones ORDER BY creada DESC")

def de_alumno(codigo_alumno: str) -> list[dict]:
    return _filas("SELECT * FROM publicaciones WHERE TRIM(codigo_alumno)=? ORDER BY creada DESC",
                  (str(codigo_alumno).strip(),))

def cambiar_estado(codigo: str, estado: str, nota: str = ""):
    if estado not in ESTADOS:
        raise ValueError(f"Estado inválido: {estado}")
    con = db.conectar()
    con.execute("UPDATE publicaciones SET estado=?, nota=? WHERE codigo=?", (estado, nota, codigo))
    con.commit()
    con.close()

def marcar_vendida(codigo: str, codigo_alumno: str) -> bool:
    """Solo el dueño (con el código PUB-XXXX que recibió por correo) puede marcarla como vendida."""
    p = obtener(codigo)
    if p is None or p["codigo_alumno"].strip() != str(codigo_alumno).strip() or p["estado"] != "publicada":
        return False
    cambiar_estado(p["codigo"], "vendida", p.get("nota") or "")
    return True
