from pathlib import Path
logo_b64 = Path(__file__).with_name("logo_base64.txt").read_text().strip()
import re
import streamlit as st
import pandas as pd
import datetime
from variables_processor import process_unmatched_to_df
from gmail_fetcher import fetch_bice_transfers_from_gmail
import database
from config import VALORES_BASE_MES, FACTORES_DIVISION
from processor_v3 import extract_all_text, process_data, reconcile, summarize
from training_ui import active_rules, refresh_results, stored_rules
from workflow import learn_variable_corrections
from utils import format_clp, standardize_date, fetch_indicators
from sheets_exporter import export_to_sheets
import streamlit.components.v1 as components

st.set_page_config(page_title="Hadita", page_icon="🪄", layout="wide", initial_sidebar_state="collapsed")

components.html("""
<script>
    if (!window.parent.document.getElementById('material-fonts-script')) {
        const fonts = window.parent.document.createElement('link');
        fonts.id = 'material-fonts-script';
        fonts.rel = 'stylesheet';
        fonts.href = 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200';
        window.parent.document.head.appendChild(fonts);
    }
</script>
""", height=0, width=0)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }
    
    /* Clean up top padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 1100px !important;
    }
    
    
    /* Global font-family enforce */
    html, body, [class*="css"], [class*="st-"]:not(svg):not(path):not([data-testid="stIconMaterial"]):not(.material-symbols-rounded) {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Protect Material Icons */
    .stIcon, .material-symbols-outlined, .material-symbols-rounded, .material-icons, 
    [data-testid="stIconMaterial"], [data-testid="stExpanderToggleIcon"] {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons", sans-serif !important;
        font-weight: 400 !important;
        font-style: normal !important;
        text-transform: none !important;
        letter-spacing: normal !important;
        line-height: 1 !important;
    }
    
    /* File Uploader Translation and Typography */
    [data-testid="stFileUploadDropzone"] {
        padding: 24px !important;
        border-radius: 16px !important;
    }
    
    /* Drag and drop files here */
    [data-testid="stFileUploaderDropzoneInstructions"] > div > span:nth-child(1) {
        font-size: 0px !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] > div > span:nth-child(1)::after {
        content: "Arrastra y suelta tus archivos aquí";
        font-size: 12px !important;
        line-height: 16px !important;
        font-weight: 500 !important;
        color: #1D1D1F !important;
        visibility: visible;
        display: block;
        margin-bottom: 4px;
    }
    
    /* Limit 200MB per file */
    [data-testid="stFileUploaderDropzoneInstructions"] > div > span:nth-child(2) {
        font-size: 0px !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] > div > span:nth-child(2)::after {
        content: "Límite 200MB por archivo";
        font-size: 12px !important;
        color: #86868B !important;
        visibility: visible;
        display: block;
    }
    
    [data-testid="stFileUploaderDropzone"] {
        box-sizing: border-box !important;
        min-width: 0 !important;
        max-width: 100% !important;
        padding: 12px !important;
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 12px !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"],
    [data-testid="stFileUploaderDropzoneInstructions"] > div {
        min-width: 0 !important;
        max-width: 100% !important;
        white-space: normal !important;
        overflow-wrap: anywhere;
    }
    [data-testid="stFileUploaderDropzone"] button > * {
        display: none !important;
    }
    [data-testid="stFileUploaderDropzone"] button {
        box-sizing: border-box !important;
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        white-space: nowrap !important;
        overflow: hidden !important;
    }
    /* Browse files button */
    [data-testid="stFileUploaderDropzone"] button {
        font-size: 0px !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
        background: #FFFFFF !important;
    }
    [data-testid="stFileUploaderDropzone"] button::after {
        content: "Subir";
        font-size: 12px !important;
        font-weight: 500 !important;
        color: #1D1D1F !important;
        visibility: visible;
    }
    [data-testid="stFileUploaderDropzone"] button:hover {
        background: #F5F5F7 !important;
        border: 1px solid rgba(0,0,0,0.15) !important;
    }

    /* Header and Title */
    h1 {
        font-weight: 700 !important;
        letter-spacing: -0.025em;
        color: #1D1D1F !important;
        text-align: center;
    }
    
    /* Hide default radio buttons and style as pills */
    div[data-testid="stRadio"], div[data-testid="stRadioGroup"] {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 20px;
    }
    div[data-testid="stRadio"] > div, div[data-testid="stRadioGroup"] > div {
        display: inline-flex !important;
        flex-direction: row !important;
        background: #E8E8ED !important;
        border-radius: 9999px !important;
        padding: 4px !important;
        gap: 4px !important;
    }
    div[data-testid="stRadio"] label, div[data-testid="stRadioGroup"] label {
        padding: 8px 20px !important;
        border-radius: 9999px !important;
        background: transparent !important;
        color: #86868B !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        cursor: pointer;
        transition: all 0.2s ease;
        border: none !important;
    }
    /* Streamlit hides the radio input, we target the checked state via aria-checked */
    div[data-testid="stRadio"] label[data-checked="true"], div[data-testid="stRadioGroup"] label[data-selected="true"] {
        background: #FFFFFF !important;
        color: #1D1D1F !important;
        box-shadow: 0 2px 8px -1px rgba(0, 0, 0, 0.04) !important;
    }
    div[data-testid="stRadio"] label:hover:not([data-checked="true"]), div[data-testid="stRadioGroup"] label:hover:not([data-selected="true"]) {
        color: #1D1D1F !important;
    }
    /* Hide the circle icon next to radio labels robustly */
    div[data-testid="stRadio"] .st-emotion-cache-1n76uvr, div[data-testid="stRadio"] .st-emotion-cache-9hdc3e, div[data-testid="stRadio"] .e1326t814, div[data-testid="stRadioGroup"] label[data-testid="stRadioOption"] > div > div:first-child {
        display: none !important;
    }
    
    /* Expander / Cards */
    section[data-testid="stExpander"], div[data-testid="stVerticalBlock"] > div.element-container > div > section {
        border: 1px solid rgba(0,0,0,0.07) !important;
        border-radius: 24px !important;
        background: #FFFFFF !important;
        box-shadow: 0 4px 24px -2px rgba(0,0,0,0.04) !important;
    }
    
    /* Primary Button */
    .stButton>button {
        background-color: #7C3AED !important;
        color: #FFFFFF !important;
        border-radius: 16px !important;
        border: none !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.15s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #6D28D9 !important;
        transform: scale(0.99);
    }
    
    /* Inputs */
    .stSelectbox>div>div, .stTextInput>div>div, .stNumberInput>div>div {
        border-radius: 12px !important;
        border: 1px solid rgba(0,0,0,0.07) !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)




st.markdown(re.sub(r'^[ \t]+', '', r'''
<div style="display: flex; flex-direction: column; gap: 8px; margin-top: 16px; margin-bottom: 24px;">
    <div style="display: flex; align-items: center; gap: 8px; font-size: 11px; font-weight: 700; letter-spacing: 0.05em; color: #0071E3; text-transform: uppercase;">
        <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background-color: #0071E3;"></span>
        <span>Motor de Conciliación Bi-Familiar</span>
    </div>
    <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 16px;">
        <img src="data:image/png;base64,''' + logo_b64 + r'''" style="height: 48px; width: auto; object-fit: contain;">
        <h1 style="font-size: 48px; font-weight: 700; color: #1D1D1F; letter-spacing: -0.04em; margin: 0; line-height: 1;">
            Hadita de las cuentas<span style="color: #0071E3;">.</span>
        </h1>
    </div>
    <p style="font-size: 15px; color: #86868B; margin: 8px 0 0 0; max-width: 600px; line-height: 1.4;">
        Conciliación financiera, mágicamente simple. Asignación transparente, lectura de extractos bancarios y balance en tiempo real.
    </p>
</div>
''', flags=re.MULTILINE), unsafe_allow_html=True)
page = st.radio("Navegación", ["Gastos Fijos", "Gastos Variables", "Pago Cuota Casa", "Historial", "Entrenar gastos"], horizontal=True, label_visibility="collapsed")
st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)

if page == "Gastos Fijos":
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    col_left, col_right = st.columns([1, 1.2], gap="large")
    with col_left:

        def reset_confirm():
            st.session_state.periodo_confirmado = False
            for key in ['resultados_fijos','unmatched','records','fechas_fijas','edited_variables']:
                st.session_state.pop(key,None)

        if "periodo_confirmado" not in st.session_state:
            st.session_state.periodo_confirmado = False
            
        col_m1, col_m2, col_m3 = st.columns([1.5, 1, 0.5])
        with col_m1:
            sel_mes = st.selectbox("Mes de Análisis", meses, index=7, label_visibility="collapsed", on_change=reset_confirm)
        with col_m2:
            sel_ano = st.selectbox("Año", [2024, 2025, 2026, 2027], index=2, label_visibility="collapsed", on_change=reset_confirm)
            
        month_str = f"{sel_mes} {sel_ano}"
        st.session_state.current_month_str = month_str

        live_uf, live_dolar = 38000, 950 # default
        
        with col_m3:
            if not st.session_state.periodo_confirmado:
                if st.button("✓", help="Confirmar período", type="primary", use_container_width=True):
                    st.session_state.periodo_confirmado = True
                    st.rerun()
                valor_uf = float(live_uf)
                dolar_val = float(live_dolar)
                manda_val = VALORES_BASE_MES["mensualidad_mandarino"]
                beneficio_val = VALORES_BASE_MES["beneficio_empleador_por_hijo"]
                manda_mat_val = VALORES_BASE_MES.get("jardin_mandarino_materiales", 0)
                pdf_password = ""
            else:
                live_uf, live_dolar = fetch_indicators()
                valor_uf = float(live_uf)
                dolar_val = float(live_dolar)
                manda_val = VALORES_BASE_MES["mensualidad_mandarino"]
                manda_mat_val = VALORES_BASE_MES.get("jardin_mandarino_materiales", 0)
                with st.popover("⚙️", help="Ajustes y Contraseñas"):
                    beneficio_val = st.number_input("Beneficio Empresa", value=VALORES_BASE_MES["beneficio_empleador_por_hijo"], step=1000, help="Monto de la bonificación o subsidio de sala cuna/escolaridad que entrega la empresa. Se restará del costo final a pagar.")
                    pdf_password = st.text_input("Contraseña PDF (Opcional)", type="password", key="pdf_password_input", help="Si tu banco te envía la cartola protegida, ingresa aquí la clave (suele ser tu RUT) para que el sistema pueda leer el archivo.")
        
        procesar = False
        if st.session_state.periodo_confirmado:
            st.markdown("""
            <style>
            @keyframes fadeInDown {
                from { opacity: 0; transform: translateY(-10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .fade-in-title, div[data-testid="stFileUploader"], div[data-testid="stTextArea"], div.stButton > button[kind="primary"] {
                animation: fadeInDown 1.2s cubic-bezier(0.22, 1, 0.36, 1) forwards;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown(re.sub(r'^[ 	]+', '', r"""
            <div class="fade-in-title" style="margin-bottom: 24px; margin-top: 24px;">
                <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.05em; color: #86868B; text-transform: uppercase;">Importación Asistida</span>
                <h2 style="font-size: 24px; font-weight: 700; color: #1D1D1F; margin: 4px 0 0 0; letter-spacing: -0.02em;">Ingreso de Cartolas</h2>
                <p style="font-size: 13px; color: #86868B; margin: 4px 0 0 0;">Lectura inteligente con categorización semántica inmediata.</p>
            </div>
            """, flags=re.MULTILINE), unsafe_allow_html=True)
        
            with st.container():
                st.markdown("<div class='fade-in-title'><span style='font-size:11px; font-weight:600; color:#4c4546;'>Cartola PDF o Excel (Manual)</span></div>", unsafe_allow_html=True)
                uploaded_files = st.file_uploader("Arrastra tu cartola", accept_multiple_files=True, label_visibility="collapsed")
            with st.container():
                st.markdown("<div class='fade-in-title'><span style='font-size:11px; font-weight:600; color:#4c4546;'>Automático</span></div>", unsafe_allow_html=True)
                buscar_email = st.button("📥 Buscar en mi Gmail", use_container_width=True)

            st.markdown("<div class='fade-in-title'><span style='font-size:11px; font-weight:600; color:#4c4546; margin-top:10px; display:inline-block;'>O pega el texto aquí</span></div>", unsafe_allow_html=True)
            pasted_text = st.text_area("Pega aquí la cartola", height=120, label_visibility="collapsed")
        
            procesar = st.button("Procesar Cartola Bancaria", type="primary", use_container_width=True)
            
            if buscar_email:
                with st.spinner("Buscando cartolas del mes en tu correo..."):
                    from gmail_fetcher import fetch_statement_pdfs_from_gmail
                    try:
                        fetched_pdfs = fetch_statement_pdfs_from_gmail(sel_mes, int(sel_ano), st.session_state.get("pdf_password_input", ""))
                    except (ValueError, RuntimeError) as e:
                        st.error(str(e)); st.stop()
                    if fetched_pdfs:
                        st.success(f"¡Se extrajeron {len(fetched_pdfs)} cartolas de tu Gmail!")
                        uploaded_files = fetched_pdfs
                        procesar = True
                    else:
                        st.error("No se encontraron correos del BICE para ese mes. Intenta subir el PDF manualmente.")
        
        csfj_val = VALORES_BASE_MES.get("uf_colegio", 13.5) * valor_uf

    with col_right:
        if procesar:
            if not uploaded_files and not pasted_text.strip():
                st.error("Por favor, ingresa al menos una fuente de datos.")
            else:
                import random
                mensajes_procesamiento = [
                    "Despertando a los duendes contables...",
                    "Traduciendo el lenguaje del banco a español...",
                    "Buscando los gastos escondidos en el PDF...",
                    "Inyectando café en el procesador...",
                    "Sacando la calculadora científica...",
                    "Leyendo la letra chica de la cartola..."
                ]
                try:
                    with st.spinner(random.choice(mensajes_procesamiento)):
                        raw_text = extract_all_text(uploaded_files, pasted_text, st.session_state.get("pdf_password_input", ""))
                except Exception as e:
                    import traceback
                    pass
                    traceback.print_exc()
                    st.error(f"Error ({type(e).__name__}): {str(e) or 'Ocurrió un error (el mensaje original está vacío)'}")
                    st.stop()
                try:
                    records = reconcile(raw_text, dolar_val, int(sel_ano), rules=active_rules())
                except ValueError as e:
                    st.error(str(e)); st.stop()
                notices=sorted({r['Estado'] for r in records if r['Estado']})
                for notice in notices: st.warning(notice)
                st.session_state.records = records
                st.session_state.beneficio_aplicado = beneficio_val
                resultados, fechas = summarize(records, beneficio_val)
                unmatched = [r for r in records if r['Tipo'] != 'Fijo']
                st.session_state.unmatched = unmatched
                st.session_state.fechas_fijas = fechas
                st.session_state.pop('edited_variables', None)

                # DATE WARNING LOGIC
                from datetime import datetime, timedelta
                import calendar
                meses_lista = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
                target_month = meses_lista.index(sel_mes) + 1
                target_year = int(sel_ano)
                _, last_day = calendar.monthrange(target_year, target_month)
                start_date = datetime(target_year, target_month, 1) - timedelta(days=35)
                end_date = datetime(target_year, target_month, last_day) + timedelta(days=5)
                
                fixed_inside_month = False
                out_of_bounds_count = 0
                
                # Check fixed expenses
                for k, v in fechas.items():
                    if not v or v == "N/A": continue
                    try:
                        dt = datetime.strptime(v, "%d/%m/%Y")
                        if dt.month == target_month and dt.year == target_year:
                            fixed_inside_month = True
                        if not (start_date <= dt <= end_date):
                            out_of_bounds_count += 1
                    except:
                        pass
                        
                # Check unmatched
                for item in unmatched:
                    v = item.get("Fecha")
                    if not v or v == "N/A": continue
                    try:
                        dt = datetime.strptime(v, "%d/%m/%Y")
                        if not (start_date <= dt <= end_date):
                            out_of_bounds_count += 1
                    except:
                        pass
                
                if out_of_bounds_count > 0 and not fixed_inside_month:
                    st.warning(f"⚠️ **Advertencia de fechas:** Se encontraron {out_of_bounds_count} gastos fuera del mes seleccionado ({sel_mes} {sel_ano}) por más de 5 días de margen, y no se detectó ningún gasto fijo dentro del mes. Asegúrate de estar subiendo la cartola correcta.")
            
                total = sum(resultados.values())
                papa = int(total * FACTORES_DIVISION['PAPA'])
                mama = int(total * FACTORES_DIVISION['MAMA'])
            
                icons = {
                    "AGUAS": "water_drop", "LUZ": "bolt", "ENEL": "bolt", "GAS": "mode_heat", "METROGAS": "mode_heat",
                    "CSFJ": "school", "COLEGIO": "school", "YOUTUBE": "devices", "SPOTIFY": "devices",
                    "NETFLIX": "devices", "AMAZON": "devices", "ZAPPING": "devices", "HBO": "devices",
                    "GASTOS COMUNES": "apartment", "MANDARINO": "home_work", "ASEO": "cleaning_services",
                    "INTERNET": "wifi", "VTR": "wifi", "GTD": "wifi", "CONSORCIO": "security"
                }
                def get_icon(n):
                    for k, v in icons.items():
                        if k in n.upper(): return v
                    return "receipt_long"
            
                                # --- Right Column Apple Style HTML ---
                out = f"""
                <section style="background: #FFFFFF; border-radius: 24px; padding: 32px; border: 1px solid rgba(0,0,0,0.07); box-shadow: 0 4px 24px -2px rgba(0,0,0,0.04); margin-bottom: 24px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid rgba(0,0,0,0.05); padding-bottom: 20px; margin-bottom: 16px;">
                        <div>
                            <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.05em; color: #86868B; text-transform: uppercase;">Balance Consolidado</span>
                            <h2 style="font-size: 24px; font-weight: 700; color: #1D1D1F; margin: 4px 0 0 0; letter-spacing: -0.02em;">Desglose Detectado</h2>
                            <p style="font-size: 13px; color: #86868B; margin: 4px 0 0 0;">Gastos directos e indexados asignados a la cuenta compartida.</p>
                        </div>
                        <span style="background: #F5F5F7; color: #1D1D1F; padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 600; border: 1px solid rgba(0,0,0,0.05);">
                            {sum(v > 0 for v in resultados.values())} gastos reconocidos
                        </span>
                    </div>
                    <div style="max-height: 580px; overflow-y: auto;">
                """
                
                for k, v in resultados.items():
                    pill_html = ""
                    original_amount_html = ""
                    if beneficio_val > 0 and (k == "CSFJ (Mensualidad)" or k == "MANDARINO"):
                        pill_html = f'''<div style="background: #e8f5e9; color: #1b5e20; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin-top: 4px; display: inline-block; font-weight: 600; border: 1px solid #c8e6c9;">Beneficio empresa -$ {format_clp(beneficio_val)}</div>'''
                        original_amount_html = f'''<div style="font-size: 11px; color: #86868B; text-decoration: line-through; margin-top: 2px; text-align: right;">$ {format_clp(v + beneficio_val)}</div>'''
                    
                    out += f"""
                    <article style="display: flex; justify-content: space-between; align-items: center; padding: 12px 8px; border-bottom: 1px solid rgba(0,0,0,0.03);">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <div style="width: 36px; height: 36px; border-radius: 50%; background: #F5F5F7; display: flex; align-items: center; justify-content: center; color: #1D1D1F;">
                                <span class="material-symbols-outlined" style="font-size: 18px;">{get_icon(k)}</span>
                            </div>
                            <div>
                                <h3 style="margin: 0; font-size: 14px; font-weight: 600; color: #1D1D1F;">{k}</h3>
                                <p style="margin: 0; font-size: 11px; color: #86868B;">Detectado aut. • {standardize_date(fechas.get(k, 'N/A'))}</p>
                                {pill_html}
                            </div>
                        </div>
                        <div style="display: flex; flex-direction: column; align-items: flex-end;">
                            <span style="font-size: 14px; font-weight: 600; color: #1D1D1F; letter-spacing: -0.01em;">$ {format_clp(v)}</span>
                            {original_amount_html}
                        </div>
                    </article>
                    """
                
                if beneficio_val > 0 and resultados.get("CSFJ (Mensualidad)", 0) > 0:
                    out += f"""
                    <article style="display: flex; justify-content: space-between; align-items: center; padding: 14px; margin-top: 16px; border-radius: 16px; background: #F0F6FF; border: 1px solid rgba(0,113,227,0.1);">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <div style="width: 36px; height: 36px; border-radius: 50%; background: #0071E3; display: flex; align-items: center; justify-content: center; color: #FFF; box-shadow: 0 2px 8px rgba(0,113,227,0.3);">
                                <span class="material-symbols-outlined" style="font-size: 18px;">redeem</span>
                            </div>
                            <div>
                                <h3 style="margin: 0; font-size: 14px; font-weight: 600; color: #0071E3;">Beneficio Empresa</h3>
                                <p style="margin: 0; font-size: 11px; color: rgba(0,113,227,0.8);">Reembolso aplicado</p>
                            </div>
                        </div>
                        <span style="font-size: 14px; font-weight: 700; color: #0071E3; letter-spacing: -0.01em;">-$ {format_clp(beneficio_val)}</span>
                    </article>
                    """
                    
                papa_pct = (papa / total) * 100 if total > 0 else 0
                mama_pct = (mama / total) * 100 if total > 0 else 0

                out += f"""
                    </div>
                    
                    <div style="margin-top: 24px; padding: 24px; border-radius: 16px; background: #FAFAFC; border: 1px solid rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.05em; color: #86868B; text-transform: uppercase;">Consolidado Actual</span>
                            <div style="font-size: 16px; font-weight: 500; color: #1D1D1F; margin-top: 2px;">Total Gastos Fijos Netos</div>
                        </div>
                        <div style="font-size: 26px; font-weight: 800; color: #1D1D1F; letter-spacing: -0.03em; white-space: nowrap;">
                            $ {format_clp(total)}<span style="font-size: 11px; font-weight: 600; color: #86868B; margin-left: 4px;">CLP</span>
                        </div>
                    </div>
                    
                    <div style="margin-top: 24px; padding-top: 24px; border-top: 1px solid rgba(0,0,0,0.05);">
                        <div style="margin-bottom: 16px;">
                            <span style="font-size: 10px; font-weight: 700; letter-spacing: 0.05em; color: #86868B; text-transform: uppercase;">Acuerdo Bi-Parental</span>
                            <h4 style="font-size: 14px; font-weight: 700; color: #1D1D1F; margin: 4px 0 0 0;">Reparto Proporcional Acordado</h4>
                        </div>
                        
                        <div style="width: 100%; height: 10px; background: #F5F5F7; border-radius: 9999px; display: flex; overflow: hidden; margin-bottom: 20px; box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);">
                            <div style="height: 100%; background: #0071E3; width: {papa_pct}%;"></div>
                            <div style="height: 100%; background: #7C3AED; width: {mama_pct}%;"></div>
                        </div>
                        
                        <div style="display: flex; flex-wrap: wrap; gap: 16px;">
                            <!-- Replaced grid with flex for mobile responsiveness -->
                            <div style="flex: 1; min-width: 200px; background: rgba(0,113,227,0.05); border: 1px solid rgba(0,113,227,0.15); padding: 16px; border-radius: 16px;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                                    <div style="display: flex; align-items: center; gap: 8px;">
                                        <div style="width: 24px; height: 24px; border-radius: 50%; background: #0071E3; color: white; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700;">P</div>
                                        <span style="font-size: 12px; font-weight: 600; color: #1D1D1F;">Cuota Papá</span>
                                    </div>
                                    <span style="font-size: 11px; font-weight: 700; background: #0071E3; color: white; padding: 2px 8px; border-radius: 9999px;">{papa_pct:.2f}%</span>
                                </div>
                                <div style="font-size: 22px; font-weight: 700; color: #1D1D1F; letter-spacing: -0.02em;">$ {format_clp(papa)}</div>
                                <div style="font-size: 10px; color: #86868B; margin-top: 4px;">Asignación automática neta</div>
                            </div>
                            
                            <div style="flex: 1; min-width: 200px; background: rgba(124,58,237,0.05); border: 1px solid rgba(124,58,237,0.15); padding: 16px; border-radius: 16px;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                                    <div style="display: flex; align-items: center; gap: 8px;">
                                        <div style="width: 24px; height: 24px; border-radius: 50%; background: #7C3AED; color: white; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700;">M</div>
                                        <span style="font-size: 12px; font-weight: 600; color: #1D1D1F;">Deuda Mamá</span>
                                    </div>
                                    <span style="font-size: 11px; font-weight: 700; background: #7C3AED; color: white; padding: 2px 8px; border-radius: 9999px;">{mama_pct:.2f}%</span>
                                </div>
                                <div style="font-size: 22px; font-weight: 700; color: #1D1D1F; letter-spacing: -0.02em;">$ {format_clp(mama)}</div>
                                <div style="font-size: 10px; color: #86868B; margin-top: 4px;">Por transferir a cuenta origen</div>
                            </div>
                        </div>
                    </div>
                </section>
                """
                
                # --- End Apple Style HTML ---
                st.markdown(re.sub(r'^[ \t]+', '', out, flags=re.MULTILINE), unsafe_allow_html=True)

                st.toast('✨ ¡Cálculo mágico completado con éxito!', icon='🪄')
                st.session_state.resultados_fijos = resultados
                
                
                # Alertas de gastos faltantes
                mandatory = [
                    "YOUTUBE PREMIUM", "GASTOS COMUNES (Khipu)", "PISCINA (Andy)", 
                    "AGUA (Aguas Andinas)", "LUZ (Enel)", "ZAPPING", "GAS (Metrogas)", 
                    "SPOTIFY DUO", "INTERNET (GTD)", "SEGURO CASA (Consorcio)", "MANDARINO"
                ]
                missing = []
                for m in mandatory:
                    if resultados.get(m, 0) == 0:
                        missing.append(m)
                        
                # CSFJ varies by month
                if sel_mes not in ["Enero", "Febrero"]:
                    if resultados.get("CSFJ (Mensualidad)", 0) == 0:
                        missing.append("CSFJ (Mensualidad)")
                    if resultados.get("CSFJ (Jornada Extendida)", 0) == 0:
                        missing.append("CSFJ (Jornada Extendida)")
                        
                if missing:
                    st.warning("⚠️ **Faltan los siguientes gastos obligatorios en este mes:**\n" + "\n".join([f"- {m}" for m in missing]))





    if not procesar and 'resultados_fijos' in st.session_state:
        with col_right:
            import pandas as pd
            st.subheader('Desglose guardado en esta sesión')
            st.dataframe(pd.DataFrame([{'Gasto fijo':k,'Monto CLP':v} for k,v in st.session_state.resultados_fijos.items() if v]),hide_index=True,use_container_width=True)
    if 'resultados_fijos' in st.session_state:
        if st.button('Guardar conciliación e historial'):
            try:
                import json
                rows=st.session_state.get('records',[])
                state={'period':st.session_state.current_month_str,'records':rows,'beneficio':st.session_state.get('beneficio_aplicado',0)}
                database.save_reconciliation(database.get_db(),state)
                st.success('Conciliación e historial guardados.')
            except Exception:
                st.error('No se pudo guardar en Firebase. Tus resultados siguen en esta sesión.')
        st.info('Los cobros del colegio sin concepto explícito se revisan en Entrenar gastos. Allí también puedes corregir y aprender cualquier gasto fijo.')

elif page == "Entrenar gastos":
    from training_ui import render
    render()

elif page == "Gastos Variables":
    st.header("Gastos Variables, Abonos y Entrenamiento")
    if 'unmatched' in st.session_state and st.session_state.unmatched:
        import random
        mensajes_clasificacion = [
            "Llamando a la IA para que haga el trabajo sucio...",
            "Aplicando tus reglas maestras de entrenamiento...",
            "Decidiendo si ese minimarket fue un 'Gustito'...",
            "Consultando la bola de cristal de los gastos...",
            "Acomodando los abonos en la sección correcta...",
            "Alineando los chakras financieros..."
        ]
        with st.spinner(random.choice(mensajes_clasificacion)):
            df_vars = st.session_state.get("edited_variables")
            if df_vars is None: df_vars = process_unmatched_to_df(st.session_state.unmatched)
            
        # Keep unreadable movements visible so users can correct their amounts.
        df_vars = df_vars.copy()
        missing_amount = pd.to_numeric(df_vars['Monto'], errors='coerce').isna()
        if missing_amount.any():
            df_vars.loc[missing_amount, 'Categoría'] = 'Por Revisar'
            st.warning(f'{int(missing_amount.sum())} movimientos sin monto legible. Revísalos antes de guardar.')

        # Split DataFrames
        if "_Original" not in df_vars.columns: df_vars["_Original"] = df_vars["Descripción"]
        df_ingresos = df_vars[df_vars["Categoría"] == "Ingresos"].reset_index(drop=True)
        df_no_identificados = df_vars[df_vars["Categoría"] == "Por Revisar"].reset_index(drop=True).copy()
        
        # Enrich only unclassified transfers, retaining raw text and learned rules.
        try:
            if 'gmail' in st.secrets and not df_no_identificados.empty:
                period=st.session_state.get('current_month_str')
                cache=st.session_state.setdefault('bice_transfer_emails',{})
                if period not in cache:cache[period]=fetch_bice_transfers_from_gmail(period)
                from bice_email import enrich_transfers
                df_no_identificados=pd.DataFrame(enrich_transfers(df_no_identificados.to_dict('records'),cache[period]))
        except Exception:
            st.warning('No se pudieron consultar los mensajes BICE. Puedes continuar clasificando; tus datos no se han cambiado.')
        df_identificados = df_vars[(df_vars["Categoría"] != "Ingresos") & (df_vars["Categoría"] != "Por Revisar") & (df_vars["Categoría"] != "Ignorar")].reset_index(drop=True)
        
        col_config = {
            "Categoría": st.column_config.TextColumn(
                "Categoría (editable)",
                help="Escribe la categoría que desees",
                width="medium"
            ),
            "Responsable": st.column_config.SelectboxColumn(
                "Responsabilidad",
                help="Quién asume este gasto",
                width="small",
                options=["Compartido", "Personal", "Por Revisar"]
            ),
            "Monto": st.column_config.NumberColumn(
                "Monto ($)",
                help="Valor de la transacción",
                format="$ %d"
            ),
            "Descripción": st.column_config.TextColumn(
                "Descripción",
                width="large"
            ),
            "_Original": None
        }
        
        st.subheader("⚠️ Gastos Pendientes por Entrenar", help="Todo lo que clasifiques y guardes en esta tabla, el sistema intentará aprenderlo como una regla automática para el futuro. Si no estás seguro de algo, déjalo en 'Por Revisar'.")
        st.markdown("Clasifica estos gastos. El sistema aprenderá automáticamente para la próxima vez.")
        edited_no_identificados = st.data_editor(
            df_no_identificados,
            column_config=col_config,
            hide_index=True,
            use_container_width=True,
            key="editor_no_id"
        )
        if not edited_no_identificados.empty:
            st.markdown(f"<p style='text-align:right; font-weight:600; font-size:15px; color:#1D1D1F;'>Total Pendientes: $ {format_clp(edited_no_identificados['Monto'].sum())}</p>", unsafe_allow_html=True)
        
        st.subheader("✅ Gastos Identificados (Compartidos)")
        st.markdown("Gastos que el sistema reconoce como responsabilidad Compartida.")
        df_identificados_comp = df_identificados[df_identificados["Responsable"] == "Compartido"].reset_index(drop=True)
        edited_comp = st.data_editor(
            df_identificados_comp,
            column_config=col_config,
            hide_index=True,
            use_container_width=True,
            key="editor_id_comp"
        )
        if not edited_comp.empty:
            st.markdown(f"<p style='text-align:right; font-weight:600; font-size:15px; color:#1D1D1F;'>Total Compartidos: $ {format_clp(edited_comp['Monto'].sum())}</p>", unsafe_allow_html=True)
            
        st.subheader("✅ Gastos Identificados (Personales / Otros)")
        st.markdown("Gastos que el sistema reconoce como responsabilidad Personal u otra.")
        df_identificados_pers = df_identificados[df_identificados["Responsable"] != "Compartido"].reset_index(drop=True)
        edited_pers = st.data_editor(
            df_identificados_pers,
            column_config=col_config,
            hide_index=True,
            use_container_width=True,
            key="editor_id_pers"
        )
        if not edited_pers.empty:
            st.markdown(f"<p style='text-align:right; font-weight:600; font-size:15px; color:#1D1D1F;'>Total Personales: $ {format_clp(edited_pers['Monto'].sum())}</p>", unsafe_allow_html=True)
            
        import pandas as pd
        edited_identificados = pd.concat([edited_comp, edited_pers], ignore_index=True)
        
        st.subheader("💰 Abonos / Ingresos")
        st.markdown("Transferencias recibidas o abonos detectados.")
        edited_ingresos = st.data_editor(
            df_ingresos,
            column_config=col_config,
            hide_index=True,
            use_container_width=True,
            key="editor_ingresos"
        )
        if not edited_ingresos.empty:
            st.markdown(f"<p style='text-align:right; font-weight:600; font-size:15px; color:#1D1D1F;'>Total Ingresos: $ {format_clp(edited_ingresos['Monto'].sum())}</p>", unsafe_allow_html=True)
        
        # Combine back into a single dataframe for saving
        import pandas as pd
        edited_df = pd.concat([edited_no_identificados, edited_identificados, edited_ingresos, df_vars[df_vars['Categoría']=='Ignorar']], ignore_index=True)
        edited_df['Tipo'] = edited_df['Categoría'].map(lambda c: 'Ingreso' if c=='Ingresos' else ('Ignorar' if c=='Ignorar' else ('Revisar' if c=='Por Revisar' else 'Variable')))
        # Keep _Original in edited_df for training logic
        edited_df_clean = edited_df.drop(columns=["_Original"]) if "_Original" in edited_df.columns else edited_df
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Guardar correcciones y aprender"):
                month_to_save = st.session_state.get('current_month_str', 'Desconocido')
                db = database.get_db()
                if db:
                    try:
                        saved, revision = stored_rules()
                        baseline = process_unmatched_to_df(st.session_state.unmatched)
                        candidate, learned, skipped = learn_variable_corrections(baseline.to_dict('records'), edited_df.to_dict('records'), saved)
                        revision = database.save_rulebook(db, candidate, revision, variables=(month_to_save, edited_df_clean))
                    except Exception as e:
                        st.error(str(e) if isinstance(e, ValueError) else "No se pudo guardar. Tus cambios siguen en la tabla; reintenta la conexión.")
                        st.stop()
                    st.session_state.saved_rules = candidate
                    st.session_state.rule_revision = revision
                    
                    st.session_state.edited_variables = edited_df.copy()
                    reviewed={r.get('_Original',r['Descripción']):r for r in edited_df.to_dict('records')}
                    for record in st.session_state.get('records',[]):
                        changed=reviewed.get(record['_Original'])
                        if changed:
                            record.update({k:changed[k] for k in ['Descripción','Monto','Categoría','Responsable']})
                            record['Tipo']='Ingreso' if changed['Categoría']=='Ingresos' else ('Ignorar' if changed['Categoría']=='Ignorar' else ('Revisar' if changed['Categoría']=='Por Revisar' else 'Variable'))
                            record['Revisado']=True
                    st.success(f"{learned} reglas aprendidas para próximas cartolas.")
                    if skipped: st.warning(f"{skipped} correcciones se guardaron solo para este mes porque no se pudo identificar un comercio o destinatario seguro.")

                    st.success(f"¡Gastos Variables de {month_to_save} guardados en Firebase!")

        with col2:
            import io
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                # 3 sheets exactly as requested
                def drop_orig(df):
                    return df.drop(columns=["_Original"]) if "_Original" in df.columns else df
                    
                drop_orig(edited_identificados).to_excel(writer, index=False, sheet_name="Gastos")
                drop_orig(edited_ingresos).to_excel(writer, index=False, sheet_name="Abonos")
                drop_orig(edited_no_identificados).to_excel(writer, index=False, sheet_name="Gastos no identificados")
                
            st.download_button(
                label="📊 Exportar a Excel",
                data=excel_buffer.getvalue(),
                file_name=f"Gastos_Variables_{st.session_state.get('current_month_str', 'Mes')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #1D1D1F;'>Exportar a Archivo Maestro</h3>", unsafe_allow_html=True)
        
        col_space1, col_exp, col_space2 = st.columns([1, 2, 1])
        with col_exp:
            gcp_secrets = st.secrets.get("gcp_service_account", {})
            if "private_key" in gcp_secrets:
                if "master_sheet_url" not in gcp_secrets:
                    st.warning("Falta agregar `master_sheet_url` en tus secretos de Streamlit (debajo de private_key).")
                else:
                    if st.button("Subir mes a Google Sheets", type="primary", use_container_width=True):
                        with st.spinner("Conectando con tu archivo maestro... (esto puede tomar unos segundos)"):
                            new_url = export_to_sheets(
                                st.session_state.resultados_fijos, 
                                edited_identificados, 
                                edited_no_identificados, 
                                edited_ingresos
                            )
                            if new_url:
                                st.success(f"¡Listo! Pestañas del mes agregadas exitosamente.")
                                st.markdown(f"**[Haz clic aquí para ir a tu Archivo Maestro]({new_url})**", unsafe_allow_html=True)
                                
                    st.markdown("<p style='font-size: 11px; color: #86868B; text-align: center;'>Se agregarán 4 pestañas nuevas a tu archivo maestro existente.</p>", unsafe_allow_html=True)
            else:
                st.info("Falta configurar las credenciales de Google. Agrega `gcp_service_account` a tus secretos de Streamlit.")


    else:
        st.info("No hay gastos variables para mostrar. Primero procesa una cartola en 'Conciliación Fija'.")

elif page == "Pago Cuota Casa":
    st.header("Pago Cuota Casa")
    
    with st.spinner("Consultando valor de UF actualizado..."):
        live_uf, _ = fetch_indicators()
    
    total_clp = round(live_uf * 23.91)
    hern_clp = round(total_clp * 0.6377)
    vane_clp = total_clp - hern_clp
    
    import datetime
    today_str = datetime.datetime.now().strftime("%d/%m/%Y")
    
    st.markdown(f"""
    <div style="background: #FAFAFC; padding: 24px; border-radius: 16px; border: 1px solid rgba(0,0,0,0.05); margin-bottom: 24px; margin-top: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 24px;">
            <div>
                <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.05em; color: #86868B; text-transform: uppercase;">Monto Total Cuota</span>
                <h2 style="font-size: 32px; font-weight: 700; color: #1D1D1F; margin: 4px 0 0 0; letter-spacing: -0.02em;">$ {format_clp(total_clp)}</h2>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 13px; color: #86868B; margin-bottom: 4px;">Valor UF hoy ({today_str}): <strong>$ {format_clp(live_uf)}</strong></div>
                <div style="font-size: 13px; color: #86868B;">Base Cuota: <strong>23,91 UF</strong></div>
            </div>
        </div>
        <div style="height: 1px; background: rgba(0,0,0,0.05); margin: 20px 0;"></div>
        <h3 style="font-size: 15px; font-weight: 600; color: #1D1D1F; margin-top: 0; margin-bottom: 16px;">Distribución Acordada</h3>
        <div style="display: flex; gap: 16px; flex-wrap: wrap;">
            <!-- Hernanja -->
            <div style="flex: 1; min-width: 250px; background: #FFFFFF; border: 1px solid rgba(0,0,0,0.05); border-radius: 12px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="width: 28px; height: 28px; border-radius: 50%; background: #E8F0FE; display: flex; align-items: center; justify-content: center; color: #1A73E8;">
                            <span class="material-symbols-outlined" style="font-size: 16px;">person</span>
                        </div>
                        <span style="font-size: 14px; font-weight: 600; color: #1D1D1F;">Hernanja</span>
                    </div>
                    <span style="background: #F5F5F7; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; color: #86868B;">63,77%</span>
                </div>
                <div style="font-size: 24px; font-weight: 700; color: #1D1D1F; margin-top: 8px;">$ {format_clp(hern_clp)}</div>
            </div>
            <!-- Vane -->
            <div style="flex: 1; min-width: 250px; background: #FFFFFF; border: 1px solid rgba(0,0,0,0.05); border-radius: 12px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="width: 28px; height: 28px; border-radius: 50%; background: #FCE8E6; display: flex; align-items: center; justify-content: center; color: #D93025;">
                            <span class="material-symbols-outlined" style="font-size: 16px;">person</span>
                        </div>
                        <span style="font-size: 14px; font-weight: 600; color: #1D1D1F;">Vane</span>
                    </div>
                    <span style="background: #F5F5F7; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; color: #86868B;">36,23%</span>
                </div>
                <div style="font-size: 24px; font-weight: 700; color: #1D1D1F; margin-top: 8px;">$ {format_clp(vane_clp)}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif page == "Historial":
    st.header("Historial de Meses")
    db = database.get_db()
    if db:
        docs = database.get_all_historial(db)
        if docs:
            def get_icon(name):
                name = name.lower()
                if "agua" in name: return "water_drop"
                if "luz" in name or "enel" in name: return "lightbulb"
                if "gas" in name or "metrogas" in name: return "mode_heat"
                if "internet" in name or "vtr" in name or "gtd" in name: return "wifi"
                if "netflix" in name or "hbo" in name or "spotify" in name or "amazon" in name or "youtube" in name or "zapping" in name: return "play_circle"
                if "csfj" in name or "colegio" in name or "mandarino" in name: return "school"
                if "contribuciones" in name or "sii" in name: return "account_balance"
                if "seguro" in name: return "health_and_safety"
                if "gastos comunes" in name: return "location_city"
                if "aseo" in name: return "cleaning_services"
                if "piscina" in name: return "pool"
                return "receipt_long"
            
            for doc in docs:
                data = doc.to_dict()
                total = data.get('total_neto', 0)
                papa = data.get('aporte_papa', 0)
                mama = data.get('aporte_mama', 0)
                papa_pct = data.get('pct_papa', 0)
                mama_pct = data.get('pct_mama', 0)
                resultados = data.get('desglose', {})
                fechas = data.get('fechas_detectadas', {})
                
                with st.expander(f"{doc.id} - Total: {format_clp(total)} CLP"):
                    html = f'''
                    <div style="display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 24px; padding: 16px; background: #FAFAFC; border-radius: 16px; border: 1px solid rgba(0,0,0,0.05);">
                        <div style="flex: 1; min-width: 200px; padding: 12px; background: white; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                            <div style="font-size: 11px; font-weight: 700; color: #86868B; text-transform: uppercase;">Aporte Papá ({papa_pct:.1f}%)</div>
                            <div style="font-size: 20px; font-weight: 700; color: #0071E3; margin-top: 4px;">$ {format_clp(papa)}</div>
                        </div>
                        <div style="flex: 1; min-width: 200px; padding: 12px; background: white; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                            <div style="font-size: 11px; font-weight: 700; color: #86868B; text-transform: uppercase;">Aporte Mamá ({mama_pct:.1f}%)</div>
                            <div style="font-size: 20px; font-weight: 700; color: #7C3AED; margin-top: 4px;">$ {format_clp(mama)}</div>
                        </div>
                    </div>
                    '''
                    
                    for k, v in resultados.items():
                        html += f'''
                        <article style="display: flex; justify-content: space-between; align-items: center; padding: 12px 8px; border-bottom: 1px solid rgba(0,0,0,0.03);">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="width: 36px; height: 36px; border-radius: 50%; background: #F5F5F7; display: flex; align-items: center; justify-content: center; color: #1D1D1F;">
                                    <span class="material-symbols-outlined" style="font-size: 18px;">{get_icon(k)}</span>
                                </div>
                                <div>
                                    <h3 style="margin: 0; font-size: 14px; font-weight: 600; color: #1D1D1F;">{k}</h3>
                                    <p style="margin: 0; font-size: 11px; color: #86868B;">Fecha: {standardize_date(fechas.get(k, 'N/A'))}</p>
                                </div>
                            </div>
                            <span style="font-size: 14px; font-weight: 600; color: #1D1D1F;">$ {format_clp(v)}</span>
                        </article>
                        '''
                    
                    st.markdown(re.sub(r'^[ 	]+', '', html, flags=re.MULTILINE), unsafe_allow_html=True)
        else:
            st.info("No hay historial guardado.")
