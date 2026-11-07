"""estilo.py - diseño visual de Khipu: colores, tipografía y pestañas tipo khipu (dueño: P3)."""
import streamlit as st

NAVY, AZUL, AMBAR, NIEBLA = "#0B1F3A", "#1E6BFF", "#FFB000", "#F2F5FA"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, p, li, label, input, textarea, button, h1, h2, h3, h4, h5,
[data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"] {{
    font-family: 'Inter', sans-serif !important;
}}
.block-container {{ padding-top: 1.2rem; max-width: 1200px; }}
#MainMenu, footer {{ visibility: hidden; }}
header[data-testid="stHeader"] {{ background: transparent; }}

/* ---------- Encabezado ---------- */
.khipu-hero {{
    background: linear-gradient(120deg, {NAVY} 0%, #12305A 60%, {AZUL} 140%);
    border-radius: 18px; padding: 22px 28px; color: white; margin-bottom: 6px;
}}
.khipu-hero h1 {{ font-size: 1.9rem; font-weight: 800; margin: 0; color: white; letter-spacing: -0.5px; }}
.khipu-hero p {{ margin: 4px 0 12px 0; opacity: .85; font-size: .98rem; }}
.khipu-pasos span {{
    display: inline-block; background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.25);
    border-radius: 999px; padding: 4px 12px; margin: 0 6px 6px 0; font-size: .82rem; font-weight: 600;
}}
.khipu-pasos b {{ color: {AMBAR}; }}

/* ---------- Pestañas tipo khipu: cordón + nudos ---------- */
.stTabs, .stTabs > div, .stTabs [role="tablist"], .stTabs [role="tablist"] > div {{
    overflow: visible !important;
}}
.stTabs [role="tablist"], .stTabs [data-baseweb="tab-list"] {{
    gap: 14px !important; position: relative; padding-top: 30px !important;
    border-bottom: none !important; flex-wrap: wrap;
}}
.stTabs [role="tablist"]::before, .stTabs [data-baseweb="tab-list"]::before {{
    content: ""; position: absolute; top: 11px; left: 0; right: 0; height: 3px;
    background: {NAVY}; border-radius: 3px;
}}
.stTabs button[role="tab"], .stTabs [data-baseweb="tab"] {{
    position: relative !important; overflow: visible !important; height: auto !important;
    background: white !important; border: 1.5px solid #D5DCE8 !important;
    border-radius: 12px !important; padding: 10px 22px !important; margin: 0 !important;
    font-weight: 600 !important; color: {NAVY} !important; transition: all .15s ease;
}}
.stTabs button[role="tab"]::before, .stTabs [data-baseweb="tab"]::before {{
    content: ""; position: absolute; top: -17px; left: 50%; width: 2px; height: 17px;
    background: {NAVY}; transform: translateX(-50%);
}}
.stTabs button[role="tab"]::after, .stTabs [data-baseweb="tab"]::after {{
    content: ""; position: absolute; top: -24px; left: 50%; width: 13px; height: 13px;
    border-radius: 50%; background: {NAVY}; transform: translateX(-50%);
}}
.stTabs button[role="tab"]:hover {{ border-color: {AZUL} !important; color: {AZUL} !important; }}
.stTabs button[role="tab"][aria-selected="true"], .stTabs [aria-selected="true"] {{
    background: {NAVY} !important; color: white !important; border-color: {NAVY} !important;
}}
.stTabs button[role="tab"][aria-selected="true"] p {{ color: white !important; }}
.stTabs button[role="tab"][aria-selected="true"]::after, .stTabs [aria-selected="true"]::after {{
    background: {AMBAR}; box-shadow: 0 0 0 4px rgba(255,176,0,.30);
}}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"],
.stTabs [data-testid="stTabsHighlight"] {{ display: none !important; }}
.stTabs [role="tabpanel"], .stTabs [data-baseweb="tab-panel"] {{ padding-top: 16px; }}

/* ---------- Componentes ---------- */
.stButton > button, .stDownloadButton > button {{ border-radius: 10px; font-weight: 600; }}
[data-testid="stChatMessage"] {{
    background: white; border: 1px solid #E3E8F1; border-radius: 14px;
    box-shadow: 0 1px 3px rgba(11,31,58,.05);
}}
[data-testid="stExpander"] {{ background: white; border-radius: 12px; }}
[data-testid="stMetric"] {{
    background: white; border: 1px solid #E3E8F1; border-radius: 14px; padding: 12px 16px;
}}
[data-testid="stSidebar"] {{ background: white; border-right: 1px solid #E3E8F1; }}
.khipu-chip {{
    display: inline-block; background: {NIEBLA}; border: 1px solid #D5DCE8; color: {NAVY};
    border-radius: 999px; padding: 3px 10px; font-size: .8rem; font-weight: 600;
}}
.khipu-alerta {{
    background: #FFF6E0; border: 1px solid {AMBAR}; color: {NAVY}; border-radius: 12px;
    padding: 10px 14px; font-weight: 600; margin-bottom: 8px;
}}
</style>
"""

def aplicar():
    st.markdown(CSS, unsafe_allow_html=True)

def encabezado(titulo: str, subtitulo: str, pasos: list[str] | None = None):
    chips = "".join(f"<span><b>{i}</b>&nbsp; {p}</span>" for i, p in enumerate(pasos or [], 1))
    st.markdown(f"""<div class="khipu-hero"><h1>{titulo}</h1><p>{subtitulo}</p>
                    <div class="khipu-pasos">{chips}</div></div>""", unsafe_allow_html=True)
