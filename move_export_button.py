import re

with open("app.py", "r") as f:
    content = f.read()

# 1. Extract the Google Sheets block
export_block_regex = r"(\s+# --- Google Sheets Export ---.*?)(?=\s+else:\s+st\.info\(\"No hay historial guardado\.\"\))"
match = re.search(export_block_regex, content, flags=re.DOTALL)
if not match:
    print("Could not find export block")
    exit(1)

export_block = match.group(1)

# Remove it from the current location
content = content.replace(export_block, "")

# We need to change `export_to_sheets(resultados, sheet_input_email.strip())` 
# to `export_to_sheets(resultados, final_df, sheet_input_email.strip())`
export_block = export_block.replace(
    "export_to_sheets(resultados, sheet_input_email.strip())",
    "export_to_sheets(st.session_state.get('resultados_fijos', {}), final_df, sheet_input_email.strip())"
)

# Wait, `resultados` is in `col_right` block, but at the end of the file we might not have `resultados` in scope if it's inside `if procesar:`.
# Actually, if we put it at the very end of the file, we need `resultados`. So let's store it in session_state!
