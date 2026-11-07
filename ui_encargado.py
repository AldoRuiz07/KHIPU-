"""ui_encargado.py - pestaña Encargado, protegida con clave (dueño: P3)."""
import os
import streamlit as st
import pandas as pd
import db


def mostrar():
    clave = st.text_input("Clave del encargado", type="password", key="clave_enc")
    if clave != os.getenv("CLAVE_ENCARGADO", "fiee2026"):
        st.info("Solo para el encargado de almacén y laboratorios.")
        return
    sol, comp, labs, dem = st.tabs(["Solicitudes", "Componentes", "Laboratorios", "Demanda"])
    with sol:
        _solicitudes()
    with comp:
        _editar("componentes", db.listar_componentes())
    with labs:
        st.markdown("**Laboratorios**")
        _editar("laboratorios", db.listar_laboratorios())
        st.markdown("**Horario de clases** (bloquea esas franjas cada semana)")
        _editar("horario_clases", db.listar_horario())
    with dem:
        _demanda()


def _solicitudes():
    estado = st.radio("Ver", ["pendiente", "aceptada", "rechazada", "finalizada"],
                      horizontal=True, format_func=str.capitalize)
    solicitudes = db.listar_solicitudes(estado)
    if not solicitudes:
        st.caption("No hay solicitudes en este estado.")
    for s in solicitudes:
        with st.expander(f"{s['codigo']} · {s['lab_nombre']} · {s['fecha']} {s['inicio']}–{s['fin']}"):
            st.write(f"**Motivo:** {s['motivo']}")
            st.dataframe(pd.DataFrame(s["estudiantes"]), hide_index=True)
            st.dataframe(pd.DataFrame(s["items"]), hide_index=True)
            nota = st.text_input("Nota para los estudiantes (opcional)", key=f"nota_{s['codigo']}")
            c1, c2, c3 = st.columns(3)
            if estado == "pendiente" and c1.button("Aceptar", key=f"a_{s['codigo']}"):
                db.cambiar_estado(s["codigo"], "aceptada", nota); st.rerun()
            if estado == "pendiente" and c2.button("Rechazar", key=f"r_{s['codigo']}"):
                db.cambiar_estado(s["codigo"], "rechazada", nota); st.rerun()
            if estado == "aceptada" and c3.button("Finalizada", key=f"f_{s['codigo']}"):
                db.cambiar_estado(s["codigo"], "finalizada", nota); st.rerun()


def _editar(tabla: str, filas: list[dict]):
    editado = st.data_editor(pd.DataFrame(filas), num_rows="dynamic", hide_index=True,
                             key=f"editor_{tabla}", use_container_width=True)
    if st.button("Guardar cambios", key=f"guardar_{tabla}"):
        db.reemplazar_tabla(tabla, editado.to_dict("records"))
        st.success("Guardado.")


def _demanda():
    d = db.demanda()
    st.metric("Consultas a Khipu", d["consultas"])
    st.markdown("**Lo más pedido en reservas**")
    st.bar_chart(pd.DataFrame(d["mas_pedidos"]), x="componente", y="unidades") \
        if d["mas_pedidos"] else st.caption("Aún no hay reservas.")
    st.markdown("**Agotados** (para planificar compras)")
    st.dataframe(pd.DataFrame(d["agotados"]), hide_index=True)
