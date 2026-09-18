import re

with open("processor.py", "r") as f:
    content = f.read()

old_aseo = """        # Aseo
        if "35.000" in line or "35000" in line.replace('.', ''):
            if "TRANSFERENCIA" in line or "MARISEL" in line:
                resultados["ASEO"] = 35000
                
        # Piscina
        if "27.000" in line or "27000" in line.replace('.', '') or "17.766.248-8" in line:
            if "TRANSFERENCIA" in line or "ANDY" in line or "17.766.248-8" in line:
                resultados["PISCINA (Andy)"] = 27000"""

new_aseo = """        # Aseo
        if "MARISEL" in line_upper or "CAROLINA MENDOZA" in line_upper or ("35000" in line.replace('.', '') and "TRANSFERENCIA" in line_upper):
            for a in amounts:
                val = clean_amount(a)
                if val >= 20000 and val < 5000000:
                    resultados["ASEO"] += val  # += en caso de que pague 2 veces en el mes
                    break
            if resultados["ASEO"] == 0 and ("35000" in line.replace('.', '')):
                resultados["ASEO"] = 35000
                
        # Piscina
        if "ANDY" in line_upper or "17.766.248-8" in line or ("27000" in line.replace('.', '') and "TRANSFERENCIA" in line_upper):
            for a in amounts:
                val = clean_amount(a)
                if val >= 15000 and val < 5000000:
                    resultados["PISCINA (Andy)"] += val
                    break
            if resultados["PISCINA (Andy)"] == 0 and ("27000" in line.replace('.', '')):
                resultados["PISCINA (Andy)"] = 27000"""

content = content.replace(old_aseo, new_aseo)

with open("processor.py", "w") as f:
    f.write(content)

