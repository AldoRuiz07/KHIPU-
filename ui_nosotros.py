"""ui_nosotros.py - secciones institucionales: Misión y visión, ¿Por qué nace Khipu? y
¿Quiénes somos? Se abren desde la barra lateral (dueño: P3). Contenido basado en el README."""
import streamlit as st
import estilo

# Pestañas de la página principal (ícono Material + título)
ICONOS = {"mision": ":material/target:", "porque": ":material/lightbulb:",
          "quienes": ":material/groups:"}
TITULOS = {"mision": "Misión y visión", "porque": "¿Por qué nace Khipu?",
           "quienes": "¿Quiénes somos?"}

EQUIPO = [
    ("karla.png", "Karla Montes", "Base de datos y reservas de laboratorio",
     "https://www.linkedin.com/in/karlamontesm"),
    ("aldo.png", "Aldo Ruiz", "Chat con IA, fotos y PDFs",
     "https://www.linkedin.com/in/aldoruiz07/"),
    ("erik.png", "Erik Espinel", "Interfaz, Mi proyecto y panel del encargado",
     "https://www.linkedin.com/in/erik-espinel-bernilla"),
]


def _html(texto: str):
    """Pasa HTML a Streamlit sin saltos de línea ni sangrías (evita que Markdown lo tome como código)."""
    st.markdown(" ".join(linea.strip() for linea in texto.splitlines() if linea.strip()),
                unsafe_allow_html=True)


def _tarjetas(items: list[tuple[str, str, str]]) -> str:
    return '<div class="khipu-grid">' + "".join(
        f'<div class="khipu-card"><div class="ico">{i}</div><h4>{t}</h4><p>{d}</p></div>'
        for i, t, d in items) + "</div>"


def pestanas(inicio=None):
    """Dibuja las pestañas informativas. Si se pasa `inicio` (una función), agrega antes la
    pestaña Inicio; luego: Misión y visión, ¿Por qué nace Khipu? y ¿Quiénes somos?"""
    etiquetas = [f"{ICONOS[k]} {TITULOS[k]}" for k in TITULOS]
    funciones = [_mision_vision, _por_que_nace, _quienes_somos]
    if inicio is not None:
        etiquetas.insert(0, ":material/home: Inicio")
        funciones.insert(0, inicio)
    for tab, funcion in zip(st.tabs(etiquetas), funciones):
        with tab:
            funcion()


# ====================================================================== Misión y visión
def _mision_vision():
    _html('<div class="khipu-eyebrow">Khipu · FIEE · UNMSM</div><h2 class=\"khipu-h2\">Misión y visión</h2>')
    _html("""<div class="khipu-grid">
        <div class="khipu-card grande"><div class="khipu-eyebrow">Misión</div>
        <p>Facilitar a los estudiantes de la FIEE el acceso al almacén y a los laboratorios de
        electrónica con una plataforma web que usa inteligencia artificial sobre datos reales de la
        facultad: para consultar componentes, planificar proyectos y reservar laboratorios de forma
        rápida, confiable y sin trámites manuales.</p></div>
        <div class="khipu-card grande"><div class="khipu-eyebrow">Visión</div>
        <p>Ser la plataforma de referencia para la gestión de almacenes y laboratorios de San Marcos:
        con inicio de sesión institucional, firma digital, inventario real y una comunidad que comparte
        proyectos, y llevarla a otros laboratorios y facultades de la universidad.</p></div>
        </div>""")

    _html("<h2 class=\"khipu-h2\">Nuestros principios</h2>")
    _html(_tarjetas([
        ("🧠", "La IA no inventa",
         "El modelo entiende texto, fotos y PDFs, pero el stock y la ocupación salen de nuestra base de "
         "datos a través de funciones que nosotros controlamos."),
        ("🎓", "De estudiantes, para estudiantes",
         "Lo construimos desde lo que vivimos cada ciclo en la FIEE. Las equivalencias entre componentes "
         "las armamos y revisamos con los datasheets."),
        ("🔏", "Confianza y seguridad",
         "Las reservas se confirman con un código al correo institucional y se guardan con sello digital "
         "SHA-256. Las validaciones las hace Python, no el modelo."),
        ("🛠️", "Datos al alcance del encargado",
         "El encargado mantiene inventario, laboratorios y horarios desde su panel, sin tocar código."),
    ]))

    _html("<h2 class=\"khipu-h2\">Hacia dónde vamos</h2>")
    _html("""<div class="khipu-grid">
        <div class="khipu-card"><h4>✅ Ya funciona</h4><div class="khipu-hecho"><ul>
        <li>Chat con inventario real, equivalentes, fotos y PDFs</li>
        <li>Lista de componentes a partir de tu proyecto</li>
        <li>Reserva de laboratorio con stock por franja</li>
        <li>Confirmación por correo institucional y sello digital</li>
        <li>Panel del encargado en tiempo real</li></ul></div></div>
        <div class="khipu-card"><h4>🚀 Lo que sigue</h4><div class="khipu-hecho"><ul>
        <li>Iniciar sesión con la cuenta @unmsm.edu.pe</li>
        <li>Firma digital con DNIe (RENIEC)</li>
        <li>Base de datos en la nube, para que nada se pierda</li>
        <li>Un foro para compartir proyectos y dudas</li>
        <li>Inventario real del almacén, en más laboratorios y facultades</li></ul></div></div>
        </div>""")


# ====================================================================== ¿Por qué nace Khipu?
def _por_que_nace():
    _html('<div class="khipu-eyebrow">Nuestro origen</div><h2 class=\"khipu-h2\">¿Por qué nace Khipu?</h2>')
    _html("""<div class="khipu-cita">Más de una vez fuimos al almacén sin saber si había lo que
        buscábamos, compramos algo que la facultad ya tenía o llenamos solicitudes a mano.
        Khipu nació de eso.</div>""")

    _html("<h2 class=\"khipu-h2\">El contexto</h2>")
    _html("""<p class="sub">En la Facultad de Ingeniería Electrónica y Eléctrica de San Marcos armamos
        circuitos desde los primeros ciclos: fuentes, amplificadores, sistemas digitales, robots y
        proyectos IoT. Para eso la facultad tiene un <b>almacén</b> con circuitos integrados,
        transistores, sensores y módulos que se prestan a los estudiantes, y <b>laboratorios de
        electrónica</b> que se piden formalmente según el Reglamento General de los Laboratorios de
        Electrónica (R.D. N.° 000989-2023-D-FIEE/UNMSM). Los componentes solo se pueden usar dentro de
        un laboratorio, y hoy todo depende de ir en persona, preguntar y llenar formatos a mano.</p>""")

    _html("<h2 class=\"khipu-h2\">El problema que vivimos cada ciclo</h2>")
    _html(_tarjetas([
        ("🚶", "Ir sin saber si hay",
         "Vas al almacén sin saber si tienen lo que necesitas, y muchas veces te regresas con las manos vacías."),
        ("📄", "No saber qué pide tu proyecto",
         "Tienes que leerte toda la guía para saber qué componentes necesitas, a veces minutos antes de entrar a clase."),
        ("🔁", "Nadie dice qué lo reemplaza",
         "Si algo falta, no hay quien te diga qué lo puede sustituir, y terminas comprando algo que la facultad sí tenía."),
        ("🔍", "Marcas ilegibles",
         "Hay componentes con marcas tan pequeñas o borrosas que cuesta saber qué son."),
        ("📝", "Reservar es un trámite manual",
         "Formato, datos de al menos dos estudiantes, firmas y un correo a la jefatura del laboratorio."),
        ("📉", "El almacén no sabe qué buscan",
         "Sin ver lo que piden los alumnos, no puede anticipar qué comprar."),
    ]))

    _html("<h2 class=\"khipu-h2\">Nuestra respuesta</h2>")
    _html("""<p class="sub">Una sola app web que te acompaña desde que tienes la idea del proyecto hasta
        que tienes el laboratorio y los componentes reservados. Lo que el chat o tu proyecto te
        recomiendan se guarda en <b>Mi lista</b>, y al reservar esos componentes ya están cargados.</p>
        <div class="khipu-pasos-flujo">
        <span>💬 Pregunto o subo una foto/PDF</span><i>→</i>
        <span>📋 Cuento mi proyecto</span><i>→</i>
        <span>🛒 Mi lista</span><i>→</i>
        <span>🔬 Reservo laboratorio</span><i>→</i>
        <span>✉️ Confirmo con mi correo UNMSM</span><i>→</i>
        <span>🔐 El encargado responde</span></div>""")

    _html("<h2 class=\"khipu-h2\">¿Por qué el nombre «Khipu»?</h2>")
    _html("""<div class="khipu-card grande"><p>Los incas llevaban el registro de sus almacenes
        (<i>qollqas</i>), censos e inventarios con el <b>khipu</b>: un cordón principal del que
        colgaban cuerdas con nudos, y cada nudo guardaba un dato. Nos pareció la metáfora perfecta.
        Nuestro logo es un cordón del que cuelgan componentes electrónicos. Khipu es, en el fondo,
        el registro del almacén de nuestra facultad, hecho por estudiantes de Electrónica para
        estudiantes.</p></div>""")


# ====================================================================== ¿Quiénes somos?
def _quienes_somos():
    _html('<div class="khipu-eyebrow">El equipo</div><h2 class=\"khipu-h2\">¿Quiénes somos?</h2>')
    _html("""<p class="sub">Somos tres estudiantes de <b>Ingeniería Electrónica de San Marcos</b>.
        Creamos Khipu para ENEISOFT 2026 (XVI edición), en el sub-eje de Gestión universitaria,
        a partir de lo que vivimos nosotros mismos en el almacén y los laboratorios de la FIEE.</p>""")

    personas = "".join(
        f'<div class="khipu-persona"><img src="{estilo.imagen("equipo/" + foto) or estilo.imagen(foto)}" '
        f'alt="{nombre}"><b>{nombre}</b><span>{rol}</span>'
        f'<a href="{url}" target="_blank" rel="noopener noreferrer">LinkedIn</a></div>'
        for foto, nombre, rol, url in EQUIPO)
    _html(f'<div class="khipu-equipo">{personas}</div>')

    _html("<h2 class=\"khipu-h2\">Cómo está construido</h2>")
    _html("""<p class="sub">No entrenamos un modelo propio: conectamos modelos que ya existen a datos
        reales de la facultad, de forma que la IA nunca tenga que adivinar.</p>
        <div class="khipu-tec"><span>Python</span><span>Streamlit</span><span>SQLite</span>
        <span>Google Gemini</span><span>SMTP · SHA-256</span></div>""")

    _html("""<div class="khipu-cita">Hecho pensando en la FIEE · Universidad Nacional Mayor de San
        Marcos.</div>""")
