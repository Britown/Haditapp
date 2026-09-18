with open("app.py", "r") as f:
    content = f.read()

debug_inject = """
                resultados, fechas, unmatched = process_data(raw_text, dolar_val, csfj_val, manda_val, beneficio_val, manda_mat_val)
                st.info(f"Modo Debug: Se leyeron {len(raw_text)} caracteres de texto de tus archivos.")
                st.write(resultados)
"""
content = content.replace("                resultados, fechas, unmatched = process_data(raw_text, dolar_val, csfj_val, manda_val, beneficio_val, manda_mat_val)\\n                print(\"DEBUG STREAMLIT: extracted text length =\", len(raw_text))\\n                print(\"DEBUG STREAMLIT: resultados =\", resultados)\\n                st.info(f\"Modo Debug: Se leyeron {len(raw_text)} caracteres de texto de tus archivos.\")", debug_inject)

with open("app.py", "w") as f:
    f.write(content)
