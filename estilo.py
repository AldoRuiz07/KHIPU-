"""estilo.py - diseño visual de Khipu: base limpia tipo vercel.com (blanco, bordes finos, Geist)
con identidad institucional de la UNMSM / FIEE: azul institucional, acento dorado y logos.
Incluye modo claro y modo oscuro (dueño: P3). Solo CSS y encabezados: no toca la lógica."""
import base64
from functools import lru_cache
from pathlib import Path
import streamlit as st

ASSETS = Path(__file__).parent / "assets"

# ---------------------------------------------------------------- paletas
CLARO = dict(
    TXT="#0A0A0A", MUTED="#666666", BORDE="#EAEAEA", SURF="#FFFFFF", SURF2="#FAFAFA",
    LINK="#0070F3", BTN="#0B1F66", BTN_H="#162E8F", TITULO="#0B1F66", ORO="#C9A227",
    PAGINA="rgba(255,255,255,.93)", H1="rgba(255,255,255,.97)", H2="rgba(255,255,255,.88)",
    H3="rgba(255,255,255,.28)", FOCO="rgba(0,0,0,.08)", ESQUEMA="light",
    TINTE="#F2F5FF", TINTE_ORO="#FBF6E6", LIBRE="#E6F6EC", LIBRE_B="#B5E0C4", LIBRE_T="#155C35",
    OFF="#F1F2F4", OFF_T="#9AA0AB", SEL_T="#FFFFFF",
)
OSCURO = dict(
    TXT="#EDEDED", MUTED="#A1A1A1", BORDE="#2C2C31", SURF="#16161A", SURF2="#101013",
    LINK="#6AA5FF", BTN="#1D3FBF", BTN_H="#2A52E0", TITULO="#9DB8FF", ORO="#E0B93A",
    PAGINA="rgba(8,8,10,.92)", H1="rgba(8,8,10,.96)", H2="rgba(8,8,10,.88)",
    H3="rgba(8,8,10,.40)", FOCO="rgba(106,165,255,.25)", ESQUEMA="dark",
    TINTE="#1A2140", TINTE_ORO="#2A2412", LIBRE="#123322", LIBRE_B="#2C6E47", LIBRE_T="#9BE7B6",
    OFF="#1C1C21", OFF_T="#6B7080", SEL_T="#FFFFFF",
)


@lru_cache(maxsize=None)
def imagen(nombre: str) -> str:
    """Devuelve la imagen de assets/ como data-URI para incrustarla en el HTML (vacío si no existe)."""
    f = ASSETS / nombre
    if not f.exists():
        return ""
    mime = "image/jpeg" if f.suffix.lower() in (".jpg", ".jpeg") else "image/png"
    return f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode()


_img = imagen                              # nombre anterior: lo usa ui_inicio.py
FONDO = imagen("fondo_fiee.jpg")           # foto de la facultad (fondo de página y encabezado)


def _css(oscuro: bool) -> str:
    p = OSCURO if oscuro else CLARO
    TXT, MUTED, BORDE, SURF, SURF2 = p["TXT"], p["MUTED"], p["BORDE"], p["SURF"], p["SURF2"]
    LINK, BTN, BTN_H, TITULO, ORO = p["LINK"], p["BTN"], p["BTN_H"], p["TITULO"], p["ORO"]
    base = f"""
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
    color: {TXT}; background-color: {SURF2 if oscuro else "#FFFFFF"}; color-scheme: {p["ESQUEMA"]};
    background-image: linear-gradient({p["PAGINA"]}, {p["PAGINA"]}), url("{FONDO}");
    background-size: cover; background-position: center top; background-attachment: fixed;
}}
:root, .stApp {{
    --k-txt: {TXT}; --k-muted: {MUTED}; --k-borde: {BORDE}; --k-surf: {SURF}; --k-surf2: {SURF2};
    --k-titulo: {TITULO}; --k-oro: {ORO}; --k-btn: {BTN}; --k-tinte: {p["TINTE"]}; --k-tinte-oro: {p["TINTE_ORO"]};
    --k-libre: {p["LIBRE"]}; --k-libre-b: {p["LIBRE_B"]}; --k-libre-t: {p["LIBRE_T"]};
    --k-off: {p["OFF"]}; --k-off-t: {p["OFF_T"]};
}}
.block-container {{ padding-top: 1.4rem; max-width: 1080px; }}
#MainMenu, footer {{ visibility: hidden; }}
header[data-testid="stHeader"] {{ background: transparent; }}
hr {{ border-color: {BORDE}; }}
h1, h2, h3, h4 {{ letter-spacing: -0.03em; font-weight: 600; color: {TXT}; }}
a {{ color: {LINK}; }}

/* ---------- Encabezado (hero) ---------- */
.khipu-hero {{
    position: relative; padding: 44px 28px 30px 28px; margin: 14px 0 10px 0;
    border: 1px solid {BORDE}; border-radius: 10px; overflow: hidden;
}}
.khipu-hero::before {{
    content: ""; position: absolute; inset: 0; z-index: 0; pointer-events: none; border-radius: 10px;
    background-image:
        linear-gradient(90deg, {p["H1"]} 0%, {p["H2"]} 42%, {p["H3"]} 100%),
        url("{FONDO}");
    background-size: cover; background-position: center 40%;
}}
.khipu-hero > * {{ position: relative; z-index: 1; }}
.khipu-hero h1::after {{ content: ""; display: block; width: 64px; height: 4px; background: {ORO}; margin-top: 16px; }}
.khipu-hero h1 {{
    font-size: clamp(2.1rem, 5vw, 3.4rem); font-weight: 700; margin: 0; color: {TXT};
    letter-spacing: -0.055em; line-height: 1.05;
}}
.khipu-hero p {{ margin: 14px 0 18px 0; color: {MUTED}; font-size: 1.05rem; max-width: 640px; }}
.khipu-pasos span {{
    display: inline-flex; align-items: center; gap: 8px; background: {SURF};
    border: 1px solid {BORDE}; border-radius: 999px; padding: 5px 14px 5px 6px;
    margin: 0 8px 8px 0; font-size: .82rem; font-weight: 500; color: {TXT};
}}
.khipu-pasos b {{
    display: inline-flex; align-items: center; justify-content: center; width: 20px; height: 20px;
    border-radius: 50%; background: {BTN}; color: #FFFFFF; font-size: .7rem;
    font-family: 'Geist Mono', monospace !important; font-weight: 500;
}}

/* ---------- Barra institucional (logos UNMSM, FIEE y Khipu) ---------- */
.inst-barra {{
    display: flex; align-items: center; gap: 18px; padding: 6px 0 12px 0;
    border-bottom: 1px solid {BORDE}; position: relative;
}}
.inst-barra::after {{
    content: ""; position: absolute; left: 0; bottom: -1px; width: 96px; height: 3px; background: {ORO};
}}
.inst-barra {{ gap: 14px; }}
.inst-barra img {{ background: #FFFFFF; border-radius: 6px; padding: 2px 6px; flex: 0 1 auto; min-width: 0; object-fit: contain; }}
.inst-barra img.unmsm {{ height: 44px; }}
.inst-barra img.fiee {{ height: 50px; }}
.inst-barra img.khipu {{ height: 44px; }}
.inst-barra .sep {{ flex: none; }}
.inst-barra .sep {{ width: 1px; height: 36px; background: {BORDE}; }}
.inst-barra .fac {{ line-height: 1.25; font-size: .78rem; color: {MUTED}; }}
.inst-barra .fac b {{ display: block; color: {TITULO}; font-size: .86rem; font-weight: 600; letter-spacing: -0.01em; }}
@media (max-width: 760px) {{ .inst-barra img.unmsm {{ height: 32px; }} .inst-barra img.fiee {{ height: 36px; }} .inst-barra img.khipu {{ height: 32px; }} .inst-barra {{ gap: 8px; }} }}

/* ---------- Pie ---------- */
.khipu-pie {{
    margin-top: 48px; padding: 18px 0 8px 0; border-top: 1px solid {BORDE}; display: flex;
    align-items: center; gap: 14px; color: {MUTED}; font-size: .8rem;
}}
.khipu-pie img {{ height: 34px; background: #FFFFFF; border-radius: 6px; padding: 2px 6px; }}
.khipu-pie b {{ color: {TITULO}; font-weight: 600; }}

/* ---------- Pestañas: texto con subrayado ---------- */
.stTabs [data-baseweb="tab-list"] {{ gap: 4px; border-bottom: 1px solid {BORDE}; }}
.stTabs [data-baseweb="tab"] {{
    height: 44px; padding: 0 14px; background: transparent; color: {MUTED};
    font-weight: 500; font-size: .95rem; border-radius: 6px 6px 0 0; transition: color .15s ease;
}}
.stTabs [data-baseweb="tab"]:hover {{ color: {TXT}; background: {SURF2}; }}
.stTabs [aria-selected="true"] {{ color: {TXT} !important; font-weight: 600; }}
.stTabs [data-baseweb="tab-highlight"] {{ background: {BTN}; height: 3px; border-radius: 3px 3px 0 0; }}
.stTabs [data-baseweb="tab-border"] {{ display: none; }}
.stTabs [data-baseweb="tab-panel"] {{ padding-top: 18px; }}

/* ---------- Botones ---------- */
.stButton > button, .stDownloadButton > button, [data-testid^="stBaseButton"] {{
    border-radius: 6px; font-weight: 500; border: 1px solid {BORDE}; background: {SURF};
    color: {TXT}; box-shadow: none; transition: all .15s ease;
}}
.stButton > button:hover, .stDownloadButton > button:hover {{
    border-color: {TXT}; color: {TXT}; background: {SURF2};
}}
button[kind="primary"], [data-testid="stBaseButton-primary"] {{
    background: {BTN} !important; color: #FFFFFF !important; border: 1px solid {BTN} !important;
}}
button[kind="primary"] p, [data-testid="stBaseButton-primary"] p {{ color: #FFFFFF !important; }}
button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover {{
    background: {BTN_H} !important; border-color: {BTN_H} !important; color: #FFFFFF !important;
}}

/* ---------- Campos de texto ---------- */
.stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input,
[data-baseweb="select"] > div, [data-baseweb="input"], [data-baseweb="textarea"] {{
    border-radius: 6px !important; border-color: {BORDE} !important; background: {SURF} !important;
    color: {TXT} !important;
}}
.stTextInput input:focus, .stTextArea textarea:focus {{
    border-color: {TXT} !important; box-shadow: 0 0 0 3px {p["FOCO"]} !important;
}}
label, [data-testid="stWidgetLabel"] p {{ font-size: .85rem; font-weight: 500; color: {TXT}; }}

/* ---------- Tarjetas de Streamlit ---------- */
[data-testid="stChatMessage"] {{
    background: {SURF}; border: 1px solid {BORDE}; border-radius: 8px; box-shadow: none;
}}
[data-testid="stExpander"], [data-testid="stExpander"] details {{
    background: {SURF}; border: 1px solid {BORDE}; border-radius: 8px; box-shadow: none;
}}
[data-testid="stMetric"] {{
    background: {SURF}; border: 1px solid {BORDE}; border-radius: 8px; padding: 14px 18px;
}}
[data-testid="stDataFrame"], [data-testid="stDataEditor"] {{
    border: 1px solid {BORDE}; border-radius: 8px; overflow: hidden;
}}
[data-testid="stAlert"] {{ border-radius: 8px; border: 1px solid {BORDE}; background: {SURF2}; }}
[data-testid="stChatInput"] {{ border-radius: 8px; border: 1px solid {BORDE}; }}

/* ---------- Selector de modo y barra lateral ---------- */
[data-testid="stSegmentedControl"] button {{ border-radius: 6px; }}
[data-testid="stSidebar"] {{ background: {SURF2}; border-right: 1px solid {BORDE}; }}
[data-testid="stSidebar"] h3 {{ font-size: 1rem; letter-spacing: -0.02em; }}
.khipu-nav-titulo {{
    font-size: .72rem; font-weight: 600; letter-spacing: .08em; text-transform: uppercase;
    color: {MUTED}; margin: 22px 0 6px 0; padding-top: 14px; border-top: 1px solid {BORDE};
}}

/* ---------- Botón que abre/cierra la barra lateral: ícono "menu" en vez de las flechas ---------- */
[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
[data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"] {{
    font-size: 0 !important; width: 24px; height: 24px; display: inline-flex; align-items: center; justify-content: center;
}}
[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"]::before,
[data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"]::before {{
    content: "menu"; font-family: "Material Symbols Rounded" !important; font-size: 24px; line-height: 1;
    font-weight: 400; letter-spacing: normal; text-transform: none; white-space: nowrap;
    font-feature-settings: "liga"; -webkit-font-feature-settings: "liga";
}}

/* ---------- Detalles propios de Khipu ---------- */
.khipu-chip {{
    display: inline-block; background: {SURF2}; border: 1px solid {BORDE}; color: {TXT};
    border-radius: 999px; padding: 2px 10px; font-size: .78rem; font-weight: 500;
}}
.khipu-alerta {{
    background: {SURF2}; border: 1px solid {BORDE}; border-left: 3px solid {ORO}; color: {TXT};
    border-radius: 8px; padding: 10px 14px; font-weight: 500; margin-bottom: 8px;
}}

/* ---------- Secciones: Misión y visión, ¿Por qué nace Khipu?, ¿Quiénes somos? ---------- */
h2.khipu-h2 {{ font-size: 1.5rem; margin: 30px 0 4px 0; padding: 0; }}
h2.khipu-h2::after {{ content: ""; display: block; width: 40px; height: 3px; background: {ORO}; margin-top: 8px; }}
p.sub {{ color: {MUTED}; margin: 8px 0 16px 0; max-width: 720px; line-height: 1.6; }}
.khipu-eyebrow {{
    font-size: .74rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: {TITULO};
}}
.khipu-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 14px; margin: 10px 0 6px 0; }}
.khipu-card {{
    background: {SURF}; border: 1px solid {BORDE}; border-radius: 10px; padding: 18px 20px;
    transition: border-color .15s ease, transform .15s ease;
}}
.khipu-card:hover {{ border-color: {TITULO}; transform: translateY(-2px); }}
.khipu-card .ico {{ font-size: 1.4rem; line-height: 1; margin-bottom: 8px; }}
.khipu-card h4 {{ margin: 0 0 6px 0; padding: 0; font-size: 1rem; line-height: 1.3; }}
.khipu-card p {{ margin: 0; color: {MUTED}; font-size: .92rem; line-height: 1.55; }}
.khipu-card.grande {{ padding: 26px 28px; border-top: 3px solid {ORO}; }}
.khipu-card.grande p {{ font-size: 1.02rem; color: {TXT}; line-height: 1.65; }}
.khipu-cita {{
    border-left: 3px solid {ORO}; background: {SURF}; border-radius: 0 10px 10px 0;
    padding: 16px 22px; margin: 18px 0; font-size: 1.05rem; line-height: 1.6; color: {TXT};
}}
.khipu-pasos-flujo {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin: 12px 0; }}
.khipu-pasos-flujo span {{
    background: {SURF}; border: 1px solid {BORDE}; border-radius: 999px; padding: 6px 14px;
    font-size: .88rem; font-weight: 500; color: {TXT};
}}
.khipu-pasos-flujo i {{ color: {ORO}; font-style: normal; font-weight: 700; }}
.khipu-hecho li {{ margin: 6px 0; line-height: 1.5; }}
.khipu-equipo {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin: 14px 0; }}
.khipu-persona {{
    background: {SURF}; border: 1px solid {BORDE}; border-radius: 12px; padding: 24px 18px; text-align: center;
    transition: border-color .15s ease, transform .15s ease;
}}
.khipu-persona:hover {{ border-color: {TITULO}; transform: translateY(-2px); }}
.khipu-persona img {{
    width: 112px; height: 112px; border-radius: 50%; object-fit: cover;
    border: 3px solid {ORO}; margin-bottom: 12px;
}}
.khipu-persona b {{ display: block; font-size: 1.05rem; color: {TXT}; }}
.khipu-persona span {{ display: block; color: {MUTED}; font-size: .86rem; margin: 4px 0 12px 0; line-height: 1.4; }}
.khipu-persona a {{
    display: inline-block; border: 1px solid {BORDE}; border-radius: 6px; padding: 4px 14px;
    font-size: .82rem; font-weight: 500; text-decoration: none; color: {TXT};
}}
.khipu-persona a:hover {{ border-color: {TITULO}; color: {TITULO}; }}
.khipu-tec {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0; }}
.khipu-tec span {{
    background: {SURF2}; border: 1px solid {BORDE}; border-radius: 6px; padding: 4px 12px;
    font-size: .84rem; font-weight: 500; font-family: 'Geist Mono', monospace !important;
}}
</style>
"""
    if not oscuro:
        return base
    # ---- Ajustes extra del modo oscuro: los componentes de Streamlit traen colores claros
    return base + f"""
<style>
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{ color: {TXT}; }}
.stApp p, .stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
.stApp label, .stApp summary, [data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"],
[data-testid="stMetricValue"], [data-testid="stMetricLabel"], [data-testid="stExpander"] summary,
[data-testid="stChatMessage"] {{ color: {TXT}; }}
[data-testid="stCaptionContainer"], .stApp small {{ color: {MUTED} !important; }}
header[data-testid="stHeader"] *, [data-testid="stToolbar"] * {{ color: {TXT} !important; }}
[data-testid="stSidebar"] * {{ color: {TXT}; }}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {{ color: {MUTED} !important; }}
code, pre {{ background: {SURF2} !important; color: {TXT} !important; }}
[data-baseweb="popover"], [data-baseweb="popover"] > div, [data-baseweb="menu"],
ul[role="listbox"], [data-baseweb="calendar"] {{ background: {SURF} !important; color: {TXT} !important; }}
[data-baseweb="popover"] li:hover, ul[role="listbox"] li:hover {{ background: {SURF2} !important; }}
[data-testid="stBottom"], [data-testid="stBottom"] > div, [data-testid="stBottomBlockContainer"] {{
    background: {SURF2} !important;
}}
[data-testid="stChatInput"] {{ background: {SURF} !important; }}
[data-testid="stChatInput"] * {{ background: transparent !important; color: {TXT} !important; }}
[data-testid="stChatInput"] textarea::placeholder {{ color: {MUTED} !important; }}
[data-testid="stAlert"], [data-testid="stAlert"] * {{ color: {TXT} !important; }}
[data-testid="stAlert"] > div, [data-testid="stAlertContainer"] {{ background: {SURF} !important; }}
input::placeholder, textarea::placeholder {{ color: {MUTED} !important; opacity: 1 !important; }}
[data-testid="stExpander"] summary:hover * {{ color: {TITULO} !important; }}
[data-testid="stDataFrame"], [data-testid="stDataEditor"] {{ filter: invert(.92) hue-rotate(180deg); }}
[data-testid="stFileUploaderDropzone"] {{ background: {SURF}; }}
[data-testid="stSegmentedControl"] button, [data-testid="stButtonGroup"] button,
[data-testid^="stBaseButton-segmented_control"], [data-testid^="stBaseButton-pills"] {{
    background: {SURF} !important; color: {TXT} !important; border-color: {BORDE} !important;
}}
[data-testid="stButtonGroup"] button *, [data-testid^="stBaseButton-segmented_control"] *,
[data-testid^="stBaseButton-pills"] * {{ color: inherit !important; }}
[data-testid="stBaseButton-segmented_controlActive"], [data-testid="stBaseButton-pillsActive"],
[data-testid="stButtonGroup"] button[aria-checked="true"] {{
    background: {BTN} !important; color: #FFFFFF !important; border-color: {BTN} !important;
}}
[data-testid="stToast"] {{ background: {SURF} !important; border: 1px solid {BORDE} !important; }}
[data-testid="stToast"] * {{ background: transparent !important; }}
[data-testid="stToast"], [data-testid="stToast"] * {{ color: {TXT} !important; }}
</style>
"""


def aplicar(oscuro: bool | None = None):
    """Inyecta el CSS. Si no se indica, lee el interruptor de la app (st.session_state.oscuro)."""
    if oscuro is None:
        oscuro = bool(st.session_state.get("oscuro", False))
    st.markdown(_css(oscuro), unsafe_allow_html=True)


def encabezado(titulo: str, subtitulo: str, pasos: list[str] | None = None):
    chips = "".join(f"<span><b>{i}</b>{p}</span>" for i, p in enumerate(pasos or [], 1))
    st.markdown(f"""<div class="khipu-hero"><h1>{titulo}</h1><p>{subtitulo}</p>
                    <div class="khipu-pasos">{chips}</div></div>""", unsafe_allow_html=True)


def barra_institucional():
    """Logos de la UNMSM, la FIEE y Khipu con el nombre de la facultad (va arriba de todo)."""
    u, f, k = imagen("unmsm_logo.png"), imagen("fiee_logo.png"), imagen("logo.png")
    st.markdown(f"""<div class="inst-barra">
        <img class="unmsm" src="{u}" alt="Universidad Nacional Mayor de San Marcos">
        <div class="sep"></div>
        <img class="fiee" src="{f}" alt="FIEE">
        <div class="sep"></div>
        <img class="khipu" src="{k}" alt="Khipu">
        </div>""", unsafe_allow_html=True)


def pie():
    f = imagen("fiee_logo.png")
    st.markdown(f"""<div class="khipu-pie"><img src="{f}" alt="FIEE">
        <div><b>Khipu</b> · Asistente de almacén y laboratorios<br>
        Facultad de Ingeniería Electrónica y Eléctrica · UNMSM · ENEISOFT 2026</div></div>""",
                unsafe_allow_html=True)
