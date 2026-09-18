import re
with open("processor.py", "r") as f:
    content = f.read()

old_mandarino = """        elif "MANDARINO" in line_upper:
            val = get_best_amount(amounts, "MANDARINO", fecha, line_for_amounts)
            if val > 0:
                resultados["MANDARINO"] = val"""

new_mandarino = """        elif "MANDARINO" in line_upper or "CHEQUE" in line_upper:
            val = get_best_amount(amounts, "MANDARINO", fecha, line_for_amounts)
            if val > 0 and (val == manda_base or "MANDARINO" in line_upper):
                resultados["MANDARINO"] = val"""

content = content.replace(old_mandarino, new_mandarino)

with open("processor.py", "w") as f:
    f.write(content)
