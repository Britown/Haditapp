import re

with open("app.py", "r") as f:
    content = f.read()

old_button = """    c1, c2 = st.columns(2)
    with c1:
        if st.button("Guardar Gastos Variables", type="primary", use_container_width=True):
            st.success("¡Gastos guardados! (Conexión a Firebase para variables pendiente de habilitar)")"""

new_button = """    c1, c2 = st.columns(2)
    with c1:
        if st.button("Guardar Gastos Variables", type="primary", use_container_width=True):
            from database import get_db, save_gastos_variables
            db = get_db()
            if db:
                month_year = st.session_state.get("last_month_str", "Mes Desconocido")
                if save_gastos_variables(db, month_year, edited_df):
                    st.success("¡Gastos variables guardados exitosamente en la base de datos!")
                else:
                    st.error("Error al guardar en la base de datos.")
            else:
                st.error("No hay conexión a Firebase.")"""

content = content.replace(old_button, new_button)

with open("app.py", "w") as f:
    f.write(content)
