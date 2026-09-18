with open("app.py", "r") as f:
    lines = f.readlines()

ajustes_start = -1
ajustes_end = -1
col_right2_start = -1

for i, line in enumerate(lines):
    if "VARIABLES CLAVE" in line:
        ajustes_start = i - 1
    if "csfj_val =" in line and ajustes_start != -1:
        ajustes_end = i
    if "with col_right:" in line and i > 400:
        col_right2_start = i

# Extract Ajustes
ajustes_block = lines[ajustes_start:ajustes_end+2] # includes the </div>

# Clean file by removing Ajustes and second col_right
# Wait, let's just use the FIRST col_right!
# Wait! Is the first col_right complete? Let's check lines 490-495!
