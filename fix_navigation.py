with open("app.py", "r") as f:
    content = f.read()

nav_logic = """
st.sidebar.title("Hadita 🪄")
page = st.sidebar.radio("Navegación", ["Conciliación Fija", "Gastos Variables", "Historial de Meses"])

if page == "Gastos Variables":
    st.title("Gastos Variables (En Construcción 🚧)")
    st.info("Aquí cargaremos las cartolas para analizar supermercado, farmacia y otros gastos no fijos, descartando automáticamente los que ya fueron procesados en la conciliación fija.")
    st.stop()

if page == "Historial de Meses":
    st.title("Historial de Meses")
    st.info("Aquí conectaremos con Firebase para leer y comparar los meses guardados.")
    st.stop()
"""

# Insert nav_logic after st.set_page_config
import re
content = re.sub(r'(st\.set_page_config.*?)\n', r'\1\n' + nav_logic, content)

with open("app.py", "w") as f:
    f.write(content)
