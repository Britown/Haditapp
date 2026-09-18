import re

with open("app.py", "r") as f:
    content = f.read()

old_nav = """st.sidebar.title("Hadita 🪄")
page = st.sidebar.radio("Navegación", ["Conciliación Fija", "Gastos Variables", "Historial de Meses"])"""

new_nav = """st.markdown("<h1 style='text-align: center; margin-top: 10px; margin-bottom: -10px;'>Hadita 🪄</h1>", unsafe_allow_html=True)
page = st.radio("Navegación", ["Conciliación Fija", "Gastos Variables", "Historial de Meses"], horizontal=True, label_visibility="collapsed")
st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)"""

content = content.replace(old_nav, new_nav)

with open("app.py", "w") as f:
    f.write(content)

