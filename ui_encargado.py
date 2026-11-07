"""ui_encargado.py - pestaña Encargado, protegida con clave (dueño: P3)."""
import os
import streamlit as st
import pandas as pd
import db, correo
from config_ia import valor


def mostrar():
    clave = st.text_input("Clave del encargado", type="password", key="clave_enc")
    if clave != valor("CLAVE_ENCARGADO", "fiee2026"):
        st.info("🔐 Solo para el encargado de almacén y laboratorios.")
        return
    _resumen_en_vivo()
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


@st.fragment(run_every="5s")
def _resumen_en_vivo():
    """Se actualiza solo cada 5 s: si llega una solicitud nueva, recarga el panel."""
    pendientes = len(db.listar_solicitudes("pendiente"))
    antes = st.session_state.get("pendientes_vistos")
    st.session_state.pendientes_vistos = pendientes
    c1, c2, c3 = st.columns(3)
    c1.metric("⏳ Pendientes", pendientes)
    c2.metric("✅ Aceptadas", len(db.listar_solicitudes("aceptada")))
    c3.metric("🔴 Agotados", len(db.demanda()["agotados"]))
    if antes is not None and pendientes > antes:
        st.session_state.aviso = "🔔 Llegó una nueva solicitud de laboratorio"
        st.rerun()                                  # actualiza la lista de solicitudes


def _solicitudes():
    estado = st.radio("Ver", ["pendiente", "aceptada", "rechazada", "finalizada"],
                      horizontal=True, format_func=str.capitalize)
    solicitudes = db.listar_solicitudes(estado)
    if not solicitudes:
        st.caption("No hay solicitudes en este estado.")
    for s in solicitudes:
        with st.expander(f"{s['codigo']} · {s['lab_nombre']} · {s['fecha']} {s['inicio']}–{s['fin']}"):
            st.write(f"**Motivo:** {s['motivo']}")
            if s.get("huella"):
                if db.huella_valida(s):
                    st.success(f"🔏 Firma válida · {s.get('verificacion')} · sello `{s['huella'][:16]}…`")
                else:
                    st.error("⚠️ El sello digital NO coincide: los datos fueron alterados.")
            else:
                st.warning("Sin firma: solicitud no verificada.")
            st.dataframe(pd.DataFrame(s["estudiantes"]), hide_index=True)
            st.dataframe(pd.DataFrame(s["items"]), hide_index=True)
            nota = st.text_input("Nota para los estudiantes (opcional)", key=f"nota_{s['codigo']}")
            c1, c2, c3 = st.columns(3)
            if estado == "pendiente" and c1.button("Aceptar", key=f"a_{s['codigo']}"):
                db.cambiar_estado(s["codigo"], "aceptada", nota); _avisar(s["codigo"]); st.rerun()
            if estado == "pendiente" and c2.button("Rechazar", key=f"r_{s['codigo']}"):
                db.cambiar_estado(s["codigo"], "rechazada", nota); _avisar(s["codigo"]); st.rerun()
            if estado == "aceptada" and c3.button("Finalizada", key=f"f_{s['codigo']}"):
                db.cambiar_estado(s["codigo"], "finalizada", nota); st.rerun()


def _avisar(codigo: str):
    """Avisa al líder por correo que su solicitud cambió de estado."""
    try:
        st.session_state.aviso = f"📧 Avisamos por correo a {correo.avisar(codigo)}"
    except Exception as e:
        st.session_state.aviso = f"Estado actualizado (sin correo: {e})"


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
