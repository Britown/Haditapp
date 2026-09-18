import re

with open("app.py", "r") as f:
    content = f.read()

old_top_bar = """        col_m1, col_m2 = st.columns(2)
        with col_m1:
            sel_mes = st.selectbox("Mes de Análisis", meses, index=7) # Agosto by default
        with col_m2:
            sel_ano = st.selectbox("Año", [2024, 2025, 2026, 2027], index=2)"""

new_top_bar = """        col_m1, col_m2, col_m3 = st.columns([1, 1, 1.5])
        with col_m1:
            sel_mes = st.selectbox("Mes de Análisis", meses, index=7, label_visibility="collapsed")
        with col_m2:
            sel_ano = st.selectbox("Año", [2024, 2025, 2026, 2027], index=2, label_visibility="collapsed")
        with col_m3:
            st.markdown('<div style="display: flex; align-items: center; justify-content: flex-end; height: 100%;"><div style="display: flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 500; color: #86868B;"><span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #10B981;"></span> Sincronizado con banco</div></div>', unsafe_allow_html=True)"""

content = content.replace(old_top_bar, new_top_bar)

with open("app.py", "w") as f:
    f.write(content)
print("Top bar updated!")
