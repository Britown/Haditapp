import re

lines = [
    "18/08 Cargo por Compra en Zapping Chile El 19.900,00 1.433.078,00",
    "04/08 12397759 Transferencia de Hernan Brito Rodriguez Rut 976.598,00",
    "10/08 Cargo por Pago Metlife Seg. Gen Nro. 108977010272. 09:00:17.978 1.030,00",
    "25/03/2026 Hogar GTD MANQUEHUE S.A COMPRAS NaN NaN NaN NaN 1 de 1 34859",
    "2 mar 2026 Cargos - Cargo por compra en MERCADOPAGO*EMPOR el01/03/2026 a las 18:20:04 hrs., $3.000",
    "01/04/2026 Educación COLEGIO FCO.JAVIER COMPRAS NaN NaN NaN NaN 1 de 1 597626",
    "04/08 Cargo por Compra en TUU*369 BARBER ST El 25.000,00"
]

def clean_amount(val_str):
    val_str = val_str.replace('$', '').strip()
    if ',' in val_str:
        parts = val_str.split(',')
        if len(parts[-1]) <= 2:
            val_str = parts[0]
    val_str = val_str.replace('.', '').replace(',', '')
    try:
        return float(val_str)
    except:
        return 0

def get_best(line):
    # Remove times
    line = re.sub(r'\b\d{2}:\d{2}:\d{2}(?:\.\d+)?\b', ' ', line)
    # Remove quotas
    line = re.sub(r'\b\d+\s+de\s+\d+\b', ' ', line, flags=re.IGNORECASE)
    line = re.sub(r'\b\d{1,2}/\d{1,2}\b', ' ', line)
    
    # Extract ALL numbers
    raw_vals = re.findall(r'[\d\.\,]+', line)
    vals = [clean_amount(v) for v in raw_vals]
    vals = [v for v in vals if v > 0]
    
    if not vals: return 0
    
    if len(vals) == 1:
        return vals[0]
        
    # Check if the last two numbers are both at the very end of the string
    # We can just look at the string's end
    match = re.search(r'((?:[\$\s]*[\d\.\,]+\s*)+)$', line)
    if match:
        end_str = match.group(1)
        end_raw_vals = re.findall(r'[\d\.\,]+', end_str)
        end_vals = [clean_amount(v) for v in end_raw_vals]
        end_vals = [v for v in end_vals if v > 0]
        
        if len(end_vals) >= 2:
            return end_vals[-2]
            
    return vals[-1]

for line in lines:
    print(f"{get_best(line)} <- {line}")
