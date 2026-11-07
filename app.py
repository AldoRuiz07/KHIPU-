"""app.py - arma la página: logo, Mi lista y las 4 pestañas (dueño: P3).
Ejecutar con: streamlit run app.py"""
import streamlit as st
import db, lista, ui_chat, ui_proyecto, ui_laboratorio, ui_encargado

st.set_page_config(page_title="Khipu - Almacén FIEE", page_icon="assets/icono.png",
                   layout="wide")
db.iniciar()
if "mi_lista" not in st.session_state:
    st.session_state.mi_lista = []                  # compartida por todas las pestañas
if "aviso" in st.session_state:
    st.toast(st.session_state.pop("aviso"))

# ---- Barra lateral: Mi lista
with st.sidebar:
    st.image("assets/logo.png")
    st.subheader("Mi lista")
    if not st.session_state.mi_lista:
        st.caption("Vacía. Lo que te recomiende el chat o Mi proyecto aparecerá aquí.")
    for item in list(st.session_state.mi_lista):
        c1, c2 = st.columns([4, 1])
        c1.write(f"**{item['codigo']}** × {item['cantidad']}")
        if c2.button("✕", key=f"quitar_{item['codigo']}"):
            lista.quitar(st.session_state.mi_lista, item["codigo"]); st.rerun()

st.image("assets/logo.png", width=300)
pestanas = st.tabs(["Preguntar", "Mi proyecto", "Laboratorio", "Encargado"])
for pestana, modulo in zip(pestanas, [ui_chat, ui_proyecto, ui_laboratorio, ui_encargado]):
    with pestana:
        modulo.mostrar()
