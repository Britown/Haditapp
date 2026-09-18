with open("app.py", "r") as f:
    content = f.read()

debug_inject = """
                resultados, fechas, unmatched = process_data(raw_text, dolar_val, csfj_val, manda_val, beneficio_val, manda_mat_val)
                with open("dump.txt", "w") as f_dump:
                    f_dump.write(raw_text)
                st.info(f"Modo Debug: Se leyeron {len(raw_text)} caracteres de texto de tus archivos.")
                st.write(resultados)
"""
content = content.replace("                resultados, fechas, unmatched = process_data(raw_text, dolar_val, csfj_val, manda_val, beneficio_val, manda_mat_val)\\n                st.info(f\"Modo Debug: Se leyeron {len(raw_text)} caracteres de texto de tus archivos.\")\\n                st.write(resultados)", debug_inject)

with open("app.py", "w") as f:
    f.write(content)
