import re

with open("processor.py", "r") as f:
    content = f.read()

old_logic = """        elif "CONSORCIO" in line_upper:
            if resultados["SEGURO CASA (Consorcio)"] == 0: resultados["SEGURO CASA (Consorcio)"] = get_best_amount(amounts, "SEGURO CASA (Consorcio)", fecha)"""

new_logic = """        elif "CONSORCIO VIDA" in line_upper:
            if resultados["SEGURO CASA (Consorcio)"] == 0: resultados["SEGURO CASA (Consorcio)"] = get_best_amount(amounts, "SEGURO CASA (Consorcio)", fecha)"""

content = content.replace(old_logic, new_logic)

with open("processor.py", "w") as f:
    f.write(content)
