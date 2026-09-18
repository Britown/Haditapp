import re

with open("stitch_ui/code.html", "r") as f:
    html = f.read()

match = re.search(r'tailwind\.config = (\{.*?\});', html, re.DOTALL)
config_json = match.group(1) if match else "{}"
# Escape double quotes for Python string
config_json = config_json.replace('"', '\\"')

header_match = re.search(r'(<header class="fixed top-0.*?</header>)', html, re.DOTALL)
header_html = header_match.group(1) if header_match else ""

hero_match = re.search(r'(<header class="flex flex-col lg:flex-row.*?</header>)', html, re.DOTALL)
hero_html = hero_match.group(1) if hero_match else ""

header_html = header_html.replace('fixed top-0 left-0 right-0', 'relative')
header_html = header_html.replace('"', '\\"')
hero_html = hero_html.replace('Mayo 2024', '{month_str}')
hero_html = hero_html.replace('30 de Mayo, 2024', 'Fines de {month_str}')
hero_html = hero_html.replace('"', '\\"')


with open("app.py", "w") as f:
    f.write('''import streamlit as st
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
    .block-container { max-width: 1360px !important; padding: 0 !important; margin: 0 auto !important; }
    #MainMenu, footer, header { visibility: hidden; }
    html, body, [class*="css"] { background-color: rgb(241, 243, 247) !important; }
    
    div[data-baseweb="input"], div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
    }
    label { font-weight: 600 !important; color: #1a1b1f !important; font-size: 13px !important; }
    
    .stButton>button {
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
    }
    .ui-card {
        background: #FFFFFF; border-radius: 24px; padding: 32px; margin-bottom: 24px;
        box-shadow: rgba(15, 23, 42, 0.04) 0px 4px 16px -2px; border: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

if "processed" not in st.session_state:
    st.session_state.processed = False

def do_process():
    st.session_state.processed = True

target_month = st.date_input("Mes de Análisis (Selección)", value=datetime.date(2026, 5, 1))
month_str = target_month.strftime("%B %Y").capitalize()

''')

    f.write('head_template = """\n')
    f.write('<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">\n')
    f.write('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet">\n')
    f.write('<style>body { margin: 0; padding: 0; background-color: rgb(241, 243, 247); } ::-webkit-scrollbar { display: none; }</style>\n')
    f.write('<script src="https://cdn.tailwindcss.com"></script>\n')
    f.write('<script>tailwind.config = ' + config_json.replace('\\"', '"') + ';</script>\n')
    f.write('"""\n\n')

    f.write('top_html = """\n')
    f.write(f'{head_template}\n') # No wait, this is writing python code
