import re

with open("stitch_ui/code.html", "r") as f:
    html = f.read()

match = re.search(r'tailwind\.config = (\{.*?\});', html, re.DOTALL)
config_json = match.group(1) if match else "{}"

header_match = re.search(r'(<header class="fixed top-0.*?</header>)', html, re.DOTALL)
header_html = header_match.group(1).replace('fixed top-0 left-0 right-0', 'relative') if header_match else ""

hero_match = re.search(r'(<header class="flex flex-col lg:flex-row.*?</header>)', html, re.DOTALL)
hero_html = hero_match.group(1) if hero_match else ""

with open("app.py", "w") as f:
    f.write(f'''import streamlit as st
import datetime
import locale
from config import VALORES_BASE_MES, FACTORES_DIVISION
from processor import extract_all_text, process_data
import streamlit.components.v1 as components

try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    pass

st.set_page_config(page_title="Hadita", page_icon="🪄", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .block-container {{ max-width: 1360px !important; padding: 0 !important; margin: 0 auto !important; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    html, body, [class*="css"] {{ background-color: rgb(241, 243, 247) !important; }}
    
    div[data-baseweb="input"], div[data-baseweb="base-input"] {{
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
    }}
    label {{ font-weight: 600 !important; color: #1a1b1f !important; font-size: 13px !important; }}
    
    .stButton>button {{
        width: 100%;
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border-radius: 9999px !important;
        height: 54px;
        font-weight: 600;
        font-size: 1.1rem;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        margin-top: 1rem;
    }}
    .ui-card {{
        background: #FFFFFF; border-radius: 24px; padding: 32px; margin-bottom: 24px;
        box-shadow: rgba(15, 23, 42, 0.04) 0px 4px 16px -2px; border: 1px solid #E2E8F0;
    }}
</style>
""", unsafe_allow_html=True)

if "processed" not in st.session_state:
    st.session_state.processed = False

def do_process():
    st.session_state.processed = True

target_month = st.date_input("Mes de Análisis (Selección)", value=datetime.date(2026, 5, 1))
month_str = target_month.strftime("%B %Y").capitalize()

config_json = """{config_json}"""
head_template = f"""
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet">
<style>body {{ margin: 0; padding: 0; background-color: rgb(241, 243, 247); }} ::-webkit-scrollbar {{ display: none; }}</style>
<script src="https://cdn.tailwindcss.com"></script>
<script>tailwind.config = {{config_json}};</script>
"""

header_html = """{header_html}"""
hero_html = """{hero_html}"""
hero_html = hero_html.replace('Mayo 2024', month_str).replace('30 de Mayo, 2024', f'Fines de {{month_str}}')

top_html = f"""
{{head_template}}
<body class="bg-surface text-on-surface font-body-md">
    {{header_html}}
    <main class="w-full bg-surface pt-8">
        <div class="max-w-[1360px] mx-auto w-full px-margin-mobile md:px-gutter lg:px-margin flex flex-col gap-space-xl">
            {{hero_html}}
        </div>
    </main>
</body>
"""

components.html(top_html, height=260, scrolling=False)

st.markdown("<div style='padding: 0 2rem;'>", unsafe_allow_html=True)
col_left, col_right = st.columns([5, 7], gap="large")

with col_left:
    st.markdown('<div class="ui-card"><h3 style="margin-top:0; color:#1a1b1f;">Ajustes Dinámicos</h3>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        valor_uf = st.number_input("Colegio SFJ (UF Base)", value=float(VALORES_BASE_MES.get("valor_uf", 37900.0)), step=10.0)
        dolar_val = st.number_input("Dólar Observado", value=VALORES_BASE_MES["valor_dolar"], step=10.0)
    with c2:
        manda_val = st.number_input("Mandarino (CLP)", value=VALORES_BASE_MES["mensualidad_mandarino"], step=1000)
        beneficio_val = st.number_input("Beneficio Empresa", value=VALORES_BASE_MES["beneficio_empleador_por_hijo"], step=1000)
    csfj_val = VALORES_BASE_MES.get("uf_colegio", 13.5) * valor_uf
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ui-card"><h3 style="margin-top:0; color:#1a1b1f;">Ingesta de Cartolas</h3>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Arrastrar Archivos", "Pegar Texto"])
    with tab1:
        uploaded_files = st.file_uploader("Arrastra tu cartola bancaria", accept_multiple_files=True, label_visibility="collapsed")
    with tab2:
        pasted_text = st.text_area("Pega aquí la cartola", height=120, label_visibility="collapsed")
    st.button("Procesar Gastos Fijos (Cmd + Enter)", on_click=do_process)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    if st.session_state.processed:
        if not uploaded_files and not pasted_text.strip():
            st.error("Por favor, ingresa al menos una fuente de datos.")
            st.session_state.processed = False
        else:
            raw_text = extract_all_text(uploaded_files, pasted_text)
            resultados, fechas = process_data(raw_text, dolar_val, csfj_val, manda_val, beneficio_val)
            
            total = sum(resultados.values())
            papa = int(total * FACTORES_DIVISION['PAPA'])
            mama = int(total * FACTORES_DIVISION['MAMA'])
            count_items = len([v for v in resultados.values() if v > 0])
            
            icons = {{
                "AGUAS": "water_drop", "LUZ": "bolt", "ENEL": "bolt", "GAS": "mode_heat", "METROGAS": "mode_heat",
                "CSFJ": "school", "COLEGIO": "school", "YOUTUBE": "devices", "SPOTIFY": "devices",
                "NETFLIX": "devices", "AMAZON": "devices", "ZAPPING": "devices", "HBO": "devices",
                "GASTOS COMUNES": "apartment", "MANDARINO": "home_work", "ASEO": "cleaning_services",
                "INTERNET": "wifi", "VTR": "wifi", "GTD": "wifi", "CONSORCIO": "security"
            }}
            def get_icon(n):
                for k, v in icons.items():
                    if k in n.upper(): return v
                return "receipt_long"
            
            items_html = ""
            for k, v in resultados.items():
                if v > 0:
                    icon_name = get_icon(k)
                    f_val = f"{{int(v):,}}".replace(",", ".")
                    f_date = fechas.get(k, "Mes actual")
                    items_html += f"""
                    <div class="flex items-center justify-between p-space-md rounded-DEFAULT hover:bg-surface-container-low transition-colors" style="padding:16px; border-radius:16px;">
                        <div class="flex items-center gap-space-md min-w-0" style="gap:16px;">
                            <div class="w-10 h-10 rounded-DEFAULT bg-surface-container-low flex items-center justify-center text-on-surface-variant shrink-0" style="width:40px; height:40px; border-radius:12px; background:#f4f3f8; color:#4c4546;">
                                <span class="material-symbols-outlined text-[20px]">{{icon_name}}</span>
                            </div>
                            <div class="flex flex-col min-w-0">
                                <span class="font-label-lg text-label-lg text-on-surface truncate" style="font-size:15px; font-weight:600; color:#1a1b1f;">{{k}}</span>
                                <div class="flex items-center gap-space-xs" style="gap:4px; font-size:13px; color:#4c4546;">
                                    <span>Detectado aut.</span><span>•</span><span>{{f_date}}</span>
                                </div>
                            </div>
                        </div>
                        <div class="text-right">
                            <span class="font-label-lg text-label-lg text-on-surface tabular-nums" style="font-size:15px; font-weight:600; color:#1a1b1f;">$ {{f_val}}</span>
                        </div>
                    </div>
                    """
            
            if beneficio_val > 0 and resultados.get("CSFJ (Mensualidad)", 0) > 0:
                b_val = f"{{int(beneficio_val):,}}".replace(",", ".")
                items_html += f"""
                <div class="flex items-center justify-between p-space-md rounded-DEFAULT bg-secondary-fixed/40 hover:bg-secondary-fixed/60 transition-colors" style="padding:16px; border-radius:16px; background:rgba(218,226,255,0.4);">
                    <div class="flex items-center gap-space-md min-w-0" style="gap:16px;">
                        <div class="w-10 h-10 rounded-DEFAULT bg-secondary text-on-secondary flex items-center justify-center shrink-0" style="width:40px; height:40px; border-radius:12px; background:#dae2ff; color:#001848;">
                            <span class="material-symbols-outlined text-[20px]">redeem</span>
                        </div>
                        <div class="flex flex-col min-w-0">
                            <span class="font-label-lg text-label-lg text-secondary truncate" style="font-size:15px; font-weight:600; color:#0053cf;">Beneficio Empresa</span>
                            <div class="flex items-center gap-space-xs" style="gap:4px; font-size:13px; color:#0053cf; font-weight:500;">
                                <span>Reembolso aplicado</span>
                            </div>
                        </div>
                    </div>
                    <div class="text-right">
                        <span class="font-label-lg text-label-lg text-secondary tabular-nums" style="font-size:15px; font-weight:600; color:#0053cf;">-$ {{b_val}}</span>
                    </div>
                </div>
                """
                
            t_val = f"{{int(total):,}}".replace(",", ".")
            p_val = f"{{papa:,}}".replace(",", ".")
            m_val = f"{{mama:,}}".replace(",", ".")
            
            final_right = f"""
            {{head_template}}
            <body class="bg-surface text-on-surface font-body-md" style="background: rgb(241, 243, 247);">
            <div class="flex flex-col gap-space-xl">
            <section class="bg-surface-container-lowest p-space-xl rounded-lg shadow-sm flex flex-col gap-space-lg" style="background: #fff; border-radius: 24px;">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-space-sm mb-4">
                    <div class="flex flex-col">
                        <span class="font-label-sm uppercase tracking-wider text-on-surface-variant">Balance Consolidado</span>
                        <h2 class="font-headline-md text-headline-md text-on-surface">Desglose Detectado</h2>
                    </div>
                    <div><span class="px-space-md py-1 rounded-full bg-surface-container-high text-on-surface font-label-sm text-label-sm">{{count_items}} gastos reconocidos</span></div>
                </div>
                <div class="flex flex-col gap-space-xs">
                    {{items_html}}
                </div>
                
                <div class="p-space-lg rounded-DEFAULT bg-surface-container-low flex flex-col sm:flex-row items-start sm:items-center justify-between gap-space-md mt-6" style="border: 1px solid #e2e8f0; padding:24px; border-radius:16px;">
                    <div class="flex flex-col">
                        <span class="font-label-sm uppercase tracking-wider text-on-surface-variant">Consolidado Actual</span>
                        <span class="font-headline-sm text-headline-sm text-on-surface">Total Gastos Fijos Netos</span>
                    </div>
                    <div class="flex items-baseline gap-space-xs">
                        <span class="font-currency-display text-currency-display text-on-surface tabular-nums leading-none" style="font-size:44px; font-weight:700;">$ {{t_val}}</span>
                        <span class="font-label-sm text-label-sm text-on-surface-variant">CLP</span>
                    </div>
                </div>
                
                <div class="flex flex-col gap-space-md pt-space-xs mt-8">
                    <div class="flex flex-col">
                        <span class="font-label-sm uppercase tracking-wider text-on-surface-variant">Acuerdo Bi-Parental</span>
                        <span class="font-headline-sm text-headline-sm text-on-surface">Reparto Proporcional Acordado</span>
                    </div>
                    <div class="w-full h-2 rounded-full overflow-hidden flex bg-surface-container-high mt-4 mb-4">
                        <div class="h-full bg-secondary transition-all" style="width: 63.77%; background:#0053cf;"></div>
                        <div class="h-full bg-tertiary-fixed-dim transition-all" style="width: 36.23%; background:#d0bcff;"></div>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-space-md">
                        <div class="p-space-lg rounded-DEFAULT bg-secondary-fixed/40 flex flex-col justify-between gap-space-md" style="border: 1px solid rgb(191,219,254); padding:24px; border-radius:20px;">
                            <div class="flex items-center justify-between mb-4">
                                <div class="flex items-center gap-space-sm">
                                    <div class="w-10 h-10 rounded-full bg-secondary text-on-secondary flex items-center justify-center font-label-lg font-bold">P</div>
                                    <span class="font-headline-sm text-headline-sm text-on-secondary-fixed">Cuota Papá</span>
                                </div>
                                <span class="px-space-sm py-1 rounded-full bg-secondary text-on-secondary font-label-sm text-label-sm font-semibold">63,77%</span>
                            </div>
                            <div class="font-headline-lg text-headline-lg text-on-surface tabular-nums" style="font-size:32px; font-weight:700;">$ {{p_val}}</div>
                        </div>
                        <div class="p-space-lg rounded-DEFAULT bg-tertiary-fixed/40 flex flex-col justify-between gap-space-md" style="border: 1px solid rgb(233,213,255); padding:24px; border-radius:20px;">
                            <div class="flex items-center justify-between mb-4">
                                <div class="flex items-center gap-space-sm">
                                    <div class="w-10 h-10 rounded-full bg-on-tertiary-fixed text-tertiary-fixed flex items-center justify-center font-label-lg font-bold">M</div>
                                    <span class="font-headline-sm text-headline-sm text-on-tertiary-fixed">Deuda de Mamá</span>
                                </div>
                                <span class="px-space-sm py-1 rounded-full bg-on-tertiary-fixed text-tertiary-fixed font-label-sm text-label-sm font-semibold">36,23%</span>
                            </div>
                            <div class="font-headline-lg text-headline-lg text-on-surface tabular-nums" style="font-size:32px; font-weight:700;">$ {{m_val}}</div>
                        </div>
                    </div>
                </div>
            </section>
            </div>
            </body>
            """
            components.html(final_right, height=1200, scrolling=False)
            
st.markdown("</div>", unsafe_allow_html=True)
''')
