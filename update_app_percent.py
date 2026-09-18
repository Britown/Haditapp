import re

with open("app.py", "r") as f:
    content = f.read()

# Add sliders for PAPA and MAMA to Ajustes Dinamicos
old_inputs = """    with c3:
        beneficio_val = st.number_input("Beneficio Empresa", value=VALORES_BASE_MES["beneficio_empleador_por_hijo"], step=1000)"""

new_inputs = """    with c3:
        beneficio_val = st.number_input("Beneficio Empresa", value=VALORES_BASE_MES["beneficio_empleador_por_hijo"], step=1000)
    
    st.markdown('<hr style="margin: 1rem 0; border-color: #e2e8f0;">', unsafe_allow_html=True)
    c4, c5 = st.columns(2)
    with c4:
        papa_pct = st.number_input("% Aporte Papá", value=63.77, step=0.1, format="%.2f")
    with c5:
        mama_pct = st.number_input("% Aporte Mamá", value=36.23, step=0.1, format="%.2f")"""

content = content.replace(old_inputs, new_inputs)

# Use the dynamic percentages instead of fixed dict
old_total = """            total = sum(resultados.values())
            papa = int(total * FACTORES_DIVISION['PAPA'])
            mama = int(total * FACTORES_DIVISION['MAMA'])"""

new_total = """            total = sum(resultados.values())
            papa = int(total * (papa_pct / 100.0))
            mama = int(total * (mama_pct / 100.0))"""

content = content.replace(old_total, new_total)

with open("app.py", "w") as f:
    f.write(content)
