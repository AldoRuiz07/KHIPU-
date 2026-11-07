"""ui_ventas.py - pestaña Compra y venta entre estudiantes (dueño: P1)."""
import hashlib, secrets, time
from datetime import datetime
from urllib.parse import quote
import streamlit as st
import correo, ventas

MAX_FOTO = 2 * 1024 * 1024          # 2 MB


def mostrar():
    st.caption("Compra y vende componentes entre estudiantes de la FIEE. Cada publicación se confirma "
               "con tu correo UNMSM y la revisa el encargado antes de aparecer.")
    ver, publicar, mias = st.tabs(["Ver publicaciones", "Publicar", "Mis publicaciones"])
    with ver:
        _ver()
    with publicar:
        _publicar()
    with mias:
        _mis_publicaciones()


# ------------------------------------------------------------------ ver
def _ver():
    texto = st.text_input("Buscar", placeholder="Arduino, sensor, motor…", key="buscar_venta")
    pubs = ventas.listar("publicada", texto)
    if not pubs:
        st.info("Todavía no hay publicaciones aprobadas." if not texto else "No encontramos nada con esa búsqueda.")
        return
    for i in range(0, len(pubs), 3):
        for col, p in zip(st.columns(3), pubs[i:i + 3]):
            with col.container(border=True):
                if p["foto"]:
                    st.image(p["foto"], use_container_width=True)
                st.markdown(f"**{p['titulo']}**")
                st.markdown(f"### S/ {p['precio']:.2f}")
                st.caption(f"{p['cantidad']} unid. · {p['condicion']} · {p['nombre']}")
                if p["descripcion"]:
                    st.write(p["descripcion"])
                asunto = quote(f"Khipu: {p['titulo']}")
                c1, c2 = st.columns(2)
                c1.link_button("Correo", f"mailto:{p['correo']}?subject={asunto}",
                               use_container_width=True)
                if p["whatsapp"]:
                    msg = quote(f"Hola {p['nombre']}, vi tu publicación en Khipu: {p['titulo']}")
                    c2.link_button("WhatsApp", f"https://wa.me/51{p['whatsapp']}?text={msg}",
                                   use_container_width=True)
    st.caption("Khipu solo publica los avisos: el trato es entre estudiantes. "
               "Recomendamos hacer la entrega dentro de la universidad.")


# ------------------------------------------------------------------ publicar
def _publicar():
    if st.session_state.get("pub_creada"):
        st.success(f"Tu publicación **{st.session_state.pub_creada}** quedó registrada. "
                   "El encargado la revisará y te avisaremos por correo cuando esté visible.")
        if st.button("Publicar otra cosa"):
            st.session_state.pop("pub_creada"); st.rerun()
        return
    if st.session_state.get("pub_firma"):
        _paso_firma()
        return

    c1, c2, c3 = st.columns([3, 1, 1])
    titulo = c1.text_input("¿Qué vendes?", placeholder="Arduino Uno R3", key="v_titulo")
    cantidad = c2.number_input("Cantidad", min_value=1, step=1, value=1, key="v_cant")
    precio = c3.number_input("Precio por unidad (S/)", min_value=0.0, step=0.5, value=0.0,
                             format="%.2f", key="v_precio")
    condicion = st.selectbox("Estado", ventas.CONDICION, key="v_cond")
    descripcion = st.text_area("Descripción (opcional)", key="v_desc",
                               placeholder="Incluye cable USB. Probado en el curso de Microcontroladores.")
    foto = st.file_uploader("Foto (opcional, máx. 2 MB)", type=["jpg", "jpeg", "png", "webp"], key="v_foto")
    st.markdown("**Tus datos de contacto**")
    d1, d2 = st.columns(2)
    nombre = d1.text_input("Nombre y apellido", key="v_nombre")
    codigo_alumno = d2.text_input("Código de alumno", key="v_cod")
    e1, e2 = st.columns(2)
    correo_ = e1.text_input("Correo @unmsm.edu.pe", key="v_correo")
    whatsapp = e2.text_input("WhatsApp (opcional, 9 dígitos)", key="v_wsp")
    acepto = st.checkbox("Confirmo que lo que vendo es mío y que el trato es entre estudiantes.",
                         key="v_acepto")

    if st.button("Continuar y confirmar con mi correo", type="primary"):
        if not acepto:
            st.error("Marca la casilla de confirmación para continuar.")
            return
        if foto is not None and foto.size > MAX_FOTO:
            st.error("La foto pesa más de 2 MB. Prueba con una más liviana.")
            return
        try:
            ventas.validar(titulo, cantidad, precio, nombre, codigo_alumno, correo_, whatsapp)
        except ValueError as e:
            st.error(str(e))
            return
        st.session_state.pub_firma = {
            "datos": dict(titulo=titulo, cantidad=cantidad, precio=precio, condicion=condicion,
                          descripcion=descripcion, nombre=nombre, codigo_alumno=codigo_alumno,
                          correo=correo_.strip(), whatsapp=whatsapp,
                          foto=foto.getvalue() if foto else None, foto_tipo=foto.type if foto else "")}
        if _enviar_codigo():
            st.rerun()


def _hash(c: str) -> str:
    return hashlib.sha256(c.encode()).hexdigest()


def _enviar_codigo() -> bool:
    f = st.session_state.pub_firma
    codigo6 = f"{secrets.randbelow(10**6):06d}"
    f.update(hash=_hash(codigo6), vence=time.time() + 600, intentos=0, demo=None)
    try:
        with st.spinner("Enviando código de verificación..."):
            correo.enviar_codigo(f["datos"]["correo"], f["datos"]["nombre"], codigo6,
                                 para="confirmar tu publicación de venta")
    except Exception as e:
        if correo.modo_demo():
            f["demo"] = codigo6
        else:
            st.session_state.pop("pub_firma")
            st.error(f"No pudimos enviar el código ({e}). Intenta de nuevo.")
            return False
    return True


def _paso_firma():
    f = st.session_state.pub_firma
    st.markdown("### Verificación de identidad")
    st.write(f"Te enviamos un código de 6 dígitos a **{f['datos']['correo']}**.")
    if f.get("demo"):
        st.warning(f"Modo demostración (no se pudo enviar el correo): el código es **{f['demo']}**")
    codigo6 = st.text_input("Código de verificación", max_chars=6, key="v_codigo6")
    c1, c2, c3 = st.columns(3)
    if c1.button("Confirmar publicación", type="primary"):
        if time.time() > f["vence"]:
            st.error("El código venció. Toca **Reenviar código**.")
        elif _hash(codigo6.strip()) != f["hash"]:
            f["intentos"] += 1
            if f["intentos"] >= 5:
                st.session_state.pop("pub_firma")
                st.error("Demasiados intentos. Vuelve a llenar la publicación.")
            else:
                st.error(f"Código incorrecto. Te quedan {5 - f['intentos']} intentos.")
        else:
            ahora = datetime.now().strftime("%d/%m/%Y %H:%M")
            codigo = ventas.crear(**f["datos"],
                                  verificacion=f"Correo {f['datos']['correo']} verificado el {ahora}")
            st.session_state.pop("pub_firma")
            st.session_state.pub_creada = codigo
            st.session_state.aviso = "Publicación enviada para revisión"
            st.rerun()
    if c2.button("Reenviar código", key="v_reenviar"):
        if _enviar_codigo():
            st.toast("Te enviamos un código nuevo.")
    if c3.button("Cancelar", key="v_cancelar"):
        st.session_state.pop("pub_firma")
        st.rerun()


# ------------------------------------------------------------------ mis publicaciones
ICONO = {"pendiente": "En revisión", "publicada": "Publicada",
         "rechazada": "Rechazada", "vendida": "Vendida"}


def _mis_publicaciones():
    codigo_alumno = st.text_input("Tu código de alumno", key="v_mis")
    if not codigo_alumno:
        return
    pubs = ventas.de_alumno(codigo_alumno)
    if not pubs:
        st.info("No tienes publicaciones.")
        return
    for p in pubs:
        with st.container(border=True):
            st.markdown(f"**{p['titulo']}** · S/ {p['precio']:.2f} · {p['cantidad']} unid. — "
                        f"{ICONO[p['estado']]}")
            if p["nota"]:
                st.caption(f"Nota del encargado: {p['nota']}")
    st.markdown("**¿Ya vendiste algo?**")
    c1, c2 = st.columns([2, 1], vertical_alignment="bottom")
    cod_pub = c1.text_input("Código de la publicación (te llegó por correo, PUB-XXXX)", key="v_pub")
    if c2.button("Marcar como vendida"):
        if ventas.marcar_vendida(cod_pub, codigo_alumno):
            st.success("La publicación se marcó como vendida.")
        else:
            st.error("Revisa el código: debe ser una publicación tuya y que esté publicada.")
