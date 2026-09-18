with open("app.py", "r") as f:
    content = f.read()

meses_str = 'meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]\n    '
if "meses = [" not in content:
    content = content.replace('if page == "Conciliación Fija":\n', 'if page == "Conciliación Fija":\n    ' + meses_str)

inject_code = """
        st.markdown("<br>", unsafe_allow_html=True)
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            sel_mes = st.selectbox("Mes de Análisis", meses, index=7) # Agosto by default
        with col_m2:
            sel_ano = st.selectbox("Año", [2024, 2025, 2026, 2027], index=2)
        month_str = f"{sel_mes} {sel_ano}"
        st.session_state.current_month_str = month_str
"""

# Insert right after `with col_left:`
if "sel_mes = " not in content:
    content = content.replace('    with col_left:\n', '    with col_left:\n' + inject_code)

# Add manda_mat_val back so it doesn't crash
if "manda_mat_val =" not in content:
    content = content.replace('beneficio_val = st.number_input("Beneficio Empresa", value=VALORES_BASE_MES["beneficio_empleador_por_hijo"], step=1000)',
                              'beneficio_val = st.number_input("Beneficio Empresa", value=VALORES_BASE_MES["beneficio_empleador_por_hijo"], step=1000)\n        manda_mat_val = VALORES_BASE_MES.get("jardin_mandarino_materiales", 0)')

with open("app.py", "w") as f:
    f.write(content)
