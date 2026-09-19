import re

with open("processor2.py", "r") as f:
    content = f.read()

old_logic = """
            if line_val > 0:
                if "CENTRO DE PADRES" in line_upper or "CPADRES" in line_upper:
                    resultados["CSFJ (Centro de Padres)"] += line_val
                elif line_val >= csfj_base - 2000:
                    resultados["CSFJ (Mensualidad)"] = line_val if line_val < csfj_base + 2000 else csfj_base
                    if line_val > csfj_base + 2000:
                        # La diferencia (aprox 40k) suele ser materiales/seguro, no jornada extendida
                        resultados["CSFJ (Extras/Materiales)"] += (line_val - csfj_base)
                else:
                    if line_val >= 30000 and line_val <= 70000:
                        resultados["CSFJ (Extras/Materiales)"] += line_val
                    else:
                        resultados["CSFJ (Jornada Extendida)"] += line_val
"""

new_logic = """
            if line_val > 0:
                if "CENTRO DE PADRES" in line_upper or "CPADRES" in line_upper:
                    resultados["CSFJ (Centro de Padres)"] += line_val
                elif line_val >= csfj_base - 50000: # Permitir mayor flexibilidad
                    # Si supera la base o no, el monto que manda es el de la cartola. 
                    # No lo dividimos artificialmente.
                    resultados["CSFJ (Mensualidad)"] += line_val
                else:
                    if line_val >= 30000 and line_val <= 70000:
                        resultados["CSFJ (Extras/Materiales)"] += line_val
                    else:
                        resultados["CSFJ (Jornada Extendida)"] += line_val
"""

content = content.replace(old_logic.strip(), new_logic.strip())

with open("processor2.py", "w") as f:
    f.write(content)
