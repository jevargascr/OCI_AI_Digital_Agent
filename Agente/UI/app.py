# app.py — Oculta "Nueva Sesión", conserva la pregunta visible y muestra chip de consulta
import inspect, asyncio, streamlit as st
from agente_oci import ejecutar_agente, borrar_session

# ------------------ CONFIG ------------------
try:
    st.set_page_config(page_title="Asistente Virtual", page_icon="🤖", layout="centered")
except Exception:
    pass

# ------------------ ASYNC LOOP FIX ------------------
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# Oculta el expander mientras se procesa la consulta
if st.session_state.get("processing", False):
    st.markdown(
        "<style>[data-testid='stExpander']{display:none!important}</style>",
        unsafe_allow_html=True
    )
    
# ------------------ STATE ------------------
ss = st.session_state
if "hist_key" not in ss:
    ss["hist_key"] = 0   # clave dinámica del expander del historial
ss.setdefault("hist_suffix", 0)   # contador para forzar re-montaje del expander
ss.setdefault("session_id", None)
ss.setdefault("processing", False)
ss.setdefault("pending", None)
ss.setdefault("log", [])
ss.setdefault("last_error", None)

# ——— dev: reset oculto por query param ?reset=1 (mantiene funcionalidad sin botón) ———
# Reset vía query param (?reset=1) usando API estable
params = st.query_params
if params.get("reset", "0") == "1":
    if ss.session_id:
        try:
            borrar_session(ss.session_id)
        except Exception:
            pass
    ss.session_id = None
    ss.log = []
    ss.last_error = None
    ss.pending = None
    st.rerun()

# ------------------ UTILS ------------------
def call_agente_safe(prompt: str, **kwargs):
    res = ejecutar_agente(prompt, **kwargs)
    if inspect.isawaitable(res):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(res)
        finally:
            loop.close()
    return res

def extract_text(resp):
    if resp is None: return None
    return getattr(resp, "final_output", None) or getattr(resp, "output", None) or str(resp)

# ------------------ STYLES ------------------
BRAND, BRAND_DARK, TEXT_DARK, TEXT_MUTED = "#2D7FFB", "#085BB5", "#111827", "#556170"
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
  html, body, .stApp {{ background:#fff !important; color:{TEXT_DARK} !important; font-family:"Montserrat",system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}}
  [data-testid="stHeader"], [data-testid="stToolbar"], footer {{ display:none !important; }}
  .block-container {{ max-width:860px !important; padding:0 16px 14px !important; }}
  [data-testid="stAppViewContainer"] > .main > div:first-child {{
    background:#fff; border:1px solid rgba(0,0,0,.06); border-radius:14px; box-shadow:0 10px 30px rgba(0,0,0,.08); padding:8px 12px 8px; }}
  .stCaption, [data-testid="stCaptionContainer"] p {{ color:{TEXT_MUTED} }}

  /* labels siempre visibles */
  .stSelectbox label, .stTextInput label, [data-testid="stWidgetLabel"] label, label {{
    color:#0B1220 !important; -webkit-text-fill-color:#0B1220 !important; opacity:1 !important; font-weight:600 !important; margin-bottom:.25rem !important;
  }}

  /* input */
  .stTextInput > div > div > input {{
    background:#F3F4F6 !important; color:{TEXT_DARK} !important; border:1px solid #D1D5DB !important; border-radius:12px !important; height:44px !important;
  }}

  /* select claro */
  .stSelectbox [data-baseweb="select"] > div {{ background:#F3F4F6 !important; border:1px solid #D1D5DB !important; border-radius:12px !important; min-height:44px }}
  .stSelectbox [data-baseweb="select"] * {{ color:#111827 !important; -webkit-text-fill-color:#111827 !important; }}
  .stSelectbox [data-baseweb="select"] svg {{ fill:#6B7280 !important; }}

  /* botones */
  .stButton > button {{
    display:inline-flex; background:linear-gradient(180deg,{BRAND} 0%,{BRAND_DARK} 100%) !important; color:#fff !important; border:none !important; border-radius:12px !important;
    padding:.65rem 1.05rem !important; font-weight:700 !important; box-shadow:0 12px 28px rgba(236,28,36,.28) !important;
  }}

  /* tarjeta de respuesta */
  .answer-card {{ background:#fff; border:1px solid #E5E7EB; border-left:6px solid #22C55E; border-radius:14px; box-shadow:0 8px 22px rgba(0,0,0,.06); padding:14px 16px; margin:10px 0 14px; }}

  /* chip de consulta en curso */
  .query-chip {{ display:inline-block; background:#F1F5FF; border:1px solid #C7D7FE; color:#0B1220; border-radius:999px; padding:6px 12px; margin:6px 0 0; font-size:0.92rem; }}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Expander: caja y cabecera (cerrado/abierto) */
[data-testid="stExpander"] > details {
  background:#FFFFFF !important;
  border:1px solid #E5E7EB !important;
  border-radius:12px !important;
  box-shadow:0 8px 22px rgba(0,0,0,.06) !important;
  overflow:hidden !important;
}
[data-testid="stExpander"] > details > summary {
  background:#F3F4F6 !important;
  color:#0B1220 !important;
  border-bottom:1px solid #E5E7EB !important;
  font-weight:700 !important;
}

/* ✅ Contenido cuando está ABIERTO: fondo y texto claros */
[data-testid="stExpander"] > details[open] > div[role="region"],
[data-testid="stExpander"] > details > div[role="region"] {
  background:#FFFFFF !important;
  color:#111827 !important;
}

/* Asegurar color interno del texto/listas/enlaces */
[data-testid="stExpander"] > details[open] > div[role="region"] *,
[data-testid="stExpander"] > details > div[role="region"] * {
  color:#111827 !important;
  -webkit-text-fill-color:#111827 !important;
}

/* Fallback para versiones antiguas de Streamlit */
.streamlit-expanderContent { background:#FFFFFF !important; color:#111827 !important; }
.streamlit-expanderContent * { color:#111827 !important; -webkit-text-fill-color:#111827 !important; }
</style>
""", unsafe_allow_html=True)


# ------------------ HEADER ------------------
st.image("MutiBot.png", width=200)
st.caption("Atención de consultas, productos, requisitos y canales de servicio.")

# ------------------ WIDGETS ------------------
idioma = st.selectbox("Idioma de Respuesta", ["Español","English","Portugués"], disabled=ss.processing)
# 👉 clave para que NO se borre en los reruns:
st.text_input("¿Qué deseas preguntar al agente?", placeholder="Ej.: Resumen del Informe anual 2024…", key="q", disabled=ss.processing)

# ------------------ ACCIONES ------------------
# Botón Consultar (único visible)
if not ss.processing:
    if st.button("Consultar"):
        pregunta = ss.get("q", "").strip()
        if not pregunta:
            st.warning("Por favor escribe una pregunta antes de consultar.")
        else:
            ss.pending = {"pregunta": pregunta, "idioma": idioma}
            ss.processing = True
            ss.hist_suffix += 1   # 👈 fuerza recrear el expander (y se colapsa)
            st.rerun()

# Respuesta (última) entre Consultar y (botón oculto de nueva sesión)
# Mostrar respuesta SOLO cuando NO se está procesando
if not ss.processing and ss.log:
    last = ss.log[-1]
    st.markdown(
        f"<div class='answer-card'><p>{last['output']}</p></div>",
        unsafe_allow_html=True
    )

# (BOTÓN NUEVA SESIÓN OCULTO) — funcionalidad disponible vía ?reset=1

# Procesamiento: oculta botón y muestra chip con la pregunta visible
if ss.processing:
    pregunta_actual = (ss.pending or {}).get("pregunta","")
    if pregunta_actual:
        st.markdown(f"<span class='query-chip'>🕑 Consultando: {pregunta_actual}</span>", unsafe_allow_html=True)
    with st.spinner("Consultando al agente... por favor espera."):
        try:
            data = ss.pending or {}
            lang = data.get("idioma","Español")
            if   lang == "English":   sys = "Please respond in English."
            elif lang == "Portugués": sys = "Por favor responda em português."
            else:                     sys = "Responde en español."
            prompt_final = f"{sys}\n{data.get('pregunta','')}"
            resp = call_agente_safe(prompt_final, session_id=ss.session_id, max_steps=8)
            if resp and not ss.session_id and hasattr(resp,"session_id"):
                ss.session_id = resp.session_id
            out = extract_text(resp)
            if out:
                ss.log.append({"input": data.get("pregunta",""), "output": out})
                ss.last_error = None
            else:
                ss.last_error = "No hubo respuesta del agente."
        except Exception as e:
            ss.last_error = f"❌ Error ejecutando el agente: {e}"
        finally:
            ss.processing = False
            ss.pending = None
            # 👇 Mantenemos la pregunta en el input tras la respuesta (no se limpia)
            st.rerun()

# Errores
if ss.last_error:
    st.warning(ss.last_error)

# Historial (colapsable) solo cuando NO se procesa
if not ss.processing and ss.log:
    zws = "\u200B" * ss.hist_suffix   # zero-width space dinámico
    title = f"📜 Historial de interacción{zws}"
    with st.expander(title, expanded=False):
        for i, item in enumerate(ss.log, 1):
            st.markdown(f"**{i}. Pregunta:** {item['input']}")
            st.markdown(f"**Respuesta:** {item['output']}")
            st.markdown("---")
