"""ui_laboratorio.py pestaña Laboratorio: reservar sala + componentes (dueño: P1)."""
import hashlib, secrets, time
from datetime import date, datetime
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
    if st.session_state.get("ultima_solicitud"):
        _comprobante(st.session_state.ultima_solicitud, "dl_nueva")
        if st.button("Hacer otra reserva"):
            st.session_state.pop("ultima_solicitud"); st.session_state.pop("ultimo_correo", None)
            st.rerun()
        return
    if st.session_state.get("firma"):
        _paso_firma()
        return
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
        
    if st.button("Continuar y firmar la solicitud", type="primary"):
        filas = [e for e in estudiantes.to_dict("records")
                 if str(e.get("nombre") or "").strip() and str(e.get("codigo_alumno") or "").strip()]
        correo_lider = str(filas[0].get("correo") or "").strip() if filas else ""
        if filas and not correo_lider.endswith("@unmsm.edu.pe"):
            st.error("El líder (fila 1) debe poner su correo @unmsm.edu.pe: ahí llega el código para firmar.")
            return
        datos = (lab["codigo"], fecha_txt, inicio, fin, motivo, estudiantes.to_dict("records"), pedidos)
        try:
            db.validar_solicitud(*datos)            # revisa todo antes de pedir la firma
        except ValueError as e:
            st.error(str(e))
            return
        st.session_state.firma = {"datos": datos, "correo": correo_lider,
                                  "nombre": str(filas[0]["nombre"]).strip()}
        if _enviar_codigo():
            st.rerun()

# ------------------------------------------------------------------ firma electrónica simple
def _hash(codigo6: str) -> str:
    return hashlib.sha256(codigo6.encode()).hexdigest()

def _enviar_codigo() -> bool:
    """Genera un código de 6 dígitos y lo manda al correo institucional del líder."""
    f = st.session_state.firma
    codigo6 = f"{secrets.randbelow(10**6):06d}"
    f.update(hash=_hash(codigo6), vence=time.time() + 600, intentos=0, demo=None)
    try:
        with st.spinner("Enviando código de verificación..."):
            correo.enviar_codigo(f["correo"], f["nombre"], codigo6)
    except Exception as e:
        if correo.modo_demo():
            f["demo"] = codigo6                     # solo para presentaciones
        else:
            st.session_state.pop("firma")
            st.error(f"No pudimos enviar el código de verificación ({e}). Intenta de nuevo.")
            return False
    return True

def _oculto(c: str) -> str:
    usuario, _, dominio = c.partition("@")
    return usuario[:2] + "•" * max(len(usuario) - 2, 3) + "@" + dominio

def _ahora() -> str:
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("America/Lima")).strftime("%d/%m/%Y %H:%M")
    except Exception:
        return datetime.now().strftime("%d/%m/%Y %H:%M")

def _paso_firma():
    f = st.session_state.firma
    st.markdown("### 🔏 Firma tu solicitud")
    st.write(f"Para evitar que alguien reserve a nombre de otra persona, enviamos un **código de "
             f"6 dígitos** al correo institucional del líder: **{_oculto(f['correo'])}**.")
    if f.get("demo"):
        st.warning(f"Modo demostración (no se pudo enviar el correo): el código es **{f['demo']}**")
    codigo6 = st.text_input("Código de verificación", max_chars=6, placeholder="123456")
    c1, c2, c3 = st.columns(3)
    if c1.button("Firmar y enviar solicitud", type="primary"):
        if time.time() > f["vence"]:
            st.error("El código venció. Toca **Reenviar código**.")
        elif _hash(codigo6.strip()) != f["hash"]:
            f["intentos"] += 1
            if f["intentos"] >= 5:
                st.session_state.pop("firma")
                st.error("Demasiados intentos. Vuelve a llenar la solicitud.")
            else:
                st.error(f"Código incorrecto. Te quedan {5 - f['intentos']} intentos.")
        else:
            verificacion = f"Identidad verificada con código enviado a {f['correo']} el {_ahora()}"
            try:
                codigo = db.crear_solicitud(*f["datos"], verificacion=verificacion)
            except ValueError as e:                 # p. ej. otro grupo tomó el laboratorio
                st.session_state.pop("firma")
                st.error(f"No se pudo guardar: {e}")
                return
            st.session_state.pop("firma")
            st.session_state.mi_lista.clear()
            st.session_state.ultima_solicitud = codigo
            try:
                with st.spinner("Enviando confirmación por correo..."):
                    st.session_state.ultimo_correo = f"📧 Te enviamos la confirmación a **{correo.avisar(codigo)}**."
            except Exception:
                st.session_state.ultimo_correo = ("Guarda tu comprobante o busca tus reservas con tu "
                                                  "código de alumno en *Consultar mi solicitud*.")
            st.rerun()
    if c2.button("Reenviar código"):
        if _enviar_codigo():
            st.toast("Te enviamos un código nuevo.")
    if c3.button("Cancelar"):
        st.session_state.pop("firma")
        st.rerun()

def _comprobante(codigo: str, clave: str):
    """Mensaje de éxito + botón para descargar el comprobante (no se pierde al recargar)."""
    s = db.ver_solicitud(codigo)
    if s is None:
        return
    st.success(f"Solicitud firmada y enviada. Tu código es **{codigo}**. El encargado la revisará.")
    if s.get("huella"):
        st.caption(f"🔏 {s.get('verificacion')} · Sello digital: `{s['huella'][:16]}…`")
    if st.session_state.get("ultimo_correo"):
        st.info(st.session_state.ultimo_correo)
    _, html = correo.contenido(s)
    st.download_button("⬇️ Descargar comprobante", data=html, file_name=f"Khipu_{codigo}.html",
                       mime="text/html", key=clave)

def _consultar():
    texto = st.text_input("Tu código de solicitud (LAB-XXXX) o tu código de alumno",
                          placeholder="LAB-7Q2M  ·  20200001").strip()
    if not texto:
        st.caption("Con tu código de alumno ves todas tus reservas, aunque hayas cerrado la página.")
        return
    if texto.upper().startswith("LAB-"):
        s = db.ver_solicitud(texto)
        solicitudes = [s] if s else []
    else:
        solicitudes = db.solicitudes_de_alumno(texto)
    if not solicitudes:
        st.warning("No encontramos solicitudes con ese código.")
        return
    for s in solicitudes:
        with st.container(border=True):
            st.markdown(f"#### {ICONO[s['estado']]} {s['codigo']} · {s['estado'].capitalize()}")
            st.write(f"**{s['lab_nombre']}** — {s['fecha']} · {s['inicio']} - {s['fin']}")
            st.write(f"Motivo: {s['motivo']}")
            if s["nota"]:
                st.info(f"Nota del encargado: {s['nota']}")
            if s["items"]:
                st.dataframe(pd.DataFrame(s["items"]), hide_index=True)
            _, html = correo.contenido(s)
            st.download_button("⬇️ Comprobante", data=html, file_name=f"Khipu_{s['codigo']}.html",
                               mime="text/html", key=f"dl_{s['codigo']}")
