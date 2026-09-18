import re

with open("processor.py", "r") as f:
    content = f.read()

# 1. Add get_best_amount function at the top of process_data
old_def = "def process_data(raw_text, dolar_val, csfj_val, manda_val, beneficio_val, manda_mat_val):"
new_def = """def process_data(raw_text, dolar_val, csfj_val, manda_val, beneficio_val, manda_mat_val):
    def get_best_amount(amounts_list, cat):
        vals = []
        for a in amounts_list:
            v = clean_amount(a)
            if v > 0: vals.append(v)
        if not vals: return 0
        
        if cat in ["CSFJ (Mensualidad)", "MANDARINO"]:
            valid = [v for v in vals if v < 5000000]
            return max(valid) if valid else 0
        elif cat in ["ZAPPING", "AMAZON PRIME", "HBO MAX", "YOUTUBE PREMIUM", "SPOTIFY DUO"]:
            valid = [v for v in vals if v < 30000]
            if not valid: return 0
            res = max(valid)
            # If it's a small USD amount, convert it
            if res < 200: return res * get_dolar_historico(fecha, dolar_val)
            return res
        else:
            # Servicios basicos, seguros, etc. < 400.000
            valid = [v for v in vals if v < 400000]
            return max(valid) if valid else 0
"""
content = content.replace(old_def, new_def)

# 2. Replace the massive elif block with a cleaner dictionary mapping
old_block = """        if "AGUAS ANDINAS" in line:
            for a in amounts:
                val = clean_amount(a)
                if val > 1000 and val < 5000000:
                    resultados["AGUA (Aguas Andinas)"] = val
                    break
        elif "ENEL" in line:
            for a in amounts:
                val = clean_amount(a)
                if val > 1000 and val < 5000000:
                    resultados["LUZ (Enel)"] = val
                    break
        elif "METROGAS" in line:
            for a in amounts:
                val = clean_amount(a)
                if val > 1000 and val < 5000000:
                    resultados["GAS (Metrogas)"] = val
                    break
        elif "GTD" in line:
            for a in amounts:
                val = clean_amount(a)
                if val > 1000 and val < 5000000:
                    resultados["INTERNET (GTD)"] = val
                    break
        elif "CONSORCIO" in line:
            for a in amounts:
                val = clean_amount(a)
                if val > 1000 and val < 5000000:
                    resultados["SEGURO CASA (Consorcio)"] = val
                    break
        elif "ZAPPING" in line:
            for a in amounts:
                val = clean_amount(a)
                if val > 0 and val < 200:
                    resultados["ZAPPING"] = val * get_dolar_historico(fecha, dolar_val)
                elif val > 1000 and val < 5000000:
                    resultados["ZAPPING"] = val
        elif "AMAZON" in line or "PRIME VIDEO" in line:
            for a in amounts:
                val = clean_amount(a)
                if val > 0 and val < 200:
                    resultados["AMAZON PRIME"] = val * get_dolar_historico(fecha, dolar_val)
                elif val > 1000 and val < 5000000:
                    resultados["AMAZON PRIME"] = val
        elif "MAX" in line and ("HBO" in line or "MP*MAX" in line):
            for a in amounts:
                val = clean_amount(a)
                if val > 0 and val < 200:
                    resultados["HBO MAX"] = val * get_dolar_historico(fecha, dolar_val)
                elif val > 1000 and val < 5000000:
                    resultados["HBO MAX"] = val
        elif "YOUTUBE" in line:
            for a in amounts:
                val = clean_amount(a)
                if val > 0 and val < 200: 
                    resultados["YOUTUBE PREMIUM"] = val * get_dolar_historico(fecha, dolar_val)
                elif val > 1000 and val < 5000000:
                    resultados["YOUTUBE PREMIUM"] = val
        elif "SPOTIFY" in line:
            for a in amounts:
                val = clean_amount(a)
                if val > 0 and val < 200:
                    resultados["SPOTIFY DUO"] = val * get_dolar_historico(fecha, dolar_val)
                elif val > 1000 and val < 5000000:
                    resultados["SPOTIFY DUO"] = val"""

new_block = """        if "AGUAS ANDINAS" in line_upper:
            if resultados["AGUA (Aguas Andinas)"] == 0: resultados["AGUA (Aguas Andinas)"] = get_best_amount(amounts, "AGUA (Aguas Andinas)")
        elif "ENEL" in line_upper:
            if resultados["LUZ (Enel)"] == 0: resultados["LUZ (Enel)"] = get_best_amount(amounts, "LUZ (Enel)")
        elif "METROGAS" in line_upper:
            if resultados["GAS (Metrogas)"] == 0: resultados["GAS (Metrogas)"] = get_best_amount(amounts, "GAS (Metrogas)")
        elif "GTD" in line_upper:
            if resultados["INTERNET (GTD)"] == 0: resultados["INTERNET (GTD)"] = get_best_amount(amounts, "INTERNET (GTD)")
        elif "CONSORCIO" in line_upper:
            if resultados["SEGURO CASA (Consorcio)"] == 0: resultados["SEGURO CASA (Consorcio)"] = get_best_amount(amounts, "SEGURO CASA (Consorcio)")
        elif "ZAPPING" in line_upper:
            if resultados["ZAPPING"] == 0: resultados["ZAPPING"] = get_best_amount(amounts, "ZAPPING")
        elif "AMAZON" in line_upper or "PRIME VIDEO" in line_upper:
            if resultados["AMAZON PRIME"] == 0: resultados["AMAZON PRIME"] = get_best_amount(amounts, "AMAZON PRIME")
        elif "MAX" in line_upper and ("HBO" in line_upper or "MP*MAX" in line_upper):
            if resultados["HBO MAX"] == 0: resultados["HBO MAX"] = get_best_amount(amounts, "HBO MAX")
        elif "YOUTUBE" in line_upper:
            if resultados["YOUTUBE PREMIUM"] == 0: resultados["YOUTUBE PREMIUM"] = get_best_amount(amounts, "YOUTUBE PREMIUM")
        elif "SPOTIFY" in line_upper:
            if resultados["SPOTIFY DUO"] == 0: resultados["SPOTIFY DUO"] = get_best_amount(amounts, "SPOTIFY DUO")"""

content = content.replace(old_block, new_block)

with open("processor.py", "w") as f:
    f.write(content)
