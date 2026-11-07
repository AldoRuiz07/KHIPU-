"""app.py - arma la página: encabezado, modo Estudiante/Encargado y pestañas (dueño: P3).
Ejecutar con: streamlit run app.py"""
import streamlit as st
import db, lista, estilo, ui_chat, ui_proyecto, ui_laboratorio, ui_encargado

st.set_page_config(page_title="Khipu - Almacén FIEE", page_icon="assets/icono.png",
                   layout="wide")
estilo.aplicar()
db.iniciar()
if "mi_lista" not in st.session_state:
    st.session_state.mi_lista = []                  # compartida por todas las pestañas
if "aviso" in st.session_state:
    st.toast(st.session_state.pop("aviso"))

# ---- Barra superior: logo + selector de modo (arriba a la derecha)
izq, der = st.columns([3, 1.3], vertical_alignment="center")
with izq:
    estilo.barra_institucional()                     # logos UNMSM + FIEE
modo = der.segmented_control("Modo", ["🎓 Estudiante", "🔐 Encargado"],
                             default="🎓 Estudiante", label_visibility="collapsed",
                             key="modo") or "🎓 Estudiante"

# ================================================================ MODO ENCARGADO
if modo == "🔐 Encargado":
    estilo.encabezado("Panel del encargado",
                      "Solicitudes de laboratorio, inventario, laboratorios y demanda en tiempo real.")
    ui_encargado.mostrar()
    estilo.pie()
    st.stop()

# ================================================================ MODO ESTUDIANTE
n = sum(i["cantidad"] for i in st.session_state.mi_lista)
estilo.encabezado("Consulta, planifica y reserva",
                  f"Componentes y laboratorios de la FIEE con IA · 🛒 Mi lista: {n} unidades",
                  ["Pregunta o sube una foto/PDF", "Arma tu proyecto", "Reserva tu laboratorio"])

with st.sidebar:                                    # Mi lista
    st.markdown("### 🛒 Mi lista")
    if not st.session_state.mi_lista:
        st.caption("Vacía. Lo que te recomiende el chat o Mi proyecto aparecerá aquí.")
    for item in list(st.session_state.mi_lista):
        c1, c2 = st.columns([4, 1], vertical_alignment="center")
        c1.markdown(f"**{item['codigo']}** × {item['cantidad']}  \n"
                    f"<span style='font-size:.8rem;color:#5B6B82'>{item.get('nombre', '')}</span>",
                    unsafe_allow_html=True)
        if c2.button("✕", key=f"quitar_{item['codigo']}"):
            lista.quitar(st.session_state.mi_lista, item["codigo"]); st.rerun()
    if st.session_state.mi_lista:
        st.info("Resérvalos en la pestaña **🔬 Laboratorio**.")

pestanas = st.tabs(["💬 Preguntar", "📋 Mi proyecto", "🔬 Laboratorio"])
for pestana, modulo in zip(pestanas, [ui_chat, ui_proyecto, ui_laboratorio]):
    with pestana:
        modulo.mostrar()

estilo.pie()
