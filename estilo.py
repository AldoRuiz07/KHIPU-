"""estilo.py - diseño visual de Khipu: base limpia tipo vercel.com (blanco, bordes finos, Geist)
con identidad institucional de la UNMSM / FIEE: azul institucional, acento dorado y logos (dueño: P3).
Solo CSS y encabezados: no cambia la lógica de ninguna pestaña."""
import base64
from functools import lru_cache
from pathlib import Path
import streamlit as st

NEGRO, GRIS, BORDE, FONDO2, AZUL = "#0A0A0A", "#666666", "#EAEAEA", "#FAFAFA", "#0070F3"
INST, ORO = "#0B1F66", "#C9A227"          # azul de la FIEE y dorado del escudo UNMSM
ASSETS = Path(__file__).parent / "assets"


@lru_cache(maxsize=None)
def _img(nombre: str) -> str:
    """Devuelve la imagen como data-URI para incrustarla en el HTML (vacío si no existe)."""
    f = ASSETS / nombre
    if not f.exists():
        return ""
    mime = "image/jpeg" if f.suffix.lower() in (".jpg", ".jpeg") else "image/png"
    return f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode()


FONDO = _img("fondo_fiee.jpg")             # foto de la facultad (fondo de página y encabezado)

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@500&display=swap');
html, body, [class*="css"], .stMarkdown, .stTextInput, .stTextArea, .stButton, .stTabs,
[data-testid="stSidebar"], button, input, textarea, select {{
    font-family: 'Geist', -apple-system, 'Segoe UI', Inter, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}}
/* Los íconos de Streamlit usan su propia fuente: si se reemplaza, aparecen como texto */
[data-testid="stIconMaterial"], span[class*="material-symbols"], .material-icons,
[data-testid="stExpanderToggleIcon"], [data-testid="stSidebarCollapseButton"] span,
[data-testid="stSidebarCollapsedControl"] span {{
    font-family: 'Material Symbols Rounded' !important;
}}
.stApp {{
    color: {NEGRO}; background-color: #FFFFFF;
    background-image: linear-gradient(rgba(255,255,255,.93), rgba(255,255,255,.93)), url("{FONDO}");
    background-size: cover; background-position: center top; background-attachment: fixed;
}}
.block-container {{ padding-top: 1.4rem; max-width: 1080px; }}
#MainMenu, footer {{ visibility: hidden; }}
header[data-testid="stHeader"] {{ background: transparent; }}
hr {{ border-color: {BORDE}; }}
h1, h2, h3, h4 {{ letter-spacing: -0.03em; font-weight: 600; color: {NEGRO}; }}

/* ---------- Encabezado (hero) ---------- */
.khipu-hero {{
    position: relative; padding: 44px 28px 30px 28px; margin: 14px 0 10px 0;
    border: 1px solid {BORDE}; border-radius: 10px; overflow: hidden;
}}
.khipu-hero::before {{
    content: ""; position: absolute; inset: 0; z-index: 0; pointer-events: none; border-radius: 10px;
    background-image:
        linear-gradient(90deg, rgba(255,255,255,.97) 0%, rgba(255,255,255,.88) 42%, rgba(255,255,255,.28) 100%),
        url("{FONDO}");
    background-size: cover; background-position: center 40%;
}}
.khipu-hero > * {{ position: relative; z-index: 1; }}
.khipu-hero h1::after {{ content: ""; display: block; width: 64px; height: 4px; background: {ORO}; margin-top: 16px; }}
.khipu-hero h1 {{
    font-size: clamp(2.1rem, 5vw, 3.4rem); font-weight: 700; margin: 0; color: {NEGRO};
    letter-spacing: -0.055em; line-height: 1.05;
}}
.khipu-hero p {{ margin: 14px 0 18px 0; color: {GRIS}; font-size: 1.05rem; max-width: 640px; }}
.khipu-pasos span {{
    display: inline-flex; align-items: center; gap: 8px; background: #FFFFFF;
    border: 1px solid {BORDE}; border-radius: 999px; padding: 5px 14px 5px 6px;
    margin: 0 8px 8px 0; font-size: .82rem; font-weight: 500; color: {NEGRO};
}}
.khipu-pasos b {{
    display: inline-flex; align-items: center; justify-content: center; width: 20px; height: 20px;
    border-radius: 50%; background: {INST}; color: #FFFFFF; font-size: .7rem;
    font-family: 'Geist Mono', monospace !important; font-weight: 500;
}}

/* ---------- Barra institucional (logos UNMSM y FIEE) ---------- */
.inst-barra {{
    display: flex; align-items: center; gap: 18px; padding: 6px 0 12px 0;
    border-bottom: 1px solid {BORDE}; position: relative;
}}
.inst-barra::after {{
    content: ""; position: absolute; left: 0; bottom: -1px; width: 96px; height: 3px; background: {ORO};
}}
.inst-barra img.unmsm {{ height: 46px; }}
.inst-barra img.fiee {{ height: 52px; }}
.inst-barra img.khipu {{ height: 46px; }}
.inst-barra .sep {{ width: 1px; height: 36px; background: {BORDE}; }}
.inst-barra .fac {{ line-height: 1.25; font-size: .78rem; color: {GRIS}; }}
.inst-barra .fac b {{ display: block; color: {INST}; font-size: .86rem; font-weight: 600; letter-spacing: -0.01em; }}
@media (max-width: 760px) {{ .inst-barra .fac {{ display: none; }} .inst-barra img.unmsm {{ height: 36px; }} .inst-barra img.fiee {{ height: 40px; }} .inst-barra img.khipu {{ height: 34px; }} }}

/* ---------- Pie ---------- */
.khipu-pie {{
    margin-top: 48px; padding: 18px 0 8px 0; border-top: 1px solid {BORDE}; display: flex;
    align-items: center; gap: 14px; color: {GRIS}; font-size: .8rem;
}}
.khipu-pie img {{ height: 34px; }}
.khipu-pie b {{ color: {INST}; font-weight: 600; }}

/* ---------- Pestañas: texto con subrayado negro ---------- */
.stTabs [data-baseweb="tab-list"] {{ gap: 4px; border-bottom: 1px solid {BORDE}; }}
.stTabs [data-baseweb="tab"] {{
    height: 44px; padding: 0 14px; background: transparent; color: {GRIS};
    font-weight: 500; font-size: .95rem; border-radius: 6px 6px 0 0; transition: color .15s ease;
}}
.stTabs [data-baseweb="tab"]:hover {{ color: {NEGRO}; background: {FONDO2}; }}
.stTabs [aria-selected="true"] {{ color: {NEGRO} !important; font-weight: 600; }}
.stTabs [data-baseweb="tab-highlight"] {{ background: {INST}; height: 3px; border-radius: 3px 3px 0 0; }}
.stTabs [data-baseweb="tab-border"] {{ display: none; }}
.stTabs [data-baseweb="tab-panel"] {{ padding-top: 18px; }}

/* ---------- Botones ---------- */
.stButton > button, .stDownloadButton > button, [data-testid^="stBaseButton"] {{
    border-radius: 6px; font-weight: 500; border: 1px solid {BORDE}; background: #FFFFFF;
    color: {NEGRO}; box-shadow: none; transition: all .15s ease;
}}
.stButton > button:hover, .stDownloadButton > button:hover {{
    border-color: {NEGRO}; color: {NEGRO}; background: {FONDO2};
}}
button[kind="primary"], [data-testid="stBaseButton-primary"] {{
    background: {INST} !important; color: #FFFFFF !important; border: 1px solid {INST} !important;
}}
button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover {{
    background: #162E8F !important; border-color: #162E8F !important; color: #FFFFFF !important;
}}

/* ---------- Campos de texto ---------- */
.stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input,
[data-baseweb="select"] > div, [data-baseweb="input"], [data-baseweb="textarea"] {{
    border-radius: 6px !important; border-color: {BORDE} !important; background: #FFFFFF !important;
}}
.stTextInput input:focus, .stTextArea textarea:focus {{
    border-color: {NEGRO} !important; box-shadow: 0 0 0 3px rgba(0,0,0,.08) !important;
}}
label, [data-testid="stWidgetLabel"] p {{ font-size: .85rem; font-weight: 500; color: {NEGRO}; }}

/* ---------- Tarjetas ---------- */
[data-testid="stChatMessage"] {{
    background: #FFFFFF; border: 1px solid {BORDE}; border-radius: 8px; box-shadow: none;
}}
[data-testid="stExpander"], [data-testid="stExpander"] details {{
    background: #FFFFFF; border: 1px solid {BORDE}; border-radius: 8px; box-shadow: none;
}}
[data-testid="stMetric"] {{
    background: #FFFFFF; border: 1px solid {BORDE}; border-radius: 8px; padding: 14px 18px;
}}
[data-testid="stDataFrame"], [data-testid="stDataEditor"] {{
    border: 1px solid {BORDE}; border-radius: 8px; overflow: hidden;
}}
[data-testid="stAlert"] {{ border-radius: 8px; border: 1px solid {BORDE}; background: {FONDO2}; }}
[data-testid="stChatInput"] {{ border-radius: 8px; border: 1px solid {BORDE}; }}

/* ---------- Selector de modo y barra lateral ---------- */
[data-testid="stSegmentedControl"] button {{ border-radius: 6px; }}
[data-testid="stSidebar"] {{ background: {FONDO2}; border-right: 1px solid {BORDE}; }}
[data-testid="stSidebar"] h3 {{ font-size: 1rem; letter-spacing: -0.02em; }}

/* ---------- Detalles propios de Khipu ---------- */
.khipu-chip {{
    display: inline-block; background: {FONDO2}; border: 1px solid {BORDE}; color: {NEGRO};
    border-radius: 999px; padding: 2px 10px; font-size: .78rem; font-weight: 500;
}}
.khipu-alerta {{
    background: {FONDO2}; border: 1px solid {BORDE}; border-left: 3px solid {ORO}; color: {NEGRO};
    border-radius: 8px; padding: 10px 14px; font-weight: 500; margin-bottom: 8px;
}}
a {{ color: {AZUL}; }}
</style>
"""

def aplicar():
    st.markdown(CSS, unsafe_allow_html=True)

def encabezado(titulo: str, subtitulo: str, pasos: list[str] | None = None):
    chips = "".join(f"<span><b>{i}</b>{p}</span>" for i, p in enumerate(pasos or [], 1))
    st.markdown(f"""<div class="khipu-hero"><h1>{titulo}</h1><p>{subtitulo}</p>
                    <div class="khipu-pasos">{chips}</div></div>""", unsafe_allow_html=True)


def barra_institucional():
    """Logos de la UNMSM y de la FIEE con el nombre de la facultad (va arriba de todo)."""
    u, f, k = _img("unmsm_logo.png"), _img("fiee_logo.png"), _img("logo.png")
    st.markdown(f"""<div class="inst-barra">
        <img class="unmsm" src="{u}" alt="Universidad Nacional Mayor de San Marcos">
        <div class="sep"></div>
        <img class="fiee" src="{f}" alt="FIEE">
        <div class="sep"></div>
        <img class="khipu" src="{k}" alt="Khipu">
        <div class="fac"><b>Facultad de Ingeniería Electrónica y Eléctrica</b>Universidad Nacional Mayor de San Marcos</div>
        </div>""", unsafe_allow_html=True)


def pie():
    f = _img("fiee_logo.png")
    st.markdown(f"""<div class="khipu-pie"><img src="{f}" alt="FIEE">
        <div><b>Khipu</b> · Asistente de almacén y laboratorios<br>
        Facultad de Ingeniería Electrónica y Eléctrica · UNMSM · ENEISOFT 2026</div></div>""",
                unsafe_allow_html=True)
