import re

with open("app.py", "r") as f:
    content = f.read()

# I will replace the 3 column layout with a 2 column layout
old_layout = """        col_m1, col_m2, col_m3 = st.columns([1.6, 1, 1.8])
        with col_m1:
            sel_mes = st.selectbox("Mes de Análisis", meses, index=7, label_visibility="collapsed")
        with col_m2:
            sel_ano = st.selectbox("Año", [2024, 2025, 2026, 2027], index=2, label_visibility="collapsed")
        with col_m3:
            st.markdown('<div style="display: flex; align-items: center; justify-content: flex-end; height: 100%;"><div style="display: flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 500; color: #86868B;"><span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #10B981;"></span> Sincronizado con banco</div></div>', unsafe_allow_html=True)"""

new_layout = """        col_m1, col_m2 = st.columns([1.5, 1])
        with col_m1:
            sel_mes = st.selectbox("Mes de Análisis", meses, index=7, label_visibility="collapsed")
        with col_m2:
            sel_ano = st.selectbox("Año", [2024, 2025, 2026, 2027], index=2, label_visibility="collapsed")"""

content = content.replace(old_layout, new_layout)

with open("app.py", "w") as f:
    f.write(content)
print("Badge removed and layout updated")
