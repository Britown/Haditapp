import re
with open("app.py", "r") as f:
    content = f.read()

# Enhance the CSS for inputs
old_css = """    div[data-baseweb="input"], div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
    }"""

new_css = """    div[data-baseweb="input"], div[data-baseweb="base-input"] {
        background-color: rgb(248, 250, 252) !important;
        border: 1px solid rgb(226, 232, 240) !important;
        border-radius: 16px !important;
        padding: 4px !important;
    }
    .ui-card {
        background: #FFFFFF; border-radius: 24px; padding: 40px; margin-bottom: 24px;
        box-shadow: rgba(15, 23, 42, 0.06) 0px 4px 16px -2px; border: 1px solid #E2E8F0;
    }
    .card-header {
        font-family: 'Inter', sans-serif;
        color: #4c4546;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .card-title {
        font-family: 'Inter', sans-serif;
        color: #1a1b1f;
        font-size: 24px;
        font-weight: 600;
        margin-top: 0;
        margin-bottom: 8px;
    }
    .card-subtitle {
        font-family: 'Inter', sans-serif;
        color: #4c4546;
        font-size: 13px;
        margin-top: 0;
        margin-bottom: 24px;
    }
"""

content = content.replace(old_css, new_css)

old_card1 = """<div class="ui-card"><h3 style="margin-top:0; color:#1a1b1f;">Ajustes Dinámicos</h3>"""
new_card1 = """<div class="ui-card">
    <div class="card-header">Variables Clave</div>
    <div class="card-title">Ajustes Dinámicos</div>
    <div class="card-subtitle">Variables macroeconómicas y tipo de cambio para indexación automática.</div>"""

old_card2 = """<div class="ui-card"><h3 style="margin-top:0; color:#1a1b1f;">Ingesta de Cartolas</h3>"""
new_card2 = """<div class="ui-card">
    <div class="card-header">Procesamiento de Datos</div>
    <div class="card-title">Ingesta de Cartolas</div>
    <div class="card-subtitle">Arrastra el extracto bancario en PDF o Excel para su lectura.</div>"""

content = content.replace(old_card1, new_card1)
content = content.replace(old_card2, new_card2)

with open("app.py", "w") as f:
    f.write(content)

print("Fixed CSS")
