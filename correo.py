"""correo.py - correos de confirmación y de estado de la solicitud (dueño: P1).
Se envían desde una cuenta Gmail del equipo con una 'contraseña de aplicación'.
Configuración (en .env o en Secrets de Streamlit Cloud):
    CORREO_REMITENTE = "khipu.fiee@gmail.com"
    CORREO_CLAVE     = "abcd efgh ijkl mnop"     (contraseña de aplicación de 16 letras)
Si no está configurado, la reserva funciona igual: solo no se envía el correo."""
import os, smtplib, ssl
from email.message import EmailMessage
from html import escape
import db

NAVY, AZUL, AMBAR = "#0B1F3A", "#1E6BFF", "#FFB000"
TITULOS = {"pendiente": "Confirmación de solicitud de laboratorio",
           "aceptada": "Tu reserva de laboratorio fue aceptada",
           "rechazada": "Tu reserva de laboratorio fue rechazada",
           "finalizada": "Tu reserva de laboratorio fue finalizada"}

def _valor(nombre: str) -> str:
    if os.getenv(nombre):
        return os.getenv(nombre)
    try:
        import streamlit as st
        return str(st.secrets.get(nombre, ""))
    except Exception:
        return ""

def modo_demo() -> bool:
    """Si VERIFICACION_DEMO = "si", el código se muestra en pantalla (solo para presentaciones)."""
    return _valor("VERIFICACION_DEMO").strip().lower() in ("si", "sí", "true", "1")

def configurado() -> bool:
    return bool(_valor("CORREO_REMITENTE") and _valor("CORREO_CLAVE"))

def _enviar(destino: str, asunto: str, texto: str, html: str):
    remitente, clave = _valor("CORREO_REMITENTE"), _valor("CORREO_CLAVE").replace(" ", "")
    msg = EmailMessage()
    msg["Subject"], msg["From"], msg["To"] = asunto, f"Khipu FIEE <{remitente}>", destino
    msg.set_content(texto)
    msg.add_alternative(html, subtype="html")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context(),
                          timeout=20) as servidor:
        servidor.login(remitente, clave)
        servidor.send_message(msg)

def contenido(s: dict) -> tuple[str, str]:
    """Arma el correo en texto plano y en HTML a partir de la solicitud."""
    lider = s["estudiantes"][0]
    items = []
    for it in s["items"]:
        comp = db.obtener(it["componente"]) or {}
        items.append((it["componente"], comp.get("nombre", ""), it["cantidad"]))
    titulo = TITULOS.get(s["estado"], "Solicitud de laboratorio")
    nota = f"Nota del encargado: {s['nota']}" if s.get("nota") else ""
    siguiente = {"pendiente": "El encargado revisará tu solicitud. Te avisaremos por este medio.",
                 "aceptada": "Preséntate con tu grupo en el laboratorio a la hora indicada.",
                 "rechazada": "Puedes intentar con otra fecha u horario en Khipu.",
                 }.get(s["estado"], "")
    texto = "\n".join([
        f"Hola {lider['nombre']},", "", titulo, "",
        f"Código de consulta: {s['codigo']}",
        f"Laboratorio: {s['lab_nombre']}",
        f"Fecha y hora: {s['fecha']}, de {s['inicio']} a {s['fin']}",
        f"Motivo: {s['motivo']}",
        "Componentes:" if items else "Componentes: ninguno",
        *[f"  - {c} ({n}) x {q}" for c, n, q in items],
        "Estudiantes:", *[f"  - {e['nombre']} ({e['codigo_alumno']})" for e in s["estudiantes"]],
        "", f"Firma: {s.get('verificacion') or 'sin verificar'}",
        f"Sello digital (SHA-256): {s.get('huella') or '-'}",
        "", nota, siguiente, "", "Khipu · Asistente de Almacén IA · FIEE-UNMSM"])
    filas_items = "".join(
        f"<tr><td style='padding:6px 10px;border-bottom:1px solid #E3E8F1'><b>{escape(c)}</b></td>"
        f"<td style='padding:6px 10px;border-bottom:1px solid #E3E8F1;color:#5B6B82'>{escape(n)}</td>"
        f"<td style='padding:6px 10px;border-bottom:1px solid #E3E8F1;text-align:right'>{q}</td></tr>"
        for c, n, q in items) or "<tr><td style='padding:6px 10px'>Sin componentes</td></tr>"
    estudiantes = "".join(f"<li>{escape(e['nombre'])} ({escape(str(e['codigo_alumno']))})</li>"
                          for e in s["estudiantes"])
    html = f"""<div style="font-family:Arial,sans-serif;max-width:560px;margin:auto;color:{NAVY}">
  <div style="background:{NAVY};color:white;padding:18px 22px;border-radius:12px 12px 0 0">
    <div style="font-size:22px;font-weight:800">Khipu</div>
    <div style="opacity:.8;font-size:13px">Asistente de Almacén IA · FIEE-UNMSM</div></div>
  <div style="border:1px solid #E3E8F1;border-top:none;padding:20px 22px;border-radius:0 0 12px 12px">
    <p>Hola <b>{escape(lider['nombre'])}</b>,</p>
    <h2 style="font-size:18px;margin:4px 0 14px">{escape(titulo)}</h2>
    <div style="background:#F2F5FA;border-left:4px solid {AMBAR};padding:12px 14px;border-radius:8px;margin-bottom:14px">
      <div style="font-size:12px;color:#5B6B82">Código de consulta</div>
      <div style="font-size:26px;font-weight:800;letter-spacing:2px">{s['codigo']}</div></div>
    <p style="margin:4px 0"><b>Laboratorio:</b> {escape(s['lab_nombre'] or '')}</p>
    <p style="margin:4px 0"><b>Fecha y hora:</b> {s['fecha']}, de {s['inicio']} a {s['fin']}</p>
    <p style="margin:4px 0 12px"><b>Motivo:</b> {escape(s['motivo'] or '')}</p>
    <b>Componentes</b>
    <table style="width:100%;border-collapse:collapse;margin:6px 0 12px;font-size:14px">{filas_items}</table>
    <b>Estudiantes</b><ul style="margin:6px 0 12px">{estudiantes}</ul>
    {f"<p style='background:#FFF6E0;padding:10px;border-radius:8px'>{escape(nota)}</p>" if nota else ""}
    <div style="border:1px dashed #9AA8BD;border-radius:8px;padding:10px 12px;font-size:12px;margin:10px 0">
      <b>Firma electrónica:</b> {escape(s.get('verificacion') or 'sin verificar')}<br>
      <b>Sello digital (SHA-256):</b> <span style="font-family:monospace;word-break:break-all">{s.get('huella') or '-'}</span></div>
    <p style="color:#5B6B82">{siguiente}</p>
    <p style="font-size:12px;color:#5B6B82">Consulta el estado cuando quieras en Khipu → Laboratorio → Consultar mi solicitud.</p>
  </div></div>"""
    return texto, html

def enviar_codigo(destino: str, nombre: str, codigo6: str, para: str = "firmar tu reserva de laboratorio"):
    """Envía el código de verificación de identidad (firma electrónica simple)."""
    texto = (f"Hola {nombre},\n\nTu código para {para} en Khipu es: {codigo6}\n"
             "Vence en 10 minutos. Si no fuiste tú, ignora este correo.\n\nKhipu · FIEE-UNMSM")
    html = f"""<div style="font-family:Arial,sans-serif;max-width:480px;margin:auto;color:{NAVY}">
  <div style="background:{NAVY};color:white;padding:16px 20px;border-radius:12px 12px 0 0">
    <b style="font-size:20px">Khipu</b> · verificación de identidad</div>
  <div style="border:1px solid #E3E8F1;border-top:none;padding:20px;border-radius:0 0 12px 12px">
    <p>Hola <b>{escape(nombre)}</b>, usa este código para {escape(para)}:</p>
    <div style="font-size:34px;font-weight:800;letter-spacing:8px;text-align:center;
                background:#F2F5FA;border-left:4px solid {AMBAR};padding:14px;border-radius:8px">{codigo6}</div>
    <p style="color:#5B6B82;font-size:13px">Vence en 10 minutos. Si no fuiste tú, ignora este correo:
    nadie podrá reservar a tu nombre sin este código.</p></div></div>"""
    _enviar(destino, f"Khipu · Tu código de verificación: {codigo6}", texto, html)

def avisar(codigo: str) -> str:
    """Envía el correo según el estado actual de la solicitud al líder (estudiante 1).
    Devuelve el correo al que se envió, o lanza RuntimeError con el motivo."""
    if not configurado():
        raise RuntimeError("el envío de correos no está configurado")
    s = db.ver_solicitud(codigo)
    if s is None or not s["estudiantes"]:
        raise RuntimeError("no se encontró la solicitud")
    destino = str(s["estudiantes"][0].get("correo") or "").strip()
    if not destino:
        raise RuntimeError("el líder no tiene correo")
    texto, html = contenido(s)
    _enviar(destino, f"Khipu · {TITULOS.get(s['estado'], 'Solicitud')} · {s['codigo']}", texto, html)
    return destino


def avisar_publicacion(p: dict):
    """Avisa al vendedor si su publicación fue aprobada o rechazada."""
    if not configurado():
        raise RuntimeError("el envío de correos no está configurado")
    aprobada = p["estado"] == "publicada"
    titulo = "Tu publicación fue aprobada y ya está visible" if aprobada else "Tu publicación no fue aprobada"
    detalle = (f"Para marcarla como vendida usa este código en Khipu → Compra y venta → "
               f"Mis publicaciones: {p['codigo']}") if aprobada else "Puedes corregirla y publicar de nuevo."
    nota = f"Nota del encargado: {p['nota']}" if p.get("nota") else ""
    texto = (f"Hola {p['nombre']},\n\n{titulo}\n\n{p['titulo']} · {p['cantidad']} unid. · "
             f"S/ {p['precio']:.2f}\n{nota}\n{detalle}\n\nKhipu · FIEE-UNMSM")
    html = f"""<div style="font-family:Arial,sans-serif;max-width:520px;margin:auto;color:{NAVY}">
  <div style="background:{NAVY};color:white;padding:16px 20px;border-radius:12px 12px 0 0">
    <b style="font-size:20px">Khipu</b> · Compra y venta</div>
  <div style="border:1px solid #E3E8F1;border-top:none;padding:20px;border-radius:0 0 12px 12px">
    <p>Hola <b>{escape(p['nombre'])}</b>,</p><h3 style="margin:4px 0 12px">{escape(titulo)}</h3>
    <p><b>{escape(p['titulo'])}</b> · {p['cantidad']} unid. · S/ {p['precio']:.2f}</p>
    {f"<p style='background:#FFF6E0;padding:10px;border-radius:8px'>{escape(nota)}</p>" if nota else ""}
    <div style="background:#F2F5FA;border-left:4px solid {AMBAR};padding:12px 14px;border-radius:8px">
      {escape(detalle)}</div></div></div>"""
    _enviar(p["correo"], f"Khipu · {titulo} · {p['codigo']}", texto, html)
