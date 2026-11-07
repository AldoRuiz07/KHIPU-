"""ui_proyecto.py - pestaña Mi proyecto (dueño: P3)."""
import streamlit as st
import pandas as pd
import bom, ia_proyecto, lista

COLORES = {"OK": "#1B8A4B", "FALTA": "#B7791F", "NO EXISTE": "#C62828"}


def mostrar():
    idea = st.text_area("¿Qué proyecto tienes en mente?",
                        placeholder="Robot seguidor de línea con Arduino y dos motores DC")
    if st.button("Armar mi lista de componentes", type="primary"):
        if not idea.strip():
            st.warning("Describe tu proyecto primero.")
        else:
            with st.spinner("Pensando el proyecto y revisando el stock..."):
                try:
                    datos = ia_proyecto.proyecto_a_bom(idea)
                    st.session_state.bom = bom.cruzar_bom(datos["componentes"])
                    st.session_state.tips = datos["tips"]
                except Exception as e:
                    st.error(f"No se pudo generar la lista: {e}")
    if "bom" not in st.session_state:
        return
    st.info("Punto de partida generado por IA: verifica valores y pinout con el datasheet.")
    df = pd.DataFrame(st.session_state.bom).drop(columns=["alt_codigo"])
    st.dataframe(df.style.map(lambda v: f"color: {COLORES.get(v, 'inherit')}; font-weight: 600"
                              if v in COLORES else "", subset=["estado"]), hide_index=True)
    if st.session_state.get("tips"):
        st.markdown("**Tips:**\n" + "\n".join(f"- {t}" for t in st.session_state.tips))
    if st.button("Agregar a Mi lista lo disponible (y sus equivalentes)"):
        n = 0
        for f in st.session_state.bom:
            codigo = f["en_almacen"] if f["estado"] == "OK" else f["alt_codigo"]
            if codigo:
                lista.agregar(st.session_state.mi_lista, codigo, f["cantidad"], origen="proyecto")
                n += 1
        st.session_state.aviso = f"Agregué {n} componentes a Mi lista. Resérvalos en Laboratorio."
        st.rerun()
