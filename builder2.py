import re

with open("stitch_ui/code.html", "r") as f:
    html = f.read()

match = re.search(r'tailwind\.config = (\{.*?\});', html, re.DOTALL)
config_json = match.group(1) if match else "{}"

header_match = re.search(r'(<header class="fixed top-0.*?</header>)', html, re.DOTALL)
navbar_html = header_match.group(1) if header_match else ""

hero_match = re.search(r'(<header class="flex flex-col lg:flex-row.*?</header>)', html, re.DOTALL)
hero_html = hero_match.group(1) if hero_match else ""

ajustes_match = re.search(r'(<div class="flex flex-col">\s*<span class="font-label-sm uppercase tracking-wider text-on-surface-variant">Variables Clave</span>.*?)<div class="grid grid-cols-1 sm:grid-cols-2', html, re.DOTALL)
ajustes_header = ajustes_match.group(1) if ajustes_match else ""

ingesta_match = re.search(r'(<div class="flex flex-col">\s*<span class="font-label-sm uppercase tracking-wider text-on-surface-variant">Importación asistida</span>.*?)<!-- Switch Tabs -->', html, re.DOTALL)
ingesta_header = ingesta_match.group(1) if ingesta_match else ""

with open("app.py", "w") as f:
    f.write(f'''import streamlit as st
import datetime
from config import VALORES_BASE_MES, FACTORES_DIVISION
from processor import extract_all_text, process_data
import streamlit.components.v1 as components

st.set_page_config(page_title="Hadita", page_icon="🪄", layout="wide", initial_sidebar_state="collapsed")

components.html("""
<script>
    if (!window.parent.document.getElementById('tailwind-script')) {{
        const tailwind = window.parent.document.createElement('script');
        tailwind.id = 'tailwind-script';
        tailwind.src = 'https://cdn.tailwindcss.com';
        window.parent.document.head.appendChild(tailwind);
        
        const config = window.parent.document.createElement('script');
        config.innerHTML = `tailwind.config = {{ corePlugins: {{ preflight: false }}, ...{config_json} }}`;
        window.parent.document.head.appendChild(config);
        
        const fonts = window.parent.document.createElement('link');
        fonts.rel = 'stylesheet';
        fonts.href = 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200';
        window.parent.document.head.appendChild(fonts);
    }}
</script>
""", height=0, width=0)

st.markdown("""
<style>
    .block-container {{ max-width: 1360px !important; padding-top: 5rem !important; padding-bottom: 2rem !important; }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    html, body, [class*="css"] {{
        background-color: rgb(241, 243, 247) !important;
    }}
    
    div[data-baseweb="input"], div[data-baseweb="base-input"] {{
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
    }}
    .stButton>button {{
        width: 100%;
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border-radius: 9999px !important;
        height: 48px;
        font-weight: 600;
        font-size: 1.05rem;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }}
</style>
""", unsafe_allow_html=True)

st.markdown(r"""{navbar_html}""", unsafe_allow_html=True)
st.markdown(r"""{hero_html}""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col_left, col_right = st.columns([5, 7], gap="large")

with col_left:
    st.markdown('<section class="bg-surface-container-lowest p-space-xl rounded-lg shadow-sm flex flex-col gap-space-lg" style="background-color: rgb(255, 255, 255); border: 1px solid rgb(226, 232, 240); box-shadow: rgba(15, 23, 42, 0.06) 0px 4px 16px -2px;">', unsafe_allow_html=True)
    st.markdown(r"""{ajustes_header}""", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        valor_uf = st.number_input("Colegio SFJ (UF Base)", value=float(VALORES_BASE_MES.get("valor_uf", 37900.0)), step=10.0)
        dolar_val = st.number_input("Dólar Observado", value=VALORES_BASE_MES["valor_dolar"], step=10.0)
    with c2:
        manda_val = st.number_input("Mandarino (CLP)", value=VALORES_BASE_MES["mensualidad_mandarino"], step=1000)
        beneficio_val = st.number_input("Beneficio Empresa", value=VALORES_BASE_MES["beneficio_empleador_por_hijo"], step=1000)
    
    csfj_val = VALORES_BASE_MES.get("uf_colegio", 13.5) * valor_uf
    st.markdown('</section><br>', unsafe_allow_html=True)

    st.markdown('<section class="bg-surface-container-lowest p-space-xl rounded-lg shadow-sm flex flex-col gap-space-lg" style="background-color: rgb(255, 255, 255); border: 1px solid rgb(226, 232, 240); box-shadow: rgba(15, 23, 42, 0.06) 0px 4px 16px -2px;">', unsafe_allow_html=True)
    st.markdown(r"""{ingesta_header}""", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Arrastrar Archivos", "Pegar Texto"])
    with tab1:
        uploaded_files = st.file_uploader("Arrastra tu cartola bancaria", accept_multiple_files=True, label_visibility="collapsed")
    with tab2:
        pasted_text = st.text_area("Pega aquí la cartola", height=120, label_visibility="collapsed")
    
    procesar = st.button("Procesar Gastos Fijos (Cmd + Enter)")
    st.markdown('</section>', unsafe_allow_html=True)

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
            
            out = """
            <section class="bg-surface-container-lowest p-space-xl rounded-lg shadow-sm flex flex-col gap-space-lg" style="background-color: rgb(255, 255, 255); border: 1px solid rgb(226, 232, 240); box-shadow: rgba(15, 23, 42, 0.06) 0px 4px 16px -2px; font-family: 'Inter', sans-serif;">
            
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-space-sm mb-4">
                <div class="flex flex-col">
                    <span class="font-label-sm uppercase tracking-wider text-on-surface-variant" style="font-size:11px; font-weight:600; color:#4c4546;">Balance Consolidado</span>
                    <h2 class="font-headline-md text-headline-md text-on-surface mt-0.5" style="font-size:24px; font-weight:600; margin-top:4px;">Desglose Detectado</h2>
                    <p class="font-body-sm text-body-sm text-on-surface-variant" style="font-size:13px; color:#4c4546;">Gastos directos e indexados asignados a la cuenta compartida.</p>
                </div>
                <div><span class="px-space-md py-1 rounded-full bg-surface-container-high text-on-surface font-label-sm text-label-sm" style="background:#e9e7ed; padding:4px 16px; border-radius:99px; font-size:11px; font-weight:600;">{{count}} gastos reconocidos</span></div>
            </div>
            
            <div class="flex flex-col gap-space-xs">
            """.replace("{{count}}", str(len([v for v in resultados.values() if v > 0])))
            
            for k, v in resultados.items():
                if v > 0:
                    out += f"""
                    <div class="flex items-center justify-between p-space-md rounded-DEFAULT hover:bg-surface-container-low transition-colors" style="padding:16px; border-radius:16px; transition:0.2s;">
                        <div class="flex items-center gap-space-md min-w-0" style="gap:16px;">
                            <div class="w-10 h-10 rounded-DEFAULT bg-surface-container-low flex items-center justify-center text-on-surface-variant shrink-0" style="width:40px; height:40px; border-radius:12px; background:#f4f3f8; color:#4c4546;">
                                <span class="material-symbols-outlined text-[20px]">{{icon}}</span>
                            </div>
                            <div class="flex flex-col min-w-0">
                                <span class="font-label-lg text-label-lg text-on-surface truncate" style="font-size:15px; font-weight:500; color:#1a1b1f;">{{k}}</span>
                                <div class="flex items-center gap-space-xs" style="gap:4px; font-size:13px; color:#4c4546;">
                                    <span>Detectado aut.</span><span>•</span><span>{{fecha}}</span>
                                </div>
                            </div>
                        </div>
                        <div class="text-right">
                            <span class="font-label-lg text-label-lg text-on-surface tabular-nums" style="font-size:15px; font-weight:500; color:#1a1b1f;">$ {{v}}</span>
                        </div>
                    </div>
                    """.replace("{{k}}", k).replace("{{v}}", f"{{int(v):,}}".format().replace(",", ".")).replace("{{icon}}", get_icon(k)).replace("{{fecha}}", fechas.get(k, 'Mes actual'))
            
            if beneficio_val > 0 and resultados.get("CSFJ (Mensualidad)", 0) > 0:
                out += f"""
                <div class="flex items-center justify-between p-space-md rounded-DEFAULT bg-surface-container-low/60 hover:bg-surface-container-low transition-colors" style="padding:16px; border-radius:16px; background:rgba(218,226,255,0.4);">
                    <div class="flex items-center gap-space-md min-w-0" style="gap:16px;">
                        <div class="w-10 h-10 rounded-DEFAULT bg-secondary-fixed text-on-secondary-fixed flex items-center justify-center shrink-0" style="width:40px; height:40px; border-radius:12px; background:#dae2ff; color:#001848;">
                            <span class="material-symbols-outlined text-[20px]">redeem</span>
                        </div>
                        <div class="flex flex-col min-w-0">
                            <span class="font-label-lg text-label-lg text-secondary truncate" style="font-size:15px; font-weight:500; color:#0053cf;">Beneficio Empresa</span>
                            <div class="flex items-center gap-space-xs" style="gap:4px; font-size:13px; color:#4c4546;">
                                <span>Reembolso aplicado</span>
                            </div>
                        </div>
                    </div>
                    <div class="text-right">
                        <span class="font-label-lg text-label-lg text-secondary tabular-nums" style="font-size:15px; font-weight:500; color:#0053cf;">-$ {{b}}</span>
                    </div>
                </div>
                """.replace("{{b}}", f"{{int(beneficio_val):,}}".format().replace(",", "."))
                
            out += "</div>"
            
            out += f"""
            <div class="p-space-lg rounded-DEFAULT bg-surface-container-low flex flex-col sm:flex-row items-start sm:items-center justify-between gap-space-md mt-6" style="padding:24px; border-radius:16px; background-color: rgb(248, 250, 252); border: 1px solid rgb(226, 232, 240);">
                <div class="flex flex-col">
                    <span class="font-label-sm uppercase tracking-wider text-on-surface-variant" style="font-size:11px; font-weight:600; color:#4c4546;">Consolidado Actual</span>
                    <span class="font-headline-sm text-headline-sm text-on-surface" style="font-size:19px; font-weight:600; color:#1a1b1f;">Total Gastos Fijos Netos</span>
                </div>
                <div class="flex items-baseline gap-space-xs" style="gap:8px; align-items:baseline;">
                    <span class="font-currency-display text-currency-display text-on-surface tabular-nums leading-none" style="font-size:44px; font-weight:600; color:#1a1b1f; letter-spacing:-0.03em;">$ {{t}}</span>
                    <span class="font-label-sm text-label-sm text-on-surface-variant" style="font-size:13px; font-weight:600; color:#4c4546;">CLP</span>
                </div>
            </div>
            """.replace("{{t}}", f"{{int(total):,}}".format().replace(",", "."))
            
            out += f"""
            <div class="flex flex-col gap-space-md pt-space-xs mt-8">
                <div class="flex items-center justify-between">
                    <div class="flex flex-col">
                        <span class="font-label-sm uppercase tracking-wider text-on-surface-variant" style="font-size:11px; font-weight:600; color:#4c4546;">Acuerdo Bi-Parental</span>
                        <span class="font-headline-sm text-headline-sm text-on-surface" style="font-size:19px; font-weight:600; color:#1a1b1f;">Reparto Proporcional Acordado</span>
                    </div>
                </div>
                
                <div class="w-full h-2 rounded-full overflow-hidden flex bg-surface-container-high mt-4 mb-4" style="height:8px; background:#e9e7ed; border-radius:99px; display:flex;">
                    <div class="h-full bg-secondary transition-all" style="width: 63.77%; background:#0053cf;"></div>
                    <div class="h-full bg-tertiary-fixed-dim transition-all" style="width: 36.23%; background:#d0bcff;"></div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-space-md" style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
                    <div class="p-space-lg rounded-DEFAULT bg-secondary-fixed/40 flex flex-col justify-between gap-space-md" style="padding:24px; border-radius:16px; background-color: rgb(239, 246, 255); border: 1px solid rgb(191, 219, 254);">
                        <div class="flex items-center justify-between mb-4">
                            <div class="flex items-center gap-space-sm" style="gap:12px;">
                                <div class="w-10 h-10 rounded-full bg-secondary text-on-secondary flex items-center justify-center font-label-lg font-bold" style="width:40px; height:40px; border-radius:50%; background:#0053cf; color:white; font-weight:bold;">P</div>
                                <div class="flex flex-col">
                                    <span class="font-headline-sm text-headline-sm text-on-secondary-fixed" style="font-size:15px; font-weight:600; color:#001848;">Cuota Papá</span>
                                </div>
                            </div>
                            <span class="px-space-sm py-1 rounded-full bg-secondary text-on-secondary font-label-sm text-label-sm font-semibold" style="padding:4px 8px; border-radius:99px; background:#0053cf; color:white; font-size:11px; font-weight:700;">63,77%</span>
                        </div>
                        <div class="font-headline-lg text-headline-lg text-on-surface tabular-nums" style="font-size:32px; font-weight:600; color:#1a1b1f;">$ {{p}}</div>
                    </div>
                    
                    <div class="p-space-lg rounded-DEFAULT bg-tertiary-fixed/40 flex flex-col justify-between gap-space-md" style="padding:24px; border-radius:16px; background-color: rgb(250, 245, 255); border: 1px solid rgb(233, 213, 255);">
                        <div class="flex items-center justify-between mb-4">
                            <div class="flex items-center gap-space-sm" style="gap:12px;">
                                <div class="w-10 h-10 rounded-full bg-on-tertiary-fixed text-tertiary-fixed flex items-center justify-center font-label-lg font-bold" style="width:40px; height:40px; border-radius:50%; background:#23005c; color:#e9ddff; font-weight:bold;">M</div>
                                <div class="flex flex-col">
                                    <span class="font-headline-sm text-headline-sm text-on-tertiary-fixed" style="font-size:15px; font-weight:600; color:#23005c;">Deuda de Mamá</span>
                                </div>
                            </div>
                            <span class="px-space-sm py-1 rounded-full bg-on-tertiary-fixed text-tertiary-fixed font-label-sm text-label-sm font-semibold" style="padding:4px 8px; border-radius:99px; background:#23005c; color:#e9ddff; font-size:11px; font-weight:700;">36,23%</span>
                        </div>
                        <div class="font-headline-lg text-headline-lg text-on-surface tabular-nums" style="font-size:32px; font-weight:600; color:#1a1b1f;">$ {{m}}</div>
                    </div>
                </div>
            </div>
            </section>
            """.replace("{{p}}", f"{{papa:,}}".format().replace(",", ".")).replace("{{m}}", f"{{mama:,}}".format().replace(",", "."))
            
            st.markdown(out, unsafe_allow_html=True)
            st.balloons()
''')
