with open("app.py", "r") as f:
    content = f.read()

old_end = """    if st.session_state.processed and "resultados" in st.session_state:
        resultados = st.session_state.resultados
        fechas = st.session_state.fechas
        unmatched = st.session_state.unmatched"""

new_end = """    if st.session_state.processed and "resultados" in st.session_state:
        resultados = st.session_state.resultados
        fechas = st.session_state.fechas
        unmatched = st.session_state.unmatched
        
        # DEBUG DUMP TO PROVE BACKEND WORKS
        st.success(f"DEBUG BACKEND: CSFJ Mensualidad = {resultados.get('CSFJ (Mensualidad)', 0)} | MANDARINO = {resultados.get('MANDARINO', 0)}")"""

content = content.replace(old_end, new_end)
with open("app.py", "w") as f:
    f.write(content)
