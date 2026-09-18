import re

def clean_amount(s):
    s = re.sub(r'[^\d]', '', str(s))
    return int(s) if s else 0

def get_best_amount(amounts_list, cat, raw_line):
    vals = []
    for a in amounts_list:
        v = clean_amount(a)
        if v > 0: vals.append(v)
    
    vals = [v for v in vals if v < 5000000]
    
    is_usd_candidate = cat in ["AMAZON PRIME", "HBO MAX", "YOUTUBE PREMIUM", "SPOTIFY DUO", "UNMATCHED"]
    
    if is_usd_candidate:
        vals = [v for v in vals if (v < 200) or (v >= 1000)]
    else:
        vals = [v for v in vals if v >= 1000]
        
    if not vals: return 0
    
    if len(vals) > 1 and vals[0] <= 3112:
        vals = vals[1:]
        
    if not vals: return 0
    
    is_visa_quota = bool(re.search(r'\b\d{2}/\d{2}\b\s*\$\s*-?\d', raw_line))
    
    if is_visa_quota:
        res = vals[-1]
    else:
        res = vals[0]
        
    return res

csfj_base = 37900.0 * 13.5
resultados = {
    "CSFJ (Mensualidad)": 0,
    "CSFJ (Extras/Materiales)": 0,
    "CSFJ (Jornada Extendida)": 0,
    "CSFJ (Centro de Padres)": 0
}

lines = [
    "05/08/26 0608 10679592 COLEGIO FCO.JAVIER HUECSANTIAGO $551.405 $551.405 01/01 $551.405",
    "29/06/26 0309 10551638 COLEGIO FCO.JAVIER HUEC TASA INT. 2,86% $660.000 $741.780 02/06 $123.630"
]

for raw_line in lines:
    amounts = []
    for t in raw_line.split():
        t_clean = t.strip('.,;:')
        if re.match(r'^(?:US\$|\$)?-?\d+(?:[\.\,]\d+)*$', t_clean):
            amounts.append(t_clean)
            
    line_val = get_best_amount(amounts, "CSFJ (Mensualidad)", raw_line)
    
    line_upper = raw_line.upper()
    
    if line_val > 0:
        if "CENTRO DE PADRES" in line_upper or "CPADRES" in line_upper:
            resultados["CSFJ (Centro de Padres)"] += line_val
        elif line_val >= csfj_base - 2000:
            resultados["CSFJ (Mensualidad)"] = line_val if line_val < csfj_base + 2000 else csfj_base
            if line_val > csfj_base + 2000:
                resultados["CSFJ (Extras/Materiales)"] += (line_val - csfj_base)
        else:
            if line_val >= 30000 and line_val <= 70000:
                resultados["CSFJ (Extras/Materiales)"] += line_val
            else:
                resultados["CSFJ (Jornada Extendida)"] += line_val

beneficio = 212600
if resultados["CSFJ (Mensualidad)"] > 0:
    resultados["CSFJ (Mensualidad)"] = max(0, resultados["CSFJ (Mensualidad)"] - beneficio)

print(resultados)
