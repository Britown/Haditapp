with open("app.py", "r") as f:
    content = f.read()

# Update process_data call
old_call = "resultados, fechas = process_data(raw_text, dolar_val, csfj_val, manda_val, beneficio_val, manda_mat_val)"
new_call = """resultados, fechas, unmatched = process_data(raw_text, dolar_val, csfj_val, manda_val, beneficio_val, manda_mat_val)
                    st.session_state.unmatched = unmatched"""

content = content.replace(old_call, new_call)

with open("app.py", "w") as f:
    f.write(content)
