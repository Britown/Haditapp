import re

with open("app.py", "r") as f:
    content = f.read()

# Replace the "Procesando archivos y texto..." spinner
spinner_1 = 'with st.spinner("Procesando archivos y texto..."):\\'
# Wait, let's just find `with st.spinner("Procesando archivos y texto..."):`
spinner_1 = 'with st.spinner("Procesando archivos y texto..."):'
new_spinner_1 = """
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
"""

# Replace the "Clasificando con IA y Reglas..." spinner
spinner_2 = 'with st.spinner("Clasificando con IA y Reglas..."):'
new_spinner_2 = """
        import random
        mensajes_clasificacion = [
            "Llamando a la IA para que haga el trabajo sucio...",
            "Aplicando tus reglas maestras de entrenamiento...",
            "Decidiendo si ese minimarket fue un 'Gustito'...",
            "Consultando la bola de cristal de los gastos...",
            "Acomodando los abonos en la sección correcta...",
            "Alineando los chakras financieros..."
        ]
        with st.spinner(random.choice(mensajes_clasificacion)):
"""

if spinner_1 in content:
    content = content.replace(spinner_1, new_spinner_1.strip('\n'))
if spinner_2 in content:
    content = content.replace(spinner_2, new_spinner_2.strip('\n'))

with open("app.py", "w") as f:
    f.write(content)
print("Spinners patched!")
