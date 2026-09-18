with open("app.py", "r") as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
button_idx = -1

for i, line in enumerate(lines):
    if "VARIABLES CLAVE" in line:
        start_idx = i - 1 # Include the <div class="ui-card"...
    if "csfj_val =" in line:
        end_idx = i
    if "st.button(\"Procesar Gastos Fijos (Cmd + Enter)\"" in line:
        button_idx = i

# Extract the block
ajustes_block = lines[start_idx:end_idx+1]

# Rebuild file
# We remove the block from its original position
new_lines = lines[:start_idx] + lines[end_idx+1:button_idx] + ajustes_block + lines[button_idx:]

with open("app.py", "w") as f:
    f.writelines(new_lines)
