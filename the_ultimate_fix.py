with open("app.py", "r") as f:
    lines = f.readlines()

ajustes_start = -1
ajustes_end = -1
col_right2_start = -1
button_idx = -1

for i, line in enumerate(lines):
    if "VARIABLES CLAVE" in line:
        ajustes_start = i - 1
    if "csfj_val =" in line and ajustes_start != -1:
        ajustes_end = i
    if "with col_right:" in line and i > 400:
        col_right2_start = i
    if "st.button(\"Procesar Gastos Fijos (Cmd + Enter)\"" in line and i < 400:
        button_idx = i

# Adjust the end of ajustes to include the closing div
ajustes_end = ajustes_end + 1

ajustes_block = lines[ajustes_start:ajustes_end+1]

# Now, we delete the ajustes block from the bottom, and the second col_right block
# Everything after `ajustes_start` is trash (because it's either Ajustes or the duplicate col_right).
clean_bottom_lines = lines[:ajustes_start]

# Now we insert the ajustes block right BEFORE the button in col_left!
final_lines = clean_bottom_lines[:button_idx] + ajustes_block + clean_bottom_lines[button_idx:]

with open("app.py", "w") as f:
    f.writelines(final_lines)
