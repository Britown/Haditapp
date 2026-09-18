with open("app.py", "r") as f:
    content = f.read()

old_process = """        else:
            raw_text = extract_all_text(uploaded_files, pasted_text)
            resultados, fechas = process_data(raw_text, dolar_val, csfj_val, manda_val, beneficio_val)
            
            beneficios_aplicados = 0"""

new_process = """        else:
            with st.spinner('Magia en proceso... Extrayendo y cuadrando movimientos bancarios 🪄'):
                raw_text = extract_all_text(uploaded_files, pasted_text)
                resultados, fechas = process_data(raw_text, dolar_val, csfj_val, manda_val, beneficio_val)
            
            beneficios_aplicados = 0"""

content = content.replace(old_process, new_process)

with open("app.py", "w") as f:
    f.write(content)
