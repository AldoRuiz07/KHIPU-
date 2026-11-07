"""ui_chat.py - pestaña Preguntar: texto, fotos y PDFs (dueño: P2)."""
import streamlit as st
import ia_chat

TIPOS = ["jpg", "jpeg", "png", "webp", "pdf"]

def mostrar():
    if "mi_lista" not in st.session_state:             # por si se prueba esta pestaña sola
        st.session_state.mi_lista = []
    if "chat" not in st.session_state:                 # una vez por visitante
        st.session_state.chat = ia_chat.nuevo_chat(st.session_state.mi_lista)
        st.session_state.mensajes = []
    st.caption("Pregunta por un componente, sube la **foto** de uno o el **PDF** de tu guía. "
               "Desde el celular, el clip permite tomar la foto con la cámara.")
    for m in st.session_state.mensajes:                # historial (no se borra al cambiar de pestaña)
        with st.chat_message(m["rol"]):
            if m.get("imagen"):
                st.image(m["imagen"], width=220)
            if m.get("archivo"):
                st.caption(f"Archivo adjunto: {m['archivo']}")
            st.markdown(m["texto"])

    entrada = st.chat_input("Ej: ¿hay LM358? · ¿qué uso si no hay 2N2222?",
                            accept_file=True, file_type=TIPOS)
    if not entrada:
        return
    texto = entrada.text or ""
    antes = len(st.session_state.mi_lista)
    archivos, msg = [], {"rol": "user", "texto": texto}
    for f in entrada.files:
        datos = f.getvalue()
        archivos.append((datos, f.type))
        if f.type.startswith("image/"):
            msg["imagen"] = datos
        else:
            msg["archivo"] = f.name
    st.session_state.mensajes.append(msg)
    with st.chat_message("user"):
        if msg.get("imagen"):
            st.image(msg["imagen"], width=220)
        if msg.get("archivo"):
            st.caption(f"Archivo adjunto: {msg['archivo']}")
        st.markdown(texto)
    with st.chat_message("assistant"):
        with st.spinner("Revisando el almacén..."):
            try:
                respuesta = ia_chat.preguntar(st.session_state.chat, texto, archivos)
            except Exception:
                try:                                   # plan B
                    respuesta = ia_chat.preguntar_simple(texto, archivos)
                except Exception:
                    respuesta = "No pude conectarme con la IA. Intenta de nuevo en unos segundos."
        st.markdown(respuesta)
    st.session_state.mensajes.append({"rol": "assistant", "texto": respuesta})
    if len(st.session_state.mi_lista) != antes:
        st.session_state.aviso = "Khipu agregó componentes a Mi lista."
        st.rerun()                                     # refresca la barra lateral


if __name__ == "__main__":       # para probar esta pestaña sola: streamlit run ui_chat.py
    st.set_page_config(page_title="Khipu - Preguntar", layout="wide")
    if "aviso" in st.session_state:
        st.toast(st.session_state.pop("aviso"))
    mostrar()
    st.sidebar.write("Mi lista:", st.session_state.mi_lista)
