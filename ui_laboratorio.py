"""ui_laboratorio.py pestaña Laboratorio: reservar sala + componentes (dueño: P1)."""
import hashlib, secrets, time
from datetime import date, datetime, timedelta
import streamlit as st
import pandas as pd
import db, lista, correo

ESTADO = {"pendiente": "Pendiente", "aceptada": "Aceptada", "rechazada": "Rechazada", "finalizada": "Finalizada"}

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
    _calendario()
    st.markdown("**Fecha y horario**")
    c1, c2 = st.columns(2)
    fecha = c1.date_input("Fecha", min_value=date.today(), format="DD/MM/YYYY", key="lab_fecha")
    franja = c2.selectbox("Horario", db.FRANJAS, format_func=lambda f: f"{f[0]} - {f[1]}", key="lab_franja")
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
        
    preferido = st.session_state.get("lab_preferido")
    indice = next((i for i, l in enumerate(libres) if l["codigo"] == preferido), 0)
    lab = st.radio("Disponibles", libres, index=indice,
                   format_func=lambda l: f"{l['nombre']} ({l['capacidad']} personas)",
                   label_visibility="collapsed")
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

# ------------------------------------------------------------------ calendario semanal
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]
SEMANAS_MAX = 8                                   # cuántas semanas hacia adelante se pueden ver

ESTILO_CALENDARIO = """<style>
.st-key-calendario { background: #FAFBFF; border: 1px solid #E3E8F5 !important; border-radius: 14px; }
.st-key-calendario [data-testid="stHorizontalBlock"] { gap: 6px; flex-wrap: nowrap; }
.st-key-calendario [data-testid="stColumn"] { min-width: 0; }
.st-key-calendario button { min-height: 44px; border-radius: 10px !important; font-size: .82rem;
    padding: 4px 2px; transition: transform .08s ease, box-shadow .12s ease; }
.st-key-calendario [class*="st-key-cal_libre"] button {
    background: #E9F7EF; border: 1px solid #BFE5CC; color: #17633A; }
.st-key-calendario [class*="st-key-cal_libre"] button:hover {
    background: #D4F0DF; border-color: #6CC08D; color: #0F4D2B; transform: translateY(-1px); }
.st-key-calendario [class*="st-key-cal_lleno"] button,
.st-key-calendario [class*="st-key-cal_pasado"] button {
    background: #F3F4F6 !important; border: 1px dashed #E0E2E7 !important; color: #A3A8B3 !important; }
.st-key-calendario [class*="st-key-cal_sel"] button {
    box-shadow: 0 0 0 3px rgba(201,162,39,.55); transform: translateY(-1px); font-weight: 600; }
.cal-dia { text-align: center; padding: 6px 0 4px; border-radius: 10px; line-height: 1.15; }
.cal-dia b { display: block; font-size: .8rem; color: #0B1F66; }
.cal-dia span { font-size: .72rem; color: #6B7280; }
.cal-dia.hoy { background: #0B1F66; }
.cal-dia.hoy b, .cal-dia.hoy span { color: #FFFFFF; }
.cal-hora { font-size: .75rem; color: #6B7280; text-align: right; padding-top: 12px; white-space: nowrap; }
.cal-leyenda { display: flex; gap: 14px; flex-wrap: wrap; font-size: .78rem; color: #4B5563; margin: 2px 0 6px; }
.cal-leyenda i { display: inline-block; width: 12px; height: 12px; border-radius: 4px;
    margin-right: 5px; vertical-align: -1px; }
.cal-elegido { background: #EEF2FF; border-left: 4px solid #0B1F66; border-radius: 8px;
    padding: 8px 12px; font-size: .88rem; color: #0B1F66; margin-top: 6px; }
@media (max-width: 640px) {
  .st-key-calendario button { font-size: .66rem; min-height: 38px; }
  .cal-hora { font-size: .62rem; } .cal-dia b { font-size: .68rem; } .cal-dia span { font-size: .6rem; }
}
</style>"""

def _ahora_lima() -> datetime:
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("America/Lima"))     # el servidor está en otra zona horaria
    except Exception:
        return datetime.now()

def _calendario():
    """Semana de lunes a sábado con las franjas libres. Al tocar una, se llena el formulario."""
    st.markdown(ESTILO_CALENDARIO, unsafe_allow_html=True)
    ahora = _ahora_lima()
    hoy, hora = ahora.date(), ahora.strftime("%H:%M")
    if "cal_semana" not in st.session_state:
        st.session_state.cal_semana = 0
    # Sábado o domingo: la semana actual casi terminó, así que se abre la siguiente
    base = hoy - timedelta(days=hoy.weekday()) + timedelta(weeks=1 if hoy.weekday() >= 5 else 0)
    minimo = -1 if hoy.weekday() == 5 else 0              # el sábado aún se puede volver a hoy
    lunes = base + timedelta(weeks=st.session_state.cal_semana)
    sabado = lunes + timedelta(days=5)
    elegido_fecha = st.session_state.get("lab_fecha")
    elegido_franja = st.session_state.get("lab_franja")

    with st.container(border=True, key="calendario"):
        st.markdown("**Horarios libres de los laboratorios**")
        labs = db.listar_laboratorios()
        nombres = {l["codigo"]: l["nombre"] for l in labs}
        opcion = st.selectbox("Laboratorio", ["Todos"] + list(nombres), key="cal_lab",
                              format_func=lambda c: "Todos los laboratorios" if c == "Todos" else nombres[c])

        # Navegación por semanas
        n1, n2, n3 = st.columns([1, 2, 1], vertical_alignment="center")
        if n1.button("‹ Anterior", key="cal_ant", use_container_width=True,
                     disabled=st.session_state.cal_semana <= minimo):
            st.session_state.cal_semana -= 1
            st.rerun()
        if lunes.month == sabado.month:
            rango = f"{lunes.day} al {sabado.day} de {MESES[lunes.month - 1]}"
        else:
            rango = f"{lunes.day} de {MESES[lunes.month - 1]} al {sabado.day} de {MESES[sabado.month - 1]}"
        n2.markdown(f"<div style='text-align:center;font-weight:600;color:#0B1F66'>Semana del {rango}</div>",
                    unsafe_allow_html=True)
        if n3.button("Siguiente ›", key="cal_sig", use_container_width=True,
                     disabled=st.session_state.cal_semana >= SEMANAS_MAX):
            st.session_state.cal_semana += 1
            st.rerun()

        st.markdown("<div class='cal-leyenda'>"
                    "<span><i style='background:#E9F7EF;border:1px solid #BFE5CC'></i>Libre</span>"
                    "<span><i style='background:#0B1F66'></i>Tu elección</span>"
                    "<span><i style='background:#F3F4F6;border:1px dashed #D1D5DB'></i>Ocupado o pasado</span>"
                    "</div>", unsafe_allow_html=True)

        # Cabecera con los días
        cabecera = st.columns([0.9] + [1] * 6)
        for j in range(6):
            d = lunes + timedelta(days=j)
            clase = "cal-dia hoy" if d == hoy else "cal-dia"
            cabecera[j + 1].markdown(f"<div class='{clase}'><b>{DIAS[j][:3]}</b><span>{d.day:02d}/{d.month:02d}</span></div>",
                                     unsafe_allow_html=True)

        # Una fila por franja de 2 horas
        for inicio, fin in db.FRANJAS:
            fila = st.columns([0.9] + [1] * 6)
            fila[0].markdown(f"<div class='cal-hora'>{inicio}<br>{fin}</div>", unsafe_allow_html=True)
            for j in range(6):
                d = lunes + timedelta(days=j)
                pasado = d < hoy or (d == hoy and inicio <= hora)
                estado = db.estado_laboratorios(d.isoformat(), inicio, fin)
                if opcion != "Todos":
                    estado = [l for l in estado if l["codigo"] == opcion]
                libres = [l for l in estado if not l["ocupado"]]
                seleccionada = (not pasado and libres and elegido_fecha == d
                                and tuple(elegido_franja or ()) == (inicio, fin))
                if pasado:
                    texto, tipo = "·", "pasado"
                elif not libres:
                    texto, tipo = ("Lleno" if opcion == "Todos" else "Ocupado"), "lleno"
                else:
                    texto = (f"{len(libres)} libre" + ("s" if len(libres) > 1 else "")) if opcion == "Todos" else "Libre"
                    tipo = "sel" if seleccionada else "libre"
                if pasado:
                    ayuda = "Esta franja ya pasó"
                elif libres:
                    ayuda = "Libres: " + ", ".join(l["nombre"] for l in libres)
                else:
                    ayuda = "Ocupado: " + "; ".join(l["motivo"] for l in estado if l["ocupado"])
                if fila[j + 1].button(texto, key=f"cal_{tipo}_{d}_{inicio}", disabled=pasado or not libres,
                                      type="primary" if seleccionada else "secondary",
                                      use_container_width=True, help=ayuda):
                    st.session_state.lab_fecha = d
                    st.session_state.lab_franja = (inicio, fin)
                    if opcion != "Todos":
                        st.session_state.lab_preferido = opcion
                    st.rerun()

        if elegido_fecha and elegido_franja and lunes <= elegido_fecha <= sabado:
            st.markdown(f"<div class='cal-elegido'>Elegiste el <b>{DIAS[elegido_fecha.weekday()].lower() if elegido_fecha.weekday() < 6 else 'domingo'} "
                        f"{elegido_fecha.day:02d}/{elegido_fecha.month:02d}</b>, de <b>{elegido_franja[0]} a {elegido_franja[1]}</b>. "
                        "Completa los datos de abajo.</div>", unsafe_allow_html=True)
        else:
            st.caption("Toca una franja libre: la fecha y el horario de abajo se llenan solos.")


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
    st.markdown("### Verificación de identidad")
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
                    st.session_state.ultimo_correo = f"Se envió la confirmación a **{correo.avisar(codigo)}**."
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
        st.caption(f"{s.get('verificacion')} · Sello digital: `{s['huella'][:16]}…`")
    if st.session_state.get("ultimo_correo"):
        st.info(st.session_state.ultimo_correo)
    _, html = correo.contenido(s)
    st.download_button("Descargar comprobante", data=html, file_name=f"Khipu_{codigo}.html",
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
            st.markdown(f"#### {s['codigo']} · {ESTADO[s['estado']]}")
            st.write(f"**{s['lab_nombre']}** — {s['fecha']} · {s['inicio']} - {s['fin']}")
            st.write(f"Motivo: {s['motivo']}")
            if s["nota"]:
                st.info(f"Nota del encargado: {s['nota']}")
            if s["items"]:
                st.dataframe(pd.DataFrame(s["items"]), hide_index=True)
            _, html = correo.contenido(s)
            st.download_button("Descargar comprobante", data=html, file_name=f"Khipu_{s['codigo']}.html",
                               mime="text/html", key=f"dl_{s['codigo']}")
