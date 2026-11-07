"""ui_inicio.py - pestaña Inicio: qué es Khipu, cómo se usa y preguntas frecuentes."""
import streamlit as st
import db

ESTILO = """<style>
.ini-intro { font-size: 1.05rem; color: var(--k-txt); max-width: 820px; line-height: 1.65; }
.ini-titulo { font-size: 1.35rem; font-weight: 700; color: var(--k-titulo); margin: 28px 0 4px; }
.ini-titulo::after { content: ""; display: block; width: 48px; height: 3px; background: var(--k-oro); margin-top: 8px; }
.ini-sub { color: var(--k-muted); font-size: .92rem; margin: 8px 0 14px; }
.ini-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 14px; margin-top: 10px; }
.ini-card { background: var(--k-surf); border: 1px solid var(--k-borde); border-radius: 12px; padding: 18px; }
.ini-card .num { display: inline-flex; align-items: center; justify-content: center; width: 28px; height: 28px;
    border-radius: 50%; background: var(--k-btn); color: #FFFFFF; font-weight: 700; font-size: .85rem; }
.ini-card h4 { margin: 10px 0 6px; font-size: 1rem; color: var(--k-txt); }
.ini-card p { margin: 0; font-size: .9rem; color: var(--k-muted); line-height: 1.55; }
.ini-cifras { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-top: 18px; }
.ini-cifra { background: var(--k-tinte); border: 1px solid var(--k-borde); border-radius: 12px; padding: 14px 16px; }
.ini-cifra b { display: block; font-size: 1.5rem; color: var(--k-titulo); }
.ini-cifra span { font-size: .85rem; color: var(--k-txt); }
.ini-nombre { background: var(--k-tinte-oro); border-left: 4px solid var(--k-oro); border-radius: 8px;
    padding: 14px 18px; color: var(--k-txt); font-size: .94rem; line-height: 1.6; margin-top: 18px; }
.ini-nombre b { color: var(--k-txt); }
</style>"""

PASOS = [
    ("Preguntar a Khipu",
     "Pregunta si hay un componente, dónde está y cuántos quedan. También puedes enviar la foto de "
     "una pieza o el PDF de tu guía de laboratorio."),
    ("Armar un proyecto",
     "Describe tu idea y Khipu arma la lista de materiales, revisa el stock real y propone "
     "equivalentes cuando algo se agotó."),
    ("Reservar Laboratorio",
     "Elige una franja libre en el calendario, junta a tu grupo y pide los componentes. "
     "El líder firma la solicitud con un código que llega a su correo UNMSM."),
    ("Compra y Venta",
     "Publica los componentes que ya no usas o encuentra los que te faltan entre estudiantes "
     "de la facultad. Cada publicación la revisa el encargado."),
]

PREGUNTAS = [
    ("¿Necesito crear una cuenta?",
     "No. Puedes preguntar y armar proyectos sin registrarte. Solo al reservar un laboratorio o "
     "publicar en Compra y Venta se pide tu correo @unmsm.edu.pe, al que llega un código de 6 "
     "dígitos para confirmar que eres tú."),
    ("¿El stock que muestra Khipu es real?",
     "Sí. La inteligencia artificial no inventa cantidades: el stock y la ubicación salen siempre "
     "del inventario del almacén. Cuando identifica una pieza por foto, te dice qué tan seguro "
     "está (alta, media o baja) antes de buscarla."),
    ("¿Qué pasa si el componente que necesito está agotado?",
     "Khipu te muestra equivalentes verificados por estudiantes de Electrónica, con su stock y "
     "las diferencias que debes tener en cuenta, por ejemplo un pinout distinto."),
    ("¿Puedo llevarme los componentes a mi casa?",
     "No. Los componentes del almacén se usan dentro del laboratorio, durante la franja que "
     "reservaste. Por eso se piden junto con la reserva."),
    ("¿Cómo funciona la reserva de laboratorio?",
     "Las reservas son por franjas de 2 horas, de lunes a sábado entre las 08:00 y las 20:00. "
     "Se necesitan al menos 2 estudiantes; el de la primera fila es el líder y firma la "
     "solicitud. El calendario solo te deja elegir franjas libres, sin cruces con clases."),
    ("¿Cómo sé si aceptaron mi solicitud?",
     "El encargado la revisa y el líder recibe un correo con la respuesta. También puedes "
     "consultarla en Reservar Laboratorio → Consultar mi solicitud, con el código LAB- o con tu "
     "código de alumno."),
    ("¿Qué es la firma y el sello de una solicitud?",
     "La firma es el código que confirma que el líder es quien dice ser. El sello es una huella "
     "digital (SHA-256) de la solicitud: si alguien la modifica después, el encargado ve que el "
     "sello no coincide."),
    ("¿Khipu cobra o interviene en las ventas?",
     "No. Compra y Venta solo pone en contacto a los estudiantes por correo o WhatsApp. El "
     "precio y la entrega se acuerdan directamente entre ustedes."),
    ("¿Funciona en el celular?",
     "Sí. Se abre desde el navegador, sin instalar nada, y puedes tomar la foto de un componente "
     "con la cámara del celular."),
]


def _titulo(texto: str, sub: str = ""):
    st.markdown(f"<div class='ini-titulo'>{texto}</div>" + (f"<div class='ini-sub'>{sub}</div>" if sub else ""),
                unsafe_allow_html=True)


def mostrar():
    st.markdown(ESTILO, unsafe_allow_html=True)

    n_comp, n_labs = len(db.listar_componentes()), len(db.listar_laboratorios())

    # Qué es Khipu
    _titulo("¿Qué es Khipu?")
    st.markdown(
        "<div class='ini-intro'>Khipu es el asistente del almacén y los laboratorios de la FIEE. "
        "Reúne en un solo lugar lo que antes requería ir al almacén a preguntar, revisar horarios "
        "pegados en la puerta y llenar solicitudes en papel: consultar qué componentes hay, "
        "planificar un proyecto con la ayuda de la inteligencia artificial, reservar un "
        "laboratorio con tu grupo y conseguir piezas entre compañeros.</div>"
        "<div class='ini-cifras'>"
        f"<div class='ini-cifra'><b>{n_comp}</b><span>componentes en el catálogo del almacén</span></div>"
        f"<div class='ini-cifra'><b>{n_labs}</b><span>laboratorios que puedes reservar</span></div>"
        "<div class='ini-cifra'><b>2 horas</b><span>por franja, de lunes a sábado</span></div>"
        "<div class='ini-cifra'><b>0 papeles</b><span>solicitudes firmadas con tu correo UNMSM</span></div>"
        "</div>"
        "<div class='ini-nombre'><b>¿Por qué «Khipu»?</b> Los khipus eran cuerdas con nudos que "
        "los incas usaban para llevar la cuenta de sus almacenes y recursos. Nos pareció el "
        "nombre justo para una herramienta que lleva la cuenta del almacén de la facultad.</div>",
        unsafe_allow_html=True)

    # Cómo funciona
    _titulo("¿Cómo funciona?", "Cuatro herramientas: ábrelas desde el menú de la izquierda.")
    tarjetas = "".join(f"<div class='ini-card'><span class='num'>{i}</span><h4>{t}</h4><p>{d}</p></div>"
                       for i, (t, d) in enumerate(PASOS, 1))
    st.markdown(f"<div class='ini-grid' lang='es'>{tarjetas}</div>", unsafe_allow_html=True)

    # Preguntas frecuentes
    _titulo("Preguntas frecuentes")
    for pregunta, respuesta in PREGUNTAS:
        with st.expander(pregunta):
            st.markdown(respuesta)
