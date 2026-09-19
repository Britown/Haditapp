import re

with open("app.py", "r") as f:
    content = f.read()

# Add import
content = content.replace(
    "from utils import format_clp, standardize_date",
    "from utils import format_clp, standardize_date, fetch_indicators"
)

# Replace the input initialization
old_inputs = """
            c1, c2 = st.columns(2)
            with c1:
                valor_uf = st.number_input("Colegio SFJ (UF Base)", value=float(VALORES_BASE_MES.get("valor_uf", 37900.0)), step=10.0)
                dolar_val = st.number_input("Dólar Observado", value=VALORES_BASE_MES["valor_dolar"], step=10.0)
"""

new_inputs = """
            c1, c2 = st.columns(2)
            
            # Obtener indicadores reales desde la API
            live_uf, live_dolar = fetch_indicators()
            
            with c1:
                valor_uf = st.number_input("Colegio SFJ (UF Base)", value=float(live_uf), step=10.0)
                dolar_val = st.number_input("Dólar Observado", value=float(live_dolar), step=10.0)
"""

content = content.replace(old_inputs.strip(), new_inputs.strip())

with open("app.py", "w") as f:
    f.write(content)
