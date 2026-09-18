import re

with open("processor.py", "r") as f:
    content = f.read()

old_aseo = """        # Aseo
        if "MARISEL" in line_upper or "CAROLINA MENDOZA" in line_upper or ("35000" in line.replace('.', '') and "TRANSFERENCIA" in line_upper):"""

new_aseo = """        # Aseo
        if "MARISEL" in line_upper or "CAROLINA MENDOZA" in line_upper or "CRISTINA CAISALUISA" in line_upper or ("35000" in line.replace('.', '') and "TRANSFERENCIA" in line_upper):"""

content = content.replace(old_aseo, new_aseo)

with open("processor.py", "w") as f:
    f.write(content)
