import re

with open("app.py", "r") as f:
    content = f.read()

content = content.replace(
    'sheet_input_email = st.text_input("Ingresa tu correo de Gmail para enviarte el archivo:", placeholder="tu.correo@gmail.com")',
    'sheet_input_email = st.text_input("Ingresa tu correo de Gmail para enviarte el archivo:", value="hbrito@gmail.com", placeholder="tu.correo@gmail.com")'
)

with open("app.py", "w") as f:
    f.write(content)
