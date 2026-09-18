import re
with open("processor.py", "r") as f:
    content = f.read()

old_logic = """                    if line_val > csfj_base + 2000:
                        resultados["CSFJ (Jornada Extendida)"] += (line_val - csfj_base)"""

new_logic = """                    if line_val > csfj_base + 2000:
                        # La diferencia (aprox 40k) suele ser materiales/seguro, no jornada extendida
                        resultados["CSFJ (Extras/Materiales)"] += (line_val - csfj_base)"""

content = content.replace(old_logic, new_logic)

with open("processor.py", "w") as f:
    f.write(content)
