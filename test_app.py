import streamlit as st
from config import VALORES_BASE_MES, FACTORES_DIVISION
from processor import extract_all_text, process_data
import datetime

st.set_page_config(page_title="Hadita", page_icon="🪄", layout="wide", initial_sidebar_state="collapsed")

# Inject the exact CSS used in the previous step, plus some margin overrides
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding-top: 2rem; max-width: 1360px; }
    
    .hero-title { font-size: 3.5rem; font-weight: 800; letter-spacing: -0.04em; line-height: 1.1; margin-bottom: 0.5rem; color: #0F172A; }
    .hero-subtitle { font-size: 1.1rem; font-weight: 400; color: #475569; letter-spacing: -0.01em; margin-bottom: 2rem; max-width: 600px; }
    
    .section-container {
        background: #FFFFFF; border-radius: 12px; padding: 24px; margin-bottom: 24px;
        box-shadow: rgba(15, 23, 42, 0.06) 0px 4px 16px -2px; border: 1px solid rgb(226, 232, 240);
    }
    .section-header { font-size: 1.25rem; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 8px; color: #0F172A; }
    .section-desc { font-size: 0.85rem; color: #64748B; margin-bottom: 24px; }
    
    div[data-baseweb="input"], div[data-baseweb="base-input"] {
        border-radius: 8px; background-color: rgb(248, 250, 252) !important; border: 1px solid rgb(226, 232, 240) !important;
    }
    label, .st-bv {
        font-weight: 600 !important; color: #334155 !important; text-transform: uppercase; font-size: 0.75rem !important; letter-spacing: 0.05em;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; border-bottom: 1px solid rgb(226, 232, 240); padding-bottom: 10px; }
    .stTabs [data-baseweb="tab"] { padding: 0; font-weight: 500; color: #64748B; font-size: 1rem; }
    .stTabs [aria-selected="true"] { color: #0F172A !important; border-bottom: 2px solid #0F172A !important; }
    
    .stButton>button {
        width: 100%; background-color: #0F172A !important; color: #FFFFFF !important;
        border-radius: 8px !important; height: 56px; font-weight: 600; font-size: 1.05rem;
        letter-spacing: -0.01em; border: none; margin-top: 10px;
        box-shadow: rgba(15, 23, 42, 0.08) 0px 4px 12px -2px; transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stButton>button:hover { transform: translateY(-1px); box-shadow: rgba(15, 23, 42, 0.12) 0px 6px 16px -2px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="color: #0053cf; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">MOTOR DE CONCILIACIÓN BI-FAMILIAR</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Hadita<span style="color:#0053cf;">.</span></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Conciliación financiera, mágicamente simple. Asignación transparente, lectura de extractos bancarios y balance en tiempo real.</div>', unsafe_allow_html=True)

col_left, col_right = st.columns([5, 7], gap="large")

with col_left:
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Ajustes Dinámicos</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Variables macroeconómicas y tipo de cambio para indexación.</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        valor_uf = st.number_input("Colegio SFJ (UF Base)", value=float(VALORES_BASE_MES.get("valor_uf", 37900.0)), step=10.0)
        dolar_val = st.number_input("Dólar Observado", value=VALORES_BASE_MES["valor_dolar"], step=10.0)
    with c2:
        manda_val = st.number_input("Mandarino (CLP)", value=VALORES_BASE_MES["mensualidad_mandarino"], step=1000)
        beneficio_val = st.number_input("Beneficio Empresa", value=VALORES_BASE_MES["beneficio_empleador_por_hijo"], step=1000)
    
    csfj_val = VALORES_BASE_MES.get("uf_colegio", 13.5) * valor_uf
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Ingesta de Cartolas</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Lectura inteligente con categorización semántica inmediata.</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Arrastrar Archivos", "Pegar Texto"])
    with tab1:
        uploaded_files = st.file_uploader("Formato PDF, Excel (.xlsx) o CSV", accept_multiple_files=True, label_visibility="collapsed")
    with tab2:
        pasted_text = st.text_area("Pega aquí la cartola", height=150, label_visibility="collapsed")
    
    procesar = st.button("Procesar Gastos Fijos (Cmd + Enter)")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    if procesar:
        if not uploaded_files and not pasted_text.strip():
            st.error("Por favor, ingresa al menos una fuente de datos.")
        else:
            raw_text = extract_all_text(uploaded_files, pasted_text)
            resultados, fechas = process_data(raw_text, dolar_val, csfj_val, manda_val, beneficio_val)
            
            total = sum(resultados.values())
            papa = int(total * FACTORES_DIVISION['PAPA'])
            mama = int(total * FACTORES_DIVISION['MAMA'])
            
            # Read the right column HTML directly from code.html
            with open("stitch_ui/code.html", "r") as f:
                html_full = f.read()
            
            # Extract just the <head> and the Right Column
            head_part = html_full.split("</head>")[0] + "</head>"
            right_col = html_full.split('<!-- RIGHT COLUMN: Reconciliation & Allocation (~58%) -->')[1]
            right_col = right_col.split('<!-- Antigravity Direct Status Pill Container -->')[0]
            
            # Inject Tailwind fix for iframe
            head_part = head_part.replace('tailwind.config = {', 'tailwind.config = { corePlugins: { preflight: false },')
            
            # We will render the right column in an iframe using components.html!
            # Since the data is dynamic, we SHOULD replace the values in the right_col string.
            # But parsing and replacing all items in right_col is tricky if the items change.
            # It's better to rebuild the inner HTML of the list manually using the same tailwind classes.
            pass
