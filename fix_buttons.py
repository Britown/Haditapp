import re

with open("app.py", "r") as f:
    content = f.read()

# Update the button text
content = content.replace('st.button("Procesar Gastos Fijos (Cmd + Enter)")', 'st.button("Procesar Gastos Fijos")')

# Update the CSS colors
content = content.replace('background-color: #0071E3 !important;', 'background-color: #7C3AED !important;')
content = content.replace('background-color: #005BB5 !important;', 'background-color: #6D28D9 !important;')

with open("app.py", "w") as f:
    f.write(content)
print("Button updated")
