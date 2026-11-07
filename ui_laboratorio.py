"""ui_laboratorio.py pestaña Laboratorio: reservar sala + componentes (dueño: P1)."""
from datetime import date
import streamlit as st
import pandas as pd
import db, lista, correo

ICONO = {"pendiente": "⏳", "aceptada": "✅", "rechazada": "❌", "finalizada": "🏁"}

def mostrar():
    nueva, consultar = st.tabs(["Nueva reserva", "Consultar mi solicitud"])
    with nueva:
        _nueva_reserva()
    with consultar:
        _consultar()

def _nueva_reserva():
    st.caption("Los componentes solo se usan en laboratorio: reserva una franja de 2 horas y pide lo que necesitas.")
    c1, c2 = st.columns(2)
    fecha = c1.date_input("Fecha", min_value=date.today(), format="DD/MM/YYYY")
    franja = c2.selectbox("Horario", db.FRANJAS, format_func=lambda f: f"{f[0]} - {f[1]}")
    fecha_txt, (inicio, fin) = fecha.isoformat(), franja
    
    # 1. Laboratorios: los ocupados salen tachados
    st.markdown("**1. Elige el laboratorio**")
    labs = db.estado_laboratorios(fecha_txt, inicio, fin)
    for l in labs:
        if l["ocupado"]:
            st.markdown(f"~~{l['nombre']}~~ &nbsp; <span style='color:#C62828'>ocupado: {l['motivo']}</span>", unsafe_allow_html=True)
            
    libres = [l for l in labs if not l["ocupado"]]
    if not libres:
        st.warning("No hay laboratorios libres en esa franja. Prueba otro horario.")
        return
        
    lab = st.radio("Disponibles", libres, format_func=lambda l: f"{l['nombre']} ({l['capacidad']} personas)", label_visibility="collapsed")
    motivo = st.text_input("Motivo", placeholder="Armado del proyecto final de Electrónica I")

    # 2. Estudiantes (mínimo 2)
    st.markdown("**2. Estudiantes (mínimo 2)** · el de la **fila 1 es el líder** y recibe la "
                "confirmación por correo")
    estudiantes = st.data_editor(
        pd.DataFrame([{"nombre": "", "codigo_alumno": "", "correo": ""}] * 2),
        num_rows="dynamic", hide_index=True, key="estudiantes",
        column_config={"nombre": "Apellidos y nombres", "codigo_alumno": "Código",
                       "correo": "Correo @unmsm.edu.pe (obligatorio el líder)"}
    )

    # 3. Componentes: llega lo de Mi lista, con lo disponible en esa franja
    st.markdown("**3. Componentes**")
    disp = db.disponibles_en_franja(fecha_txt, inicio, fin)
    base = [{"codigo": i["codigo"], "cantidad": i["cantidad"]} for i in st.session_state.mi_lista]
    items = st.data_editor(
        pd.DataFrame(base or [{"codigo": None, "cantidad": 1}]),
        num_rows="dynamic", hide_index=True, key=f"items_{len(base)}",
        column_config={"codigo": st.column_config.SelectboxColumn("Componente", options=sorted(disp)),
                       "cantidad": st.column_config.NumberColumn("Cantidad", min_value=1, step=1)}
    )
    
    pedidos = [(r["codigo"], r["cantidad"]) for r in items.to_dict("records") if r["codigo"]]
    if pedidos:
        st.caption("Disponible en esa franja: " + ", ".join(f"{c}: {max(disp.get(c, 0), 0)}" for c, _ in pedidos))
        
    if st.button("Enviar solicitud", type="primary"):
        filas = [e for e in estudiantes.to_dict("records")
                 if str(e.get("nombre") or "").strip() and str(e.get("codigo_alumno") or "").strip()]
        correo_lider = str(filas[0].get("correo") or "").strip() if filas else ""
        if filas and not correo_lider.endswith("@unmsm.edu.pe"):
            st.error("El líder (fila 1) debe poner su correo @unmsm.edu.pe para recibir la confirmación.")
            return
        try:
            codigo = db.crear_solicitud(
                lab["codigo"], fecha_txt, inicio, fin, motivo,
                estudiantes.to_dict("records"), pedidos
            )
        except ValueError as e:
            st.error(str(e))
            return
        st.session_state.mi_lista.clear()
        st.success(f"Solicitud enviada. Tu código es **{codigo}**. El encargado la revisará; "
                   "consulta el estado en la otra pestaña.")
        with st.spinner("Enviando confirmación por correo..."):
            try:
                st.info(f"📧 Te enviamos la confirmación a **{correo.avisar(codigo)}**.")
            except Exception as e:
                st.warning(f"No se pudo enviar el correo ({e}). Guarda tu código: **{codigo}**.")

def _consultar():
    codigo = st.text_input("Código de solicitud (LAB-XXXX)")
    if not codigo:
        return
    s = db.ver_solicitud(codigo)
    if s is None:
        st.warning("No existe esa solicitud.")
        return
    st.markdown(f"### {ICONO[s['estado']]} {s['estado'].capitalize()}")
    st.write(f"**{s['lab_nombre']}** — {s['fecha']} {s['inicio']} - {s['fin']}")
    st.write(f"Motivo: {s['motivo']}")
    if s["nota"]:
        st.info(f"Nota del encargado: {s['nota']}")
    st.dataframe(pd.DataFrame(s["items"]), hide_index=True)