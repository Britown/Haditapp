import re

with open("processor.py", "r") as f:
    content = f.read()

old_logic = """            if line_val > 0:
                if line_val >= csfj_base - 2000:
                    resultados["CSFJ (Mensualidad)"] = line_val if line_val < csfj_base + 2000 else csfj_base
                    if line_val > csfj_base + 2000:
                        resultados["CSFJ (Jornada Extendida)"] = (line_val - csfj_base)
                else:
                    if line_val <= csfj_base * 0.6:
                        resultados["CSFJ (Jornada Extendida)"] = line_val
                    else:
                        resultados["CSFJ (Mensualidad)"] = line_val"""

new_logic = """            if line_val > 0:
                # Detectar Centro de Padres explícito
                if "CENTRO DE PADRES" in line_upper or "CPADRES" in line_upper:
                    resultados["CSFJ (Centro de Padres)"] += line_val
                # Detectar Mensualidad / Jornada Extendida
                elif line_val >= csfj_base - 2000:
                    resultados["CSFJ (Mensualidad)"] = line_val if line_val < csfj_base + 2000 else csfj_base
                    if line_val > csfj_base + 2000:
                        resultados["CSFJ (Jornada Extendida)"] += (line_val - csfj_base)
                else:
                    # Es un cobro extra, pero ¿es jornada extendida o materiales?
                    # El usuario indica que materiales suele ser 40k-60k
                    if line_val >= 30000 and line_val <= 70000:
                        resultados["CSFJ (Extras/Materiales)"] += line_val
                    else:
                        # Otros montos menores (jornada extendida u otros)
                        resultados["CSFJ (Jornada Extendida)"] += line_val"""

content = content.replace(old_logic, new_logic)

# Also detect matricula Mandarino if keyword is present
old_mandarino = """        elif str(int(manda_base)) in line.replace('.', ''):
            resultados["MANDARINO"] = manda_base"""

new_mandarino = """        elif str(int(manda_base)) in line.replace('.', ''):
            resultados["MANDARINO"] = manda_base
        elif "MANDARINO" in line_upper and "MATRICULA" in line_upper:
            for a in amounts:
                val = clean_amount(a)
                if val > 10000 and val < 5000000:
                    resultados["MANDARINO (Matrícula)"] = val
                    break"""

content = content.replace(old_mandarino, new_mandarino)

with open("processor.py", "w") as f:
    f.write(content)
