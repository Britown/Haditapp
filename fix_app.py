import re

with open("app.py", "r") as f:
    content = f.read()

# Import utils
content = content.replace('from processor_v3 import extract_all_text, process_data', 'from processor_v3 import extract_all_text, process_data\nfrom utils import format_clp, standardize_date')

# Replace formatting logic
content = content.replace('{int(v):,}', '{format_clp(v)}')
content = content.replace('{int(beneficio_val):,}', '{format_clp(beneficio_val)}')
content = content.replace('{int(papa_mat_val):,}', '{format_clp(papa_mat_val)}')
content = content.replace('{int(total):,}', '{format_clp(total)}')
content = content.replace('{int(papa):,}', '{format_clp(papa)}')
content = content.replace('{int(mama):,}', '{format_clp(mama)}')

# Remove the dangerous .replace(",", ".")
content = content.replace('""".replace(",", ".")', '"""')

# Standardize dates in Gastos Fijos
content = content.replace("fechas.get(k, 'N/A')", "standardize_date(fechas.get(k, 'N/A'))")

with open("app.py", "w") as f:
    f.write(content)
print("app.py fixed")
