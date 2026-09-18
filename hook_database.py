import re

with open("app.py", "r") as f:
    content = f.read()

# Add import
content = content.replace("import streamlit as st\nimport pandas as pd", "import streamlit as st\nimport pandas as pd\nimport database")

# Connect the "Guardar Mes" button
old_button = """                if st.button("Guardar Mes", type="primary", use_container_width=True):
                    st.success("Guardado en el historial exitosamente.")"""

new_button = """                if st.button("Guardar Mes", type="primary", use_container_width=True):
                    db = database.get_db()
                    if db:
                        # Convertir fechas al string del mes (ej: 'Febrero 2026')
                        # Podemos usar el selectbox del mes
                        month_year = f"{st.session_state.get('sel_mes', 'Mes')} {st.session_state.get('sel_ano', '2026')}"
                        success = database.save_month_data(
                            db, month_year, total, papa, mama, papa_pct, mama_pct, resultados, fechas
                        )
                        if success:
                            st.success(f"¡{month_year} guardado en Firebase exitosamente!")
                        else:
                            st.error("Hubo un error guardando en Firebase.")"""

content = content.replace(old_button, new_button)

# Also wait, the selectboxes for month and year don't write to session_state with these keys by default unless we assign a key.
# Let's check how selectboxes are defined.
with open("app.py", "w") as f:
    f.write(content)
