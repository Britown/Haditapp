import re

with open("app.py", "r") as f:
    content = f.read()

old_logic = """
        if procesar:
            if not uploaded_files and not pasted_text.strip():
                st.error("Por favor, ingresa al menos una fuente de datos.")
            else:
                raw_text = extract_all_text(uploaded_files, pasted_text)
"""

new_logic = """
        if procesar:
            if not uploaded_files and not pasted_text.strip():
                st.error("Por favor, ingresa al menos una fuente de datos.")
            else:
                import random
                mensajes_procesamiento = [
                    "Despertando a los duendes contables...",
                    "Traduciendo el lenguaje del banco a español...",
                    "Buscando los gastos escondidos en el PDF...",
                    "Inyectando café en el procesador...",
                    "Sacando la calculadora científica...",
                    "Leyendo la letra chica de la cartola..."
                ]
                with st.spinner(random.choice(mensajes_procesamiento)):
                    raw_text = extract_all_text(uploaded_files, pasted_text)
"""
content = content.replace(old_logic, new_logic.strip('\n'))

with open("app.py", "w") as f:
    f.write(content)
print("Added spinner to Fija!")
