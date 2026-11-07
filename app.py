"""app.py - arma la página: encabezado, modo Estudiante/Encargado y pestañas (dueño: P3).
Ejecutar con: streamlit run app.py"""
import streamlit as st
import db, estilo, ventas, ui_inicio, ui_chat, ui_proyecto, ui_laboratorio, ui_ventas, ui_encargado, ui_nosotros

st.set_page_config(page_title="Khipu - Almacén FIEE", page_icon="assets/icono.png",
                   layout="wide")
estilo.aplicar()                                    # claro u oscuro según el interruptor
db.iniciar()
ventas.iniciar()
if "mi_lista" not in st.session_state:
    st.session_state.mi_lista = []                  # compartida por Preguntar, Armar un proyecto y Reservar
if "vista" not in st.session_state:
    st.session_state.vista = None                   # None = inicio; o la clave de una herramienta
if "aviso" in st.session_state:
    st.toast(st.session_state.pop("aviso"))

# ---- Barra superior: logos + selector de modo + modo oscuro (arriba a la derecha)
izq, der, osc = st.columns([2.6, 1.5, 1], vertical_alignment="center")
with izq:
    estilo.barra_institucional()                     # logos UNMSM + FIEE + Khipu
ETIQUETAS_MODO = {"estudiante": ":material/school: Estudiante", "encargado": ":material/lock: Encargado"}
modo = der.segmented_control("Modo", list(ETIQUETAS_MODO), format_func=ETIQUETAS_MODO.get,
                             default="estudiante", label_visibility="collapsed",
                             key="modo") or "estudiante"
osc.toggle(":material/dark_mode: Oscuro", key="oscuro")

# ================================================================ MODO ENCARGADO
if modo == "encargado":
    estilo.encabezado("Panel del encargado",
                      "Solicitudes de laboratorio, inventario, laboratorios y demanda en tiempo real.")
    ui_encargado.mostrar()
    estilo.pie()
    st.stop()

# ================================================================ MODO ESTUDIANTE
# Herramientas de la barra lateral: clave -> (ícono Material, título, módulo)
VISTAS = {
    "preguntar": (":material/indeterminate_question_box:", "Preguntar a Khipu", ui_chat),
    "proyecto": (":material/assignment:", "Armar un proyecto", ui_proyecto),
    "laboratorio": (":material/memory:", "Reservar Laboratorio", ui_laboratorio),
    "ventas": (":material/storefront:", "Compra y Venta", ui_ventas),
}


def _abrir(vista: str):
    """Abre la herramienta; si ya estaba abierta, vuelve al inicio."""
    st.session_state.vista = None if st.session_state.vista == vista else vista


with st.sidebar:
    st.markdown('<div class="khipu-nav-titulo" style="border-top:0;margin-top:8px">Herramientas</div>',
                unsafe_allow_html=True)
    for clave, (icono, titulo, _) in VISTAS.items():
        st.button(titulo, icon=icono, key=f"vista_{clave}", use_container_width=True,
                  on_click=_abrir, args=(clave,),
                  type="primary" if st.session_state.vista == clave else "secondary")

estilo.encabezado("KHIPU",
                  "Consulta, planifica y reserva: componentes y laboratorios de la FIEE con "
                  "inteligencia artificial, desde la idea de tu proyecto hasta tu reserva.",
                  ["Consulta disponibilidad", "Planifica tu proyecto", "Reserva tu laboratorio"],
                  marca="Almacén y laboratorios · FIEE · UNMSM")

if st.session_state.vista:                          # una herramienta elegida en la barra lateral
    if st.button("← Volver al inicio", key="volver_inicio"):
        st.session_state.vista = None
        st.rerun()
    VISTAS[st.session_state.vista][2].mostrar()
else:                                               # inicio: Inicio, Misión y visión, ¿Por qué nace?, ¿Quiénes somos?
    ui_nosotros.pestanas(inicio=ui_inicio.mostrar)

estilo.pie()
